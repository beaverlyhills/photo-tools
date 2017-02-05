import sys
import utils.renamers as renamers
import utils.walkers as walkers


if len(sys.argv) < 5:
    print(('Usage: {} rename_method1,rename_method2,... ' +
           'source_directory destination_directory ' +
           'destination_video_directory').format(sys.argv[0]))
    sys.exit()

dry_run = True

for i in range(1, len(sys.argv)):
    arg = sys.argv[i]
    if not arg.startswith('-'):
        break
    if arg == '-apply':
        dry_run = False

rename_methods = sys.argv[i].split(',')
source_directory = sys.argv[i + 1].strip("/")
destination_directory = sys.argv[i + 2].strip("/")
destination_video_directory = sys.argv[i + 3].strip("/")

renamers_chain = []
try:
    for renamer_name in rename_methods:
        renamers_chain.append(getattr(renamers, renamer_name))
except:
    print('Unknown rename method: {}'.format(renamer_name))
    help(renamers)
    sys.exit()

walkers.walk_folder(source_directory, destination_directory,
                    destination_video_directory, renamers_chain, dry_run)
