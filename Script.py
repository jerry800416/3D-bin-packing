import random
import time
import cProfile
import pstats
import logging
import sys
from py3dbp.main import Packer, Bin, Item, Painter, set_external_logger  # Import from external module


def setup_logger(name, level=logging.DEBUG):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

logger = setup_logger(__name__)

logger.info('Logger successfully configured in the main module.')

# Pass the logger to the external module
set_external_logger(logger)

# Create an instance of the profiler
# profiler = cProfile.Profile()
# Enable the profiler, execute the function, and disable the profiler
# profiler.enable()

pallet_types = {
    "Heavy": {
        "Quarter Pallet": {"Max Length": 120, "Max Width": 100, "Max Height": 100, "Max Weight": 300, "Priority_pallet_choice": 2, "Color": "red"},
        "Half Pallet": {"Max Length": 120, "Max Width": 100, "Max Height": 150, "Max Weight": 600, "Priority_pallet_choice": 5, "Color": "orange"},
        "Full Pallet": {"Max Length": 120, "Max Width": 100, "Max Height": 240, "Max Weight": 1200, "Priority_pallet_choice": 7, "Color": "yellow"},
    },
    "Light": {
        "Light Pallet": {"Max Length": 120, "Max Width": 100, "Max Height": 240, "Max Weight": 750, "Priority_pallet_choice": 6, "Color": "green"},
        "Extra Light Pallet": {"Max Length": 120, "Max Width": 100, "Max Height": 150, "Max Weight": 450, "Priority_pallet_choice": 3, "Color": "olive"},
        "Ultra Light Pallet": {"Max Length": 120, "Max Width": 100, "Max Height": 240, "Max Weight": 350, "Priority_pallet_choice": 4, "Color": "blue"},
        "Mini Quarter": {"Max Length": 120, "Max Width": 100, "Max Height": 60, "Max Weight": 150, "Priority_pallet_choice": 1, "Color": "pink"},
    },
    "Oversized": {
        "Custom Pallet": {"Max Length": 1300, "Max Width": 240, "Max Height": 240, "Max Weight": 22000, "Priority_pallet_choice": 8, "Color": "brown"},
    }
}

pallet_dimensions = {
    "EUR": {"Length": 120, "Width": 80, "Height": 15, "Weight": 25},
    "ISO": {"Length": 120, "Width": 100, "Height": 15, "Weight": 28},
    "120x120": {"Length": 120, "Width": 120, "Height": 15, "Weight": 30},
}

all_subtypes = []
for type_, subtype in pallet_types.items():
    for subtype_name, dimensions in subtype.items():
        all_subtypes.append((type_, subtype_name, dimensions))

sorted_all_types = sorted(all_subtypes, key=lambda x: x[2]["Priority_pallet_choice"], reverse=True)

min_possible_height = sorted(pallet_dimensions.values(), key=lambda x: x["Height"])[0]["Height"]
# print(min_possible_height)
min_possible_weight = sorted(pallet_dimensions.values(), key=lambda x: x["Weight"])[0]["Weight"]
# print(min_possible_weight)

class Pallet:
    def __init__(self, type_):
        self.type = type_
        self.length = pallet_dimensions[type_]["Length"]
        self.width = pallet_dimensions[type_]["Width"]
        self.height = pallet_dimensions[type_]["Height"]
        self.weight = pallet_dimensions[type_]["Weight"]


