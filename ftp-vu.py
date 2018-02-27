#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Autor: Hrvoje T.
Email: hrvooje@gmail.com
Created: 23.02.2018.
Last edit: 25.02.2018.
Version: 0.0.1

Send files over ftp from workshops to headquarter.
"""

import datetime
import ftplib
import sys
import os


class FtpUploadTrack(object):
    """Class for tracking file upload"""
    size_written = 0
    total_size = 0
    last_shown_percent = 0

    def __init__(self, total_size):
        self.total_size = total_size

    def handler(self, chunk):
        self.size_written += 1024
        percente_complete = round((self.size_written / self.total_size) * 100)

        if self.last_shown_percent != percente_complete:
            self.last_shown_percent = percente_complete
            # Don't print, write to stdout to update numbers in the same place
            #print(str(percente_complete) + " % upload")
            sys.stdout.flush()
            sys.stdout.write("\r" + str(percente_complete) + "% upload")
            sys.stdout.flush()


# Remove those two log files if they exist
[os.remove(log_file) for log_file in ['OK.log', 'error.log'] if os.path.exists(log_file)]

# FTP server login data
ftpserver_ip = '192.168.0.232'
username = 'ftp_test'
password = 'ftp_test'

# If there is command line argument, the first one is our file to upload
if len(sys.argv) > 1:
    upload_file = sys.argv[1]
else:
    print('No input file')
    sys.exit()

# Find out total file size and create instance of FtpUploadTrack
total_size = os.path.getsize(upload_file)
print("File size: {}MB".format(str(round(total_size / 1024 / 1024, 1))))
uploadTrack = FtpUploadTrack(int(total_size))

def ftpsend():
    try:
        # ftp server running on 'ftpserver_ip' on port 21
        session = ftplib.FTP(ftpserver_ip, username, password)
        file = open(upload_file, 'rb')
        session.storbinary('STOR '+upload_file, file, 1024, uploadTrack.handler)
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
        print("\n" + str(datetime.datetime.now()), "OK")

ftpsend()



