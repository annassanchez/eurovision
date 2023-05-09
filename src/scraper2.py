from time import sleep
import re
import pickle
from datetime import datetime
import numpy as np
import pandas as pd

from IPython.display import clear_output

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options

def seleniumEurovisionArchives():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Firefox(options=options)
    # code that uses the driver
    url='https://eurovision.tv/history'
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
        for i in range(1,16):
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

def finalEurovision():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Firefox(options=options)
    with open('../data/archives.pickle', 'rb') as base_data:
        base_data = pickle.load(base_data)
    url_list = pd.DataFrame(base_data)['url'].tolist()
    dict_vacio = {key: [] for key in ['R/O', 	'Half', 	'Country', 	'Participant', 	'Song', 'Song_Youtube',	'Points', 	'Rank', 'Final']}
    for i, url in enumerate(url_list):
        try:
            print('lo intento')
            try:
                url_final = url + '/final'
                driver.get(url_final)
                driver.maximize_window()
                for element in range(1, 27):
                    r_o = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(1)').text
                                                                #.cols-7 > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1)
                    half = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(2)').text
                    country = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(3)').text
                    participant = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(4)').text
                    song = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(5)').text
                    try:
                        song_youtube = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(5) > a:nth-child(1)').get_attribute('href')    
                    except:
                        song_youtube = np.nan
                    points = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(6)').text
                    rank = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(7)').text
                    dict_vacio['R/O'].append(r_o)
                    dict_vacio['Half'].append(half)
                    dict_vacio['Country'].append(country)
                    dict_vacio['Participant'].append(participant)
                    dict_vacio['Song'].append(song)
                    dict_vacio['Song_Youtube'].append(song_youtube)
                    dict_vacio['Points'].append(points)
                    dict_vacio['Rank'].append(rank)
                    dict_vacio['Final'].append(url.split('/')[-1])
                with open(f'../data/temp/archive_{i}.pickle', 'wb') as f:
                    pickle.dump(dict_vacio, f)
            except:
                url_final = url + '/grand-final'
                driver.get(url_final)
                driver.maximize_window()
                for element in range(1, 27):
                    r_o = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(1)').text
                    half = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(2)').text
                    country = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(3)').text
                    participant = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(4)').text
                    song = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(5)').text
                    try:
                        song_youtube = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(5) > a:nth-child(1)').get_attribute('href')    
                    except:
                        song_youtube = np.nan
                    points = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(6)').text
                    rank = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(7)').text
                    dict_vacio['R/O'].append(r_o)
                    dict_vacio['Half'].append(half)
                    dict_vacio['Country'].append(country)
                    dict_vacio['Participant'].append(participant)
                    dict_vacio['Song'].append(song)
                    dict_vacio['Song_Youtube'].append(song_youtube)
                    dict_vacio['Points'].append(points)
                    dict_vacio['Rank'].append(rank)
                    dict_vacio['Final'].append(url.split('/')[-1])
                with open(f'../data/temp/final_{i}.pickle', 'wb') as f:
                    pickle.dump(dict_vacio, f)
        except Exception as e:
            print(f"Error occurred for row {url_final}: {e}")
            continue
        print('done with this page')
        clear_output(True)
    with open(f'../data/final.pickle', 'wb') as f:
        pickle.dump(dict_vacio, f)
    driver.quit()
    return dict_vacio

def your_while_generator(df):
    lista = []
    for i in df['url'].unique().tolist():
        lista.append(i)
        if 'belgrade-2008' in i:
            break
    return lista

