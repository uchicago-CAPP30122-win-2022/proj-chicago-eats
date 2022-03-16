## Data processing of the food_source_data
import pandas as pd
import geopandas as gpd


def process_data(file):
    """
    Processes food data into a DataFrame with categories
    and single years.
    Inputs:
        file: main food source data csv
    Outputs:
        final_df: Fully processed food data csv
    """

    frames = create_year_df(file)
    years = [2013, 2016, 2019]
    final_list = []

    for df, year in zip(frames, years):
        df = merge_df(df, year)
        final_list.append(df)

    final_food = pd.concat(final_list)

    # convert GeoDataFrame for plotting
    food_geo = gpd.GeoDataFrame(
    final_food, geometry=gpd.points_from_xy(final_food.longitude, final_food.latitude))
    food_geo.dropna(inplace=True)
    food_geo.drop('inspection_date', axis=1, inplace=True)

    food_geo.to_parquet("data/food.parquet")


def create_year_df(file):
    '''
    Creates dataframes from raw food data.
    Inputs:
        file: raw food data csv
    Ouputs:
        frames: list of cleaned dataframes for desired years of data 
    '''
    chi_food = pd.read_csv(file)
    chi_food = chi_food.dropna()
    chi_food['license_'] = chi_food['license_'].fillna(0.0)
    chi_food['dba_name'] = chi_food['dba_name'].str.lower()
    chi_food['dba_name'] = chi_food['dba_name'].str.replace(r'[^\w\s]+', ' ', regex=True)
    chi_food['facility_type'] = chi_food['facility_type'].str.lower()
    chi_food['facility_type'] = chi_food['facility_type'].str.replace(r'[^\w\s]+', ' ', regex=True)
    chi_food['inspection_date'] = pd.to_datetime(chi_food['inspection_date'], format='%Y-%m-%d')

    inspection_dates = [('2012-01-01', '2013-12-31'),
                        ('2015-01-01', '2016-12-31'),
                        ('2018-01-01', '2019-12-31')]
    frames = []

    for start_date, end_date in inspection_dates:
        year = chi_food.loc[(chi_food['inspection_date'] >= start_date) & \
               (chi_food['inspection_date'] < end_date)]
        year = year.drop_duplicates(['dba_name'], keep='first')
        zero_license = year.loc[year['license_'] == 0.0]
        year_zero = zero_license.iloc[1: ]
        year_df = year.drop_duplicates(["license_"], keep='first')
        year_fin = pd.concat([year_zero, year_df])
        frames.append(year_fin)

    return frames


def create_facility_dfs(df, year):
    '''
    Creates food source categories from a food dataframe.
    Helper function for merge_df().
    Inputs:
        df: food data frame processed by create_year_df()
        year: year of data
    Outputs:
        df_years_lst: list of categorized dataframes
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
    Concats the DataFrames from create_facility_dfs() together.
    Inputs:
        df: DataFrame processed by create_year_df
        year: year of data
    Outputs:
        final_master_df: final processed dataframe
    '''
    df_years_lst = create_facility_dfs(df, year)
    final_duplicates = pd.concat(df_years_lst)
    final = final_duplicates.drop_duplicates(['dba_name'], keep='first')
    zero_license_final = final.loc[final['license_'] == 0.0]
    zero_df_final = zero_license_final.iloc[1: ]
    final_df = final.drop_duplicates(["license_"], keep='first') 
    final_master_df = pd.concat([zero_df_final, final_df])

    return final_master_df
