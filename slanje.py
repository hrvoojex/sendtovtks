#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Autor: Hrvoje T.
Email: hrvooje@gmail.com
Created: 09.02.2018.
Last edit: 19.02.2018.
Version: 0.0.2

Send files over http from workshops to headquarters

Firstly, we run a simple web server from a workshop on remote location:
    python3 -m http.server 8000
from a directory where is a file located and than we run this
script to save served file localy.
"""

import requests
import os
import ntpath
import time


urls_file = 'urls.txt'

def path_leaf(path):
    """Extract a file name from a path"""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def download_file(url):
    local_filename = path_leaf(url)

    try:
        r = requests.get(url, stream=True, timeout=6)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print("HTTP exception error: {}".format(err))
        return
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print("Exception error: {}".format(e))
        return

    f = open(local_filename, 'wb')
    # File size in MB
    file_size = (int(r.headers.get('content-length', 0)) / (1024*1024))
    # This is a tenth of a file size for drawing a dot after every 10% is copied
    tenth_size = file_size / 10
    print("Downloading: {}, Size: {:.2f}MB ".format(url, file_size), end="", flush=True)
    copied = 0
    bar = 1
    start = time.time()
    # chunk is 1MB --> 1024x1kB
    for chunk in r.iter_content(1024*1024):
        if chunk:
            f.write(chunk)
            copied += len(chunk) / (1024*1024)
            # Every 10% is copied, draw one dot
            if copied >= bar * tenth_size:
                print("#", end="", flush=True)
                bar += 1
    f.close()
    end = time.time()
    duration = end - start
    print(" Finished. Time: {:.2f}s, Speed: {:.2f}MB/s".format(duration, file_size/duration))
    return

if os.path.exists(urls_file):
    with open(urls_file, 'r') as f:
        for line in f:
            # Go to next line, if line is not starting with http
            if not line.startswith("http"):
                continue
            url = line.strip()
            try:
                # save target file with the same name as source file
                download_file(url)
            except IOError as e:
                print("Could not read file: {}".format(url))
                pass
    print("End")
else:
    print("No {} file for reading".format(urls_file))