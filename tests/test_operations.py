import pytest
from decimal import Decimal
from typing import Any, Dict, Type

from app.exceptions import ValidationError
from app.operations import (
    Operation,
    Power,
    Root,
    Modulus,
    IntegerDivision,
    PercentageCalculation,
    AbsoluteDifference,
    OperationFactory,
)

# When running pytest:
    # Finds all classes starting with Test (like TestPower)
    # Runs all methods starting with test_ inside them
    # Uses the attributes (operation_class, valid_test_cases, etc.) defined in TestPower
    # Executes those inherited test methods using the data provided in TestPower

class TestOperation: # temporary base class
    """Test base Operation class functionality."""

    def test_str_representation(self):
        """Test that string representation returns class name."""
        class TestOp(Operation): # temporary subclass

            # It implements the required execute() method (so it can be instantiated)
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        # str(TestOp()) returns classname (TestOp)
        assert str(TestOp()) == "TestOp"


class BaseOperationTest:
    """Base test class for all operations."""

    operation_class: Type[Operation]
    valid_test_cases: Dict[str, Dict[str, Any]]
    invalid_test_cases: Dict[str, Dict[str, Any]]

    def test_valid_operations(self):
        """Test operation with valid inputs."""
        operation = self.operation_class()
        for name, case in self.valid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            expected = Decimal(str(case["expected"]))
            result = operation.execute(a, b)
            assert result == expected, f"Failed case: {name}"

    def test_invalid_operations(self):
        """Test operation with invalid inputs raises appropriate errors."""
        operation = self.operation_class()
        for name, case in self.invalid_test_cases.items():
            a = Decimal(str(case["a"]))
            b = Decimal(str(case["b"]))
            error = case.get("error", ValidationError)
            error_message = case.get("message", "")

            with pytest.raises(error, match=error_message):
                operation.execute(a, b)


# inherits from BaseOperationTest
# automatically runs test_valid_operations and test_invalid_operations
class TestPower(BaseOperationTest):
    """Test Power operation."""

    operation_class = Power
    valid_test_cases = {
        "positive_base_and_exponent": {"a": "2", "b": "3", "expected": "8"},
        "zero_exponent": {"a": "5", "b": "0", "expected": "1"},
        "one_exponent": {"a": "5", "b": "1", "expected": "5"},
        "decimal_base": {"a": "2.5", "b": "2", "expected": "6.25"},
        "zero_base": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "negative_exponent": {
            "a": "2",
            "b": "-3",
            "error": ValidationError,
            "message": "Negative exponents not supported"
        },
    }


class TestRoot(BaseOperationTest):
    """Test Root operation."""

    operation_class = Root
    valid_test_cases = {
        "square_root": {"a": "9", "b": "2", "expected": "3"},
        "cube_root": {"a": "27", "b": "3", "expected": "3"},
        "fourth_root": {"a": "16", "b": "4", "expected": "2"},
        "decimal_root": {"a": "2.25", "b": "2", "expected": "1.5"},
    }
    invalid_test_cases = {
        "negative_base": {
            "a": "-9",
            "b": "2",
            "error": ValidationError,
            "message": "Cannot calculate root of negative number"
        },
        "zero_root": {
            "a": "9",
            "b": "0",
            "error": ValidationError,
            "message": "Zero root is undefined"
        },
    }


class TestModulus(BaseOperationTest):
    """Test Modulus operation"""

    operation_class = Modulus
    valid_test_cases = {
        "positive_numbers": {"a": "8", "b": "4", "expected": "0"},
        "negative_numbers": {"a": "-16", "b": "-3", "expected": "-1"},
        "decimals": {"a": "8.5", "b": "2", "expected": "0.5"},
        "divide_zero": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "divide_by_zero": {
            "a": "12",
            "b": "0",
            "error": ValidationError,
            "message": "Cannot compute modulus operation, divisor cannot be zero"
        },
    }


