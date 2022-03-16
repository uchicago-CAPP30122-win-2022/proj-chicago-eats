## Data processing of the food_source_data

import pandas as pd


def create_year_df(FOOD_FILE):
    '''
    
    '''
    chi_food = pd.read_csv(FOOD_FILE)
    chi_food = chi_food.dropna()
    chi_food['license_'] = chi_food['license_'].fillna(0.0)
    chi_food['dba_name'] = chi_food['dba_name'].str.lower()
    chi_food['dba_name'] = chi_food['dba_name'].str.replace(r'[^\w\s]+', ' ', regex=True)
    chi_food['facility_type'] = chi_food['facility_type'].str.lower()
    chi_food['facility_type'] = chi_food['facility_type'].str.replace(r'[^\w\s]+', ' ', regex=True)
    chi_food['inspection_date'] = pd.to_datetime(chi_food['inspection_date'], format='%Y-%m-%d')

    yr12_13 = chi_food.loc[(chi_food['inspection_date'] >= '2012-01-01') & (chi_food['inspection_date'] < '2013-12-31')]
    yr15_16 = chi_food.loc[(chi_food['inspection_date'] >= '2015-01-01') & (chi_food['inspection_date'] < '2016-12-31')]
    yr18_19 = chi_food.loc[(chi_food['inspection_date'] >= '2018-01-01') & (chi_food['inspection_date'] < '2019-12-31')]

    yr12_13 = yr12_13.drop_duplicates(['dba_name'], keep='first')
    zero_license_13 = yr12_13.loc[yr12_13['license_'] == 0.0]
    zero_df_13 = zero_license_13.iloc[1: ]
    df12_13 = yr12_13.drop_duplicates(["license_"], keep='first')
    df12_13_fin = pd.concat([zero_df_13, df12_13])
    
    yr15_16 = yr15_16.drop_duplicates(['dba_name'], keep='first')
    zero_license_16 = yr15_16.loc[yr15_16['license_'] == 0.0]
    zero_df_16 = zero_license_16.iloc[1: ]
    df15_16= yr15_16.drop_duplicates(["license_"], keep='first')
    df15_16_fin = pd.concat([zero_df_16, df15_16])
    
    yr18_19 = yr18_19.drop_duplicates(['dba_name'], keep='first')
    zero_license_19 = yr18_19.loc[yr18_19['license_'] == 0.0]
    zero_df_19 = zero_license_19.iloc[1: ]
    df18_19 = yr18_19.drop_duplicates(["license_"], keep='first') 
    df18_19_fin = pd.concat([zero_df_19, df18_19])

    return (df12_13_fin, df15_16_fin, df18_19_fin)

def create_facility_dfs(df, year):
    '''
    Input df
    Returns 1 df for the given year
    '''

    df = df.reindex(columns = df.columns.tolist() + ['year'], fill_value = year)

    df_liquor = df[df['facility_type'].str.contains('liq') | df['dba_name'].str.contains('beverage')]
    df_liquor_final = df_liquor.reindex(columns = df_liquor.columns.tolist() + ['category'], \
        fill_value = 'Liquor Store') 
    
    df_convenience = df[df['facility_type'].str.contains('conv | gas') | \
        df['dba_name'].str.contains('gas sta')]
    df_convenience_final = df_convenience.reindex(columns = df_convenience.columns.tolist() \
        + ['category'], fill_value = 'Convenience Store/Gas Station')

    df_grocery = df[df['facility_type'].str.contains('groc')]
    df_grocery_final = df_grocery.reindex(columns = df_grocery.columns.tolist() + ['category'], \
        fill_value = 'Grocery Store') 

    df_restaurant = df[df['facility_type'].str.contains('rest')]
    df_restaurant_final = df_restaurant.reindex(columns = df_restaurant.columns.tolist() \
        + ['category'], fill_value = 'Restaurant')

    df_years_lst = [df_liquor_final, df_convenience_final, df_grocery_final, df_restaurant_final]
    
    return df_years_lst

def merge_df(df, year):
    '''
    
    '''
    df_years_lst = create_facility_dfs(df, year)
    final_duplicates = pd.concat(df_years_lst)
    final = final_duplicates.drop_duplicates(['dba_name'], keep='first')
    zero_license_final = final.loc[final['license_'] == 0.0]
    zero_df_final = zero_license_final.iloc[1: ]
    final_df = final.drop_duplicates(["license_"], keep='first') 
    final_master_df = pd.concat([zero_df_final, final_df])

    return final_master_df 

def 


