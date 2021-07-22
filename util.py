import csv
from address_mapper import address_to_index_mapper

# function to get package count from csv file
# space and time complexity: O(n)
def get_package_count():
    with open('data/package_file.csv', 'r', encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile)
        return sum(1 for row in csvreader)

# parse csv file with distance data and store it in a two-dimensional array
# space and time complexity: O(n)
def get_distance():
    all_distances = []
    with open('data/distance_data.csv', 'r', encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            all_distances.append(row)
    
    return all_distances

# get corresponding index for specific address from the mapper
# space and time complexity: O(1)
def get_index(address):
    return address_to_index_mapper[address]