import os
import time
from datetime import datetime as dt
from urllib.request import urlopen
from mywebdriver import Chrome, webdriver

from dotenv import load_dotenv

load_dotenv()
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
        urlopen('https://www.google.com/', timeout=1)
        return True
    except Exception as error:
        try:
            if 'CERTIFICATE_VERIFY_FAILED' == error.reason.reason:
                return None
        except:
            return False
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
        driver.find_element_by_xpath('/html/body/section/div/div/div/div[2]/form/div[3]/input').click()
        driver.quit()
        date=dt.now().strftime("%Y/%m/%d - %H:%M:%S")
        print(f'[{date}] => connected now')
    except Exception as error:
        date=dt.now().strftime("%Y/%m/%d - %H:%M:%S")
        print(f'[{date} ]=> Cannot login {error.__str__}.'.upper())

def connect_to_wifi():
    if not isconnected():
        if isconnected() == None:
            date=dt.now().strftime("%Y/%m/%d - %H:%M:%S")
            print(f'[{date}] => connected to a network but no internet'.upper())
            try:
                urlopen("http://172.30.250.250:1000/login?",timeout=1)
            except:
                print(f'[{date} ]=> It is not a somaiya wifi'.upper())
            else:
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
#*nohup /home/user/Projects/automation/env/bin/python -u /home/user/Projects/automation/is_connected.py &
