from datetime import datetime
import struct
import exifread
import collections

ParserResult = collections.namedtuple('ParserResult',
                                      'date_and_time tags is_video')


def get_exif_tags(path):
    """
    Read EXIF data from image file and return tags
    """
    image_file = open(path, 'rb')
    tags = exifread.process_file(image_file)
    image_file.close()

    if not tags:
        return None
    return tags


def get_date_and_time_from_tags(tags):
    """
    Return original date and time from EXIF tags
    """
    if not tags:
        return None
    if 'EXIF DateTimeOriginal' in tags:
        original_date_and_time = str(tags['EXIF DateTimeOriginal'])
    elif 'EXIF DateTimeDigitized' in tags:
        original_date_and_time = str(tags['EXIF DateTimeDigitized'])
    elif 'Image DateTime' in tags:
        original_date_and_time = str(tags['Image DateTime'])
    # elif 'GPS GPSDate' in tags:
    #     date = str(tags['GPS GPSDate'])
    #     if 'GPS GPSTimeStamp' in tags:
    #         time = str(tags['GPS GPSTimeStamp'])
    #         original_date_and_time = '{} {}'.format(str(date), str(time))
    #     else:
    #         original_date_and_time = '{} 00:00:00'.format(str(date))
    else:
        original_date_and_time = None
    if not original_date_and_time:
        return None
    parts = original_date_and_time.split(' ')
    if len(parts) == 1:
        parts = original_date_and_time.split(':')
        parts = ('-'.join(parts[0:3]), ':'.join(parts[3:6]))
    date_and_time = parts[0].replace(':', '-') + " " + parts[1]
    return date_and_time


def _match_extension(path, extensions):
    path_lower = path.lower()
    for ext in extensions:
        if path_lower.endswith(ext.lower()):
            return True
    return False


def parse_image(path):
    """
    Read EXIF data from JPEG image file and return date when it was taken
    """
    if not _match_extension(path, ['.jpg', '.jpeg']):
        return None
    tags = get_exif_tags(path)
    if not tags:
        return None
    return ParserResult(date_and_time=get_date_and_time_from_tags(tags),
                        tags=tags, is_video=False)


def parse_video(path):
    """
    Parse MOV file and find it's creation time
    https://stackoverflow.com/questions/21355316/getting-metadata-for-mov-video/21395803
    """
    if not _match_extension(path, ['.mov']):
        return None
    ATOM_HEADER_SIZE = 8
    # difference between Unix epoch and QuickTime epoch, in seconds
    EPOCH_ADJUSTER = 2082844800
    # open file and search for moov item
    video_file = open(path, "rb")
    while 1:
        atom_header = video_file.read(ATOM_HEADER_SIZE)
        if atom_header[4:8] == 'moov':
            break
        else:
            atom_size = struct.unpack(">I", atom_header[0:4])[0]
            video_file.seek(atom_size - 8, 1)

    # found 'moov', look for 'mvhd' and timestamps
    atom_header = video_file.read(ATOM_HEADER_SIZE)
    date_and_time = None
    if atom_header[4:8] == 'cmov':
        print("moov atom is compressed")
    elif atom_header[4:8] != 'mvhd':
        print("expected to find 'mvhd' header")
    else:
        video_file.seek(4, 1)
        creation_date = struct.unpack(">I", video_file.read(4))[0]
        # modification_date = struct.unpack(">I", video_file.read(4))[0]
        # print("creation date: ", datetime.
        #       fromtimestamp(creation_date - EPOCH_ADJUSTER))
        # print("modification date: ", datetime.
        #       fromtimestamp(modification_date - EPOCH_ADJUSTER))
        if creation_date > 0:
            date_and_time = str(datetime.fromtimestamp(creation_date -
                                                       EPOCH_ADJUSTER))
    video_file.close()
    if not date_and_time:
        return None
    return ParserResult(date_and_time=date_and_time, tags=None, is_video=True)
