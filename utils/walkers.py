import parsers
import os
from types import FileInfo


def walk_folder(source_directory, destination_directory,
                destination_video_directory, renamers, dry_run):
    if dry_run:
        print('Dry run, no changes will be applied')
    for (dirpath, dirnames, filenames) in os.walk(source_directory):
        for filename in filenames:
            old_path = '{dir}/{file}'.format(dir=dirpath, file=filename)
            # print("Process: {}".format(old_path))
            filename_lower = filename.lower()
            if filename_lower.endswith(".jpg") or \
               filename_lower.endswith(".jpeg"):
                output_directory = destination_directory
                tags = parsers.get_exif_tags(old_path)
                date_and_time = parsers.get_date_and_time_from_tags(tags)
            elif filename_lower.endswith(".mov"):
                output_directory = destination_video_directory
                tags = None
                date_and_time = parsers.parse_video(old_path)
            else:
                print("Skip {}: unknown file format".format(old_path))
                continue
            if not date_and_time:
                print("Skip {}: no date found".format(old_path))
                continue
            file_info = FileInfo(source_directory=dirpath,
                                 source_filename=filename,
                                 date_and_time=date_and_time,
                                 tags=tags)
            new_path = make_new_path(file_info, output_directory, renamers)
            if new_path == old_path:
                print("Skip {}: no rename needed {}".format(old_path,
                                                            date_and_time))
                continue
            new_path = handle_duplicates(old_path, new_path)
            print('Renaming {old} to {new} with date {datetime}'.
                  format(old=old_path, new=new_path, datetime=date_and_time))
            if dry_run:
                continue
            create_path_and_rename(old_path, new_path, date_and_time)


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
    new_path = '{dir}/{filename}'.format(dir=new_directory,
                                         filename=new_filename)
    return new_path


def handle_duplicates(old_path, path):
    i = 0
    new_path = path
    path_parts = path.rsplit('.', 1)
    while os.path.exists(new_path):
        i += 1
        new_path = '{}-{}.{}'.format(path_parts[0], i, path_parts[1])
    return new_path
