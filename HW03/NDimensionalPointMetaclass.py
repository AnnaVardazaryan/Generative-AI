"""In this programming exercise, you are provided with a boilerplate code for defining two classes, Point2D and Point3D,
representing points in a 2-dimensional and 3-dimensional space, respectively. The provided code uses special methods like
__init__, __eq__, __hash__, and properties to encapsulate the data and provide certain functionalities. However, the code is not generic,
and it involves some repetition.

Task is to refactor the provided code to make it more generic and DRY (Don’t Repeat Yourself) by using metaclasses.
Metaclasses allow you to create classes dynamically, enabling you to define common behaviors for multiple classes in an
elegant and efficient manner. Your refactored code should be able to generate N-dimensional point classes with the same
functionalities while minimizing duplication of code.

Hints
Analyze the provided Point2D and Point3D classes and identify the common functionalities that can be generalized for
N-dimensional points.
Create a custom metaclass called SlottedStruct that defines these common functionalities, such as initializing the
point’s coordinates, comparing points for equality, computing the hash, and generating string representations.
Modify the Point2D and Point3D classes to use the SlottedStruct metaclass instead of the current implementations.
Make sure the classes still function correctly after the changes.
Test your refactored code with various N-dimensional points (e.g., Point4D, Point5D) to verify that the generic
implementation works as expected.
"""

class Point2D:
    """Class representing a point in 2-dimensional space."""

    def __init__(self, x, y):
        """Initialize a Point2D object with x and y coordinates."""
        self._x = x
        self._y = y

    @property
    def x(self):
        """Get the x-coordinate of the point."""
        return self._x

    @property
    def y(self):
        """Get the y-coordinate of the point."""
        return self._y

    def __eq__(self, other):
        """Check if two Point2D objects are equal based on their coordinates."""
        return isinstance(other, Point2D) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):
        """Compute the hash value of the Point2D object based on its coordinates."""
        return hash((self.x, self.y))

    def __repr__(self):
        """Get the string representation of the Point2D object."""
        return f'Point2D({self.x}, {self.y})'

    def __str__(self):
        """Get the user-friendly string representation of the Point2D object."""
        return f'({self.x}, {self.y})'

class Point3D:
    """Class representing a point in 3-dimensional space."""

    def __init__(self, x, y, z):
        """Initialize a Point3D object with x, y, and z coordinates."""
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        """Get the x-coordinate of the point."""
        return self._x

    @property
    def y(self):
        """Get the y-coordinate of the point."""
        return self._y

    @property
    def z(self):
        """Get the z-coordinate of the point."""
        return self._z

    def __eq__(self, other):
        """Check if two Point3D objects are equal based on their coordinates."""
        return isinstance(other, Point3D) and (self.x, self.y, self.z) == (other.x, other.y, other.z)

    def __hash__(self):
        """Compute the hash value of the Point3D object based on its coordinates."""
        return hash((self.x, self.y, self.z))

    def __repr__(self):
        """Get the string representation of the Point3D object."""
        return f'Point3D({self.x}, {self.y}, {self.z})'

    def __str__(self):
        """Get the user-friendly string representation of the Point3D object."""
        return f'({self.x}, {self.y}, {self.z})'

# In the above implementation, we have separate classes (Point2D and Point3D) for different dimensions, leading to code repetition.
# Writing the same code multiple times for different dimension classes is inefficient and makes maintenance challenging.
# Let's adopt a smarter strategy to eliminate redundancy and improve code maintainability.


# DRY Version - Using Metaclasses
class SlottedStruct(type):
    """Metaclass to dynamically create classes for N-dimensional points."""

    def __new__(cls, name, bases, namespace):
        """Create a new class dynamically based on its name and dimension."""
        if name != 'Point':
            dim = int(name.split('D')[0][-1])  # Extract dimension from the class name
            namespace['__slots__'] = tuple(f'_{i}' for i in range(1, dim + 1))
            namespace['__init__'] = cls._init_coordinates
            namespace['__eq__'] = cls._eq_coordinates
            namespace['__hash__'] = cls._hash_coordinates
            namespace['__repr__'] = cls._repr_coordinates
            namespace['__str__'] = cls._str_coordinates

        return super().__new__(cls, name, bases, namespace)

    def _init_coordinates(self, *args):
        """Initialize the N-dimensional point object with coordinates."""
        for i, arg in enumerate(args, start=1):
            setattr(self, f'_{i}', arg)

    def _eq_coordinates(self, other):
        """Check if two N-dimensional point objects are equal based on their coordinates."""
        return isinstance(other, Point) and tuple(getattr(self, f'_{i}') for i in range(1, len(self.__slots__) + 1)) == \
               tuple(getattr(other, f'_{i}') for i in range(1, len(self.__slots__) + 1))

    def _hash_coordinates(self):
        """Compute the hash value of the N-dimensional point object based on its coordinates."""
        return hash(tuple(getattr(self, f'_{i}') for i in range(1, len(self.__slots__) + 1)))

    def _repr_coordinates(self):
        """Get the string representation of the N-dimensional point object."""
        dim = len(self.__slots__)
        coord_str = ', '.join(str(getattr(self, f'_{i}')) for i in range(1, dim + 1))
        return f'Point{dim}D({coord_str})'

    def _str_coordinates(self):
        """Get the user-friendly string representation of the N-dimensional point object."""
        dim = len(self.__slots__)
        coord_str = ', '.join(str(getattr(self, f'_{i}')) for i in range(1, dim + 1))
        return f'({coord_str})'


class Point(metaclass=SlottedStruct):
    """Base class for N-dimensional points."""

    pass
class Point2D(Point):
    """Class representing a point in 2-dimensional space."""

    pass


class Point3D(Point):
    """Class representing a point in 3-dimensional space."""

    pass


class Point4D(Point):
    """Class representing a point in 4-dimensional space."""

    pass

class Point5D(Point):
    """Class representing a point in 5-dimensional space."""

    pass

# Here the metaclass SlottedStruct dynamically creates classes for N-dimensional points.
# It is responsible for creating the __slots__, __init__, __eq__, __hash__, __repr__, and __str__ methods for the
# N-dimensional point classes and also for creating the __new__ method for the N-dimensional point classes.


# Test

p1 = Point2D(1, 2)
p2 = Point3D(1, 2, 3)
p3 = Point4D(1, 2, 3, 4)
p4 = Point5D(1, 2, 3, 4, 5)

print(p1)  # Output: (1, 2)
print(p2)  # Output: (1, 2, 3)
print(p3)  # Output: (1, 2, 3, 4)
print(p4)  # Output: (1, 2, 3, 4, 5)