class Package:
    def __init__(self, length=120, width=80, height=240, weight=1200, pallet=None, name="ERROR: No Name"):
        self.pallet = pallet
        # print(height, {self.pallet.height if self.pallet is not None else 0})
        self.height = height - (self.pallet.height if self.pallet is not None else 0)
        self.weight = weight - (self.pallet.weight if self.pallet is not None else 0)
        self.length, self.width = max(length, width), min(length, width)
        self.volume = self.length * self.width * self.height
        self.density = self.weight / self.volume  # kg/cm^3
        self.name = name
        self.assign_pallet_to_package()

    def assign_pallet_to_package(self):
        if self.pallet is None:
            # print(f"Package dimensions: Length={self.length}, Width={self.width}, Height={self.height}, Weight={self.weight}")
            # Reorder pallets by width in ascending order
            pallets = sorted(pallet_dimensions, key=lambda x: pallet_dimensions[x]["Width"], reverse=True)
            # print(pallets)
            pallets_class = [Pallet(pallet) for pallet in pallets]

            # Find the pallet with minimum width sufficient for the package (starting from the largest)
            for pallet in pallets_class:
                if pallet.width >= self.width:
                    self.pallet = pallet

            # If no pallet is sufficient, assign the largest pallet
            if self.pallet is None:
                self.pallet = pallets_class[-1]

            # print(f"Package {self.name} with width {self.width} assigned to pallet {self.pallet.type}.")

            # print(f"Package dimensions: Length={self.length}, Width={self.width}, Height={self.height}, Weight={self.weight}")
            # Ensure package dimensions


class PalletStack:
    def __init__(self, package, bay=None, assigned_truck=None, priority=5, stackable=True, stack_index=1):
        self.pallet = package.pallet
        self.stack_index = stack_index
        self.stackable = stackable
        self.length = max(package.length, self.pallet.length)
        self.width = max(package.width, self.pallet.width)
        self.height = package.height + self.pallet.height
        self.weight = package.weight + self.pallet.weight
        self.volume = self.length * self.width * self.height
        self.density = self.weight / self.volume  # kg/cm^3
        self.name = package.name
        self.position = None  # Added to track the position of the pallet stack in the truck
        self.subtype = None
        self.shape = "cube"
        self.priority = priority
        self.color = None
        self.assigned_truck = assigned_truck
        self.bay = bay
        self.load_capacity = self.calculate_dynamic_stackability()  # Call the method to calculate the dynamic load-bearing capacity
        self.assign_subtype_to_pallet_stack()  # Call the method to assign the pallet stack type
        self.version_item = Item(item_id=self.name, item_name=self.subtype, typeof=self.shape, WHD=(self.width, self.length, self.height), weight=self.weight, priority_level=self.priority, loadbear=self.load_capacity, updown=False, color=self.color, assigned_bin=(self.assigned_truck.version_bin if self.assigned_truck is not None else None))

    def update_version_item(self):
        self.version_item = Item(item_id=self.name, item_name=self.subtype, typeof=self.shape, WHD=(self.width, self.length, self.height), weight=self.weight, priority_level=self.priority, loadbear=self.load_capacity, updown=False, color=self.color, assigned_bin=(self.assigned_truck.version_bin if self.assigned_truck is not None else None))

    def calculate_dynamic_stackability(self):
        if self.stackable:
            # Calculate the load-bearing capacity based on weight and stackability index
            return self.weight * self.stack_index
        else:
            return 0

    def assign_subtype_to_pallet_stack(self):
        if self.width > self.length:
            self.length, self.width = self.width, self.length
            print(f"Pallet stack {self.name} with width greater than length. Swapping dimensions.")

        sorted_all_types_copy = sorted_all_types[:]
        for type_, subtype, dimensions in sorted_all_types_copy:
            if (
                self.length <= dimensions["Max Length"]
                and self.width <= dimensions["Max Width"]
                and self.height <= dimensions["Max Height"]
                and self.weight <= dimensions["Max Weight"]
            ):
                self.subtype = subtype  # Assign the pallet stack type to the attribute
                self.color = dimensions["Color"]  # Assign the color to the attribute
                # print(f"Assigned type: {type_}, Assigned color: {self.color}")
                self.update_version_item()
                break
        # print(f"Pallet stack {self.name} assigned as {self.subtype}")
        # print(f"Pallet stack dimensions: Length={self.length}, Width={self.width}, Height={self.height}, Weight={self.weight}")


