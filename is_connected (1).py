import os
import time
from datetime import datetime as dt
import requests
from urllib.request import urlopen
from mywebdriver import Chrome, webdriver
'''
this is will be repeated checking whether or not my wifi is connected and it will automatically
log me in it is not logged in 
using selenium webdriver
with this script i will not worry about loging in to my wifi
'''

def isconnected():
    ##################c
    try:
        ## this will check if there is connection to a network
        urlopen('http://216.58.192.142', timeout=1)
        try:
            ## this will check if there is connection to a network
            requests.get('https://www.google.com/').status_code
            return True
        except:
            return None
    except:
        return False
def mydriver():
    try:
        webdriver()
        driver = Chrome()
        driver.get("http://172.30.250.250:1000/login?")
        driver.implicitly_wait(1)
        driver.find_element_by_name('username').send_keys('abdoulie.n')
        pwd = os.environ.get('SOMAIYA_WIFI_PWD')# it is good practice to hide passwords
        driver.find_element_by_name('password').send_keys(pwd)
        driver.find_element_by_xpath('/html/body/div/div/form/div[3]/input').click()
        driver.quit()
        date=dt.now().strftime("%Y/%m/%d - %H:%M:%S")
        print(f'[{date}] => connected now')
    except:
        date=dt.now().strftime("%Y/%m/%d - %H:%M:%S")
        print(f'[{date} ]=> Cannot login. I think it is not a somaiya wifi'.upper())

def connect_to_wifi():
    if not isconnected():
        if isconnected() == None:
            date=dt.now().strftime("%Y/%m/%d - %H:%M:%S")
            print(f'[{date}] => connected to a network but no internet'.upper())
            mydriver()
        else:
            date=dt.now().strftime("%Y/%m/%d - %H:%M:%S")
            print(f'[{date}] => not connected to a network'.upper())
    else:
        date=dt.now().strftime("%Y/%m/%d - %H:%M:%S")
        print(f'[{date} ]=> ***connected***'.upper())
if __name__ == "__main__":
    while True:
        time.sleep(2)
        connect_to_wifi()

# for i in range(20):
#     time.sleep(5)
#     connect_to_wifi()
#*nohup python3 -u myscheduler.py &
#*ps ax | grep myscheduler.py
#*kill -9 ID_NUM
#*nohup /home/abdullah/Projects/automation/auto/bin/python -u /home/abdullah/Projects/automation/is_connected.py &
