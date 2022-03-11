## Data processing of the food_source_data

import pandas as pd

def clean_main_data(filename):
    '''
    
    '''

    chi_food = pd.read_csv(filename)
    chi_food = chi_food.dropna()
    chi_food['license_'] = chi_food['license_'].fillna(0.0)
    chi_food['facility_type'] = chi_food['facility_type'].str.lower()
    chi_food['facility_type'] = chi_food['facility_type'].str.replace(r'[^\w\s]+', ' ', regex=True)
    chi_food['inspection_date'] = pd.to_datetime(chi_food['inspection_date'], format='%Y-%m-%d')


    s12_13 = chi_food.loc[(chi_food['inspection_date'] >= '2012-01-01') & (chi_food['inspection_date'] < '2013-12-31')]
    s15_16 = chi_food.loc[(chi_food['inspection_date'] >= '2015-01-01') & (chi_food['inspection_date'] < '2016-12-31')]
    s18_19 = chi_food.loc[(chi_food['inspection_date'] >= '2018-01-01') & (chi_food['inspection_date'] < '2019-12-31')]

    s12_13 = s12_13.drop_duplicates(['dba_name'], keep='first')
    df12_13_final = s12_13.drop_duplicates(["license_"], keep='first')

    s15_16 = s15_16.drop_duplicates(['dba_name'], keep='first')
    df15_16_final = s15_16.drop_duplicates(["license_"], keep='first')

    s18_19 = s18_19.drop_duplicates(['dba_name'], keep='first')
    dfs18_19_final = s18_19.drop_duplicates(["license_"], keep='first') 

    return (df12_13_final, df15_16_final, dfs18_19_final)

def create_facility_dfs(df):
    '''
    Input df
    Returns 3 df of food facility categories
    '''
    
    resturants = df[df['facility_type'].str.contains('rest')]
    
    convience = df[df['facility_type'].str.contains('conv')]
        
    grocery = df[df['facility_type'].str.contains('groc')]
        
  
    return (resturants, convience, grocery)