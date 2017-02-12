from utils.walkers import make_new_path
from utils.renamers import (add_date_to_filename, organize_by_year_and_date,
                            rename_with_date_and_time,
                            only_rename_specific_model)
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


def test_all():
    renamers = [RenamerInfo(renamer=add_date_to_filename, params=None),
                RenamerInfo(renamer=organize_by_year_and_date, params=None),
                RenamerInfo(renamer=rename_with_date_and_time, params=None)]
    file_info = FileInfo(source_directory='src',
                         source_filename='file.1.jpg',
                         date_and_time='2017-01-01 12:30:15',
                         tags={'Image Model': 'B'})
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'dir/subdir/2017/2017-01-01/2017-01-01 12.30.15.jpg'

    renamers = [RenamerInfo(renamer=organize_by_year_and_date, params=None),
                RenamerInfo(renamer=add_date_to_filename, params=None),
                RenamerInfo(renamer=rename_with_date_and_time, params=None)]
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'dir/subdir/2017/2017-01-01/2017-01-01 12.30.15.jpg'

    renamers = [RenamerInfo(renamer=rename_with_date_and_time, params=None),
                RenamerInfo(renamer=organize_by_year_and_date, params=None),
                RenamerInfo(renamer=add_date_to_filename, params=None)]
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'dir/subdir/2017/2017-01-01/2017-01-01 12.30.15.jpg'

    renamers = [RenamerInfo(renamer=rename_with_date_and_time, params=None),
                RenamerInfo(renamer=organize_by_year_and_date, params=None),
                RenamerInfo(renamer=add_date_to_filename, params=None),
                RenamerInfo(renamer=only_rename_specific_model, params='A')]
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'src/file.1.jpg'

    renamers = [RenamerInfo(renamer=rename_with_date_and_time, params=None),
                RenamerInfo(renamer=organize_by_year_and_date, params=None),
                RenamerInfo(renamer=add_date_to_filename, params=None),
                RenamerInfo(renamer=only_rename_specific_model, params='B')]
    path = make_new_path(file_info, 'dir/subdir', renamers)
    assert path == 'dir/subdir/2017/2017-01-01/2017-01-01 12.30.15.jpg'
