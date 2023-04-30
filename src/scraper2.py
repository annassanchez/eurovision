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
    # code that uses the driver
    dict_vacio = {key: [] for key in ['year', 'city', 'winners', 'participant', 'song', 'song_youtube', 'points', 'url']}
    url_list = [f'https://eurovision.tv/history?page={i}' for i in range(5)]
    for next, url in enumerate(url_list):
        try:
            driver.get(url)
            driver.maximize_window()
            #driver.set_window_size(1920, 1080)
            driver.implicitly_wait(30)
        except Exception as e:
            print(f"Error occurred when opening url: {e}")
        for i in range(1,15):
            try: 
                print(f'lo intento. page: {next}, element: {i}')
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
        with open(f'../data/temp/dict_main_archives_{next}.pickle', 'wb') as f:
                pickle.dump(dict_vacio, f)
        print('done with this page')
        clear_output(True)
    with open(f'../data/archives.pickle', 'wb') as f:
        pickle.dump(dict_vacio, f)
    return dict_vacio