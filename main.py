from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import requests
start = time.time()
options = webdriver.ChromeOptions()
options.add_argument('--headless')
array = ["輸入課程代碼"]
chrome = webdriver.Chrome(options=options)
chrome.get("https://querycourse.ntust.edu.tw/querycourse/")
chrome.implicitly_wait(10)
while(1):
    num = 0
    if(time.time()-start >= 600):
        chrome.close()
        break
    chrome.refresh()
    button = (By.CLASS_NAME, "v-overlay.v-overlay--active")  # internal
    WebDriverWait(chrome, 10).until(
        EC.element_to_be_clickable(button)).click()
    button = (By.XPATH, "//*[contains(text(),'通識課程')]")  # internal
    WebDriverWait(chrome, 10).until(
        EC.element_to_be_clickable(button)).click()
    time.sleep(1)
    if(BeautifulSoup(chrome.page_source, "html.parser") == None):
        continue
    for i in range(4):
        num = 0
        soup = BeautifulSoup(chrome.page_source, "html.parser")
        titles = soup.find_all('tr')
        for title in titles:
            td = title.find("td")
            if td == None:
                continue
            td = title.find_all("td")
            if td[0].getText() in array:
                num += 1
                if((int("".join(list(filter(str.isdigit, (td[10].getText().strip())))))) > (int("".join(list(filter(str.isdigit, (td[7].getText().strip())[3:7])))))):
                    headers = {
                        "Authorization": "Bearer " + "line token",
                        "Content-Type": "application/x-www-form-urlencoded"
                    }
                    params = {
                        "message": td[0].getText().strip() + '\n' + td[2].getText().strip()+'\n'+td[8].getText().strip()+'\n' + "剩餘"+str((int("".join(list(filter(str.isdigit, (td[10].getText().strip())))[:3]))) - (int("".join(list(filter(str.isdigit, (td[7].getText().strip())[3:7]))))))}
                    r = requests.post("https://notify-api.line.me/api/notify",
                                      headers=headers, params=params)
        if(i != 3):
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
            button.click()
