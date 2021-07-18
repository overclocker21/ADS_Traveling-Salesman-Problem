import csv
from package import Package
from hash_table import HashMap
from distance_mapping import distances
import math


filename = 'data/package_file.csv'

#packages for the first truck
first_truck_load = []

#packages for the second truck
second_truck_load = []

#packages for intermediatery and the third truck
intermediary_sorting = []
thrid_truck_load = []

# Times the trucks leave the hub
first_leave_time = 8.00
second_leave_time = 9.10
third_leave_time = 11.00

#total mileage for all trucks
total_mileage = []

#total times for deliveries
first_total_time = []
second_total_time = []
third_total_time = []

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
        timestamp = None
        delivery_status = None
        newPackage = Package(id, address, delivery_time, weight, special_note, timestamp, delivery_status)

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

#loading fully first and second truck and the rest put in a third
for truck3 in intermediary_sorting:
    if (len(first_truck_load) < 16):
        first_truck_load.append(truck3)
    elif (len(second_truck_load) < 16) and (Package.get_id(truck3) != '9'):
        second_truck_load.append(truck3)
    else:
        thrid_truck_load.append(truck3)

def get_distance():
    all_distances = []
    with open('data/distance_data.csv', 'r', encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            all_distances.append(row)
    
    return all_distances

def get_index(address):
    return distances[address]

all_dist_from_point = get_distance()

#nearest neighbor algorithm(recursive)
def deliver_package(truck, start, timestamp):

    #if there are no packages in the truck, stop deliveries
    if len(truck) == 0: return

    #init lowest distance with the distance to the first delivery in the array of addresses
    lowest_distance = float(all_dist_from_point[get_index(Package.get_address(truck[0]))][start])

    #init Package holder object for next delivery data
    next_delivery = Package()

    #store initial starting point index
    start_next = start

    #store initial timestamp
    next_timestamp = timestamp

    #loop thru packages in truck and determine lowest distance from current start position to each address 
    # of the remaining packages in the array and hydrate next_delivery object with relevant data
    for package in truck[:]:
        start_to_address = float(all_dist_from_point[get_index(Package.get_address(package))][start])    
        if (start_to_address <= lowest_distance):
            lowest_distance = start_to_address
            next_delivery = package

    #adding travelled mileage to total mileage array
    total_mileage.append(lowest_distance)

    #getting id of selected delivery
    id = Package.get_id(next_delivery)

    #calculating time it took to deliver the package in current iteration
    next_timestamp += lowest_distance/18
    #print(str(math.floor(timestamp)) + ':' + str(math.floor(round(timestamp - math.floor(timestamp),2)*60)))

    #getting the index of the next closest delivery
    start_next = get_index(Package.get_address(next_delivery))

    #updating status of package in HashMap except when on the way back to HUB
    if Package.get_address(next_delivery) != "4001 South 700 East":
        Package.set_status(packages.get(id), 'DELIVERED')
        Package.set_timestamp(packages.get(id), round(next_timestamp, 2))

    #if there's a last package in the truck and it is being delivered, add one more stop back to HUB
    if len(truck) == 1 and Package.get_address(next_delivery) != "4001 South 700 East":
        hub = Package(delivery_address="4001 South 700 East", timestamp=None, delivery_status=None)
        truck.append(hub)

    #unloading delivered package from the truck
    if next_delivery in truck:
        truck.remove(next_delivery)

    #recursively deliver next package with updated starting point
    return deliver_package(truck, start_next, next_timestamp)

deliver_package(first_truck_load, 0, first_leave_time)
# deliver_package(second_truck_load, 0, second_leave_time) 
# deliver_package(thrid_truck_load, 0, third_leave_time)

#Get total travelled mileage
total = 0.0
for mile in total_mileage:
    total += mile

print("Total miles travelled", round(total, 1))

#Print hashmap:
packages.print()