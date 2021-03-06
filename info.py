import sys
import utils.parsers as parsers


if len(sys.argv) < 2:
    print(('Usage: {} file').format(sys.argv[0]))
    sys.exit()

tags = parsers.get_exif_tags(sys.argv[1])
if not tags:
    print('Could not parse image file')
    sys.exit()

for tag in tags.keys():
    print('{}: {}'.format(tag, tags[tag]))
