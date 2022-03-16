# Imports and global variables

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


north_zipcodes = [60660, 60626, 60645, 60659, 60646, 60631, 60656, 60630, 60625, 60634, 60641, 
60618, 60657, 60613, 60640, 60651, 60622, 60614, 60647, 60639, 60642]

west_zipcodes = [60644, 60624, 60612]

downtown_zipcodes = [60601, 60602, 60603, 60604, 60605, 60606, 60607, 60610, 60611, 60661, 60654]

south_zipcodes = [60628, 60608, 60616, 60653, 60615, 60609, 60632, 60638, 60629, 60636, 60621, 
60637, 60652, 60620, 60619, 60628, 60643, 60655, 60827, 60623]

east_zipcodes = [60649, 60617, 60633]

region_zip_lst = [north_zipcodes, west_zipcodes, downtown_zipcodes, south_zipcodes, east_zipcodes]

def regions_by_year(region_zip_lst, year):
    '''
    Creates a list of pandas dataframes of food sources based on Chicago regions (North, South, East, West, Downtown) 
    by a given year (2013, 2016, 2019)
    Inputs: region_zip_lst(list): a list of Chicago zipcodes sorted by region
            year(int): a year taken from the master food_source_final.csv (2013, 2016, 2019)
    Returns(list): a list of 5 dataframes, 1 for each region for the given year (ex: North_2013, South_2013, etc.)
    '''
    CLEAN_FOOD_FILE = '~/capp30122/proj-chicago-eats/chicagoeats/data/food_source_final.csv'
    region_yr_lst = []
    chi_food = pd.read_csv(CLEAN_FOOD_FILE)
    for zipcodes in region_zip_lst:
        region_year_df = chi_food[chi_food.zip.isin(zipcodes)]
        region_year_df = region_year_df[region_year_df['year'] == year]
        region_yr_lst.append(region_year_df)
    return region_yr_lst

def region_category_by_year(region_zip_lst, year):
    '''
    Creates dataframes of Chiacago regional food sources 
    Inputs: region_zip_lst(list)
            year(int)
    Returns(list) a list of lists of dataframes of Chicago regions divided by food source categories 
    (ex:north_13_restaurants, north_13_conv, etc.)
    '''
    region_categories = ['Restaurant', 'Convenience Store/Gas Station', 'Grocery Store', 'Liquor Store']
    chi_regions = regions_by_year(region_zip_lst, year)
    category_lst = []
    
    for i, region in enumerate(chi_regions): 
        category_lst.append([])
        for category in region_categories:
            region_category_year = region[region['category'] == category]
            category_lst[i].append(region_category_year)

    return category_lst

def total_food_sources(region_zip_lst, year):
    '''
    Counts the total number of food sources for a Chiacago region for a given year.
    Inputs( list of dataframes): region_categories
    Returns(list): a list of the total number of food sources in a given year for each Chicago region. 
    '''
    total_length_lst = []
    total_source_lst = []
    chi_regions= region_category_by_year(region_zip_lst, year)

    for i, regions in enumerate(chi_regions):
        total_length_lst.append([])
        for categories in regions:
            region_total = len(categories)
            total_length_lst[i].append(region_total)

    for region in total_length_lst: 
        total_food_source = sum(region)
        total_source_lst.append(total_food_source)
    return total_source_lst

    
def category_percent(region_zip_lst, year):
    '''
    Create a list of category percents for a Chicago region for a given year.
    Inputs():
    Returns(lst): a list of lists
    '''
    chi_regions= region_category_by_year(region_zip_lst, year)
    percent_lst = []
    total_length_lst = []

    for i, regions in enumerate(chi_regions):
        total_length_lst.append([])
        for categories in regions:
            region_total = len(categories)
            total_length_lst[i].append(region_total)
 

    for i, region in enumerate(total_length_lst):
        percent_lst.append([])
        for category_total in region: 
            cat_percent = category_total/sum(region)
            percent_lst[i].append(cat_percent)
    return percent_lst
   
