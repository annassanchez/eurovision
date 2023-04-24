from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common import keys
import re
import time
from collections import defaultdict


class Scraper():

    def __init__(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("headless")
            options.add_argument("no-sandbox")
            options.add_argument("disable-dev-shm-usage")
            self.driver = webdriver.Chrome(chrome_options=options)
            return
        except Exception as e:
            print('Chrome WebDriver is missing')
            pass

        
        try:
            options = webdriver.firefox.options.Options()
            options.add_argument('--headless')
            self.driver = webdriver.Firefox(options=options)
            return
        except Exception as e:
            print('Firefox WebDriver is missing')
            pass

        try:
            self.driver = webdriver.Safari()
            return
        except:
            print('Safari is missing')
            pass