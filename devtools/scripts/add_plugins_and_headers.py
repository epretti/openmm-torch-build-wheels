from delocate import wheeltools
from os.path import join, isdir
import os
import shutil
import sys

install_dir = sys.argv[1]
if len(sys.argv) == 2:
    ignore = None
else:
    platforms = sys.argv[2:]
    def ignore(dir, files):
        print('  dir:', dir)
        print('  files:', files)
        ignorefiles = []
        for platform in platforms:
            if platform[0] == '!':
                ignorefiles += [f for f in files if platform[1:] in f]
            else:
                ignorefiles += [f for f in files if platform not in f and not isdir(join(dir, f))]
            print('    platform:', platform)
            print('    ignorefiles:', ignorefiles)
        return ignorefiles
for filename in os.listdir('.'):
    if filename.startswith("openmmtorch") and filename.endswith('.whl'):
        print('filename:', filename)
        with wheeltools.InWheel(filename, filename):
            shutil.copytree(join(install_dir, 'lib'), 'openmmtorch.libs/lib', dirs_exist_ok=True, ignore=ignore)
