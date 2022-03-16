#Zipcode Data Cleaning 
import pandas as pd

north_zipcodes = [60660, 60626, 60645, 60659, 60646, 60631, 60656, 60630, 60625, 60634, 60641, 
60618, 60657, 60613, 60640, 60651, 60622, 60614, 60647, 60639]

west_zipcodes = [60644, 60624, 60612]

downtown_zipcodes = [60601, 60602, 60603, 60604, 60605, 60606, 60607, 60610, 60611, 60661, 60654]

south_zipcodes = [60628, 60608, 60616, 60653, 60615, 60609, 60632, 60638, 60629, 60636, 60621, 
60637, 60652, 60620, 60619, 60628, 60643, 60655, 60827]

east_zipcodes = [60649, 60617, 60633]

CLEAN_FOOD_FILE = '~/capp30122/proj-chicago-eats/chicagoeats/data/food_source_final_1.csv'

def regions_by_year(region_zip, year):
    '''
    '''
    CLEAN_FOOD_FILE = '~/capp30122/proj-chicago-eats/chicagoeats/data/food_source_final_1.csv'
    
    chi_food = pd.read_csv(CLEAN_FOOD_FILE)
    region_year_df = chi_food[chi_food.zip.isin(region_zip)]
    region_year_df = region_year_df[region_year_df['year'] == year]

    return region_year_df

def region_category_by_year(region_year_df, category):
    '''
    
    '''
    region_category_year = region_year_df[region_year_df['category'] == category]
    
    
    return region_category_year