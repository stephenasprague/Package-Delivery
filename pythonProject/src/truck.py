class Truck:

    # initialize truck object, current location is WGUPS hub
    def __init__(self):
        self.loaded_packages = []
        self.current_location = '4001 South 700 East'
        self.start_time = None
        self.current_time = None
        self.hub_return_time = None
        self.distance_traveled = 0.0

    # defines string function, returns string with list of packages loaded on truck
    def __str__(self):
        return f'Loaded packages: {self.loaded_packages}'

    # define function to remove packages as they are delivered
    def deliver_package(self, package_id):
        self.loaded_packages.remove(package_id)

