import os
from utils.renamers import (add_date_to_filename, organize_by_year_and_date,
                            rename_with_date_and_time,
                            only_rename_specific_model,
                            only_rename_specific_lens,
                            only_rename_specific_tag)
from utils.walkers import FileInfo

_sample_src = 'src'
_sample_dst = os.path.join('dir', 'subdir')
_sample_file = 'file.1.jpg'
_sample_date = '2017-01-01 12:30:15'


def test_add_date_to_filename():
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags=None)
    new_directory, new_filename = add_date_to_filename(file_info,
                                                       None,
                                                       _sample_dst,
                                                       _sample_file)
    assert new_directory == _sample_dst
    assert new_filename == '2017-01-01 ' + _sample_file

    # Test recursion
    new_directory, new_filename = add_date_to_filename(file_info,
                                                       None,
                                                       new_directory,
                                                       new_filename)

    assert new_directory == _sample_dst
    assert new_filename == '2017-01-01 ' + _sample_file


def test_organize_by_year_and_date():
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags=None)
    new_directory, new_filename = organize_by_year_and_date(file_info,
                                                            None,
                                                            _sample_dst,
                                                            _sample_file)
    assert new_directory == os.path.join(_sample_dst, '2017', '2017-01-01')
    assert new_filename == _sample_file

    # Test recursion
    new_directory, new_filename = organize_by_year_and_date(file_info,
                                                            None,
                                                            new_directory,
                                                            new_filename)
    assert new_directory == os.path.join(_sample_dst, '2017', '2017-01-01')
    assert new_filename == _sample_file


def test_rename_with_date_and_time():
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags=None)
    new_directory, new_filename = rename_with_date_and_time(file_info,
                                                            None,
                                                            _sample_dst,
                                                            _sample_file)
    assert new_directory == _sample_dst
    assert new_filename == '2017-01-01 12.30.15.jpg'

    # Test recursion
    new_directory, new_filename = rename_with_date_and_time(file_info,
                                                            None,
                                                            new_directory,
                                                            new_filename)
    assert new_directory == _sample_dst
    assert new_filename == '2017-01-01 12.30.15.jpg'


def test_only_rename_specific_model():
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags={'Image Model': 'A'})
    new_directory, new_filename = only_rename_specific_model(file_info,
                                                             'A',
                                                             _sample_dst,
                                                             _sample_file)
    assert new_directory == _sample_dst
    assert new_filename == _sample_file

    # Check model doesn't match
    new_directory, new_filename = only_rename_specific_model(file_info,
                                                             'B',
                                                             _sample_dst,
                                                             _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file

    # Check no model specified
    new_directory, new_filename = only_rename_specific_model(file_info,
                                                             None,
                                                             _sample_dst,
                                                             _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file

    # Check missing tag
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags=None)
    new_directory, new_filename = only_rename_specific_model(file_info,
                                                             'A',
                                                             _sample_dst,
                                                             _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file

    new_directory, new_filename = only_rename_specific_model(file_info,
                                                             None,
                                                             _sample_dst,
                                                             _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file


def test_only_rename_specific_lens():
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags={'EXIF LensModel': 'A'})
    new_directory, new_filename = only_rename_specific_lens(file_info,
                                                            'A',
                                                            _sample_dst,
                                                            _sample_file)
    assert new_directory == _sample_dst
    assert new_filename == _sample_file

    # Check model doesn't match
    new_directory, new_filename = only_rename_specific_lens(file_info,
                                                            'B',
                                                            _sample_dst,
                                                            _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file

    # Check no model specified
    new_directory, new_filename = only_rename_specific_lens(file_info,
                                                            None,
                                                            _sample_dst,
                                                            _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file

    # Check missing tag
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags=None)
    new_directory, new_filename = only_rename_specific_lens(file_info,
                                                            'A',
                                                            _sample_dst,
                                                            _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file

    new_directory, new_filename = only_rename_specific_lens(file_info,
                                                            None,
                                                            _sample_dst,
                                                            _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file


def test_only_rename_specific_tag():
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags={'TAG': 'Value:1'})
    new_directory, new_filename = only_rename_specific_tag(file_info,
                                                           'TAG:Value:1',
                                                           _sample_dst,
                                                           _sample_file)
    assert new_directory == _sample_dst
    assert new_filename == _sample_file

    # Check model doesn't match
    new_directory, new_filename = only_rename_specific_tag(file_info,
                                                           'B',
                                                           _sample_dst,
                                                           _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file

    # Check no model specified
    new_directory, new_filename = only_rename_specific_tag(file_info,
                                                           None,
                                                           _sample_dst,
                                                           _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file

    # Check missing tag
    file_info = FileInfo(source_directory=_sample_src,
                         source_filename=_sample_file,
                         date_and_time=_sample_date,
                         tags=None)
    new_directory, new_filename = only_rename_specific_tag(file_info,
                                                           'A',
                                                           _sample_dst,
                                                           _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file

    new_directory, new_filename = only_rename_specific_tag(file_info,
                                                           None,
                                                           _sample_dst,
                                                           _sample_file)
    assert new_directory == _sample_src
    assert new_filename == _sample_file
