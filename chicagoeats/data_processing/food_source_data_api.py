'''
- This is the file that connects to the Chicago Data Portal and downloads
the Food Inspection data set.  .  
- Food Inspections Dataset Identifier: 4ijn-s7e5
- Desired columns:  'Inspection ID', 'DBA Name', 'License #','Facility Type', 'Risk', 'Address', 'City', 'State','Zip','Inspection Date', 'Results', 'Latitude','Longitude'
- Code to run in ipthon3 while in the chicagoeats directory: 
    - connector = food_source_data_api.DataPortalCollector()
    - connector.find_records()
    - This will write over the food_source_data_set.csv file in the data
      directory.  
'''
import pandas as pd
from sodapy import Socrata
import csv

COLS = 'inspection_id, dba_name, license_, facility_type, zip, inspection_date, latitude, longitude'
csv_cols = ['inspection_id', 'dba_name', 'license_', 'facility_type', 'zip',
            'inspection_date', 'latitude', 'longitude']

class DataPortalCollector: 

    def __init__(self):
        self.client = Socrata("data.cityofchicago.org", "ilGInDr4ZciNQrrSGCNEjaPYZ") 
        
    def find_records(self): 
        with open('data/food_source_data_set.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_cols)
            writer.writeheader()
            data_dict = self.client.get("4ijn-s7e5", limit=1000000, select=COLS)
            writer.writerows(data_dict)




