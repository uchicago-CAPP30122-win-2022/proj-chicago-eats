#Chicago Eats App

import argparse
from data_processing.food_source_data_api import DataPortalCollector
from data_processing.cenpy_fetch import cenpy_fetcher
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', action='store_true',
                        help='Downloads and cleans all of the data used in the project')
    parser.add_argument('--viz', action='store_true',
                        help='Launches the Panel server so that it can be viewed in a web browser.')

    args = parser.parse_args()

    if args.data:
        connector = DataPortalCollector()
        connector.find_records()
        print("Food data has been downloaded into the data folder.")
        cenpy_fetcher()
        print('cenpy data has been downloaded into the data folder.')
    if args.viz:
        cmd = "panel serve visualizations/viz.ipynb"
        os.system(cmd)

if __name__ == '__main__':
    main()
