# coding=utf-8

"""
Python-Applet
Download file from url.
__author__ = 'JNingWei'
"""

import os
import urllib
import logging
import sys

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    stream=sys.stdout)

file_path = os.path.join(os.getcwd(),'dir_name/file_name')

if not os.path.isfile(file_path):
    logging.info("File doesn't exist.")
    # replace with url you need
    url = 'https://github.com/JNingWei/Notebook/blob/master/README.md'

    # if dir 'dir_name/' doesn't exist
    file_dir = file_path[:-9]
    if not os.path.exists(file_dir):
        logging.info("Mkdir 'dir_name/'.")
        os.mkdir(file_dir)

    def down(_save_path, _url):
        try:
            urllib.urlretrieve(_url, _save_path)
        except:
            print '\nError when retrieving the URL:', _save_path

    logging.info("Downloading file.")
    down(file_path, url)
else:
    logging.info("File exists.")
