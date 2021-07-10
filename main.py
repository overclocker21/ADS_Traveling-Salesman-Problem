import csv
from package import Package
from hash_table import HashMap
from distance_mapping import distances

filename = 'data/package_file.csv'

#packages for the first truck
first_truck_load = []

#packages for the second truck
second_truck_load = []

#packages for the third truck
intermediary_sorting = []

thrid_truck_load = []

#method to get row count from csv file
def get_row_count(file):
    with open(file, 'r', encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile)
        return sum(1 for row in csvreader)

#get row number
row_num = get_row_count(filename)

packages = HashMap(row_num)

with open(filename, 'r', encoding='utf-8-sig') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')

    for row in csvreader:
        id = row[0]
        address = row[1]
        delivery_time = row[5]
        weight = row[6]
        special_note = row[7]
        delivery_status = None
        newPackage = Package(id, address, delivery_time, weight, special_note, delivery_status)

        if 'Can only be on truck 2' in special_note:
            second_truck_load.append(newPackage)

        if 'Delayed' in special_note:
            second_truck_load.append(newPackage)

        if ('10:30' in delivery_time or '9:00' in delivery_time) and ('Delayed' not in special_note):
            first_truck_load.append(newPackage)

        if 'Wrong address listed' in special_note:
            address = '410 S State St'
            intermediary_sorting.append(newPackage)
        
        if ('EOD' in delivery_time) and ('None' in special_note):
            intermediary_sorting.append(newPackage)

        packages.add(id, newPackage)

for truck3 in intermediary_sorting:
    if (len(first_truck_load) < 16):
        first_truck_load.append(truck3)
    elif (len(second_truck_load) < 16) and (Package.get_id(truck3) != '9'):
        second_truck_load.append(truck3)
    else:
        thrid_truck_load.append(truck3)


def get_all_packages():
        return packages


#print truck load info
# print('Truck 1 packages:')
# for truck1 in first_truck_load:
#     print(truck1)

# print('\n')

# print('Truck 2 packages:')
# for truck2 in second_truck_load:
#     print(truck2)

# print('\n')

# print('Truck 3 packages:')
# for truck3 in thrid_truck_load:
#     print(truck3)

print(distances["0"])
