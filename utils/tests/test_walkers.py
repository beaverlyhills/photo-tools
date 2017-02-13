from utils.walkers import make_new_path, process_file
from utils.types import RenamerInfo
from utils.types import FileInfo


def test_no_change():
    renamers = []
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags=None)
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'dir/subdir/file.1.jpg'


def _simple_original_mover(file_info, params, output_directory, filename):
    return output_directory, file_info.source_filename


def _simple_date_renamer(file_info, params, output_directory, filename):
    return output_directory, file_info.date_and_time


def _simple_date_adder(file_info, params, output_directory, filename):
    return output_directory, 'd{} {}'.format(file_info.date_and_time, filename)


def _simple_date_mover(file_info, params, output_directory, filename):
    return '{}/{}'.format(output_directory, file_info.date_and_time), filename


def _simple_model_filter(file_info, params, output_directory, filename):
    if file_info.tags['Image Model'] == params:
        return output_directory, filename
    return file_info.source_directory, file_info.source_filename


def test_all():
    # Add date, move to folder, change name to date
    renamers = [RenamerInfo(renamer=_simple_date_adder, params=None),
                RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_renamer, params=None)]
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags={'Image Model': 'B'})
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'dir/subdir/2017-01-01 12:30:15/2017-01-01 12:30:15'

    # Add date, move to folder, change name to date, change name to original
    renamers = [RenamerInfo(renamer=_simple_date_adder, params=None),
                RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_renamer, params=None),
                RenamerInfo(renamer=_simple_original_mover, params=None)]
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags={'Image Model': 'B'})
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'dir/subdir/2017-01-01 12:30:15/file.1.jpg'

    # Move to folder, add date to name, change name to date
    renamers = [RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_adder, params=None),
                RenamerInfo(renamer=_simple_date_renamer, params=None)]
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'dir/subdir/2017-01-01 12:30:15/2017-01-01 12:30:15'

    # change name to date, move to folder, add date to name
    renamers = [RenamerInfo(renamer=_simple_date_renamer, params=None),
                RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_adder, params=None)]
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'dir/subdir/2017-01-01 12:30:15/d2017-01-01 12:30:15' + \
                   ' 2017-01-01 12:30:15'

    # change name to date, move to folder, add date to name, apply tag filter
    # that doesn't match and restores original path
    renamers = [RenamerInfo(renamer=_simple_date_renamer, params=None),
                RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_adder, params=None),
                RenamerInfo(renamer=_simple_model_filter, params='A')]
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'src/file.1.jpg'

    # Move to folder, add date, apply tag filter that matches and keeps new
    # name
    renamers = [RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_adder, params=None),
                RenamerInfo(renamer=_simple_model_filter, params='B')]
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'dir/subdir/2017-01-01 12:30:15/d2017-01-01 12:30:15' + \
                   ' file.1.jpg'


def _test_image_parser(path):
    success = '.jpg' in path
    date_and_time = '2017-01-01 12:30:15'
    tags = {'Image Model': 'A'}
    is_video = False
    return success, date_and_time, tags, is_video


def _test_video_parser(path):
    success = '.mov' in path
    date_and_time = '2017-01-01 12:30:15'
    tags = None
    is_video = True
    return success, date_and_time, tags, is_video


def test_process_file():
    # Image file
    renamers = [RenamerInfo(renamer=_simple_date_renamer, params=None)]
    parsers = [_test_image_parser, _test_video_parser]
    old_path, new_path, date_and_time = process_file('src', 'file.1.jpg',
                                                     'dir/photo',
                                                     'dir/video',
                                                     renamers, parsers)
    assert old_path == 'src/file.1.jpg'
    assert new_path == 'dir/photo/2017-01-01 12:30:15'
    assert date_and_time == '2017-01-01 12:30:15'

    # Video file
    old_path, new_path, date_and_time = process_file('src', 'file.1.mov',
                                                     'dir/photo',
                                                     'dir/video',
                                                     renamers, parsers)
    assert old_path == 'src/file.1.mov'
    assert new_path == 'dir/video/2017-01-01 12:30:15'
    assert date_and_time == '2017-01-01 12:30:15'