class Truck:
    def __init__(self, length=1300, width=240, height=240, max_weight=24000, license_plate="AA000AA", load_method="Side", movable_existing_pallets=True, bay=None):
        self.length = length  # in cm
        self.width = width  # in cm
        self.height = height  # in cm
        self.max_weight = max_weight  # in kg
        self.loaded_pallets = []
        self.volume = self.length * self.width * self.height
        self.current_weight = 0
        self.current_volume = 0
        self.license_plate = license_plate
        self.load_method = load_method
        self.bay = bay
        self.existing_pallets = []
        self.movable_existing_pallets = movable_existing_pallets
        self.version_bin = Bin(bin_id=self.license_plate, WHD=((self.width, self.length, self.height)), max_weight=self.max_weight, corner=0, put_type=0)
        self.bay.packer.addBin(self.version_bin)

    def consider_existing_pallets(self, initial_pallets):
        global packages  # Ensure 'packages' is accessible

        for pallet in self.existing_pallets:
            # print(pallet.name)
            pallet.priority = 1
            # position=pallet.position POSITION NOT YET MODIFIABLE TO BE IMPLEMENTED

            while not self.check_truck_compatibility(pallet):
                print(f"ERROR: The existing pallet {pallet.name} is not compatible with the truck {self.license_plate} on which it is loaded.")
                print(f"Pallet dimensions are: Length={pallet.length}, Width={pallet.width}, Height={pallet.height}, Weight={pallet.weight}, Pallet Type={pallet.pallet.type}.")
                print(f"Truck dimensions are: Length={self.length}, Width={self.width}, Height={self.height}, Weight={self.max_weight}.")
                print(f"Please re-enter the dimensions of pallet {pallet.name}.")
                length_pallet = int(get_value("Length (if empty 120): ", 120, lambda x: x.isdigit()))
                width_pallet = int(get_value("Width (if empty 80): ", 80, lambda x: x.isdigit()))
                height_pallet = int(get_value("Height (if empty 240): ", 240, lambda x: x.isdigit()))
                weight_pallet = int(get_value("Weight (if empty 1200): ", 1200, lambda x: x.isdigit()))
                pallet_type = get_value("Pallet type (EUR/ISO/120x120) (if empty automatic): ", None, lambda x: x in ["EUR", "ISO", "120x120", ""])
                pallet_included = get_value("Is pallet included in measurements? (yes/no) (if empty yes): ", "yes", lambda x: x.lower() in ["yes", "no", ""]).lower()
                for package in packages:
                    if package.name == pallet.name:
                        package.length = length_pallet
                        package.width = width_pallet
                        package.pallet = Pallet(pallet_type) if pallet_type else None
                        package.height = height_pallet - ((package.pallet.height if package.pallet is not None else min_possible_height) if pallet_included == "yes" else 0)
                        package.weight = weight_pallet - ((package.pallet.weight if package.pallet is not None else min_possible_weight) if pallet_included == "yes" else 0)
                        package.volume = package.length * package.width * package.height
                        package.density = package.weight / package.volume  # kg/cm^3
                        package.assign_pallet_to_package()
                        pallet.pallet = package.pallet
                        pallet.length = max(package.length, package.pallet.length)
                        pallet.width = max(package.width, package.pallet.width)
                        pallet.height = package.height + pallet.pallet.height
                        pallet.weight = package.weight + pallet.pallet.weight
                        pallet.volume = pallet.length * pallet.width * pallet.height
                        pallet.density = pallet.weight / pallet.volume  # kg/cm^3
                        pallet.load_capacity = pallet.calculate_dynamic_stackability()

            pallet.assign_subtype_to_pallet_stack()

            # Attempt to load the pallet
            if pallet not in self.loaded_pallets:
                if pallet.version_item not in self.bay.packer.items:
                    self.bay.packer.addItem(pallet.version_item)
                    print(f"Existing pallet {pallet.name} added to the packer of bay {pallet.assigned_truck.bay.number}. Confirmed.")
                    if pallet in initial_pallets:
                        initial_pallets.remove(pallet)
                else:
                    print(f"ERROR: The pallet {pallet.name} is already present in both truck {self.license_plate} and the packer of bay {self.bay.number}.")
            else:
                print(f"ERROR: The pallet {pallet.name} is already present among the loaded pallets of truck {self.license_plate}.")

    def check_truck_compatibility(self, pallet):
        if pallet.length <= self.length and \
           pallet.width <= self.width and \
           pallet.height <= self.height and \
           pallet.weight <= self.max_weight:
            return True
        else:
            # print(f"Concern: The pallet {pallet.name} cannot be loaded on truck {self.license_plate}.")
            return False


