import os
from utils.walkers import make_new_path, process_file
from utils.renamers import RenamerInfo
from utils.walkers import FileInfo

_sample_src = 'src'
_sample_dst = os.path.join('dir', 'subdir')
_sample_file = 'file.1.jpg'
_sample_video = 'file.1.mov'
_sample_date = '2017-01-01 12:30:15'


def test_no_change():
    renamers = []
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags=None)
    path = make_new_path(file_info, _sample_dst, renamers)
    assert path == os.path.join(_sample_dst, _sample_file)


def _simple_original_mover(file_info, params, output_directory, filename):
    return output_directory, file_info.source_filename


def _simple_date_renamer(file_info, params, output_directory, filename):
    return output_directory, file_info.date_and_time


def _simple_date_adder(file_info, params, output_directory, filename):
    return output_directory, 'd{} {}'.format(file_info.date_and_time, filename)


def _simple_date_mover(file_info, params, output_directory, filename):
    return os.path.join(output_directory, file_info.date_and_time), filename


def _simple_model_filter(file_info, params, output_directory, filename):
    if file_info.tags['Image Model'] == params:
        return output_directory, filename
    return file_info.source_directory, file_info.source_filename


def test_all():
    # Add date, move to folder, change name to date
    renamers = [RenamerInfo(renamer=_simple_date_adder, params=None),
                RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_renamer, params=None)]
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags={'Image Model': 'B'})
    path = make_new_path(file_info, _sample_dst, renamers)
    assert path == os.path.join(_sample_dst, _sample_date, _sample_date)

    # Add date, move to folder, change name to date, change name to original
    renamers = [RenamerInfo(renamer=_simple_date_adder, params=None),
                RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_renamer, params=None),
                RenamerInfo(renamer=_simple_original_mover, params=None)]
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags={'Image Model': 'B'})
    path = make_new_path(file_info, _sample_dst, renamers)
    assert path == os.path.join(_sample_dst, _sample_date, _sample_file)

    # Move to folder, add date to name, change name to date
    renamers = [RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_adder, params=None),
                RenamerInfo(renamer=_simple_date_renamer, params=None)]
    path = make_new_path(file_info, _sample_dst, renamers)
    assert path == os.path.join(_sample_dst, _sample_date, _sample_date)

    # change name to date, move to folder, add date to name
    renamers = [RenamerInfo(renamer=_simple_date_renamer, params=None),
                RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_adder, params=None)]
    path = make_new_path(file_info, _sample_dst, renamers)
    assert path == os.path.join(_sample_dst, _sample_date, 'd' +
                                _sample_date + ' ' + _sample_date)

    # change name to date, move to folder, add date to name, apply tag filter
    # that doesn't match and restores original path
    renamers = [RenamerInfo(renamer=_simple_date_renamer, params=None),
                RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_adder, params=None),
                RenamerInfo(renamer=_simple_model_filter, params='A')]
    path = make_new_path(file_info, _sample_dst, renamers)
    assert path == os.path.join(_sample_src, _sample_file)

    # Move to folder, add date, apply tag filter that matches and keeps new
    # name
    renamers = [RenamerInfo(renamer=_simple_date_mover, params=None),
                RenamerInfo(renamer=_simple_date_adder, params=None),
                RenamerInfo(renamer=_simple_model_filter, params='B')]
    path = make_new_path(file_info, _sample_dst, renamers)
    assert path == os.path.join(_sample_dst, _sample_date, 'd' +
                                _sample_date + ' ' + _sample_file)


def _test_image_parser(path):
    if '.jpg' not in path:
        return None
    date_and_time = _sample_date
    tags = {'Image Model': 'A'}
    is_video = False
    return date_and_time, tags, is_video


def _test_video_parser(path):
    if '.mov' not in path:
        return None
    date_and_time = _sample_date
    tags = None
    is_video = True
    return date_and_time, tags, is_video


def test_process_file():

    _photo_dir = os.path.join('dir', 'photo')
    _video_dir = os.path.join('dir', 'video')

    # Image file
    renamers = [RenamerInfo(renamer=_simple_date_renamer, params=None)]
    parsers = [_test_image_parser, _test_video_parser]
    old_path, new_path, date_and_time = process_file(_sample_src,
                                                     _sample_file,
                                                     _photo_dir,
                                                     _video_dir,
                                                     renamers, parsers)
    assert old_path == os.path.join(_sample_src, _sample_file)
    assert new_path == os.path.join(_photo_dir, _sample_date)
    assert date_and_time == _sample_date

    # Video file
    old_path, new_path, date_and_time = process_file(_sample_src,
                                                     _sample_video,
                                                     _photo_dir,
                                                     _video_dir,
                                                     renamers, parsers)
    assert old_path == os.path.join(_sample_src, _sample_video)
    assert new_path == os.path.join(_video_dir, _sample_date)
    assert date_and_time == _sample_date
