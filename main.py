import csv
from package import Package
from hash_table import HashMap
from util import get_package_count, get_distance, get_index

#initialize package array for the first truck
first_truck_load = []

#initialize package array for the second truck
second_truck_load = []

#initialize package array for the third truck
thrid_truck_load = []

#initialize package array for intermediary package bin after initial sorting
intermediary_sorting = []

#times when trucks leave the hub
first_leave_time = 8.00
second_leave_time = 9.10
third_leave_time = 11.00

#initialize total mileage for all trucks
total_mileage = []

#get number of packages based on supplied csv file with packages data
row_num = get_package_count()

#instantiate HashMap with specified row numbers(num of packages)
packages = HashMap(row_num)

#retrieve two-dimensional array of distances between stops
all_dist_from_point = get_distance()

#parse package csv data, create package object for each row and do initial sorting/truck loading
with open('data/package_file.csv', 'r', encoding='utf-8-sig') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')

    for row in csvreader:
        id = int(row[0])
        address = row[1]
        delivery_time = row[5]
        weight = row[6]
        special_note = row[7]
        hub_leave_time = None
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

#fully loading first and second truck and the rest of packages put in a third truck
for unassigned_package in intermediary_sorting:
    if (len(first_truck_load) < 16):
        first_truck_load.append(unassigned_package)
    #filtering out package with the wrong address and later loading it on truck 3 because it leaves after address is corrected
    elif (len(second_truck_load) < 16) and (Package.get_id(unassigned_package) != '9'):
        second_truck_load.append(unassigned_package)
    else:
        thrid_truck_load.append(unassigned_package)

#add hub leave times for truck 1, truck 2 and truck 3
for package in first_truck_load:
    Package.set_hub_leave_time(package, first_leave_time)

for package in second_truck_load:
    Package.set_hub_leave_time(package, second_leave_time)

for package in thrid_truck_load:
    Package.set_hub_leave_time(package, third_leave_time)


#Nearest neighbor algorithm(recursive)
#Time complexity: O(n)
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

    #Time complexity: O(n)
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

#apply algorithm for all trucks and deliver packages
deliver_package(first_truck_load, 0, first_leave_time)
deliver_package(second_truck_load, 0, second_leave_time) 
deliver_package(thrid_truck_load, 0, third_leave_time)

#Get total travelled mileage
total = 0.0
for mile in total_mileage:
    total += mile

#Starting user interface here
user_input = input("""
Please select one of the following options or type 'quit' to quit:
1. Get info for all packages at a particular time
2. Get info for all packages after all deliveries completed
""")

while user_input != 'quit':
    if user_input == '1':
        input_time = input('Enter a time (HH:mm): ')
        print("=========================================")
        splitted = input_time.split(':')
        try:
            hrs = int(splitted[0])
            min = int(splitted[1])
            min_converted_to_decimal = min/60
            user_entered_time = hrs + min_converted_to_decimal
        except ValueError:
            print("Entered value is not an integer")
            exit()

        if (hrs < 8 or hrs > 17):
            print("Outside of business hours, enter time from 8:00 to 17:00")
            exit()

        print('Status for specific timestamp:')
        print("=========================================")

        for id in range(1,row_num+1):
            if (Package.get_timestamp(packages.get(id)) < user_entered_time):
                Package.set_status(packages.get(id), 'DELIVERED')
            elif (user_entered_time < Package.get_hub_leave_time(packages.get(id))):
                Package.set_status(packages.get(id), 'AT HUB')
            else:
                Package.set_status(packages.get(id), 'EN ROUTE')
                
            print("ID:" + str(id), packages.get(id))

        print("=========================================")
        print(f'Route was completed in {round(total, 1)} miles.\n')
        exit()
    elif user_input == '2':

        print('Status for all packages after all deliveries have been completed')
        print("=========================================")

        for id in range(1,row_num+1):
            print("ID:" + str(id), packages.get(id))
        
        print("=========================================")
        print(f'Route was completed in {round(total, 1)} miles.\n')
        exit()
    elif user_input == 'quit':
        exit()
    else:
        print('Invalid entry')
        exit()