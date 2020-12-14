# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 22:49:59 2020

@author: Asus
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
 
 
options = Options()
options.add_argument("--disable-notifications")
 
chrome = webdriver.Chrome('D:\git/chromedriver', chrome_options=options)
chrome.get("https://www.instagram.com/p/CIu8mN1pLN3/?__a=1")
soup = BeautifulSoup(chrome.page_source, 'html.parser')

print(soup)