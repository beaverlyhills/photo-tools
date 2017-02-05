import re


def add_date_to_filename(output_directory, filename, date_and_time):
    """
    Adds date to the beginning of filename. Old date will be removed.
    """
    year = date_and_time.split('-')[0]
    date = date_and_time.split(' ')[0]
    # Strip any existing dates
    filename_without_date = re.sub(r'\s*\d{4}-\d{2}-\d{2}\s*', r'', filename)
    new_filename = '{date} {filename}'.format(year=year, date=date,
                                              filename=filename_without_date)
    return output_directory, new_filename


def organize_by_year_and_date(output_directory, filename, date_and_time):
    """
    Move files into subfolders by year and date, such as '2017/2017-01-01'.
    """
    year = date_and_time.split('-')[0]
    date = date_and_time.split(' ')[0]
    new_subdirectory = '/{year}/{date}'.format(year=year, date=date)
    output_without_subdir = output_directory.replace(new_subdirectory, '')
    new_directory = '{parent}{subdir}'.format(parent=output_without_subdir,
                                              subdir=new_subdirectory)
    return new_directory, filename


def rename_with_date_and_time(output_directory, filename, date_and_time):
    """
    Adds date to the beginning of filename. Old date will be removed.
    """
    extension = filename.split('.')[-1]
    safe_date = re.sub(r'[^\d \-]', r'.', date_and_time)
    new_filename = '{filename}.{ext}'.format(filename=safe_date, ext=extension)
    return output_directory, new_filename
