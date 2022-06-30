#!/usr/bin/env python3

"""
Author:- Pritesh Ranjan (pranjan341@gmail.com)
This is an image downloader script. It can take an input URL and download all the images from that web page.
"""

from fileinput import filename
import sys
if sys.version_info < (3, 0):
    raise SystemError("Please use python3\n")

import random
import time
import urllib.parse
import csv
import os
import re

from config import SUPPORTED_IMAGE_ATTRIBUTES, SUPPORTED_IMAGE_TYPES

try:
    import bs4 as bs
    import requests
except:
    raise ImportError("Please install beautifulsoup4 \n and requests modules for python3")

USER_AGENTS = [
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)\
Chrome/61.0.3163.91 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/61.0.3163.79 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) \
Chrome/62.0.3202.94 Safari/537.36 OPR/49.0.2725.56"]


class ImageDownloader:
    """scans a web page for all image links and downloads the images to a folder"""
    def __init__(self, catname: str, csvfile: str):
        self.seq = 0
        self.catname = catname
        self.csvfile = csvfile
        self.domain = ""

    def page_source(self):
        """ tries to connect to given URL via intermediate connector """
        print("Trying to connect to page...")
        try:
            req = self.intermediate_connector(self.url)
        except:
            try:
                print("error reconnecting...")
                req = self.intermediate_connector(self.url)
            except:
                raise ConnectionError("Check Your Internet Connection and URL")
        # print(req)
        return req

    @staticmethod
    def intermediate_connector(link:str):
        """waits for a random amount of time, uses user agents and connects to a webpage and downloads it """
        time.sleep(random.randrange(1, 5))
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        response = requests.get(link, headers=headers)
        print("Connected")
        return response.content
    
    def find_images(self):
        """scans a beautiful soup object for all image links"""
        # if self.get_file_type(self.url):
        #     self.save_image(self.url, "only")
        #     return None
        # source = self.page_source()

        filename = f"{self.catname}.txt"
        source = open(f"./source/{filename}", "r").read()
        soup = bs.BeautifulSoup(source, 'lxml')
        for image in soup.find_all("img"):
            tmp = image.get(SUPPORTED_IMAGE_ATTRIBUTES[2])
            name = image.get("alt")
            if self.domain == "" and (tmp and tmp != "" and ".com" in tmp):
                self.domain = urllib.parse.urlparse(tmp).hostname
            if tmp:
                self.save_image_to_csv(tmp, name, self.domain)
            else:
                print("error occured")

    def save_image_to_csv(self, img_link: str, name: str, source: str):
        # category name image likes source
        with open(self.csvfile, mode='a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow([self.catname, img_link, random.randint(1000, 8000), source])
    
if __name__ == "__main__":
    for file in os.listdir("./source"):
        catname = file.split(".")[0]
        csvfile = f'./img_quotes/{catname}.csv';
        ImageDownloader(catname, csvfile).find_images()
    
        