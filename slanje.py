#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Autor: Hrvoje T.
Email: hrvooje@gmail.com
Created: 09.02.2018.
Last edit: 10.02.2018.
Version: 0.0.1

Send files over http from workshops to headquarters

Firstly, we run a simple web server from a workshop on remote location:
    python3 -m http.server 8000
from a directory where is a file located and than we run this
script to save served file localy.
"""

import requests
import sys
import os
import ntpath
from tqdm import tqdm


urls_file = 'urls.txt'

# # First command line argument is a text file with urls
# if len(sys.argv) > 1:
#     text_file = sys.argv[1]
# else:
#     sys.exit("Prisilno gašenje")

def path_leaf(path):
    """
    :param path: Take path as argument
    :return: File name or if no file name, return subdirectory
    """
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

if os.path.exists(urls_file):
    with open(urls_file, 'r') as f:
        for line in f:
            try:
                url = line.strip()
                # save target file with the same name as source file
                target_path = path_leaf(url)
                # stream is true, for big files, from here:
                # http://masnun.com/2016/09/18/python-using-the-requests-module-to-download-large-files-efficiently.html
                response = requests.get(url, stream=True)
                # total size of a file in bytes
                total_size = (int(response.headers.get('content-length', 0)) / (1024 * 1024))
                handle = open(target_path, "wb")
                for chunk in tqdm((response.iter_content(1024*1024)), total=total_size, unit='M'):
                    if chunk:  # filter out keep-alive new chunks
                        handle.write(chunk)
            except IOError as e:
                print("Could not read file: {}".format(url))
                pass