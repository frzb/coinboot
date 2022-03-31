#!/usr/bin/python3

# Copyright (C) 2018, 2021-2022 Gunter Miegel coinboot.io
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

from os import scandir
import os
import tarfile
import re
from subprocess import call
from docopt import docopt

DPKG_STATUS = "/var/lib/dpkg/status"
INITIAL_DPKG_STATUS = "/tmp/initial_status"
FINAL_DPKG_STATUS = "/tmp/dpkg_status"
PLUGIN_DIR = "/mnt/plugin/rootfs"

EXCLUDE = (
    "/dev/",
    "/proc/",
    "/run/",
    "/sys/",
    "/tmp/",
    "/usr/src",
    "/usr/include",
    "/usr/share/dbus-1/system-services",
    "/vagrant",
    "/var/cache",
    "/var/lib/apt/lists",
    "/var/lib/dpkg/[^info]",
    "/var/log",
    ".*__pycache__.*",
    ".wget-hsts",
    r".*\.cache",
)


def find(path_to_scan):
    """Returns generator object with results similar to a Unix find command run without options
    traversing recursive a directory tree and returning all file paths
    """
    for entry in scandir(path_to_scan):
        if entry.is_dir(follow_symlinks=False):
            yield entry.path
            yield from find(entry.path)
        else:
            yield entry.path


def create_tar_archive(archive_name, files_for_plugin_archive):
    """Create tar archive form a list of files"""
    tar = tarfile.open(archive_name, "w:gz")
    for path in files_for_plugin_archive:
        # If a file was deleted which was in the lower directory
        # a whiteout file is created in the upper directory.
        # So we don't can look at the upper director to track the
        # deletion of such files.
        # Else we look if the file is present at the merged directory
        # with 'os.path.exists()'.
        if os.path.exists(path):
            # We have to specfiy explictly the file name in
            # the archive to get an absolute path wit a leading '/'
            # Attention: directories are added recursively be default
            tar.add(path, recursive=False, arcname=path)
        else:
            print("Whiteout file from lower dir:", path)
    tar.close()


def main(arguments):
    if arguments["start"]:
        call(["cp", "-v", DPKG_STATUS, INITIAL_DPKG_STATUS])
    elif arguments["finish"]:
        f = open(FINAL_DPKG_STATUS, "w")
        call(
            [
                "dpkg_status.py",
                "--old",
                INITIAL_DPKG_STATUS,
                "--new",
                DPKG_STATUS,
                "--diff",
            ],
            stdout=f,
        )

        files_for_plugin_archive = []
        excluded = []
        included = []

        for path in list(find(PLUGIN_DIR)):
            cleaned_path = re.sub(PLUGIN_DIR, "", path)
            # FIXME: Switch to re.match() against path without PLUGIN_DIR prefix
            if any(re.findall(pattern, cleaned_path) for pattern in EXCLUDE):
                # print("Excluded:", cleaned_path)
                excluded.append(cleaned_path)
            else:
                files_for_plugin_archive.append(cleaned_path)
                included.append(cleaned_path)

        for entry in excluded:
            print("Excluded:", entry)
        print("------------------------------------")
        for entry in included:
            print("Included:", entry)
        print("------------------------------------")

        files_for_plugin_archive.append(FINAL_DPKG_STATUS)

        archive_name = arguments["<plugin_name>"] + ".tar.gz"

        create_tar_archive(archive_name, files_for_plugin_archive)
        
        print("------------------------------------")

        print("------------------------------------")

        print("Created Coinboot Plugin:", archive_name)


if __name__ == "__main__":
    arguments = docopt(__doc__, version="Create Coinboot Plugins v0.1")
    main(arguments)
