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

"""
This script consumes two DPKG status files and can display the difference
between both on package section level.
It can also merge both files to a union set with no redudant packages sections.

The purpose of this is to track status changes of DPKG between two points in time in a separate file.
And it provides the abillity to merge that file into an existing DPKG status file.
"""

import re
import argparse

def create_status_dict(path_to_file):
    """
    Returns a dict with the processed content of a DPKG status file.
    Reads the given DPKG status file and extracts the individual package text blocks.
    These text blocks are written to the returned dict where the package name acts as key.
    """
    status_file = open(path_to_file, 'r', encoding='utf-8').read().split('\n\n')
    status_dict = {}
    for package_block in status_file:
        package_name = re.search('((?<=Package:\s)\S+)', package_block)
        if package_name:
            key = package_name.group(0)
            status_dict.update({key: package_block})
    return status_dict

def print_dict(set_dict):
    """
    Prints the package text blocks from a dict.
    """
    for package_block in set_dict:
        #print(set_dict[package_block] + '\n')
        print(set_dict[package_block] + '\n')

def main():
    """
    Setup the arguments.
    And apply the choosen set operations to the dict.
    """
    parser = argparse.ArgumentParser(description='Merge two dpkg status files.')
    parser.add_argument('--old', dest='old')
    parser.add_argument('--new', dest='new')
    parser.add_argument('--diff', action='store_true', dest='diff')
    parser.add_argument('--union', action='store_true', dest='union')
    args = parser.parse_args()
    old = args.old
    new = args.new
    set_old = set(create_status_dict(old).items())
    set_new = set(create_status_dict(new).items())

    if args.diff:
        dict_diff = dict(set_new - set_old)
        print_dict(dict_diff)

    if args.union:
        dict_union = dict(set_new | set_old)
        print_dict(dict_union)

main()
