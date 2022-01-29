#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 14:46:48 2021

@author: mhuss
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium import webdriver
import json

#This is all of our data sorted into different functions so they are easy to call

def getPAfipsData():
    #Downlaods the table with the county name and FIPS
    httpString = ('https://www.nrcs.usda.gov/wps/portal/nrcs/detail/national/home/?cid=nrcs143_013697')
    page = requests.get(httpString)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    table = soup.find(class_ = "data")
    table = pd.read_html(str(table))
    fips_table = table[0]
    fips_table['Name'] = fips_table['Name'].str.upper()
    PAfips = fips_table.drop(fips_table.loc[fips_table['State'] != 'PA'].index)
    return (PAfips)
    
    #Downloads the data from the NYT using Selenium
def getTableData():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    url = driver.get('https://www.nytimes.com/interactive/2021/us/pennsylvania-covid-cases.html')
    covid = driver.find_elements_by_xpath('//td[@class="g-table super-table withchildren"]')
    
    #For loop to recognize where buttons are on the website needed to expand the data
    #Uses selenium to automate clicking the button
    more_buttons = driver.find_elements_by_class_name("showall")
    for x in range(len(more_buttons)):
      if more_buttons[x].is_displayed():
          driver.execute_script("arguments[0].click();", more_buttons[x])
          time.sleep(1)
    page_source = driver.page_source
    
    #Back to Beautiful Soup to scrape the table
    soup = BeautifulSoup(page_source, 'lxml')
    covidtable = soup.find(class_ = "g-table super-table withchildren")
    table = pd.read_html(str(covidtable))
    table = table[0]
    table = table.rename(columns={'Unnamed: 0': 'County'})
    
    #Data cleaning to get rid of carrots in the county names
    table['County'] = table['County'].str.replace('›', '')
    table['County'] = table['County'].str.strip()
    table['County'] = table['County'].str.upper()
    return (table)
    
    #Downloads the vaccine data 
def getPA_data():
    url = 'https://data.cdc.gov/resource/8xkx-amqh.json?recip_state=PA'
    page = requests.get(url, headers={'Content-Type': 'application/json'})
    #print(page.status_code)
    data = json.loads(page.content.decode('utf-8'))
    PA_data = pd.DataFrame([] , columns = ('County' , 'State', 'FIPS', '% Vaccinated', 
                                           '% 12 or older', '% 18 or older', '% 65 or older', 'Info Date'))
    #Coded it so it should take only the most recent data from the 67 counties in PA.
    count = 0
    for x in data:
        if x['recip_state'] == 'PA' and x['fips'] != 'UNK' and count != 67:
            items = [(x['recip_county']).upper() , x['recip_state'], x['fips'], x['series_complete_pop_pct'],
            x['series_complete_12pluspop'], x['series_complete_18pluspop'], 
            x['administered_dose1_recip_65pluspop_pct'], x['date']]
            dataset = pd.Series(items, index = PA_data.columns)
            PA_data = PA_data.append(dataset, ignore_index = True)
            count += 1
    return(PA_data)

    #Downloads data for the mask survey

def getMaskData():
    maskUse = pd.read_csv('mask-use-by-county.csv')
    maskUse['NEVER'] = maskUse['NEVER'].apply(lambda x: x*100) 
    maskUse['RARELY'] = maskUse['RARELY'].apply(lambda x: x*100) 
    maskUse['SOMETIMES'] = maskUse['SOMETIMES'].apply(lambda x: x*100) 
    maskUse['FREQUENTLY'] = maskUse['FREQUENTLY'].apply(lambda x: x*100)
    maskUse['ALWAYS'] = maskUse['ALWAYS'].apply(lambda x: x*100)

    return(maskUse)

if __name__ == '__main__':
    getPAfipsData()
    getTableData()
    getPA_data()
    getMaskData()
