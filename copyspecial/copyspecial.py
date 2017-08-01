#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them
def get_special_paths(fromdir):
    '''
    Return a list of the absolute paths of all special files in the given
    directory. Special files are those whos name contains text of the form
    "__[sometext]__".
    '''
    special_paths = []

    # if the path is actually a directory
    if os.path.isdir(fromdir):

        # extract all filenames
        filenames = os.listdir(fromdir)

        # check if each path is a file and look for it's special-ness
        for name in filenames:
            if os.path.isfile(name):
                specialness = re.findall(r'__\w+__', name)

                # if the file is special, store its absolute path
                if specialness:
                    special_paths.append(os.path.join(os.path.abspath(fromdir),
                                                      name))

    # return the list of special paths
    return special_paths

def copy_to(frompaths, todir):
    '''
    Copy files in the list frompaths into the directory todir. If the directory
    does not exist, create it.
    '''
    # If the destination directory does not exist, create it
    if not os.path.isdir(todir):
        os.makedirs(todir)

    # Copy each special file to the destination directory
    for path in frompaths:
        shutil.copy(path,
                    os.path.join(todir, os.path.basename(path)))

def zip_to(paths, zippath):
    '''
    Take a list of paths and zip them all together in zippath using a 7-Zip
    command line process
    '''
    # check & enforce that the destination file has the zip extension
    zip_ext = re.search(r'\.zip$', zippath)
    if not zip_ext:
        zippath = zippath + '.zip'

    # create and print the command we will be running
    call = ['"C:\\Program Files\\7-Zip\\7z.exe"', 'a', '-tzip', zippath] + paths
    call_str = ' '.join(call)
    print 'Command to run:\n>>%s'%call_str

    # run the zip command
    status, output = getstatusoutput(call_str)
    if status:
        # pass along errors
        sys.stderr.write(output)
        sys.exit(1)

def check_filename_repeats(paths):
    '''
    Take a list of filepaths and check if any filenames are repeated. Return
    the list of non-unique filenames.
    '''
    unique = []
    repeated = []

    for path in paths:
        name = os.path.basename(path)
        if name not in unique:
            unique.append(name)
        elif name not in repeated:
            repeated.append(name)
    return repeated

def getstatusoutput(cmd):
    '''
    run command line process and return status and output data
    '''
    try:
        data = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        status = 0

    except subprocess.CalledProcessError as ex:
        data = ex.output
        status = ex.returncode

    if data[-1:] == '\n':
        data = data[:-1]

    return status, data


def main():
    # Parse command-line inputs
    args = sys.argv[1:]
    if not args:
        print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
        return

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print "error: must specify one or more dirs"
        sys.exit(1)

    # Get special files in each directory
    special_paths = []
    for fromdir in args:
        special_paths += get_special_paths(fromdir)

    # If not copying or zipping, simply print the special paths
    if not (todir or tozip):
        print 'Special paths:'
        for path in special_paths:
            print path

    # If we are copying or zipping
    else:
        # Check for repeated file names
        repeated = check_filename_repeats(special_paths)
        if repeated:
            errmsg = ('Found non-unqiue filenames, aborting copy and zip. '
                      'Repeated names: %s\n')%' '.join(repeated)
            sys.stderr.write(errmsg)
            sys.exit(1)

        # If requested, copy files to destination directory
        if todir:
            copy_to(special_paths, todir)

        # If requested, zip files into the destination file
        if tozip:
            zip_to(special_paths, tozip)

if __name__ == "__main__":
    main()
