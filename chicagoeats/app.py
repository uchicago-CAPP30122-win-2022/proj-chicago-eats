#Chicago Eats App

import argparse
from data_processing.food_source_data_api import DataPortalCollector

def main():
    connector = DataPortalCollector()
    limit = 1000000 
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='the limit of the number of inspection records to receive')
    #parser.add_argument('--des', action='store_true', help='Sort the libaries by name in Z to A order (default: ascending order)')
  
    args = parser.parse_args()
    
    if args.data: 
        connector.find_records()

    #if args.des:
        #libraries.sort(reverse=True, key=lambda obj: obj.name)
    #else:
        #libraries.sort(key=lambda obj: obj.name)

    #for library in libraries:
        #print(library)
        #print("----")


if __name__ == '__main__':
    main() 