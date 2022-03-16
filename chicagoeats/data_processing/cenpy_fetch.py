"""
Fetches and processes ACS data from the Cenpy API
"""

import cenpy
import pandas as pd

gdfs = []
years = [2013, 2016, 2019]
acs_variables = {
'B01003_001E' : 'total_pop',
'B19013_001E' : 'median_household_income',
'B25077_001E' : 'median_home_value',
'B03002_012E' : 'n_hispanic',
'B02008_001E' : 'n_white',
'B02009_001E' : 'n_black',
'B02011_001E' : 'n_asian',
'B17001_002E' : 'n_poverty'}

def cenpy_fetcher():
    """
    Fetches, cleans, processes, and writes out to the data folder
    a parquet file of a multi-year dataframe.

    Inputs:
        None
    Outputs:
        None
        Writes out file to data foler
    """
    for year in years:
        chi = cenpy.products.ACS(year).from_place('Chicago, IL', variables= [
            'B01003_001', 'B19013_001E', 'B25077_001E',
            'B03002_012E','B02008_001E', 'B02011_001E', 'B02009_001E',
            'B17001_002E'], level='tract')
        chi['year'] = year
        gdfs.append(chi)

    chi_gdf = pd.concat(gdfs)
    chi_gdf.rename(columns=acs_variables, inplace=True)
    chi_gdf.drop(['state', 'county'], axis=1, inplace=True)

    chi_gdf['p_poverty'] = chi_gdf.n_poverty/chi_gdf.total_pop
    chi_gdf['p_black'] = chi_gdf.n_black/chi_gdf.total_pop
    chi_gdf['p_white'] = chi_gdf.n_white/chi_gdf.total_pop
    chi_gdf['p_hispanic'] = chi_gdf.n_hispanic/chi_gdf.total_pop
    chi_gdf['p_asian'] = chi_gdf.n_asian/chi_gdf.total_pop

    chi_gdf.to_parquet("data/acs.parquet")