def semifinalEurovision():
    options = Options()
    options.headless = False
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Firefox(options=options)
    with open('../data/archives.pickle', 'rb') as base_data:
        base_data = pickle.load(base_data)
    url_list = pd.DataFrame(base_data)['url'].tolist()
    url_one_semifinal = ['helsinki-2007', 'athens-2006',
       'kyiv-2005', 'istanbul-2004']
    url_2_semifinal = [i for i in your_while_generator(pd.DataFrame(base_data))]
    dict_vacio = {key: [] for key in ['R/O', 	'Half', 	'Country', 	'Participant', 	'Song', 'Song_Youtube',	'Points', 	'Rank', 'Final', 'Semi-Final']}
    for i, url in enumerate(url_list):
        if url in url_2_semifinal:
            try:
                print('lo intento')
                try:
                    url_final = url + '/first-semi-final'
                    driver.get(url_final)
                    driver.maximize_window()
                    for element in range(1, 20):
                        try:
                            r_o = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(1)').text
                                                                        #.cols-7 > tbody:nth-child(2) > tr:nth-child(19) > td:nth-child(1)
                            half = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(2)').text
                            country = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(3)').text
                            participant = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(4)').text
                            song = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(5)').text
                            try:
                                song_youtube = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(5) > a:nth-child(1)').get_attribute('href')    
                            except:
                                song_youtube = np.nan
                            points = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(6)').text
                            rank = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(7)').text
                        except:
                            r_o = np.nan
                            half = np.nan
                            country = np.nan
                            participant = np.nan
                            song = np.nan
                            song_youtube = np.nan
                            points = np.nan
                            rank = np.nan
                        dict_vacio['R/O'].append(r_o)
                        dict_vacio['Half'].append(half)
                        dict_vacio['Country'].append(country)
                        dict_vacio['Participant'].append(participant)
                        dict_vacio['Song'].append(song)
                        dict_vacio['Song_Youtube'].append(song_youtube)
                        dict_vacio['Points'].append(points)
                        dict_vacio['Rank'].append(rank)
                        dict_vacio['Final'].append(url.split('/')[-1])
                        dict_vacio['Semi-Final'].append(url_final.split('/')[-1])
                    url_final = url + '/second-semi-final'
                    driver.get(url_final)
                    driver.maximize_window()
                    for element in range(1, 20):
                        try:
                            r_o = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(1)').text
                                                                        #.cols-7 > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1)
                            half = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(2)').text
                            country = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(3)').text
                            participant = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(4)').text
                            song = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(5)').text
                            try:
                                song_youtube = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(5) > a:nth-child(1)').get_attribute('href')    
                            except:
                                song_youtube = np.nan
                            points = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(6)').text
                            rank = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(7)').text
                        except:
                            r_o = np.nan
                            half = np.nan
                            country = np.nan
                            participant = np.nan
                            song = np.nan
                            song_youtube = np.nan
                            points = np.nan
                            rank = np.nan
                        dict_vacio['R/O'].append(r_o)
                        dict_vacio['Half'].append(half)
                        dict_vacio['Country'].append(country)
                        dict_vacio['Participant'].append(participant)
                        dict_vacio['Song'].append(song)
                        dict_vacio['Song_Youtube'].append(song_youtube)
                        dict_vacio['Points'].append(points)
                        dict_vacio['Rank'].append(rank)
                        dict_vacio['Final'].append(url.split('/')[-1])
                        dict_vacio['Semi-Final'].append(url_final.split('/')[-1])
                    with open(f'../data/temp/semifinal_{i}.pickle', 'wb') as f:
                        pickle.dump(dict_vacio, f)
                    print(url.split('/')[-1])
                except Exception as e:
                    print(f"Error occurred for row {url_final}: {e}")
            except Exception as e:
                print(f"Error occurred for row {url_final}: {e}")
        elif url.split('/')[-1] in url_one_semifinal:
            try:
                print('lo intento')
                try:
                    url_final = url + '/semi-final'
                    driver.get(url_final)
                    driver.maximize_window()
                    for element in range(1, 30):
                        try:
                            r_o = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(1)').text
                                                                        #.cols-7 > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(1)
                            half = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(2)').text
                            country = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(3)').text
                            participant = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(4)').text
                            song = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(5)').text
                            try:
                                song_youtube = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(5) > a:nth-child(1)').get_attribute('href')    
                            except:
                                song_youtube = np.nan
                            points = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(6)').text
                            rank = driver.find_element(By.CSS_SELECTOR, f'.cols-7 > tbody:nth-child(2) > tr:nth-child({element}) > td:nth-child(7)').text
                        except:
                            r_o = np.nan
                            half = np.nan
                            country = np.nan
                            participant = np.nan
                            song = np.nan
                            song_youtube = np.nan
                            points = np.nan
                            rank = np.nan
                        dict_vacio['R/O'].append(r_o)
                        dict_vacio['Half'].append(half)
                        dict_vacio['Country'].append(country)
                        dict_vacio['Participant'].append(participant)
                        dict_vacio['Song'].append(song)
                        dict_vacio['Song_Youtube'].append(song_youtube)
                        dict_vacio['Points'].append(points)
                        dict_vacio['Rank'].append(rank)
                        dict_vacio['Final'].append(url.split('/')[-1])
                        dict_vacio['Semi-Final'].append(url_final.split('/')[-1])
                    with open(f'../data/temp/semifinal_{i}.pickle', 'wb') as f:
                        pickle.dump(dict_vacio, f)
                    print(url.split('/')[-1])
                except:
                    print(f"Error occurred for row {url_final}: {e}")    
            except Exception as e:
                print(f"Error occurred for row {url_final}: {e}")
        elif url not in url_2_semifinal or url.split('/')[-1] not in url_one_semifinal: 
            print('done with this page')
            clear_output(True)
            with open(f'../data/semi-final.pickle', 'wb') as f:
                pickle.dump(dict_vacio, f)
            #driver.quit()
            return dict_vacio