class Bay:
    def __init__(self, number, length, width, height):
        self.number = number
        self.length = length
        self.width = width
        self.height = height
        self.pallets_in_bay = []
        self.volume = self.length * self.width * self.height
        self.current_volume = sum([b.volume for b in self.pallets_in_bay])
        self.packer = Packer(self.number)

    def add_pallet_to_bay(self, pallet_to_add, initial_pallets):
        if self.check_compatibility_with_bay(pallet_to_add):
            if pallet_to_add not in self.pallets_in_bay:
                self.pallets_in_bay.append(pallet_to_add)
                if pallet_to_add in initial_pallets:
                    initial_pallets.remove(pallet_to_add)
            else:
                print(f"ERROR: The pallet {pallet_to_add.name} is already present in bay {self.number}.")
        else:
            print(f"The pallet {pallet_to_add.name} cannot be loaded into bay {self.number}. Pallet discarded. Length {pallet_to_add.length} instead of {self.length}, width {pallet_to_add.width} instead of {self.width}, height {pallet_to_add.height} instead of {self.height}")
            pallet_to_add.bay = None

    def check_compatibility_with_bay(self, pallet):
        if pallet.length <= self.length and \
           pallet.width <= self.width and \
           pallet.height <= self.height:
            return True
        else:
            print(f"ERROR: The pallet {pallet.name} cannot be loaded into bay {self.number}.")
            return False

    def load_onto_trucks(self, initial_pallets, trucks_in_this_bay, stability_param=0.9):
        # Add new pallets to the bay packer
        for truck in trucks_in_this_bay:
            truck.consider_existing_pallets(initial_pallets)
            print(f"Truck {truck.license_plate} with {len(truck.existing_pallets)} existing pallets + {len(truck.loaded_pallets)} already loaded.")
            for pallet in self.pallets_in_bay:
                # Attempt to load the pallet
                if truck.check_truck_compatibility(pallet):
                    if pallet.name not in [item.item_id for item in self.packer.items]:
                        self.packer.addItem(pallet.version_item)
                        # print(f"Pallet {pallet.name} added to the packer of bay {self.number}.")
                    # else:
                        # print(f"ERROR: The pallet {pallet.name} is already present in the packer of bay {self.number}.")
                else:
                    print(f"Pallet {pallet.name} not compatible with truck {truck.license_plate} so left in bay")

        print(f"List of items in the packer of bay {self.number} before packing:")
        for item in self.packer.items:
            print(f"Item {item.item_id} added to packer of bay {self.number}")

        # Execute packing only for pallets without assigned position
        self.packer.pack(
            bigger_first=True,                 # bigger item first.
            fix_point=True,                    # fix item floating problem.
            # binding=None,                      # make a set of items.
            distribute_items=True,             # If multiple bins, to distribute or not.
            check_stable=True,                 # check stability on item.
            support_surface_ratio=stability_param,        # set support surface ratio.
            number_of_decimals=0
        )

        # Assign pallets to trucks
        for truck in trucks_in_this_bay:
            for bin in self.packer.bins:
                if bin.bin_id == truck.license_plate:
                    list_copy = (self.pallets_in_bay + truck.existing_pallets)[:]
                    for pallet in list_copy:
                        for item in bin.items:
                            if item.item_id == pallet.name:
                                pallet.position = item.position  # Update the position of the pallet
                                pallet.assigned_truck = truck  # Update the assigned truck of the pallet
                                if pallet not in truck.loaded_pallets:
                                    truck.loaded_pallets.append(pallet)  # Add the pallet to the list of pallets loaded on the truck
                                # print(f"Pallet {pallet.name} loaded on truck {truck.license_plate} at position x: {pallet.position[0]}, y: {pallet.position[1]}, z: {pallet.position[2]}")
                                pallet.bay = None  # Remove the bay from the pallet
                                truck.current_weight += item.weight  # Update the current weight of the truck
                                truck.current_volume += item.getVolume()  # Update the current volume of the truck
                                if pallet in initial_pallets:
                                    initial_pallets.remove(pallet)  # Remove pallet from initial_pallets as it is placed on a truck
                                if pallet in self.pallets_in_bay:
                                    self.pallets_in_bay.remove(pallet)  # Remove the pallet from the bay (if it was in this list)
                                if pallet in truck.existing_pallets:
                                    truck.existing_pallets.remove(pallet)


