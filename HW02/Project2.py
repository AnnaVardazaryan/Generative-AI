"""The application focuses on implementing a Polygon class that represents a polygon shape with a sequence of vertices.
The goal is to ensure that the vertices attribute of the Polygon class contains a sequence of Point2D instances,
where each point represents a coordinate on a 2D plane. To achieve this, the code defines several descriptor and validator classes.

Input and Output examples
Int class: This descriptor is responsible for validating that integer values assigned to attributes fall within specified bounds.
It includes a min_value and max_value parameter to define the valid range for the attribute.
Point2D class: This class represents a point on a 2D plane. It includes x and y attributes, which are instances of the
Int descriptor class with specific bounds. The Point2D class ensures that the assigned values for x and y are
non-negative integers within the defined range.
Point2DSequence class: This validator class ensures that the assigned value for the vertices attribute in the Polygon
class is a sequence (mutable or immutable) and that each element in the sequence is an instance of the Point2D class.
It includes min_length and max_length parameters to define the minimum and maximum number of vertices for a polygon.
Polygon class: This class represents a polygon shape. It includes the vertices attribute, which is assigned an
instance of the Point2DSequence validator class. The Polygon class constructor takes variable arguments as vertices,
and the assigned values are validated by the Point2DSequence validator to ensure they meet the requirements of a polygon.
The Polygon class also includes an append method, allowing additional Point2D instances to be appended to the vertices
list if the maximum length limit has not been reached.
Overall, this application provides a way to define a polygon shape with validated vertices using the Polygon class and
ensures that the assigned values meet the required criteria. """

class Int:
    """
    Descriptor class to validate integer values within specified bounds.
    """

    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        """
        Set the value for the attribute after validation.

        Args:
            instance: The instance of the class that owns the attribute.
            value (int): The value to be set for the attribute.

        Raises:
            ValueError: If the value is not an integer or not within the specified bounds.
        """
        if not isinstance(value, int):
            raise ValueError(f"Invalid type. Expected int, but got {type(value)}.")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Invalid value. Expected {self.name} >= {self.min_value}, but got {value}.")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Invalid value. Expected {self.name} <= {self.max_value}, but got {value}.")
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self.name]


class Point2D:
    """
    Represents a point on a 2D plane with validated x and y coordinates.
    """

    x = Int(0, 800)
    y = Int(0, 600)

    def __init__(self, x, y):
        """
        Initialize a Point2D instance with x and y coordinates.

        Args:
            x (int): The x-coordinate.
            y (int): The y-coordinate.
        """
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point2D(x={self.x}, y={self.y})"


from collections.abc import Sequence


class Point2DSequence:
    """
    Validator class to ensure that the assigned value for vertices in Polygon is a sequence of Point2D instances.
    """

    def __init__(self, min_length=None, max_length=None):
        """
        Initialize the Point2DSequence validator.

        Args:
            min_length (int, optional): The minimum number of vertices allowed. Defaults to None.
            max_length (int, optional): The maximum number of vertices allowed. Defaults to None.
        """
        self.min_length = min_length
        self.max_length = max_length

    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        """
        Set the value for the vertices attribute after validation.

        Args:
            instance: The instance of the class that owns the vertices attribute.
            value (sequence): The value to be set for the vertices attribute.

        Raises:
            ValueError: If the value is not a sequence or does not meet the required criteria.
        """
        if not isinstance(value, Sequence):
            raise ValueError(f"Invalid type. Expected Sequence, but got {type(value)}.")
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(f"Invalid length. Expected {self.name} >= {self.min_length}, but got {len(value)}.")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f"Invalid length. Expected {self.name} <= {self.max_length}, but got {len(value)}.")
        for item in value:
            if not isinstance(item, Point2D):
                raise ValueError(f"Invalid type. Expected Point2D, but got {type(item)}.")
        instance.__dict__[self.name] = list(value)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return instance.__dict__[self.name]


class Polygon:
    """
    Represents a polygon shape with validated vertices.
    """

    vertices = Point2DSequence(min_length=3, max_length=4)

    def __init__(self, *vertices):
        """
        Initialize a Polygon instance with validated vertices.

        Args:
            *vertices: Variable number of Point2D instances representing the vertices of the polygon.
        """
        self.vertices = vertices

    def __repr__(self):
        return f"Polygon({self.vertices})"

    def append(self, point):
        """
        Append a Point2D instance to the vertices list.

        Args:
            point (Point2D): The Point2D instance to be appended.

        Raises:
            ValueError: If the given point is not a Point2D instance or the maximum number of vertices is reached.
        """
        if not isinstance(point, Point2D):
            raise ValueError(f"Invalid type. Expected Point2D, but got {type(point)}.")
        if len(self.vertices) >= Polygon.vertices.max_length:
            raise ValueError("Cannot append more vertices. Polygon has reached maximum capacity.")
        self.vertices.append(point)


p1 = Point2D(100, 200)
p2 = Point2D(300, 400)
p3 = Point2D(500, 600)

polygon = Polygon(p1, p2, p3)

p4 = Point2D(700, 500)
polygon.append(p4)  # This will work since the maximum length is not exceeded
print(polygon)  # Output: Polygon([Point2D(x=100, y=200), Point2D(x=300, y=400), Point2D(x=500, y=600), Point2D(x=700, y=500)])

p5 = Point2D(200, 300)
polygon.append(p5)  # This will raise ValueError since the maximum length has been reached



