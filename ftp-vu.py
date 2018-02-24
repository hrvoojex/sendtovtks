#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Autor: Hrvoje T.
Email: hrvooje@gmail.com
Created: 23.02.2018.
Last edit: 23.02.2018.
Version: 0.0.1

Send files over ftp from workshops to headquarter.
"""

import datetime
import ftplib
import sys


# FTP server login data
ftpserver_ip = '192.168.0.100'
username = 'user'
password = 'pass'

# If there is command line argument, the first one is our file to upload
if len(sys.argv) > 1:
    upload_file = sys.argv[1]
else:
    print('No input file')
    sys.exit()

def ftpsend():
    try:
        # ftp server running on 'ftpserver_ip' on port 21
        session = ftplib.FTP(ftpserver_ip, username, password)
        file = open(upload_file, 'rb')
        session.storbinary('STOR '+upload_file, file)
        file.close()
        session.quit()
    except Exception as err:
        with open('error.log', 'w') as ferr:
            print(err)
            ferr.write(str(datetime.datetime.now()))
            ferr.write('\n')
            ferr.write(str(err))
        return None

    with open('OK.log', 'w') as fok:
        fok.write(str(datetime.datetime.now()))
        fok.write(" OK")
        print(datetime.datetime.now(), "OK")

ftpsend()