def distribute_pallets_to_bays(pallets_to_distribute):
    pallets_to_distribute_copy = pallets_to_distribute[:]
    for pallet in pallets_to_distribute_copy:
        if pallet.bay:
            pallet.bay.add_pallet_to_bay(pallet, pallets_to_distribute)
            if pallet.assigned_truck is not None and not pallet.assigned_truck.version_bin.items:
                pallet.priority = 2
                # If it has an assigned bay and also an assigned truck, the truck will load it during packing
        else:
            if pallet.assigned_truck is None:
                print(f"Concern: The pallet {pallet.name} is not assigned to any truck and to any bay.")


def get_value(message, default_value, validation):
    while True:
        input_value = input(message)
        if input_value == "":
            return default_value
        if validation(input_value):
            return input_value
        else:
            print("Invalid value. Please try again.")


# Initialize bays
bays = []
num_bays = 2  # random.randint(2, 3)
for i in range(num_bays):
    bay = Bay(number=i, length=1300, width=240, height=480)
    bays.append(bay)

# Initialize trucks
trucks = []
num_trucks = random.randint(7, 8)
for _ in range(num_trucks):
    truck = Truck(license_plate=f"AA{_}", bay=random.choice(bays))
    trucks.append(truck)

# Create packages
packages = []
for _ in range(50):
    length = random.randint(20, 150)
    width = random.randint(20, 150)
    height = random.randint(30, 245)
    volume = length * width * height
    weight = int(volume * random.uniform(0.0001, 0.0005))
    pallet = Pallet(random.choice(["EUR", "ISO", "120x120"]))
    name = f"{_}"
    package = Package(length=length,
                      width=width,
                      height=height,
                      weight=weight,
                      pallet=pallet,
                      name=name)
    packages.append(package)

# Transform packages into pallet stacks
initial_pallet_stacks = []
for package in packages:
    bay = random.choice(bays)
    # stackable = random.choice([True, False])
    priority = random.randint(3, 5)
    pallet_stack = PalletStack(package=package, bay=bay, priority=priority)  # stackable=stackable
    stack_index = random.random()   # random between zero and 1
    if pallet_stack.subtype is not None:  # Check if a valid type was assigned
        initial_pallet_stacks.append(pallet_stack)
    else:
        initial_pallet_stacks.append(pallet_stack)  # For testing, but to be removed later
        # print(f"Pallet stack discarded (theoretically, not now in test): Pallet stack {pallet_stack.name} with Length={pallet_stack.length}, Width={pallet_stack.width}, Height={pallet_stack.height}, Weight={pallet_stack.weight} cannot be assigned to any truck.")

# Assign some of the newly created pallet stacks to some trucks as if they had already been loaded onto them
i = 0  # Initialize i
for truck in trucks:
    i += 3
    for pallet_stack in initial_pallet_stacks[i-4:i-1]:
        pallet_stack.assigned_truck = truck
        pallet_stack.bay = None
        truck.existing_pallets.append(pallet_stack)
        # pallet_stack.position = (0, 0, 0)
        # print(f"Pallet stack {pallet_stack.name} assigned to truck {truck.license_plate}.")

# Distribute the pallet stacks into bays
distribute_pallets_to_bays(pallets_to_distribute=initial_pallet_stacks)

parametro_stabilità = 0.9

