import parsers
import os
import collections

ProcessResult = collections.namedtuple('ProcessResult',
                                       'old_path new_path date_and_time')
FileInfo = collections.namedtuple("FileInfo",
                                  "source_directory source_filename "
                                  "date_and_time tags")

_parsers = [getattr(parsers, x) for x in dir(parsers) if 'parse_' in x]


def walk_folder(source_directory, destination_directory,
                destination_video_directory, renamers, dry_run):
    print('Start from %s' % source_directory)
    if not _parsers:
        print('No file format parsers found')
        return
    if dry_run:
        print('Dry run, no changes will be applied')
    for (dirpath, dirnames, filenames) in os.walk(source_directory):
        print('Walk %s' % dirpath)
        for filename in filenames:
            print('Check %s' % filename)
            result = process_file(dirpath, filename,
                                  destination_directory,
                                  destination_video_directory,
                                  renamers, _parsers)
            if not result:
                continue
            (old_path, new_path, date_and_time) = result
            if new_path:
                print('Renaming {old} to {new} with date {datetime}'.
                      format(old=old_path, new=new_path,
                             datetime=date_and_time))
                if dry_run:
                    continue
                create_path_and_rename(old_path, new_path, date_and_time)


def process_file(dirpath, filename, destination_directory,
                 destination_video_directory, renamers, parsers):
    result = None
    old_path = os.path.join(dirpath, filename)
    for parser in parsers:
        try:
            result = parser(old_path)
            if result:
                break
        except Exception:
            pass
    if not result:
        print("Skip {}: unknown file format".format(old_path))
        return None
    (date_and_time, tags, is_video) = result
    if not date_and_time:
        print("Skip {}: no date found".format(old_path))
        return None
    if is_video:
        output_directory = destination_video_directory
    else:
        output_directory = destination_directory
    file_info = FileInfo(source_directory=dirpath,
                         source_filename=filename,
                         date_and_time=date_and_time,
                         tags=tags)
    new_path = make_new_path(file_info, output_directory, renamers)
    if new_path == old_path:
        print("Skip {}: no rename needed {}".format(old_path,
                                                    date_and_time))
        return None
    new_path = handle_duplicates(old_path, new_path)
    return ProcessResult(old_path=old_path, new_path=new_path,
                         date_and_time=date_and_time)


def create_path_and_rename(old_path, new_path, date_and_time):
    final_directory = os.path.dirname(new_path)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    os.rename(old_path, new_path)


def make_new_path(file_info, output_directory, renamers):
    new_directory = output_directory
    new_filename = file_info.source_filename
    for renamer in renamers:
        new_directory, new_filename = renamer.renamer(file_info,
                                                      renamer.params,
                                                      new_directory,
                                                      new_filename)
    new_path = os.path.join(new_directory, new_filename)
    return new_path


def handle_duplicates(old_path, path):
    i = 0
    new_path = path
    path_parts = path.rsplit('.', 1)
    while os.path.exists(new_path):
        i += 1
        new_path = '{}-{}.{}'.format(path_parts[0], i, path_parts[1])
    return new_path
