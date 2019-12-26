import sys
import utils.parsers as parsers


if len(sys.argv) < 2:
    print(('Usage: {} file').format(sys.argv[0]))
    sys.exit()

header = parsers.get_movie_header(sys.argv[1])
if not header:
    print('Could not parse video file')
    sys.exit()

print(header)
