from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import re
import json
import requests
ue = UserAgent()
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome = webdriver.Chrome(options=options)
chrome.get(url="https://courseselection.ntust.edu.tw/",
           headers={'ue': ue.random})
