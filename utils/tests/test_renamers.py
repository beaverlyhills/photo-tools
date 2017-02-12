from utils.renamers import (add_date_to_filename, organize_by_year_and_date,
                            rename_with_date_and_time,
                            only_rename_specific_model,
                            only_rename_specific_lens,
                            only_rename_specific_tag)
from utils.types import FileInfo


def test_add_date_to_filename():
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags=None)
    new_directory, new_filename = add_date_to_filename(file_info,
                                                       None,
                                                       'dir/subdir',
                                                       'file.1.jpg')
    assert new_directory == 'dir/subdir'
    assert new_filename == '2017-01-01 file.1.jpg'

    # Test recursion
    new_directory, new_filename = add_date_to_filename(file_info,
                                                       None,
                                                       new_directory,
                                                       new_filename)

    assert new_directory == 'dir/subdir'
    assert new_filename == '2017-01-01 file.1.jpg'


def test_organize_by_year_and_date():
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags=None)
    new_directory, new_filename = organize_by_year_and_date(file_info,
                                                            None,
                                                            'dir/subdir',
                                                            'file.1.jpg')
    assert new_directory == 'dir/subdir/2017/2017-01-01'
    assert new_filename == 'file.1.jpg'

    # Test recursion
    new_directory, new_filename = organize_by_year_and_date(file_info,
                                                            None,
                                                            new_directory,
                                                            new_filename)
    assert new_directory == 'dir/subdir/2017/2017-01-01'
    assert new_filename == 'file.1.jpg'


def test_rename_with_date_and_time():
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags=None)
    new_directory, new_filename = rename_with_date_and_time(file_info,
                                                            None,
                                                            'dir/subdir',
                                                            'file.1.jpg')
    assert new_directory == 'dir/subdir'
    assert new_filename == '2017-01-01 12.30.15.jpg'

    # Test recursion
    new_directory, new_filename = rename_with_date_and_time(file_info,
                                                            None,
                                                            new_directory,
                                                            new_filename)
    assert new_directory == 'dir/subdir'
    assert new_filename == '2017-01-01 12.30.15.jpg'


def test_only_rename_specific_model():
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags={'Image Model': 'A'})
    new_directory, new_filename = only_rename_specific_model(file_info,
                                                             'A',
                                                             'dir/subdir',
                                                             'file.1.jpg')
    assert new_directory == 'dir/subdir'
    assert new_filename == 'file.1.jpg'

    # Check model doesn't match
    new_directory, new_filename = only_rename_specific_model(file_info,
                                                             'B',
                                                             'dir/subdir',
                                                             'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'

    # Check no model specified
    new_directory, new_filename = only_rename_specific_model(file_info,
                                                             None,
                                                             'dir/subdir',
                                                             'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'

    # Check missing tag
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags=None)
    new_directory, new_filename = only_rename_specific_model(file_info,
                                                             'A',
                                                             'dir/subdir',
                                                             'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'

    new_directory, new_filename = only_rename_specific_model(file_info,
                                                             None,
                                                             'dir/subdir',
                                                             'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'


def test_only_rename_specific_lens():
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags={'EXIF LensModel': 'A'})
    new_directory, new_filename = only_rename_specific_lens(file_info,
                                                            'A',
                                                            'dir/subdir',
                                                            'file.1.jpg')
    assert new_directory == 'dir/subdir'
    assert new_filename == 'file.1.jpg'

    # Check model doesn't match
    new_directory, new_filename = only_rename_specific_lens(file_info,
                                                            'B',
                                                            'dir/subdir',
                                                            'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'

    # Check no model specified
    new_directory, new_filename = only_rename_specific_lens(file_info,
                                                            None,
                                                            'dir/subdir',
                                                            'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'

    # Check missing tag
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags=None)
    new_directory, new_filename = only_rename_specific_lens(file_info,
                                                            'A',
                                                            'dir/subdir',
                                                            'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'

    new_directory, new_filename = only_rename_specific_lens(file_info,
                                                            None,
                                                            'dir/subdir',
                                                            'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'


def test_only_rename_specific_tag():
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags={'TAG': 'Value:1'})
    new_directory, new_filename = only_rename_specific_tag(file_info,
                                                           'TAG:Value:1',
                                                           'dir/subdir',
                                                           'file.1.jpg')
    assert new_directory == 'dir/subdir'
    assert new_filename == 'file.1.jpg'

    # Check model doesn't match
    new_directory, new_filename = only_rename_specific_tag(file_info,
                                                           'B',
                                                           'dir/subdir',
                                                           'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'

    # Check no model specified
    new_directory, new_filename = only_rename_specific_tag(file_info,
                                                           None,
                                                           'dir/subdir',
                                                           'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'

    # Check missing tag
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags=None)
    new_directory, new_filename = only_rename_specific_tag(file_info,
                                                           'A',
                                                           'dir/subdir',
                                                           'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'

    new_directory, new_filename = only_rename_specific_tag(file_info,
                                                           None,
                                                           'dir/subdir',
                                                           'file.1.jpg')
    assert new_directory == 'src'
    assert new_filename == 'file.1.jpg'
