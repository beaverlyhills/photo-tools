from utils.walkers import make_new_path
from utils.renamers import (add_date_to_filename, organize_by_year_and_date,
                            rename_with_date_and_time)


def test_no_change():
    renamers = []
    path = make_new_path('dir/subdir', 'file.1.jpg', '2017-01-01 12:30:15',
                         renamers)
    assert path == 'dir/subdir/file.1.jpg'


def test_all():
    renamers = [add_date_to_filename, organize_by_year_and_date,
                rename_with_date_and_time]
    path = make_new_path('dir/subdir', 'file.1.jpg', '2017-01-01 12:30:15',
                         renamers)
    assert path == 'dir/subdir/2017/2017-01-01/2017-01-01 12.30.15.jpg'

    renamers = [organize_by_year_and_date, add_date_to_filename,
                rename_with_date_and_time]
    path = make_new_path('dir/subdir', 'file.1.jpg', '2017-01-01 12:30:15',
                         renamers)
    assert path == 'dir/subdir/2017/2017-01-01/2017-01-01 12.30.15.jpg'

    renamers = [rename_with_date_and_time, organize_by_year_and_date,
                add_date_to_filename]
    path = make_new_path('dir/subdir', 'file.1.jpg', '2017-01-01 12:30:15',
                         renamers)
    assert path == 'dir/subdir/2017/2017-01-01/2017-01-01 12.30.15.jpg'
