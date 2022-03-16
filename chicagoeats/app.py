#Chicago Eats App

import argparse
from data_processing.food_source_data_api import DataPortalCollector
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='Downloads and cleans all ofthe data used in the project')
    parser.add_argument('--viz', help='Launches the Panel server so that it can be viewed \
    in a web browser.')

    args = parser.parse_args()

    if args.data:
        connector = DataPortalCollector()
        connector.find_records()
    if args.viz:
        cmd = "panel serve visualizations/viz.ipynb"
        os.system(cmd)

if __name__ == '__main__':
    main()