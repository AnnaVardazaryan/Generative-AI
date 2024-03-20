""" You are writing an inventory application for a budding tech guy who has a video channel featuring computer builds. Basically they have a pool of inventory, (for example 5 x AMD Ryzen 2-2700 CPUs) that they use for builds. When they take a CPU from the pool. They will indicate this using the object that tracks that specific type of CPU. They may also purchase additional CPUs, or retire some (because they overclocked it too much and burnt them out).
Technically we would want a database to back all this data, but here we’re just going to build classes we’ll use while our program is running and not worry about retrieving or saving the state of the inventory.
The base class is going to be a general Resource. This class should provide functionality common to all the actual resources (CPU, GPU, Memory, HDD, SSD) - for the exercise we’re only going to implement CPU, HDD and SSD.

Input and Output examples
It should provide this at minimum:
 name : user-friendly name of resource instance(e.g. Intel Core i9-9900K)
 manufacturer : resource instance manufacturer(e.g. Nvidia)
 total : inventory total(how many are in the inventory pool)
 allocated : number allocated(how many already in use)
 str representation that just returns the resource name
 a mode detailed repr implementation
 claim(m) : method to take n resources from the pool(as long as inventory os available)
 freeup(n) : method to return n resources to the pool(e.g disassembled some builds)
 died(n) : method to return and permanently remove inventory from the pool(e.g. They broke something) - as long as total available allows it
 purchased(n) : method to add inventory to the pool(e.g. They purchased a new CPU)
 Category - computed property that returns a lowercase version of the class name

Hints
 For the CPU class:
 cores (e.g. 8)The SSD class extends Storage and has these additional properties:
 interface (e.g. PCIe NMVe 3.0 x4)
 socket (e.g. AM4)
 power_watts (e.g. 94)
 For the HDD and SSD classes, we’re going to create an intermediate class called Storage with these additional properties:
 capacity_GB (e.g. 120)
 The HDD class extends Storage and has these additional properties:
 size (e.g. 2.5")
 rpm (e.g. 7000)
 The SSD class extends Storage and has these additional properties:
 interface (e.g. PCIe NMVe 3.0 x4)
 For all your classes, implement a full constructor that can be used to initialize all the properties, some form of validation on numeric types, as well customized repr as you see fit.
 For the total and allocated values in the Resource init, think of the arguments there as the current total and allocated counts. Those total and allocated attributes should be private read-only properties, but they are modifiable through the various methods such as claim, return, died, purchased. Other attributes like name, manufacturer_name, etc should be read-only."""


class Resource:
    def __init__(self, name, manufacturer, total, allocated):
        self._name = name
        self._manufacturer = manufacturer
        self._total = total
        self._allocated = allocated

    @property
    def name(self):
        return self._name

    @property
    def manufacturer(self):
        return self._manufacturer

    @property
    def total(self):
        return self._total

    @property
    def allocated(self):
        return self._allocated

    def __str__(self):
        return self._name

    def __repr__(self):
        return f"Resource(name={self._name}, manufacturer={self._manufacturer}, total={self._total}, allocated={self._allocated})"

    def claim(self, n):
        if self._total - self._allocated >= n:
            self._allocated += n
        else:
            return "Not enough resources"

    def freeup(self, n):
        if self._allocated >= n:
            self._allocated -= n
        else:
            return "Not enough resources"

    def died(self, n):
        if self._total >= n:
            self._total -= n
        else:
            return "Not enough resources"

    def purchased(self, n):
        self._total += n

    @property
    def category(self):
        return self.__class__.__name__.lower()

class Storage(Resource):
    def __init__(self, name, manufacturer, total, allocated, capacity_GB):
        super().__init__(name, manufacturer, total, allocated)
        self._capacity_GB = capacity_GB

    @property
    def capacity_GB(self):
        return self._capacity_GB

    def __repr__(self):
        return f"Storage(name={self._name}, manufacturer={self._manufacturer}, total={self._total}, allocated={self._allocated}, capacity_GB={self._capacity_GB})"

class HDD(Storage):
    def __init__(self, name, manufacturer, total, allocated, capacity_GB, size, rpm):
        super().__init__(name, manufacturer, total, allocated, capacity_GB)
        self._size = size
        self._rpm = rpm

    @property
    def size(self):
        return self._size

    @property
    def rpm(self):
        return self._rpm

    def __repr__(self):
        return f"HDD(name={self._name}, manufacturer={self._manufacturer}, total={self._total}, allocated={self._allocated}, capacity_GB={self._capacity_GB}, size={self._size}, rpm={self._rpm})"

class SSD(Storage):
    def __init__(self, name, manufacturer, total, allocated, capacity_GB, interface):
        super().__init__(name, manufacturer, total, allocated, capacity_GB)
        self._interface = interface

    @property
    def interface(self):
        return self._interface

    def __repr__(self):
        return f"SSD(name={self._name}, manufacturer={self._manufacturer}, total={self._total}, allocated={self._allocated}, capacity_GB={self._capacity_GB}, interface={self._interface})"

class CPU(Resource):
    def __init__(self, name, manufacturer, total, allocated, cores, interface, socket, power_watts):
        super().__init__(name, manufacturer, total, allocated)
        self._cores = cores
        self._interface = interface
        self._socket = socket
        self._power_watts = power_watts

    @property
    def cores(self):
        return self._cores

    def __repr__(self):
        return f"CPU(name={self._name}, manufacturer={self._manufacturer}, total={self._total}, allocated={self._allocated}, cores={self._cores})"

# Testing the classes
cpu = CPU("Intel Core i9-9900K", "Intel", 10, 5, 8, "PCIe NMVe 3.0 x4", "AM4", 94)
print(cpu)      # Intel Core i9-9900K
print(cpu.category)     # cpu
print(cpu.cores)        # 8
print(cpu.total)        # 10
print(cpu.allocated)  # 5
print(cpu.claim(2))     # None
print(cpu.freeup(1))        # None
print(cpu.died(1))      # None
print(cpu.purchased(1))     # None
print(cpu.total)        # 10
print(cpu.allocated)        # 6

hdd = HDD("Seagate BarraCuda", "Seagate", 10, 5, 120, "2.5\"", 7000)
print(hdd)      # Seagate BarraCuda
print(hdd.category)     # hdd
print(hdd.size)     # 2.5"
print(hdd.rpm)      # 7000
print(hdd.capacity_GB)      # 120


ssd = SSD("Samsung 970 EVO", "Samsung", 10, 5, 120, "PCIe NMVe 3.0 x4")
print(ssd)      # Samsung 970 EVO
print(ssd.category)     # ssd
print(ssd.interface)        # PCIe NMVe 3.0 x4
print(ssd.capacity_GB)      # 120

