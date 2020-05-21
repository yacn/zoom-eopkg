#!/usr/bin/env python3

import os
import shlex
import subprocess
import sys
import tempfile
import time

import yaml

"""
1. Download package
2. sha256sum
3. extract deb
4. xtract data.tar*
5. read opt/zoom/version.txt
4. write new package.yml
"""

with open('package.yml', 'r') as f:
    data = yaml.load(f)

# package.yml source field is a list of dicts where dict key is url and dict value is sha256sum
# there's only one source here so flatten to the two items we need:
source_url, current_checksum = list(data['source'][0].items()).pop() 

fname = os.path.basename(source_url)
etag = f'{fname}.etag'

print(f"fetching latest {fname} from {source_url}")
subprocess.check_output(
    shlex.split(f'curl -L -o {fname} --etag-save {etag} --etag-compare {etag} {source_url}')
)

# using etags with curl means the file is only downloaded if there's changes
# so we only act if the file was modified in the last sixty seconds
if (time.time() - os.path.getmtime(f'./{fname}')) >= 60:
    print(f'{fname} up to date, nothing to do')
    sys.exit(0)

print(f"generating checksum of {fname}")
new_checksum, _ = subprocess.check_output(
    shlex.split(f'sha256sum {fname}')
).decode().strip().split()

# if we download the file and its checksum matches package.yml (e.g. first run)
# bail out since there's no update
if new_checksum == current_checksum:
    print(f'{fname} up to date, nothing to do')
    sys.exit(0)


print("extracting version from .deb")
with tempfile.TemporaryDirectory() as tmpdir:
    subprocess.check_output(shlex.split(
        f'ar x --output {tmpdir} {os.path.join(os.getcwd(), fname)}'
    ))
    subprocess.check_output(shlex.split('tar xf data.tar.xz'), cwd=tmpdir)
    # use zoom's provided version. we could use the deb package version but as 
    # they should always be equivalent, use vendor's version instead of pkger
    with open(os.path.join(tmpdir, 'opt/zoom/version.txt'), 'r') as f:
        new_version = f.read().strip()

new_release = data['release'] + 1
print(" ".join([
    f"version: {data['version']} -> {new_version}",
    f"checksum: {data['source'][0][source_url]} -> {new_checksum}",
    f"release: {data['release']} -> {new_release}"
]))

print("updating package.yml")
package_dot_yml = os.path.join(os.getcwd(), 'package.yml')
package_dot_yml_dot_bak = f"{package_dot_yml}.bak"
with tempfile.NamedTemporaryFile(dir=os.getcwd()) as tmpfp:
    with open(package_dot_yml, 'rb') as pkg_yml:
        print(f'./update-package-yml.sh {new_version} {new_checksum} {new_release}')
        subprocess.run(shlex.split(f'./update-package-yml.sh {new_version} {new_checksum} {new_release}'),
                stdin=pkg_yml, stdout=tmpfp
        )
    if os.path.exists(package_dot_yml_dot_bak):
        os.unlink(package_dot_yml_dot_bak)
    os.link(package_dot_yml, package_dot_yml_dot_bak)
    os.unlink(package_dot_yml)
    os.link(tmpfp.name, package_dot_yml)