class TestIntegerDivision(BaseOperationTest):
    """Test Integer Division operation."""

    operation_class = IntegerDivision
    valid_test_cases = {
        "positive_numbers": {"a": "12", "b": "3", "expected": "4"},
        "negative_numbers": {"a": "-6", "b": "-2", "expected": "3"},
        "mixed_signs": {"a": "-20", "b": "2", "expected": "-10"},
        "decimals": {"a": "5.5", "b": "2", "expected": "2"},
        "decimals-part2": {"a": "8.75", "b": "2.25", "expected": "3"},
        "divide_zero": {"a": "0", "b": "5", "expected": "0"},
    }
    invalid_test_cases = {
        "divide_by_zero": {
            "a": "5",
            "b": "0",
            "error": ValidationError,
            "message": "Cannot compute integer divison operation, divisor cannot be zero"
        },
    }


class TestPercentageCalculation(BaseOperationTest):
    """Test Percentage Calculation operation"""

    operation_class = PercentageCalculation
    valid_test_cases = {
        "simple_percentage": {"a": "50", "b": "200", "expected": "25"},
        "full_percentage": {"a": "75", "b": "75", "expected": "100"},
        "decimal_result": {"a": "5", "b": "8", "expected": "62.5"},
        "decimal_inputs": {"a": "2.5", "b": "10", "expected": "25"},
        "large_values": {"a": "100000", "b": "500000", "expected": "20"},
        "zero_numerator": {"a": "0", "b": "100", "expected": "0"},
    }
    invalid_test_cases = {
        "divide_by_zero": {
            "a": "100",
            "b": "0",
            "error": ValidationError,
            "message": "Cannot compute percentage calculation operation, divisor cannot be zero"
        },
    }


class TestAbsoluteDifference(BaseOperationTest):
    """Test Absolute Difference operation"""

    operation_class = AbsoluteDifference
    valid_test_cases = {
        "positive_numbers": {"a": "8", "b": "5", "expected": "3"},
        "reverse_order": {"a": "5", "b": "8", "expected": "3"},
        "negative_numbers": {"a": "-7", "b": "-2", "expected": "5"},
        "mixed_signs_1": {"a": "-4", "b": "6", "expected": "10"},
        "mixed_signs_2": {"a": "10", "b": "-5", "expected": "15"},
        "same_values": {"a": "9", "b": "9", "expected": "0"},
        "decimals": {"a": "5.5", "b": "2.2", "expected": "3.3"},
    }

    invalid_test_cases = {}  # Absolute Difference has no invalid cases


class TestOperationFactory:
    """Test OperationFactory functionality."""

    def test_create_valid_operations(self):
        """Test creation of all valid operations."""
        operation_map = {
            'power': Power,
            'root': Root,
            'modulus': Modulus,
            'integer-division': IntegerDivision,
            'percentage-calculation': PercentageCalculation,
            'absolute-difference': AbsoluteDifference
        }

        # op_name is the string name like "power"
        # op_class is the corresponding class like Power
        for op_name, op_class in operation_map.items():
            operation = OperationFactory.create_operation(op_name)

            # Checks that the returned object is an instance of the correct class
            assert isinstance(operation, op_class)

            # Test case-insensitive
            operation = OperationFactory.create_operation(op_name.upper())
            assert isinstance(operation, op_class)

    # testing creating an invalid operation "invalid_op"
    def test_create_invalid_operation(self):
        """Test creation of invalid operation raises error."""
        with pytest.raises(ValueError, match="Unknown operation: invalid_op"):
            OperationFactory.create_operation("invalid_op")


    # successfully register and create a new operation dynamically.
    # create and define new operation
    # register it in the dictionary
    # creates new instance of new_op in variable operation
    # checks if operation is an instance of NewOperation class
    def test_register_valid_operation(self):
        """Test registering a new valid operation."""
        class NewOperation(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        OperationFactory.register_operation("new_op", NewOperation)
        operation = OperationFactory.create_operation("new_op")
        assert isinstance(operation, NewOperation)

    # invalid operation, has to inherit from Operation class
    def test_register_invalid_operation(self):
        """Test registering an invalid operation class raises error."""
        class InvalidOperation:
            pass

        with pytest.raises(TypeError, match="Operation class must inherit"):
            OperationFactory.register_operation("invalid", InvalidOperation)