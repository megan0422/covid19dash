# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 13:50:28 2021

@author: fbarr
"""

def masks(x, maskUse):  #located index of the county chosen then located the expval and returns the expected response for the county
    index = maskUse['COUNTYFP'][maskUse['COUNTYFP'] == x].index.tolist()
    index =index[0]
    
    never = maskUse.loc[index]['NEVER']
    rarely = maskUse.loc[index]['RARELY']
    sometimes = maskUse.loc[index]['SOMETIMES']
    frequently = maskUse.loc[index]['FREQUENTLY']
    always = maskUse.loc[index]['ALWAYS']
    return([never, rarely, sometimes, frequently, always])

if __name__ == '__main__':
    masks()











