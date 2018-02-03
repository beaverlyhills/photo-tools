Image catalog organizing tools
======

This is a small set of command-line tools written in Python 
to deal with my ever growing library of images.

Example usage
------
Move image and video files from Dropbox Camera Uploads folder to a `YYYY/YYYY-MM-DD` structured folders (similar to Lightroom):
```
python rename.py -apply organize_by_year_and_date "Dropbox/Camera Uploads" "Dropbox/Photos.todo" "Dropbox/Videos.todo"
```

Dependencies
------
* exifread - https://pypi.python.org/pypi/ExifRead
