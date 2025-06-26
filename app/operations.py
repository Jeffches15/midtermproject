### Operations Classes ###

from abc import ABC, abstractmethod
from decimal import Decimal
from math import floor
from typing import Dict
from app.exceptions import ValidationError

class Operation(ABC):
    """
    - Abstract classes cannot be instantiated on its own and is meant to be 
        inherited by other classes. 
    - Its main role is to define a common interface or blueprint for subclasses.
    - This class defines the interface for all arithmetic operations
        - execute method
        - optionally override operand validation
    """

    # An abstract method is a method that is declared but not implemented in a class. 
    # It acts as a placeholder that tells subclasses:
        # "Hey, you need to implement this method"
    @abstractmethod
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Performs arithmetic operation on the provided operands

        Arguments:
            a: (Decimal): First operand
            b: (Decimal): Second operand
        
        Returns:
            Decimal: result of the operation

        Raises:
            OperationError: If the operation fails
        """
        pass # pragma: no cover

    # this is an instance method (self is the first argument)
    # belongs to an object (instance) of a class, 
        # and it can access or modify the object's state (its attributes).
    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands before execution. Can be overwritten by subclasses to enforce
        specific validation rules.

        Arguments:
            a: (Decimal): First operand
            b: (Decimal): Second operand

        Returns None (nothing)

        Raises:
            ValidationError: if operands are invalid
        """
        pass

    def __str__(self) -> str:
        """
        Returns operation name for display. Provides a string representation of the operation,
        typically the class name.

        Returns:
            str: name of the operation
        """

         # self: refers to the current instance (object).
         # self.__class__: gives the class object of that instance.
         # self.__class__.__name__: gives the name of that class as a string.
        return self.__class__.__name__
    

# Power is a subclass that is inheriting Operation class
class Power(Operation):
    """
    Power operation implementation. Raises one number to the power of another
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for Power class. Override Operation class method to ensure that the
        exponent is not negative
        """

        # running super class validate_operands method (even though it only says 'pass')
        super().validate_operands(a, b)
        if b < 0:
            raise ValidationError("Negative exponents not supported")
        
    # Once the subclass provides a concrete implementation of an abstract method, 
        # it’s a regular method — no longer abstract.
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate one number raised to the power of another
        """

        self.validate_operands(a, b)
        return Decimal( pow(float(a), float(b)) )


# Root is a subclass that is inheriting Operation class 
class Root(Operation):
    """
    Root operation implementation. Calculates the nth root of a number
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for Root class. We are making sure the degree of the root (b) isnt 0,
        and the number from which the root is taken (a) is not negative
        """

        super().validate_operands(a, b)
        if a < 0:
            raise ValidationError("Cannot calculate root of negative number")
        if b == 0:
            raise ValidationError("Zero root is undefined")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the nth root of a number
        """
        self.validate_operands(a, b)
        return Decimal( pow(float(a), 1 / float(b)) )
    

