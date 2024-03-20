"""The task involves implementing descriptor classes in Python to enforce type validation for attributes in a Person class.
The goal is to ensure that the assigned values for specific attributes have the correct types and raise a ValueError
if an incorrect type is provided.

Input and Output examples
The code includes three individual descriptor classes: Int, Float, and List. Each descriptor class defines the set_name, set,
and get methods to handle attribute assignment, type validation, and attribute retrieval. To optimize the code and avoid repeating
similar code blocks, a new descriptor class called ValidType is introduced. This class takes a type parameter during initialization and validat
hat the assigned value matches the specified type. It handles type validation for various attribute types, such as
integers, floats, lists, and tuples. The Person class utilizes these descriptor classes to define specific attributes:
with the corresponding type. By using these descriptors, any attempt to assign an incorrect type to these attributes
will raise a ValueError with an appropriate error message indicating the expected type."""

class ValidType:
    """
    Descriptor class for enforcing type validation on attributes.
    """

    def __init__(self, data_type):
        """
        Initialize the ValidType descriptor.

        Parameters:
            data_type (type): The expected data type for the attribute.
        """
        self.data_type = data_type
        self.name = None

    def __set_name__(self, owner, name):
        """
        Set the name of the attribute when accessed in the owner class.

        Parameters:
            owner (type): The owner class of the attribute.
            name (str): The name of the attribute.
        """
        self.name = name

    def __set__(self, instance, value):
        """
        Set the attribute value with type validation.

        Parameters:
            instance (object): The instance of the owner class.
            value: The value to be assigned to the attribute.

        Raises:
            ValueError: If the provided value is not of the expected data type.
        """
        if not isinstance(value, self.data_type):
            raise ValueError(f"Invalid type. Expected {self.data_type}, but got {type(value)}.")
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner=None):
        """
        Get the attribute value.

        Parameters:
            instance (object): The instance of the owner class.
            owner (type): The owner class of the attribute (optional).

        Returns:
            The value of the attribute.
        """
        if instance is None:
            return self
        return instance.__dict__[self.name]


class Int(ValidType):
    """
    Descriptor class for integer attributes.
    """

    def __init__(self):
        """
        Initialize the Int descriptor.
        """
        super().__init__(int)


class Float(ValidType):
    """
    Descriptor class for float attributes.
    """

    def __init__(self):
        """
        Initialize the Float descriptor.
        """
        super().__init__(float)


class List(ValidType):
    """
    Descriptor class for list attributes with specified element type.
    """

    def __init__(self, data_type):
        """
        Initialize the List descriptor.

        Parameters:
            data_type (type): The expected data type for the elements in the list.
        """
        super().__init__(list)
        self._type = data_type

    def __set__(self, instance, value):
        """
        Set the list attribute value with type validation for elements.

        Parameters:
            instance (object): The instance of the owner class.
            value (list): The list value to be assigned to the attribute.

        Raises:
            ValueError: If the provided value is not a list or contains elements of incorrect data type.
        """
        if not isinstance(value, list):
            raise ValueError(f"Invalid type. Expected list, but got {type(value)}.")
        for item in value:
            if not isinstance(item, self._type):
                raise ValueError(f"Invalid type. Expected {self._type}, but got {type(item)}.")
        instance.__dict__[self.name] = value


class Tuple(ValidType):
    """
    Descriptor class for tuple attributes with specified element type.
    """

    def __init__(self, data_type):
        """
        Initialize the Tuple descriptor.

        Parameters:
            data_type (type): The expected data type for the elements in the tuple.
        """
        super().__init__(tuple)
        self._type = data_type

    def __set__(self, instance, value):
        """
        Set the tuple attribute value with type validation for elements.

        Parameters:
            instance (object): The instance of the owner class.
            value (tuple): The tuple value to be assigned to the attribute.

        Raises:
            ValueError: If the provided value is not a tuple or contains elements of incorrect data type.
        """
        if not isinstance(value, tuple):
            raise ValueError(f"Invalid type. Expected tuple, but got {type(value)}.")
        for item in value:
            if not isinstance(item, self._type):
                raise ValueError(f"Invalid type. Expected {self._type}, but got {type(item)}.")
        instance.__dict__[self.name] = value


class Person:
    """
    Class representing a person with type-validated attributes.
    """

    age = ValidType(int)
    height = ValidType(float)
    tags = ValidType(list)
    favourite_foods = ValidType(tuple)
    name = ValidType(str)

    def __init__(self, age, height, tags, favourite_foods, name):
        """
        Initialize the Person class with the specified attributes.

        Parameters:
            age (int): The age of the person.
            height (float): The height of the person.
            tags (list): The tags associated with the person.
            favourite_foods (tuple): The favorite foods of the person.
            name (str): The name of the person.
        """
        self.age = age
        self.height = height
        self.tags = tags
        self.favourite_foods = favourite_foods
        self.name = name

# Test the Person class
try:
    person = Person(25, 175.5, ["reading", "swimming"], ("pizza", "pasta"), "Ann")

    print(person.age)               # Output: 25
    print(person.height)            # Output: 175.5
    print(person.tags)              # Output: ['reading', 'swimming', 'running']
    print(person.favourite_foods)   # Output: ('pizza', 'pasta')
    print(person.name)              # Output: Ann

    # Attempt to assign incorrect types
    person.age = "25"               # Raises ValueError: Invalid type. Expected <class 'int'>, but got <class 'str'>.
    person.height = "175.5"         # Raises ValueError: Invalid type. Expected <class 'float'>, but got <class 'str'>.
    person.tags = [1, 2]            # Raises ValueError: Invalid type. Expected <class 'str'>, but got <class 'int'>.
    person.favourite_foods = ["pizza", "pasta"]  # Raises ValueError: Invalid type. Expected <class 'tuple'>, but got <class 'list'>.
    person.name = 25               # Raises ValueError: Invalid type. Expected <class 'str'>, but got <class 'int'>.
except ValueError as e:
    print(str(e))



