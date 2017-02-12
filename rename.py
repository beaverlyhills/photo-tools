import sys
import utils.renamers as renamers
import utils.walkers as walkers
from utils.types import RenamerInfo


if len(sys.argv) < 5:
    print(('Usage: {} [-apply] rename_method1,rename_method2,... ' +
           'source_directory destination_directory ' +
           'destination_video_directory').format(sys.argv[0]))
    help(renamers)
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
    for renamer_spec in rename_methods:
        if '=' in renamer_spec:
            renamer_name, renamer_params = renamer_spec.split('=')
        else:
            renamer_name = renamer_spec
            renamer_params = None
        renamer_info = RenamerInfo(renamer=getattr(renamers, renamer_name),
                                   params=renamer_params)
        renamers_chain.append(renamer_info)
except:
    print('Unknown rename method: {}'.format(renamer_name))
    help(renamers)
    sys.exit()

walkers.walk_folder(source_directory, destination_directory,
                    destination_video_directory, renamers_chain, dry_run)
