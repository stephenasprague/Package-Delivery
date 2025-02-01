class Package:

    # initialize package object
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, status):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.time_loaded = None
        self.time_delivered = None

    # define string function to return package details
    def __str__(self):
        return (f'Package ID: {self.package_id}, Address: {self.address}, City: {self.city},'
                f' Zip Code: {self.zip_code}, Weight: {self.weight}, Deadline: {self.deadline}')

    # function to display delivered packages
    def display_packages(self):
        print(f'Package ID: {self.package_id}, Address: {self.address}, City: {self.city},'
              f' Zip Code: {self.zip_code}, Weight: {self.weight}, Deadline: {self.deadline}, '
              f'Status: Delivered at {self.time_delivered.time()}')
