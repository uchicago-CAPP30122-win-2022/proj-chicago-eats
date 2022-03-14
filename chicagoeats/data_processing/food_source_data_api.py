# This is the file that connects to the Chicago Data Portal and grabs the data.  
# Food Inspections Dataset Identifier: 4ijn-s7e5
# Desired columns:  'Inspection ID', 'DBA Name', 'License #','Facility Type', 'Risk', 'Address', 'City', 'State','Zip','Inspection Date', 'Results', 'Latitude','Longitude'

import pandas as pd
from sodapy import Socrata
import csv

COLS = 'inspection_id, dba_name, license_, facility_type, zip, inspection_date, latitude, longitude'
csv_cols = ['inspection_id', 'dba_name', 'license_', 'facility_type', 'zip',
            'inspection_date', 'latitude', 'longitude']
#where_clause = 'inspection_date < 2022-01-19T00:00.000'

#query = 'SELECT inspection_id, dba_name, license_, facility_type, inspection_date, latitude,\
 #       longitude WHERE inspection_date <= 2017-01-19 AND inspection_date >= 2016-01-19 LIMIT 2'

class DataPortalCollector: 

    def __init__(self):
        self.client = Socrata("data.cityofchicago.org", "ilGInDr4ZciNQrrSGCNEjaPYZ") 
        
    def find_records(self): 
        with open('data/food_source_data_set.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_cols)
            writer.writeheader()
            data_dict = self.client.get("4ijn-s7e5", limit=1000000, select=COLS)
            #data_dict = self.client.get("4ijn-s7e5", query=query)
            #print(data_dict)
            writer.writerows(data_dict)




