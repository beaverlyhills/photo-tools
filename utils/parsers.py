import datetime
import struct
import exifread


def parse_image(path):
    """
    Read EXIF data from image file and return date when it was taken
    """
    image_file = open(path, 'rb')
    tags = exifread.process_file(image_file)
    image_file.close()

    if not tags:
        print('No metadata found in image')
        return None

    if 'EXIF DateTimeOriginal' in tags:
        original_date_and_time = str(tags['EXIF DateTimeOriginal'])
    elif 'EXIF DateTimeDigitized' in tags:
        original_date_and_time = str(tags['EXIF DateTimeDigitized'])
    elif 'Image DateTime' in tags:
        original_date_and_time = str(tags['Image DateTime'])
    if not original_date_and_time:
        print('No datetime tags found in image metadata')
        return None

    parts = original_date_and_time.split(' ')
    date_and_time = parts[0].replace(':', '-') + " " + parts[1]
    return date_and_time


def parse_video(path):
    """
    Parse MOV file and find it's creation time
    """
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
        # print("creation date: ", datetime.datetime.
        #       fromtimestamp(creation_date - EPOCH_ADJUSTER))
        # print("modification date: ", datetime.datetime.
        #       fromtimestamp(modification_date - EPOCH_ADJUSTER))
        date_and_time = str(datetime.datetime.fromtimestamp(creation_date -
                                                            EPOCH_ADJUSTER))
    video_file.close()
    return date_and_time
