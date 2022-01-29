#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 13:25:56 2021

@author: mhuss
"""

#This loop will sort the results based on the age entered in the main menu

def vStat(fips, age, PA_data):
    if 12 <= age <18:
        index = PA_data['FIPS'][PA_data['FIPS'] == fips].index.tolist() 
        index = index[0]
        vaccineStat = PA_data.loc[index]['% 12 or older']
        return(vaccineStat)
    elif 19 <= age < 65:
        index = PA_data['FIPS'][PA_data['FIPS'] == fips].index.tolist() 
        index = index[0]
        vaccineStat = PA_data.loc[index]['% 18 or older']
        return(vaccineStat)
    elif age > 65:
        index = PA_data['FIPS'][PA_data['FIPS'] == fips].index.tolist() 
        index = index[0]
        vaccineStat = PA_data.loc[index]['% 65 or older']
        return(vaccineStat)

if __name__ == '__main__':
    vStat()
    
    
    
