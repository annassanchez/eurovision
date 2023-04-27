from time import sleep
import re
import pickle
from datetime import datetime

from IPython.display import clear_output

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options

def seleniumEurovision(url):
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    driver.maximize_window()
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(30)
    dict_vacio = {
        'year':[],
        'city':[],
        'winners':[],
        'participant':[],
        'song':[],
        'points':[],
        'url':[]
    }
    for i in range(1,15):
        try: 
            print('lo intento')
            print(i)
            year = driver.find_element(By.XPATH, f'/html/body/div[1]/div/div/div[3]/div/div/div/div/div[2]/div/div/table/tbody/tr[{i}]/td[1]/a').text
            dict_vacio['year'].append(year)
            #return dict_vacio
        except:
            print('no puedo')
            continue
    return dict_vacio