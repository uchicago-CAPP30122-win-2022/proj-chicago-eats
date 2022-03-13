# create clean data csv

import pandas as pd
from clean_data import merge_df, create_year_df  

FOOD_FILE = "~/capp30122/proj-chicago-eats/chicagoeats/data/food_source_data_set.csv"

(df_2013, df_2016, df_2019)= create_year_df(FOOD_FILE)

final_df13 = merge_df(df_2013, 2013)
final_df16 = merge_df(df_2016, 2016)
final_df19 = merge_df(df_2019, 2019)

final_df_lst = [final_df13, final_df16, final_df19]
final_food_df = pd.concat(final_df_lst)
    
final_food_df.to_csv(r'~/capp30122/proj-chicago-eats/chicagoeats/data/food_source_final.csv')