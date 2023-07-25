"""There’s another pattern we can implement using metaprogramming - Singletons.
If you read online, you’ll see that singleton objects are controversial in Python.
I’m not going to get into a debate on this, other than to say I do not use singleton objects, not because I have deep
thoughts about it (or even shallow ones for that matter), but rather because I have never had a need for them.
However, the question often comes up, so here it is - the metaclass way of implementing the singleton pattern.
Whether you think you should use it or not, is entirely up to you! We have seen singleton objects - objects such as
`None`, `True` or `False` for example. No matter where we create them in our code, they always refer to the **same**
object. We can recover the type used to create `None` objects:
NoneType = type(None)
And now we can create multiple instances of that type:
n1 = NoneType()
n2 = NoneType()
The same holds true for booleans:
b1 = bool([])
b2 = bool("")
There is no built-in mechanism to Python for singleton objects, so we have to do it ourselves.
The basic idea is this:
When an instance of the class is being created (but **before** the instance is actually created), check if an instance
has already been created, in which case return that instance, otherwise, create a new instance and store that instance
reference somewhere so we can recover it the next time an instance is requested.
We could do it entirely in the class itself, without any metaclasses, using the `__new__` method.

Task is to implement Singleton with metaclass

Hints
Create a custom metaclass called SingletonMeta. This metaclass will be responsible for controlling the creation of
instances of the class that uses it.
Implement the __call__ method in the SingletonMeta metaclass. The __call__ method is called when you try to create an
instance of a class. In this method, check if an instance of the class already exists. If it does, return that instance.
Otherwise, create a new instance and store it as a class attribute for future access.
Modify the target class (e.g., Hundred in the provided example) to use the SingletonMeta metaclass. This will ensure
that the Hundred class follows the Singleton pattern, allowing only one instance to be created.
Test the implementation by creating multiple instances of the target class (e.g., Hundred) and verifying that they all
refer to the same object. You can use the is operator to check if two objects are the same instance."""

class SingletonMeta(type):
    """
    Metaclass for implementing the Singleton pattern.
    This metaclass ensures that only one instance of each class using this metaclass is created.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Override the __call__ method to control instance creation.
        If an instance of the class does not exist, create a new instance and store it.
        If an instance already exists, return the existing instance.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Hundred(metaclass=SingletonMeta):
    """
    Class representing the value hundred.
    Only one instance of this class can be created due to the Singleton metaclass.
    """

    def __init__(self):
        self.name = 'hundred'
        self.value = 100

    def __repr__(self):
        return f'{self.name}: {self.value}'


class Thousand(metaclass=SingletonMeta):
    """
    Class representing the value thousand.
    Only one instance of this class can be created due to the Singleton metaclass.
    """

    def __init__(self):
        self.name = 'thousand'
        self.value = 1000

    def __repr__(self):
        return f'{self.name}: {self.value}'

# Test

h1 = Hundred()  # this will create a new instance
h2 = Hundred()  # this will return the previously created instance
print(h1)       # Output: hundred: 100
print(h2)       # Output: hundred: 100
print(h1 is h2) # Output: True - both variables refer to the same object

t1 = Thousand()  # this will create a new instance
t2 = Thousand()  # this will return the previously created instance
print(t1)        # Output: thousand: 1000
print(t2)        # Output: thousand: 1000
print(t1 is t2)  # Output: True - both variables refer to the same object

