from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import re
import json
import requests
options = webdriver.ChromeOptions()
options.add_argument('--headless')
array = ["ECG003301", "ETG301301", "TCG027301", "TCG047301", "FE1471702",
         "TCG047302", "TCG051301", "TCG057301", "TCG071302", "TCG071301",
         "TCG074301", "TCG078301", "TCG084301", "TCG087301", "TCG094301",
         "TCG100301", "TCG105301", "GE3723301", "GE3723302",
         "GE3917301", "GE3917302"]
chrome = webdriver.Chrome()
chrome.get("https://querycourse.ntust.edu.tw/querycourse/")
chrome.implicitly_wait(10)
while(1):
    num = 0
    chrome.refresh()
    button = (By.CLASS_NAME, "v-overlay.v-overlay--active")  # internal
    WebDriverWait(chrome, 10).until(
        EC.element_to_be_clickable(button)).click()
    #button = chrome.find_element_by_class_name("v-overlay.v-overlay--active")
    # button.click()
    button = (By.XPATH, "//*[contains(text(),'通識課程')]")  # internal
    WebDriverWait(chrome, 10).until(
        EC.element_to_be_clickable(button)).click()
    #button = chrome.find_element_by_xpath("//*[contains(text(),'通識課程')]")
    # button.click()
    time.sleep(1)
    if(BeautifulSoup(chrome.page_source, 'lxml') == None):
        continue
    for i in range(3):
        num = 0
        soup = BeautifulSoup(chrome.page_source, 'lxml')
        titles = soup.find_all('tr')
        for title in titles:
            td = title.find("td")
            if td == None:
                continue
            td = title.find_all("td")
            if td[0].getText() in array:
                num += 1
                if((int("".join(list(filter(str.isdigit, (td[10].getText().strip())))))) > (int("".join(list(filter(str.isdigit, (td[7].getText().strip())[:3])))))):
                    # print(td[0].getText().strip())
                    # print(td[2].getText().strip())
                    # print(
                    #    int("".join(list(filter(str.isdigit, (td[7].getText().strip())[:3])))))
                    # print(
                    #    int("".join(list(filter(str.isdigit, (td[10].getText().strip()))))))
                    headers = {
                        "Authorization": "Bearer " + "u7dqeueJNhYO4ImqE2OJ5MdLICAyG3Igms1XjEIzrz9",
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                    params = {
                        "message": td[0].getText().strip() + '\n' + td[2].getText().strip()+'\n'+td[8].getText().strip()+'\n' + "剩餘"+str((int("".join(list(filter(str.isdigit, (td[10].getText().strip())))[:3]))) - (int("".join(list(filter(str.isdigit, (td[7].getText().strip())[:3]))))))}
                    r = requests.post("https://notify-api.line.me/api/notify",
                                      headers=headers, params=params)
                    headers = {
                        "Authorization": "Bearer " + "1Vpp2D8dlKDXgzlFAYLNkwFVDfAHeTEUcLTZDkNTbUo",
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                    params = {
                        "message": td[0].getText().strip() + '\n' + td[2].getText().strip()+'\n'+td[8].getText().strip()+'\n'+"剩餘"+str((int("".join(list(filter(str.isdigit, (td[10].getText().strip())))))) - (int("".join(list(filter(str.isdigit, (td[7].getText().strip())[:3]))))))}
                    r = requests.post("https://notify-api.line.me/api/notify",
                                      headers=headers, params=params)
        if(i != 2):
            if(num == 0):
                break
            button = (By.XPATH, "//*[contains(text(),'chevron_right')]")
            button1 = (By.CLASS_NAME, "v-datatable__actions__range-controls")
            WebDriverWait(chrome, 10).until(
                EC.visibility_of_element_located(button1))
            WebDriverWait(chrome, 10).until(
                EC.element_to_be_clickable(button) and EC.visibility_of_element_located((button)) and EC.presence_of_element_located(button))
            button = chrome.find_element_by_xpath(
                "//*[contains(text(),'chevron_right')]")
            while (button.is_displayed() == False or button.is_selected() == True):
                print("1")
                time.sleep(0.1)
            button.click()
