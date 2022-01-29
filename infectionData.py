# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 14:16:21 2021

@author: mhuss
"""
#Function to return facts from the NYT infection table

def cases(county, table):
    index = table['County'][table['County'] == county].index.tolist()
    index = index[0]
    casesaverage = table.loc[index]['Per 100,000']
    change14 = table.loc[index]['14-day change']
    hospitalized = table.loc[index]['HospitalizedAvg. Per 100,000']
    deathsdaily = table.loc[index]['Deaths Daily Avg.']
    return([casesaverage, change14, hospitalized, deathsdaily])


if __name__ == '__main__':
    cases()

