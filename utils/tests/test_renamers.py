from utils.renamers import (add_date_to_filename, organize_by_year_and_date,
                            rename_with_date_and_time)


def test_add_date_to_filename():
    new_directory, new_filename = add_date_to_filename('dir/subdir',
                                                       'file.1.jpg',
                                                       '2017-01-01 12:30:15')
    assert new_directory == 'dir/subdir'
    assert new_filename == '2017-01-01 file.1.jpg'

    # Test recursion
    new_directory, new_filename = add_date_to_filename(new_directory,
                                                       new_filename,
                                                       '2017-01-01 12:30:15')

    assert new_directory == 'dir/subdir'
    assert new_filename == '2017-01-01 file.1.jpg'


def test_organize_by_year_and_date():
    new_directory, new_filename = organize_by_year_and_date('dir/subdir',
                                                            'file.1.jpg',
                                                            '2017-01-01 ' +
                                                            '12:30:15')
    assert new_directory == 'dir/subdir/2017/2017-01-01'
    assert new_filename == 'file.1.jpg'

    # Test recursion
    new_directory, new_filename = organize_by_year_and_date(new_directory,
                                                            new_filename,
                                                            '2017-01-01 ' +
                                                            '12:30:15')
    assert new_directory == 'dir/subdir/2017/2017-01-01'
    assert new_filename == 'file.1.jpg'


def test_rename_with_date_and_time():
    new_directory, new_filename = rename_with_date_and_time('dir/subdir',
                                                            'file.1.jpg',
                                                            '2017-01-01 ' +
                                                            '12:30:15')
    assert new_directory == 'dir/subdir'
    assert new_filename == '2017-01-01 12.30.15.jpg'

    # Test recursion
    new_directory, new_filename = rename_with_date_and_time(new_directory,
                                                            new_filename,
                                                            '2017-01-01 ' +
                                                            '12:30:15')
    assert new_directory == 'dir/subdir'
    assert new_filename == '2017-01-01 12.30.15.jpg'
