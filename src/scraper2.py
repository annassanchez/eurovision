from time import sleep
import re
import pickle
from datetime import datetime
import numpy as np

from IPython.display import clear_output

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options

def seleniumEurovisionArchives(url):
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    driver.maximize_window()
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(30)
    # code that uses the driver
    dict_vacio = {key: [] for key in ['year', 'city', 'winners', 'participant', 'song', 'song_youtube', 'points', 'url']}
    for next in range(1,6):
        for i in range(1,15):
            try: 
                print('lo intento')
                year = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]/td[1]/a').text
                city = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]/td[2]/span').text
                winners = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]/td[3]/a/span[2]').text
                participant = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]/td[4]/a/span').text
                try:
                    song = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]/td[5]/a').text
                    song_youtube = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]/td[5]/a').get_attribute('href')
                except:
                    song = np.nan
                    song_youtube = np.nan
                points = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]/td[6]').text
                url_ = driver.find_element(By.XPATH, f'//table/tbody/tr[{i}]/td[7]/a').get_attribute('href')            
                dict_vacio['year'].append(year)
                dict_vacio['city'].append(city)
                dict_vacio['winners'].append(winners)
                dict_vacio['participant'].append(participant)
                dict_vacio['song'].append(song)
                dict_vacio['song_youtube'].append(song_youtube)
                dict_vacio['points'].append(points)
                dict_vacio['url'].append(url_)
            except Exception as e:
                print(f"Error occurred for row {i}: {e}")
                continue
        with open(f'../data/dict_test_{next}.pickle', 'wb') as f:
                pickle.dump(dict_vacio, f)
        print('done with this page')
        try:
            sleep(5)
            #driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div/div/nav/ul/li[6]/a').click()
            element = driver.find_element(By.CSS_SELECTOR, "li.pager__item:nth-child(6) > a:nth-child(1)")
            driver.execute_script("arguments[0].click();", element)
        except:
            print('No hay más páginas')
            finished = True
    return dict_vacio