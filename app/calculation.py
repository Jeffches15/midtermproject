### Calculation Model ###

from dataclasses import dataclass, field
import datetime
from decimal import Decimal, InvalidOperation
import logging
from typing import Any, Dict

from app.exceptions import OperationError

# So, self refers to the current object — the specific instance that is calling the method.
@dataclass
class Calculation:
    """
    Value Object representing a single calculation.

    Encapsulates the details of a mathematical calculation, including the
    operation performed, operands involved, the result, and the timestamp of the
    calculation. Provides methods for preforming the calculation, serializing the
    date for storage, and deserializing data to recreate a Calculation instance.
    """

    # Required fields
    operation: str
    operand1: Decimal
    operand2: Decimal

    # fields with default values
        # result (of the calculation) won’t be set via the constructor,
        # it’s something you’ll assign later, like in a method or after computation.
    result: Decimal = field(init=False)
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    # self as first arugment -> instance method
    # this is a special function built into @dataclass
    # If you define a __post_init__() method, it will be 
        # called automatically right after the generated __init__().
    def __post_init__(self):
        """
        Post-initalization processing. Automatically calculates the result of the
        operation after the Calculation instance is created
        """
        self.result = self.calculate()

    def calculate(self) -> Decimal:
        """
        Execute calculation using the specified operation. Utilizes a dictionary to map
        operation names to their corresponding lambda functions, enabling dynamic execution
        based on the operation name.

        Returns:
            Decimal: result of calculation

        Raises:
            OperationError: if the operation is unknown or the calculation fails.
        """

        # mapping operation names to their corresponding functions
        # uses this approach instead of a bunch of if else statements
        # purpose of lambda: define small, one-line functions right inside the dictionary, 
            # without needing to create separate named functions.
        operations = {
            # self._raise_neg_power() is a static method that raises an error
            "Power": lambda x, y: Decimal(pow(float(x), float(y))) if y >= 0 else self._raise_neg_power(),
            "Root": lambda x, y: (
                Decimal(pow(float(x), 1 / float(y)))
                if x >= 0 and y != 0
                else self._raise_invalid_root(x, y)
            ),
            "Modulus": lambda x, y: x % y if y > 0 else self._raise_divisor_zero(),
            "IntegerDivision": lambda x, y: int(x // y) if y > 0 else self._raise_divisor_zero(),
            "PercentageCalculation": lambda x, y: (x / y) * 100 if y > 0 else self._raise_divisor_zero(),
            "AbsoluteDifference": lambda x, y: abs(x - y)
        }

        # retrieve the operation function based on the operation name
        op = operations.get(self.operation)
        if not op:
            raise OperationError(f"Unknown operation: {self.operation}")
        
        try:
            # execute the operation with the provided operands
            return op(self.operand1, self.operand2)
        except (InvalidOperation, ValueError, ArithmeticError) as e:
            raise OperationError(f"Calculation failed: {str(e)}") # pragma: no cover
        
    @staticmethod
    def _raise_divisor_zero(): # pragma: no cover
        """
        This method is called when a division by zero is attempted
        """
        
        raise OperationError("Division by zero is not allowed")
    
    @staticmethod
    def _raise_neg_power(): # pragma: no cover
        """
        This method is called when a negative exponent is used in a power operation
        """

        raise OperationError("Negative exponents are not supported")
    
    