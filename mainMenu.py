#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 14:48:10 2021

@author: philippinekugener
"""

import allData
import infectionData
import maskData
import vaccineData
import re

PA_data = allData.getPA_data()
PAfips = allData.getPAfipsData()
table = allData.getTableData()
maskUse = allData.getMaskData()

#Code for making sure the county is valid

#start_county = the uppercase name of the start county (without 'county' at the end)
#start_fips = the fips of the start county

run = ''
while run != 'DONE':
    x = 0
    while x == 0:
        start_county = input('What county in PA are you coming from? ')
        if bool(re.search(r'[Cc]ounty', start_county)) == True:
            start_county = start_county.upper()
            start_county = start_county.replace(' COUNTY', '')
        else:
            start_county = start_county.upper()
        index = PAfips['Name'][PAfips['Name'] == start_county].index.tolist()     
        if index == []:
            print('County is not in PA please enter again')
        else:
            index = index[0]
            start_fips = PAfips.loc[index]['FIPS']
            x = 1
     
    #end_county = the uppercase name of the destination county (without 'county' at the end)
    #end_fips = the fips of the destination county   
     
    x = 0
    while x == 0:
        end_county = input('What county in PA are you traveling to? ')  
        if bool(re.search(r'[Cc]ounty', end_county)) == True:
            end_county = end_county.upper()
            end_county = end_county.replace(' COUNTY', '')
        else:
            end_county = end_county.upper()
        index = PAfips['Name'][PAfips['Name'] == end_county].index.tolist()     
        if index == []:
            print('County is not in PA please enter again')
        else:
            index = index[0]
            end_fips = PAfips.loc[index]['FIPS']
            x = 1
            
    age = int(input('What is your age? '))
    
    print('')
    print('Start County:' , start_county.title())
    print('The vaccination percentage for {:} year olds is {:}%'
          .format(age, vaccineData.vStat(str(start_fips), age, PA_data)))
    cases_data = infectionData.cases(start_county, table)
    print('''The daily case average per 100,000 is {:} \nThe 14 day percent daily change trend in cases is {:} \nThe number hospitalized is {:} \nThe number of deaths daily is {:}'''
          .format(cases_data[0], cases_data[1], cases_data[2], cases_data[3]))
    print('')
    print('-'*54)
    print('')
    print('Destination County:' , end_county.title())
    print('The vaccination percentage for {:} year olds is {:}%'
          .format(age, vaccineData.vStat(str(end_fips), age, PA_data)))
    cases_data = infectionData.cases(end_county, table)
    print('''The daily case average per 100,000 is {:} \nThe 14 day percent daily change trend in cases is {:} \nThe number hospitalized is {:} \nThe number of deaths daily is {:}'''
          .format(cases_data[0], cases_data[1], cases_data[2], cases_data[3]))
    print('')
    print('-'*54)
    print('')
    mask_start = maskData.masks(start_fips, maskUse)
    mask_end = maskData.masks(end_fips, maskUse)
    print('How often do residents wear masks in public when they \nexpect to be within six feet of another person?')
    print('')
    print('{:<10}{:^14}{:^14}'.format('Response:' , start_county.title(), end_county.title()))
    print('{:<10}    {:>5.2f}%        {:5.2f}%'.format('NEVER', mask_start[0], mask_end[0]))
    print('{:<10}    {:>5.2f}%        {:5.2f}%'.format('RARELY', mask_start[1], mask_end[1]))
    print('{:<10}    {:>5.2f}%        {:5.2f}%'.format('SOMETIMES', mask_start[2], mask_end[2]))
    print('{:<10}    {:>5.2f}%        {:5.2f}%'.format('FREQUENTLY', mask_start[3], mask_end[3]))
    print('{:<10}    {:>5.2f}%        {:5.2f}%'.format('ALWAYS', mask_start[4], mask_end[4]))
    
    run = (input("Press return to check more counties \nEnter 'done' to end the program\n")).upper()
    
