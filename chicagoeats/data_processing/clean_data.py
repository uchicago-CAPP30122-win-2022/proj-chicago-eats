## Data processing of the food_source_data

import pandas as pd

def clean_main_data(filename):
    '''
    
    '''
    (df_2013, df_2016, df_2019)= create_year_df(filename)

    final_df13 = merge_df(df_2013, 2013)
    final_df15 = merge_df(df_2016, 2016)
    final_df19 = merge_df(df_2019, 2019)

    final_df_lst = [final_df13, final_df15, final_df19]
    final_food_df = pd.concat(final_df_lst)
    
    final_food_df.to_csv(r'~/capp30122/proj-chicago-eats/chicagoeats/data/food_source_final.csv')
    

def create_year_df(filename):
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
    df12_13 = s12_13.drop_duplicates(["license_"], keep='first')

    s15_16 = s15_16.drop_duplicates(['dba_name'], keep='first')
    df15_16= s15_16.drop_duplicates(["license_"], keep='first')

    s18_19 = s18_19.drop_duplicates(['dba_name'], keep='first')
    df18_19 = s18_19.drop_duplicates(["license_"], keep='first') 

    return (df12_13, df15_16, df18_19)

def create_facility_dfs(df, year):
    '''
    Input df
    Returns 1 df for the given year
    '''
    
    df = df.reindex(columns = df.columns.tolist() + ['year'], fill_value = year)

    df_restaurant = df[df['facility_type'].str.contains('rest')]
    df_restaurant_final = df_restaurant.reindex(columns = df_restaurant.columns.tolist() \
        + ['category'], fill_value = 'Restaurant')

    df_convenience = df[df['facility_type'].str.contains('conv')]
    df_convenience_final = df_convenience.reindex(columns = df_convenience.columns.tolist() \
        + ['category'], fill_value = 'Convenience Store')

    df_grocery = df[df['facility_type'].str.contains('groc')]
    df_grocery_final = df_grocery.reindex(columns = df_grocery.columns.tolist() + ['category'], \
        fill_value = 'Grocery Store') 
    
    df_years_lst = [df_restaurant_final, df_convenience_final,  df_grocery_final]
    
    return df_years_lst

def merge_df(df, year):
    '''
    
    '''
    df_years_lst = create_facility_dfs(df, year)
    final_duplicates = pd.concat(df_years_lst)
    final = final_duplicates.drop_duplicates(['dba_name'], keep='first')
    final_df = final.drop_duplicates(["license_"], keep='first') 
   
    return final_df