from collections import namedtuple

FileInfo = namedtuple("FileInfo",
                      "source_directory source_filename date_and_time tags")

RenamerInfo = namedtuple('RenamerInfo', 'renamer params')
