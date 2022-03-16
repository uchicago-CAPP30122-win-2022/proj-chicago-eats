# Chicago Eats App

import argparse
from data_processing.cenpy_fetch import cenpy_fetcher
from data_processing.food_source_data_api import DataPortalCollector
from data_processing.clean_data import process_data
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', action='store_true',
                        help='Downloads and cleans all of the data used in the project')
    parser.add_argument('--viz', action='store_true',
                        help='Launches the Panel server so that it can be viewed in a web browser.')
    parser.add_argument('--notebooks', action='store_true',
                        help='Launches Jupyter so user can navigate to supplemental notebooks.')

    args = parser.parse_args()

    if args.data:
        connector = DataPortalCollector()
        connector.find_records()

        process_data('data/food_source_data_set.csv')
        print("The food data has been downloaded and processed.")

        cenpy_fetcher()
        print('cenpy data has been downloaded and processed.')
    elif args.viz:
        cmd = "panel serve visualizations/viz.ipynb"
        os.system(cmd)
    elif args.notebooks:
        cmd = "python -m notebook"
        os.system(cmd)

if __name__ == '__main__':
    main()
