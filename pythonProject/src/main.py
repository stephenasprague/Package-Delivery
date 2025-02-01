# Stephen Sprague, student ID #010246742
from truck import Truck
from package import Package
import hash
import csv
import datetime


# FUNCTIONS
# this section contains the functions for the main program
# function to load packages into hash table from csv
def import_packages(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            # set initial values
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]

            # create package object with info from csv
            new_package = Package(package_id, address, city, state, zip_code, deadline, weight, 'At Hub')

            # store new package object in hash table
            package_list.insert(package_id, new_package)


# function to load distance table from csv
def import_distance_table(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            distance_table.append(row)


# function to load addresses from csv
def import_addresses(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            addresses.append(row[0])


# calculate package delivery time
def calc_time(current_time, distance):
    time_delta = datetime.timedelta(hours=(distance / 18.0))
    new_time = current_time + time_delta
    return new_time


# function to lookup packages by package ID and time
# prints status of individual packages
def lookup_package(package_id, time):
    # if package ID is not found or invalid, prints error message
    if package_list.search(package_id) is None:
        print('Package not found, please try again')
    # lookup function for packages that are delayed
    elif package_id == 6 or package_id == 25 or package_id == 28 or package_id == 32:
        # show delayed status until packages arrive at hub
        if time < package_list.search(package_id).time_loaded:
            print(str(package_list.search(package_id)) + ', Status: Delayed on flight')
        # print en route if packages are on the truck but not yet delivered
        elif package_list.search(package_id).time_loaded < time < package_list.search(package_id).time_delivered:
            print(str(package_list.search(package_id)) + ', Status: En route')
        # print package information including time delivered
        else:
            package_list.search(package_id).display_packages()
    # lookup function for package with incorrect address
    elif package_id == 9:
        # show incorrect address status and display address
        if time < package_list.search(package_id).time_loaded:
            package_list.search(package_id).address = '300 State St'
            package_list.search(package_id).zip_code = '84103'
            print(str(package_list.search(package_id)) + ', Status: Incorrect address - Waiting on update')
            # update package object with correct address
            package_list.search(package_id).address = '410 S State St'
            package_list.search(package_id).zip_code = '84111'
        # print en route if package is on the truck but not yet delivered
        elif package_list.search(package_id).time_loaded < time < package_list.search(package_id).time_delivered:
            print(str(package_list.search(package_id)) + ', Status: En route')
        # print package information including time delivered
        else:
            package_list.search(package_id).display_packages()
    # lookup function for remaining packages
    else:
        # show packages at hub if not yet loaded on truck
        if time < package_list.search(package_id).time_loaded:
            print(str(package_list.search(package_id)) + ', Status: At hub')
        # show packages as en route if on truck but not delivered
        elif package_list.search(package_id).time_loaded < time < package_list.search(package_id).time_delivered:
            print(str(package_list.search(package_id)) + ', Status: En route')
        # print package information including time delivered
        else:
            package_list.search(package_id).display_packages()


# function to deliver packages
# finds nearest neighbor, calculates and stores delivery time
# continues until all packages are delivered
# stores return time and miles traveled
def deliver_packages(truck):
    # set time loaded for all packages on truck
    for package_id in truck.loaded_packages:
        package_list.search(package_id).time_loaded = truck.start_time
    # set starting location as WGUPS hub
    current_location = addresses[0]
    # initialize current time with truck start time
    truck.current_time = truck.start_time
    # start of nearest neighbor algorithm
    while len(truck.loaded_packages) > 0:
        # initialize variables
        shortest_distance = float('inf')
        next_location = current_location
        next_package = -1
        # iterate through all packages remaining on truck to find shortest delivery distance
        # update next location/package if shorter distance found
        for package_id in truck.loaded_packages:
            if float(distance_table[addresses.index(current_location)][
                         addresses.index(package_list.search(package_id).address)]) < shortest_distance:
                shortest_distance = float(distance_table[addresses.index(current_location)][
                                              addresses.index(package_list.search(package_id).address)])
                next_location = addresses[addresses.index(package_list.search(package_id).address)]
                next_package = package_id
        # increment distance traveled by distance to deliver next package
        truck.distance_traveled += shortest_distance
        # calculate delivery time
        truck.current_time = calc_time(truck.current_time, shortest_distance)
        # remove package from truck
        truck.deliver_package(next_package)
        # store delivery time in package object
        package_list.search(next_package).time_delivered = truck.current_time
        # update starting location
        current_location = next_location
    # return to hub and calculate final mileage and return time
    shortest_distance = float(distance_table[addresses.index(current_location)][0])
    truck.distance_traveled += shortest_distance
    truck.current_time = calc_time(truck.current_time, shortest_distance)
    truck.hub_return_time = truck.current_time


# function to display the menu for the user interface
def display_menu():
    print('\n\nWGUPS Package Tracking')
    print('***********************')
    print('1. View status of all packages and total distance traveled')
    print('2. View status of individual package by ID')
    print('3. View status of all packages by time')
    print('4. View individual package status by time')
    print('5. Exit')
    print('***********************')


# INITIALIZE PROGRAM
# set up trucks and calculate delivery routes
# set date to today's date
current_date = datetime.datetime.now()
# creat truck objects to be loaded
truck1 = Truck()
truck2 = Truck()
truck3 = Truck()
# manually load packages into trucks
truck1.loaded_packages = [1, 7, 8, 13, 14, 15, 16, 20, 21, 29, 30, 31, 34, 37, 39]
truck2.loaded_packages = [2, 3, 4, 5, 6, 18, 25, 26, 28, 32, 33, 36, 38, 40]
truck3.loaded_packages = [9, 10, 11, 12, 17, 19, 22, 23, 24, 27, 35]
# manually set delivery start time per truck
truck1.start_time = current_date.replace(hour=8, minute=0, second=0, microsecond=0)
truck2.start_time = current_date.replace(hour=9, minute=5, second=0, microsecond=0)
truck3.start_time = current_date.replace(hour=10, minute=20, second=0, microsecond=0)

# create hash table to store packages
package_list = hash.ChainingHashTable()
# create distance table to be populated by csv
distance_table = []
# create address list
addresses = []


# load csv files to program
import_packages('../data/packages.csv')
import_distance_table('../data/distance_table.csv')
import_addresses('../data/addresses.csv')


# deliver all packages and calculates total distance traveled
deliver_packages(truck1)
deliver_packages(truck2)
deliver_packages(truck3)
total_distance_traveled = truck1.distance_traveled + truck2.distance_traveled + truck3.distance_traveled


# MAIN PROGRAM
if __name__ == '__main__':
    # display menu options and get user input
    display_menu()
    user_input = input('Enter your choice: ')
    # while loop asks for user input until user chooses to exit program
    while user_input != '5':
        # option 1 to print status of all packages
        if user_input == '1':
            for package in range(1, 41):
                package_list.search(package).display_packages()
            print(f'Total distance traveled: {total_distance_traveled:.1f}')
            # pause program until input given to continue
            input('Press Enter to continue')
            # display menu and get user input
            display_menu()
            user_input = input('Enter your choice: ')
        # option 2 to print status of individual package
        elif user_input == '2':
            # get package ID from input
            # give error if package ID from input is not an integer or not found
            try:
                user_choice = int(input('Enter package ID: '))
                # print package details if package ID is in table
                if package_list.search(user_choice) is not None:
                    package_list.search(user_choice).display_packages()
                else:
                    print('Package ID not found')
            except ValueError:
                print('Invalid package ID')
            # pause until input given
            input('Press Enter to continue')
            # display menu and get user input
            display_menu()
            user_input = input('Enter your choice: ')
        # option 3 to print status of all packages at specified time
        elif user_input == '3':
            # get desired time in hours and minutes
            # try statement, causes exception if input hour or minutes are outside clock bounds
            try:
                user_hour = int(input('Enter hour: '))
                user_minute = int(input('Enter minute: '))
                # print status of all packages at specified time
                for package in range(1, 41):
                    lookup_time = current_date.replace(hour=user_hour, minute=user_minute)
                    lookup_package(package, lookup_time)
            except ValueError as val:
                print(f'Invalid time: {val}')
            # pause until input given
            input('Press Enter to continue')
            # display menu and get user input
            display_menu()
            user_input = input('Enter your choice: ')
        # option 4 to print status of specified package at specified time
        elif user_input == '4':
            # get package ID from input, give error if not an integer
            try:
                user_choice = int(input('Enter package ID: '))
                # if package ID is valid, get hour and minute from input, give error if time not valid
                if package_list.search(user_choice) is not None:
                    try:
                        user_hour = int(input('Enter hour: '))
                        user_minute = int(input('Enter minute: '))
                        lookup_time = current_date.replace(hour=user_hour, minute=user_minute)
                        lookup_package(user_choice, lookup_time)
                    except ValueError as val:
                        print(f'Invalid time: {val}')
                else:
                    print('Package ID not found')
            except ValueError:
                print('Invalid package ID')
            # pause until input given
            input('Press Enter to continue')
            # display menu and get user input
            display_menu()
            user_input = input('Enter your choice: ')
        # exit program
        elif user_input == '5':
            exit()
        # if input is not integer from 1-5 give error and get new input
        else:
            print('Invalid selection, please try again.')
            user_input = input('Enter your choice: ')
