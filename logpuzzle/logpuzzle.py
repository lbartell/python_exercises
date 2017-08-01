#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""

    # extract server name from the filename
    server_match = re.search(r'.*_(.+)', filename)
    if server_match:
        server_name = 'http://' + server_match.group(1)
    else:
        sys.stderr.write('Couldn\'t find the servername!\n')
        sys.exit(1)

    # open the file and initialize list to hold the valid puzzle urls
    f = open(filename)
    urls = []

    # process each line in the file
    for line in f:

        # find any url "puzzle" pattern and create the full url
        match = re.search(r'"GET (\S*puzzle\S*) HTTP', line)
        if match:
            puzzle_url = server_name + match.group(1)

            # check if the puzzle url is new and add it to the list
            if puzzle_url not in urls:
                urls.append(puzzle_url)

    # close the file
    f.close()

    # sort url names based on the last 'word' in their name
    sorted_urls = sorted(urls, key=last_word_sorting)

    # return
    return sorted_urls

def last_word_sorting(url):
    # enable custom sorting based on the last 'word' in the url filename
    fullname = re.search(r'([^\s/]+)(?:\.\S\S\S)$', url).group(1)
    return fullname.split('-')[-1]

def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """

    # create the destination directory if necessary
    dest_dir = os.path.abspath(dest_dir)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    # initialize image counting index
    index = 0
    digits = len(str(len(img_urls)-1))

    # initialize summary file: index.html
    findex = open(os.path.join(dest_dir, 'index.html'), 'w')
    html_start_str = '<verbatim><html><body>'
    html_img_fmtstr = '<img src="%s">'
    html_end_str = '</body></html>'
    findex.write(html_start_str)

    # print status to screen
    print 'Retrieving image...',

    # download image from each url
    for url in img_urls:

        # get file extension from the url
        ext_match = re.search(r'\.\S\S\S$', url)
        if ext_match:
            ext_str = ext_match.group()
        else:
            sys.stderr.write('Couldn\'t determine the image extension!\n')
            sys.exit(1)

        # create the filename for the local copy of the image file
        img_filename = 'img' + (digits-len(str(index)))*'0' +'%d%s'%(index, ext_str)
        img_path = os.path.join(dest_dir, img_filename)

        # download and save the image file
        urllib.urlretrieve(url, img_path)

        # create and add the associated html img string in the index file
#        address_match = re.search(r'(?:http://)(?:[^\s/]+)(.+)', url)
#        if address_match:
#            address_str = address_match.group(1)
#        else:
#            sys.stderr.write('Couldn\'t determine the local image address!\n')
#            sys.exit(1)
        findex.write(html_img_fmtstr%(img_filename))

        # update index
        index += 1

    # finish the index.html file
    findex.write(html_end_str)
    findex.close()

    # print status to screen and return
    print 'image retrieved.'
    return



def main():
    args = sys.argv[1:]

    # if there are no command-line options, simply print the usage information
    if not args:
        print 'usage: [--todir dir] logfile '
        sys.exit(1)

    # parse command line options
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    # find "puzzle" urls in the logfile
    img_urls = read_urls(args[0])

    if todir:
        download_images(img_urls, todir)
    else:
        print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
