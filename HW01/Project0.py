"""1.Define an abstract base class for a data storage system, with methods like save(), load(), and delete().
Implement concrete subclasses representing different storage systems, such as file-based storage and database storage,
ensuring they adhere to the abstract interface."""


# Abstract base class for a data storage system
from abc import ABC, abstractmethod

class DataStorageSystem(ABC):
    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def delete(self):
        pass

# Concrete subclasses representing different storage systems
class FileStorage(DataStorageSystem):
    def save(self):
        print("Saving to file")

    def load(self):
        print("Loading from file")

    def delete(self):
        print("Deleting from file")

class DatabaseStorage(DataStorageSystem):
    def save(self):
        print("Saving to database")

    def load(self):
        print("Loading from database")

    def delete(self):
        print("Deleting from database")


"""2.Implement a metaclass that automatically adds type checking to class attributes. Define a class with attributes of different types,
and observe how the metaclass enforces type checking during attribute assignment."""

# Metaclass that automatically adds type checking to class attributes
class TypeCheckingMeta(type):
    def __new__(cls, name, bases, attrs):
        attrs['__setattr__'] = TypeCheckingMeta.check_type_annotations
        return super().__new__(cls, name, bases, attrs)
    def check_type_annotations(self, attr, value):
        attr_type = self.__annotations__.get(attr)
        if attr_type and not isinstance(value, attr_type):
            raise TypeError(f"Invalid type. Expected {attr_type}, but got {type(value)}.")
        object.__setattr__(self, attr, value)
        
#Class with attributes of different types
class MyClass(metaclass=TypeCheckingMeta):
    x: int
    y: str
    z: list

# Testing the metaclass
obj = MyClass()
obj.x = 5
print(obj.x)  # Output: 5

obj.y = "Hello"
print(obj.y)  # Output: Hello

obj.z = [1, 2, 3]
print(obj.z)  # Output: [1, 2, 3]

# Type checking enforcement
obj.x = "Hello"  # Raises TypeError: Invalid type. Expected <class 'int'>, but got <class 'str'>.
obj.y = 123  # Raises TypeError: Invalid type. Expected <class 'str'>, but got <class 'int'>.
obj.z = 1  # Raises TypeError: Invalid type. Expected <class 'list'>, but got <class 'int'>.


"""3.Implement a hierarchy of classes representing different types of vehicles, such as cars, motorcycles, and bicycles.
Demonstrate inheritance, method overriding, and polymorphism by implementing common methods and attributes specific to each vehicle type."""
class Vehicle:
    def __init__(self, name, color, price):
        self.name = name
        self.color = color
        self.price = price

    def drive(self):
        print(f"Driving {self.name}")

class Car(Vehicle):
    def __init__(self, name, color, price, model):
        super().__init__(name, color, price)
        self.model = model

    def drive(self):
        print(f"Driving {self.name} {self.model}")

class Motorcycle(Vehicle):
    def __init__(self, name, color, price, model):
        super().__init__(name, color, price)
        self.model = model

    def drive(self):
        print(f"Driving {self.name} {self.model}")

class Bicycle(Vehicle):
    def __init__(self, name, color, price, model):
        super().__init__(name, color, price)
        self.model = model

    def drive(self):
        print(f"Driving {self.name} {self.model}")

def test_drive(vehicle):
    vehicle.drive()

# Testing the hierarchy of classes
car = Car("BMW", "White", 50000, "X5")
motorcycle = Motorcycle("Honda", "Red", 10000, "CBR500R")
bicycle = Bicycle("Giant", "Black", 1500, "Talon 29")
car.drive() # Output: Driving BMW X5
motorcycle.drive() # Output: Driving Honda CBR500R
bicycle.drive() # Output: Driving Giant Talon 29
test_drive(car) # Output: Driving BMW X5
test_drive(motorcycle) # Output: Driving Honda CBR500R
test_drive(bicycle) # Output: Driving Giant Talon 29
