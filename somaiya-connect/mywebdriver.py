
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import os

from dotenv import load_dotenv

load_dotenv()

def webdriver(chrome=True, andriod=False):
    options = Options()

    if andriod:
        options.add_experimental_option('androidPackage', 'com.UCMobile.intl')
        options.add_experimental_option('androidActivity', 'com.UCMobile.main.UCMobile')
        options.add_experimental_option('androidProcess', ':resident')
    else:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
    if chrome:
        Chrome(executable_path=os.environ.get('DRIVER'), options=options)
    else:
        Firefox(executable_path=os.environ.get('DRIVER'))
