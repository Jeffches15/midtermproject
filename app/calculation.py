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
    
    @staticmethod
    def _raise_invalid_root(x: Decimal, y: Decimal): # pragma: no cover
        """
        This method is called when an invalid root operation is attempted, such as
        taking the root of a negative number or using zero as the root degree

        Arguments:
            x: number from which the root is taken
            y: degree of the root
        """

        if y == 0:
            raise OperationError("Zero root is undefined")
        if x < 0:
            raise OperationError("Cannot calculate root of negative number")
        raise OperationError("Invalid root operation")
    
    # convert to dictionary form to put into excel history log
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert calculation to dictionary for serialization. This method
        transforms the Calculation instance into a dictionary format,
        facilitating easy storage and retrieval (saving to a file)
        """

        return {
            'operation': self.operation,
            'operand1': str(self.operand1),
            'operand2': str(self.operand2),
            'result': str(self.result),
            'timestamp': self.timestamp.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Calculation':
        """
        Create calculation from dictionary. This method reconstructs a Calculation instance from
        a dictionary, ensuring that all required fields are present and correctly formatted.

        Arguments:
            data (Dict[str, Any]): dictionary containing calculation data

        Returns:
            Calculation: a new instance of Calculation with data populated from the dictionary

        Raises:
            OperationError: if data is invalid or missing required fields
        """

        try:
            # create Calculation object with original operands
            calc = Calculation(
                operation=data['operation'],
                operand1=Decimal(data['operand1']),
                operand2=Decimal(data['operand2']),
            )

            # set the timestamp from the saved data
            # converts a timestamp string back into a datetime object 
                # so your code can work with it like a real date/time.
            calc.timestamp = datetime.datetime.fromisoformat(data['timestamp'])

            # verify the result matches (help catch data corruption)
            # Is the result I just calculated (calc.result) different from the one we previously saved?
            saved_result = Decimal(data['result'])
            if calc.result != saved_result:
                logging.warning(
                    f"Loaded calculation result {saved_result} "
                    f"differs from computed result {calc.result}"
                ) # pragma: no cover

            return calc
        
        except(KeyError, InvalidOperation, ValueError) as e:
            raise OperationError(f"Invalid calculation data: {str(e)}")
        
    def __str__(self) -> str:
        """
        Return string representation of calculation.

        Provides a human-readable representation of the calculation, showing the
        operation performed and its result.

        Returns:
            str: Formatted string showing the calculation and result.
        """
        return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"
    
    # "How should this object look when printed in the console or logs?"
    def __repr__(self) -> str:
        """
        Return detailed string representation of calculation.

        Provides a detailed and unambiguous string representation of the Calculation
        instance, useful for debugging.

        Returns:
            str: Detailed string showing all calculation attributes.
        """
       
        return (
            f"Calculation(operation='{self.operation}', "
            f"operand1={self.operand1}, "
            f"operand2={self.operand2}, "
            f"result={self.result}, "
            f"timestamp='{self.timestamp.isoformat()}')"
        )

    def __eq__(self, other: object) -> bool:
        """
        Check if two calculations are equal.

        Compares two Calculation instances to determine if they represent the same
        operation with identical operands and results.

        Args:
            other (object): Another calculation to compare with.

        Returns:
            bool: True if calculations are equal, False otherwise.
        """

        # checks if other is an instance of Calculation
        if not isinstance(other, Calculation):
            return NotImplemented
        return (
            self.operation == other.operation and
            self.operand1 == other.operand1 and
            self.operand2 == other.operand2 and
            self.result == other.result
        )
    
    def format_result(self, precision: int = 10) -> str:
        """
        Format the calculation result with specified precision.

        This method formats the result to a fixed number of decimal places,
        removing any trailing zeros for a cleaner presentation.

        Args:
            precision (int, optional): Number of decimal places to show. Defaults to 10.

        Returns:
            str: Formatted string representation of the result.
        """
        try:
            # remove trailing zeros and format to specified precision
            return str(self.result.normalize().quantize(
                Decimal('0.' + '0' * precision)
            ).normalize())
        except InvalidOperation: # pragma: no cover
            return str(self.result)