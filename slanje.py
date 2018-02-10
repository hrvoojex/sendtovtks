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


#url = 'http://192.168.110.68:8000/text.txt'
url = 'http://localhost:8000/report.txt'
target_path = 'my_text.txt'

# stream is true, for big files, from here:
# http://masnun.com/2016/09/18/python-using-the-requests-module-to-download-large-files-efficiently.html
response = requests.get(url, stream=True)
handle = open(target_path, "wb")
for chunk in response.iter_content(chunk_size=512):
    if chunk:  # filter out keep-alive new chunks
        handle.write(chunk)
