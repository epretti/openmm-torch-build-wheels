from delocate import wheeltools
from os.path import join, isdir
import os
import shutil
import subprocess
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
    if (filename.startswith('openmmtorch') or filename.startswith('OpenMM-Torch')) and filename.endswith('.whl'):
        print('filename:', filename)
        with wheeltools.InWheel(filename, filename):
            shutil.copytree(join(install_dir, 'lib'), 'OpenMM.libs/lib', dirs_exist_ok=True, ignore=ignore)
            site_packages = os.path.dirname(os.path.realpath(install_dir))
            for soname in os.listdir('.'):
                if soname.startswith('_openmmtorch') and soname.endswith('.so'):
                    # auditwheel doesn't understand that we should depend on
                    # libraries in OpenMM.libs (not openmmtorch.libs) so the
                    # _openmmtorch compiled library is patched up manually.
                    result = subprocess.run(['patchelf', '--print-rpath', soname], check=True, capture_output=True)
                    rpath = result.stdout.decode().strip().split(':')
                    new_rpath = []
                    for rpath_entry in rpath:
                        if not rpath_entry:
                            continue
                        new_rpath.append(os.path.join('$ORIGIN', os.path.relpath(os.path.realpath(rpath_entry), site_packages)))
                    print(f'patching {soname!r}: rpath {rpath} -> {new_rpath}')
                    subprocess.run(['patchelf', '--remove-rpath', soname], check=True)
                    subprocess.run(['patchelf', '--force-rpath', '--set-rpath', ':'.join(new_rpath), soname], check=True)
