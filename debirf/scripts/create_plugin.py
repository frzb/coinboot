#!/usr/bin/python3

# Copyright (C) 2018 Gunter Miegel coinboot.io
#
# This file is part of Coinboot.
#
# Coinboot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Create Coinboot Plugins

Usage:
  create_plugin start
  create_plugin finish <plugin_name>

Options:
  -h --help     Show this screen.

"""

import os
import tarfile
import re
from subprocess import call
from docopt import docopt

DPKG_STATUS = '/var/lib/dpkg/status'
INITIAL_DPKG_STATUS = '/tmp/initial_status'
FINAL_DPKG_STATUS = '/tmp/dpkg_status'
PLUGIN_DIR = '/mnt/plugin/rootfs'

EXCLUDE = ('/dev/',
           '/proc/',
           '/run/',
           '/sys/',
           '/tmp/',
           '/usr/src',
           '/usr/include',
           '/usr/share/dbus-1/system-services',
           '/vagrant',
           '/var/cache',
           '/var/lib/apt/lists',
           '/var/lib/dpkg/[^info]',
           '/var/log',
           '.*__pycache__.*',
           '.wget-hsts'
           )


def find(path_to_walk):
    """Return results similar to the Unix find command run without options
    i.e. traverse a directory tree and return all the file paths
    """
    return [os.path.join(path, file)
            for (path, dirs, files) in os.walk(path_to_walk)
            for file in files]

def main(arguments):
    #print(arguments)
    if arguments['start']:
        call(['cp', '-v', DPKG_STATUS, INITIAL_DPKG_STATUS])
    elif arguments['finish']:
        f = open(FINAL_DPKG_STATUS, 'w')
        call(['dpkg_status.py', '--old', INITIAL_DPKG_STATUS, '--new', DPKG_STATUS, '--diff'], stdout=f)

        files_for_plugin_archive = []

        for path in find(PLUGIN_DIR):
            cleaned_path = re.sub(PLUGIN_DIR, '', path)
            # FIXME: Switch to re.match() against path without PLUGIN_DIR prefix
            if any(re.findall(pattern, cleaned_path) for pattern in EXCLUDE):
                print('Excluded:', cleaned_path)
            else:
                print('Included:', cleaned_path)
                files_for_plugin_archive.append(cleaned_path)

        files_for_plugin_archive.append(FINAL_DPKG_STATUS)

        tar = tarfile.open(arguments['<plugin_name>'] + ".tar.gz", "w:gz")
        for path in files_for_plugin_archive:
            # If a file was deleted which was in the lower directory
            # a whiteout file is created in the upper directory.
            # So we don't can look at the upper director to track the
            # deletion of such files. Else we look if the file is there
            # at the merged directory with 'os.path.exists()'.
            if os.path.exists(path):
                # We have to specfiy explictly the file name in
                # the archive to get an absolute path wit a leading '/'
                tar.add(path, arcname=path)
            else:
                print('Whiteout file from lower dir:', path)
        tar.close()


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Create Coinboot Plugins v0.1')
    main(arguments)