for bay in bays:
    trucks_in_this_bay = [truck for truck in trucks if truck.bay == bay]
    print(f"Trucks for bay {bay.number}: {[truck.license_plate for truck in trucks_in_this_bay]}")
    # Load the packages onto trucks
    bay.load_onto_trucks(initial_pallets=initial_pallet_stacks, trucks_in_this_bay=trucks_in_this_bay, stability_param=parametro_stabilità)

    # Print the loaded pallet stacks
    print(f"**Pallet stacks loaded from bay {bay.number}**")
    for truck in trucks_in_this_bay:
        print(f"- On truck {truck.license_plate}:")
        for truck_bin in bay.packer.bins:
            if truck_bin.bin_id == truck.license_plate:
                # print(truck.loaded_pallets)
                for pallet_stack in truck.loaded_pallets:
                    print(f"Pallet stack {pallet_stack.name} loaded on truck {truck.license_plate} at position x: {pallet_stack.position[0]}, y: {pallet_stack.position[1]}, z: {pallet_stack.position[2]}")

    print("Remaining in bay:")
    for pallet_stack in bay.pallets_in_bay:
        i = 0
        for truck in trucks_in_this_bay:
            i += 1
            if truck.check_truck_compatibility(pallet_stack):
                print(f"Pallet stack {pallet_stack.name} remained in bay because trucks are full. Acceptable dimensions.")
                break
            if i == len(trucks_in_this_bay):
                print(f"Pallet stack {pallet_stack.name} remained in bay but NOT TRANSPORTABLE. Dimensions: Length {pallet_stack.length}, Width {pallet_stack.width}, Height {pallet_stack.height}")

    for pallet_stack in initial_pallet_stacks:
        if pallet_stack.bay == bay:
            i = 0
            for truck in trucks_in_this_bay:
                i += 1
                if truck.check_truck_compatibility(pallet_stack):
                    print(f"ERROR: Pallet stack {pallet_stack.name} assigned to this bay ({pallet_stack.bay.number}) but never entered bay. Transportable by at least one truck.")
                    break
                if i == len(trucks_in_this_bay):
                    print(f"Pallet stack {pallet_stack.name} assigned to this bay ({pallet_stack.bay.number}) but never entered bay. NOT TRANSPORTABLE. Dimensions: Length {pallet_stack.length}, Width {pallet_stack.width}, Height {pallet_stack.height}")

    print("***************************************************")
    for truck_bin in bay.packer.bins:
        print("**", truck_bin.string(), "**")
        print("***************************************************")
        print("FITTED ITEMS:")
        print("***************************************************")
        volume = truck_bin.width * truck_bin.height * truck_bin.depth
        volume_fitted_items = 0  # Total volume of fitted items
        for item in truck_bin.items:
            volume_fitted_items += int(item.width) * int(item.height) * int(item.depth)

        print('space utilization : {}%'.format(round(volume_fitted_items / int(volume) * 100, 2)))
        print('residual volume : ', int(volume) - volume_fitted_items)
        print("gravity distribution : ", truck_bin.gravity)
        print("***************************************************")

        # Draw results
        painter = Painter(truck_bin)
        fig = painter.plotBoxAndItems(
            title=truck_bin.bin_id,
            alpha=0.6,   # Transparency
            write_name=True,
            fontsize=10,
            alpha_proportional=True,
            top_face_proportional=True
        )

    print("***************************************************")
    print(f"UNFITTED ITEMS (with acceptable dimensions) in bay {bay.number}:")
    unfitted_names = ''
    volume_unfitted_items = 0  # Total volume of unfitted items
    for item in bay.packer.unfit_items:
        print("***************************************************")
        print("Pallet stack number : ", item.item_id)
        print('type : ', item.item_name)
        print("color : ", item.color)
        print("Width*Length*Height : ", str(item.width) + ' * ' + str(item.height) + ' * ' + str(item.depth))
        print("volume : ", int(item.width) * int(item.height) * int(item.depth))
        print("weight : ", int(item.weight))
        volume_unfitted_items += int(item.width) * int(item.height) * int(item.depth)
        unfitted_names += '{},'.format(item.item_id)
        print("***************************************************")
    print("***************************************************")
    # print(f'PALLET STACKS with acceptable dimensions NOT LOADED in BAY {bay.number}: ', unfitted_names)
    print(f'VOLUME of pallet stacks with acceptable dimensions NOT LOADED in BAY {bay.number}: ', volume_unfitted_items)

