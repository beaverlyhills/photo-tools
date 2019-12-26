import exifread
import collections
from .heic import process_heic, process_mpeg

ParserResult = collections.namedtuple('ParserResult',
                                      'date_and_time tags is_video')


def get_exif_tags(path):
    """
    Read EXIF data from image file and return tags
    """
    result = parse_image(path)
    if result:
        return result.tags
    result = parse_heic(path)
    if result:
        return result.tags
    return None


def get_movie_header(path):
    return process_mpeg(path)


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
    with open(path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
        if not tags:
            return None
        return ParserResult(date_and_time=get_date_and_time_from_tags(tags),
                            tags=tags, is_video=False)


def parse_heic(path):
    """
    Read EXIF data from HEIC image file and return date when it was taken
    """
    if not _match_extension(path, ['.heic']):
        return None
    tags = process_heic(path)
    if not tags:
        return None
    return ParserResult(date_and_time=get_date_and_time_from_tags(tags),
                        tags=tags, is_video=False)


def parse_video(path):
    """
    Parse MOV/MP4 file and find it's creation time
    """
    if not _match_extension(path, ['.mov', '.mp4']):
        return None
    header = process_mpeg(path)
    if not header:
        return None
    return ParserResult(date_and_time=header.creation_date,
                        tags=None, is_video=True)