# Modulus is a subclass that is inheriting Operation class   
class Modulus(Operation):
    """
    Modulus operation implemetation. Compute the remainder of the division of two numbers.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for Modulus class. Make sure the divisor (b) is not zero
        """

        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Cannot compute modulus operation, divisor cannot be zero")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Compute the remainder of the division of two numbers.
        """

        self.validate_operands(a, b)
        return a % b
    

# IntegerDivision is a subclass that is inheriting Operation class
class IntegerDivision(Operation):
    """
    IntegerDivision operation implementation. 
    Perform division that results in an integer quotient, discarding any fractional part.
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for IntegerDivison class. Make sure the divisor (b) is not zero
        """

        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Cannot compute integer divison operation, divisor cannot be zero")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Perform division that results in an integer quotient, discarding any fractional part
        """

        self.validate_operands(a, b)

        # a // b divides a by b and returns the quotient without the remainder (the integer part).
        # If a and b are integers, the result is an integer.
        # If they are floats or Decimals, it returns the floor of the division (rounded down).
        return int(a // b)
    
# PercentageCalculation is a subclass that is inheriting Operation class
class PercentageCalculation(Operation):
    """
    PercentageCalculation operation implementation. 
    Calculate the percentage of one number with respect to another
    """

    def validate_operands(self, a: Decimal, b: Decimal) -> None:
        """
        Validate operands for PercentageCalculation class. Make sure the divisior (b) is not zero
        """

        super().validate_operands(a, b)
        if b == 0:
            raise ValidationError("Cannot compute percentage calculation operation, divisor cannot be zero")
        
    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the percentage of one number with respect to another
        """

        self.validate_operands(a, b)
        return (a / b) * 100
    
# AbsoluteDifference is a subclass that is inheriting Operation class
class AbsoluteDifference(Operation):
    """
    AbsoluteDifference operation implementation.
    Calculate the absolute difference between two numbers.
    """

    # dont need validate_operands (no special validation is needed beyond the base class)

    def execute(self, a: Decimal, b: Decimal) -> Decimal:
        """
        Calculate the absolute difference between two numbers.
        """

        self.validate_operands(a, b)
        return abs(a - b)


# In simple terms, a factory class in Python is a class that creates and 
    # gives you the right object, depending on what you ask for.
# You press a button for "Coke" → it gives you a Coke
# You press a button for "Water" → it gives you Water.
class OperationFactory:
    """
    Factory class for creating operation instances.

    Implements the Factory pattern by providing a method to instantiate
    different operation classes based on a given operation type. This promotes
    scalability and decouples the creation logic from the Calculator class.
    """

    # Dictionary mapping operation identifiers to their corresponding classes
    _operations: Dict[str, type] = {
        'power': Power,
        'root': Root,
        'modulus': Modulus,
        'integer-division': IntegerDivision,
        'percentage-calculation': PercentageCalculation,
        'absolute-difference': AbsoluteDifference
    }

    # classmethods:
        # Belongs to the class, not an instance.
        # Receives the class (cls) as its first argument instead of self.
        # Can access and modify class-level data (like shared settings or registries).
    # This method register_operation is part of a factory class, 
    # and it lets you dynamically add new operation types to the factory at runtime.
    @classmethod
    def register_operation(cls, name: str, operation_class: type) -> None:
        """
        Register a new operation type.

        Allows dynamic addition of new operations to the factory.

        Args:
            name (str): Operation identifier (e.g., 'modulus').
            operation_class (type): The class implementing the new operation.

        Raises:
            TypeError: If the operation_class does not inherit from Operation.
        """

        # Ensures the given class actually inherits from the 
            # base Operation class (which likely defines an interface like execute()).
        if not issubclass(operation_class, Operation):
            raise TypeError("Operation class must inherit from Operation")
        cls._operations[name.lower()] = operation_class

    # in addition, class methods:
        # Has access to the class itself (via cls)
        # Does not have access to the instance (no self)
    # Responsible for creating and returning the correct operation object 
        # based on a string input like "add", "modulus", etc.
    @classmethod
    def create_operation(cls, operation_type: str) -> Operation:
        """
        Create an operation instance based on the operation type.

        This method retrieves the appropriate operation class from the
        _operations dictionary and instantiates it.

        Args:
            operation_type (str): The type of operation to create (e.g., 'add').

        Returns:
            Operation: An instance of the specified operation class.

        Raises:
            ValueError: If the operation type is unknown.
        """
        # Looks up the operation name in a class-level dictionary called _operations.
        operation_class = cls._operations.get(operation_type.lower())

        if not operation_class:
            raise ValueError(f"Unknown operation: {operation_type}")
        return operation_class() # Creates and returns an instance of the operation class.
    

    # in simple terms:
    # register_operation: Adds a new operation type to the factory so it knows how to create it later.
    # create_operation: Creates and returns an actual instance of the operation.