print("***************************************************")
print("***************************************************")
print("***************************************************")
print("***************************************************")
print("***************************************************")
print("***************************************************")
print("***************************************************")

# Creation of additional packages for packing 2
additional_packages = []
for _ in range(51, 60):
    length = random.randint(20, 150)
    width = random.randint(20, 150)
    height = random.randint(30, 245)
    volume = length * width * height
    weight = int(volume * random.uniform(0.0001, 0.0005))
    pallet = Pallet(random.choice(["EUR", "ISO", "120x120"]))
    name = f"{_}"
    package = Package(length=length,
                      width=width,
                      height=height,
                      weight=weight,
                      pallet=pallet,
                      name=name)
    additional_packages.append(package)
    print(f"Name of newly created additional package: {package.name}")

# Transform additional packages into additional pallet stacks
initial_pallet_stacks_v2 = []
for package in additional_packages:
    priority = random.randint(3, 5)
    pallet_stack = PalletStack(package=package, priority=priority, bay=trucks[0].bay)
    stack_index = random.random()   # random between zero and 1
    initial_pallet_stacks_v2.append(pallet_stack)

# Assign the newly created pallet stacks to truck 0
for pallet_stack in initial_pallet_stacks_v2:
    pallet_stack.assigned_truck = trucks[0]

distribute_pallets_to_bays(pallets_to_distribute=initial_pallet_stacks_v2)
trucks_in_this_bay_v2 = [truck for truck in trucks if truck.bay == trucks[0].bay]
trucks[0].bay.load_onto_trucks(initial_pallets=initial_pallet_stacks_v2, trucks_in_this_bay=trucks_in_this_bay_v2, stability_param=parametro_stabilità)

# Print the loaded pallet stacks on the truck
print("***************************************************")
truck_bin = trucks[0].version_bin
bay = trucks[0].bay
print("**", truck_bin.string(), "**")
print("***************************************************")
print("FITTED ITEMS:")
print("***************************************************")
volume = truck_bin.width * truck_bin.height * truck_bin.depth
volume_fitted_items = 0  # Total volume of fitted items
for item in truck_bin.items:
    volume_fitted_items += int(item.width) * int(item.height) * int(item.depth)

print('space utilization : {}%'.format(round(volume_fitted_items / int(volume) * 100, 2)))
print('residual volume : ', int(volume) - volume_fitted_items)
print("gravity distribution : ", truck_bin.gravity)
print("***************************************************")

# Draw results
painter = Painter(truck_bin)
fig = painter.plotBoxAndItems(
    title=truck_bin.bin_id,
    alpha=0.6,   # Transparency
    write_name=True,
    fontsize=10,
    alpha_proportional=True,
    top_face_proportional=True
)

print("***************************************************")
print(f"UNFITTED ITEMS (with acceptable dimensions) in bay {bay.number}:")
unfitted_names = ''
volume_unfitted_items = 0  # Total volume of unfitted items
for item in bay.packer.unfit_items:
    print("***************************************************")
    print("Pallet stack number : ", item.item_id)
    print('type : ', item.item_name)
    print("color : ", item.color)
    print("Width*Length*Height : ", str(item.width) + ' * ' + str(item.height) + ' * ' + str(item.depth))
    print("volume : ", int(item.width) * int(item.height) * int(item.depth))
    print("weight : ", int(item.weight))
    volume_unfitted_items += int(item.width) * int(item.height) * int(item.depth)
    unfitted_names += '{},'.format(item.item_id)
    print("***************************************************")
print("***************************************************")
print(f'VOLUME of pallet stacks with acceptable dimensions NOT LOADED in BAY {bay.number}: ', volume_unfitted_items)
