# This is the file that connects to the Chicago Data Portal and grabs the data.  
# Food Inspections Dataset Identifier: 4ijn-s7e5
# Desired columns:  'Inspection ID', 'DBA Name', 'License #','Facility Type', 'Risk', 'Address', 'City', 'State','Zip','Inspection Date', 'Results', 'Latitude','Longitude'

import pandas as pd
from sodapy import Socrata

def _decode_libray_data(dct):
    #First check that all required attributes are inside the dictionary 
    if all (key in dct for key in ["name_","location","address"]):
        # The above line makes sure dictionary has the attributes that are wanted.
        # This executes the filtering after receiving the full dataset rather than
        # filtering with arguements added to the find_libraries method.  This is 
        # inefficient if we aren't going to be using all of the columns.  
        return Library(dct["name_"],(dct["location"]['latitude'],dct["location"]['longitude']) ,dct["address"])
        # Creates the library object
    return dct  

class DataPortalCollector: 

    def __init__(self):
        # Unauthenticated client only works with public data sets. Note 'None'
        # in place of application token, and no username or password:
        self.client = Socrata("data.cityofchicago.org", "ilGInDr4ZciNQrrSGCNEjaPYZ") 
        #creates an instance of a Socrata object
        # Second arguement is for an App Token.  Not required.
        # My app token: ilGInDr4ZciNQrrSGCNEjaPYZ 
        # Enter app token as "ilGInDr4ZciNQrrSGCNEjaPYZ"
        
    def find_records(self, limit): 
        #limit will limit the number of rows that will be returned
        libraries = [] 
        results = self.client.get("4ijn-s7e5",limit=limit)
        # first arguement is the dataset identifier.  
        # Remaining keyword arguements to this get method is how you will filter
        # out information from the entire dataset.  Could get rid of limit
        # if I want the whole dataset.  
        # results variable will be a python list dictionaries. Each dictionary within
        # the list will be a single entry (row) from the dataset The key for 
        # each dictionary is the column name and the value will be the value for 
        # that entry in that column
        ##for lib_dict in results: 
        ##    library = _decode_libray_data(lib_dict)
            # decode converts the dictionary into a library object.  
        ##    libraries.append(library)
        print(results)

        ##return libraries
        # "libraries" is a python list of dictionaries where the dictionary
        # key is the column name and the value value for the column entry.  
        # Each row of the dataset will be a dictionary and each key / value
        # in that dictionary will be a column name / element of that row.   



