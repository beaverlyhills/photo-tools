import re


def add_date_to_filename(file_info, params, output_directory, filename):
    """
    Adds date to the beginning of filename. Existing date will be removed.
    """
    year = file_info.date_and_time.split('-')[0]
    date = file_info.date_and_time.split(' ')[0]
    # Strip any existing dates
    filename_without_date = re.sub(r'\s*\d{4}-\d{2}-\d{2}\s*', r'', filename)
    new_filename = '{date} {filename}'.format(year=year, date=date,
                                              filename=filename_without_date)
    return output_directory, new_filename


def organize_by_year_and_date(file_info, params, output_directory, filename):
    """
    Move files into subfolders by year and date, such as '2017/2017-01-01'.
    """
    year = file_info.date_and_time.split('-')[0]
    date = file_info.date_and_time.split(' ')[0]
    new_subdirectory = '/{year}/{date}'.format(year=year, date=date)
    output_without_subdir = output_directory.replace(new_subdirectory, '')
    new_directory = '{parent}{subdir}'.format(parent=output_without_subdir,
                                              subdir=new_subdirectory)
    return new_directory, filename


def rename_with_date_and_time(file_info, params, output_directory, filename):
    """
    Rename file using date and time.
    """
    extension = filename.split('.')[-1]
    safe_date = re.sub(r'[^\d \-]', r'.', file_info.date_and_time)
    new_filename = '{filename}.{ext}'.format(filename=safe_date, ext=extension)
    return output_directory, new_filename


def _match_tag(tags, name, value):
    """
    Check if EXIF tag is present
    """
    return tags and name and name in tags and str(tags[name]) == value


def only_rename_specific_model(file_info, model, output_directory, filename):
    """
    Keeps original path if Image Model EXIF tag doesn't match requested model.
    Specify model using only_rename_specific_model=model in command line.
    Should be used as last renamer in chain.
    """
    if _match_tag(file_info.tags, 'Image Model', model):
        return output_directory, filename

    return file_info.source_directory, file_info.source_filename


def only_rename_specific_lens(file_info, lens, output_directory, filename):
    """
    Keeps original path if EXIF LensModel tag doesn't match requested lens.
    Specify lens model using only_rename_specific_lens=lens in command line.
    Should be used as last renamer in chain.
    """
    if _match_tag(file_info.tags, 'EXIF LensModel', lens):
        return output_directory, filename

    return file_info.source_directory, file_info.source_filename


def only_rename_specific_tag(file_info, spec, output_directory, filename):
    """
    Uses original path if EXIF tag doesn't match requested value.
    Tag name and value are specified as only_rename_specific_tag=name:value in
    command line.
    Should be used as last renamer in chain.
    """
    if not spec or ':' not in spec:
        return file_info.source_directory, file_info.source_filename
    name, value = spec.split(':', 1)
    if _match_tag(file_info.tags, name, value):
        return output_directory, filename

    return file_info.source_directory, file_info.source_filename
