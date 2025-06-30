import pytest
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError
import logging


def test_power():
    calc = Calculation(operation="Power", operand1=Decimal("2"), operand2=Decimal("5"))
    assert calc.result == Decimal("32")


# matches raise ValidationError("Negative exponents not supported") created in Power Class
def test_negative_power():
    with pytest.raises(OperationError, match="Negative exponents are not supported"):
        Calculation(operation="Power", operand1=Decimal("2"), operand2=Decimal("-3"))


def test_root():
    calc = Calculation(operation="Root", operand1=Decimal("9"), operand2=Decimal("2"))
    assert calc.result == Decimal("3")


def test_invalid_root():
    with pytest.raises(OperationError, match="Cannot calculate root of negative number"):
        Calculation(operation="Root", operand1=Decimal("-8"), operand2=Decimal("2"))


def test_modulus():
    calc = Calculation(operation="Modulus", operand1=Decimal("7"), operand2=Decimal("3"))
    assert calc.result == Decimal("1")


def test_modulus_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation(operation="Modulus", operand1=Decimal("19"), operand2=Decimal("0"))


def test_integer_division():
    calc = Calculation(operation="IntegerDivision", operand1=Decimal("8.50"), operand2=Decimal("2.75"))
    assert calc.result == Decimal("3")


def test_integer_division_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation(operation="IntegerDivision", operand1=Decimal("8"), operand2=Decimal("0"))


def test_percentage_calculation():
    calc = Calculation(operation="PercentageCalculation", operand1=Decimal("15"), operand2=Decimal("60"))
    assert calc.result == Decimal("25")


def test_percentage_calculation_by_zero():
    with pytest.raises(OperationError, match="Division by zero is not allowed"):
        Calculation(operation="PercentageCalculation", operand1=Decimal("14"), operand2=Decimal("0"))


def test_absolute_difference_both_positive():
    calc = Calculation(operation="AbsoluteDifference", operand1=Decimal("4"), operand2=Decimal("6"))
    assert calc.result == Decimal("2")


def test_absolute_difference_first_negative():
    calc = Calculation(operation="AbsoluteDifference", operand1=Decimal("-4"), operand2=Decimal("6"))
    assert calc.result == Decimal("10")


def test_absolute_difference_second_negative():
    calc = Calculation(operation="AbsoluteDifference", operand1=Decimal("4"), operand2=Decimal("-6"))
    assert calc.result == Decimal("10")


def test_absolute_difference_both_negative():
    calc = Calculation(operation="AbsoluteDifference", operand1=Decimal("-4"), operand2=Decimal("-6"))
    assert calc.result == Decimal("2")


def test_unknown_operation():
    with pytest.raises(OperationError, match="Unknown operation"):
        Calculation(operation="Unknown", operand1=Decimal("5"), operand2=Decimal("3"))


# Checks that the to_dict() method of the Calculation class correctly converts the 
    # object into a dictionary with string values — suitable for saving (e.g., to JSON or a file).
def test_to_dict():
    calc = Calculation(operation="Power", operand1=Decimal("3"), operand2=Decimal("5"))
    result_dict = calc.to_dict()
    assert result_dict == {
        "operation": "Power",
        "operand1": "3",
        "operand2": "5",
        "result": "243",
        "timestamp": calc.timestamp.isoformat()
    }


# Verifies that the from_dict() method of the Calculation class correctly
    # reconstructs a Calculation object from a dictionary.
def test_from_dict():
    data = {
        "operation": "Power",
        "operand1": "3",
        "operand2": "5",
        "result": "243",
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation == "Power"
    assert calc.operand1 == Decimal("3")
    assert calc.operand2 == Decimal("5")
    assert calc.result == Decimal("243")


def test_invalid_from_dict():
    data = {
        "operation": "Power",
        "operand1": "invalid",
        "operand2": "6",
        "result": "15",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)


# Checks the format_result function in Calculation
def test_format_result():
    calc = Calculation(operation="PercentageCalculation", operand1=Decimal("43"), operand2=Decimal("76"))
    assert calc.format_result(precision=2) == "56.58"
    assert calc.format_result(precision=10) == "56.5789473684"


# Checks that the equality comparison (==) works correctly for instances 
    # of the Calculation class by using the __eq__ method
def test_equality():
    calc1 = Calculation(operation="Modulus", operand1=Decimal("5"), operand2=Decimal("3"))
    calc2 = Calculation(operation="Modulus", operand1=Decimal("5"), operand2=Decimal("3"))
    calc3 = Calculation(operation="Power", operand1=Decimal("9"), operand2=Decimal("3"))
    assert calc1 == calc2
    assert calc1 != calc3

# New Test to Cover Logging Warning
def test_from_dict_result_mismatch(caplog):
    """
    Test the from_dict method to ensure it logs a warning when the saved result
    does not match the computed result.
    """
    # Arrange
    data = {
        "operation": "Power",
        "operand1": "2",
        "operand2": "3",
        "result": "10",  # Incorrect result to trigger logging.warning
        "timestamp": datetime.now().isoformat()
    }

    # Act
    # It temporarily listens for WARNING logs while running Calculation.from_dict(data), 
        # so the test can verify that a warning was actually logged.
    # from_dict runs above data calculation, then checks this: if calc.result != saved_result
    with caplog.at_level(logging.WARNING):
        calc = Calculation.from_dict(data)

    # Assert
    assert "Loaded calculation result 10 differs from computed result 8" in caplog.text

# covers return f"{self.operation}({self.operand1}, {self.operand2}) = {self.result}"
    # in __str__ method
def test_calculation_str_returns_expected_string():
    calc = Calculation(operation="Root", operand1=16, operand2=2)
    calc.result = 4

    output = str(calc)
    assert output == "Root(16, 2) = 4"

# tests return (
            # f"Calculation(operation='{self.operation}', "
            # f"operand1={self.operand1}, "
            # f"operand2={self.operand2}, "
            # f"result={self.result}, "
            # f"timestamp='{self.timestamp.isoformat()}')"
        # ) in __repr__ method
def test_calculation_repr_returns_expected_format():
    calc = Calculation(operation="Power", operand1=2, operand2=5)
    calc.result = 32
    calc.timestamp = datetime(2024, 1, 1, 12, 0, 0)

    expected = (
        "Calculation(operation='Power', "
        "operand1=2, operand2=5, result=32, "
        "timestamp='2024-01-01T12:00:00')"
    )

    actual = repr(calc)
    print(f"\nActual repr: {actual}")  # debug print
    assert actual == expected

# checks if other is an instance of Calculation
        # if not isinstance(other, Calculation):
           # return NotImplemented
def test_calculation_eq_returns_not_implemented_for_non_calculation():
    calc = Calculation(operation="Power", operand1=5, operand2=3)
    result = (calc == "not a calculation")

    # Python automatically converts NotImplemented into False for `==` operator
    # So we can check that the comparison result is False...
    assert result is False

    # ...but to *truly* verify it returned NotImplemented, we call __eq__ directly
    eq_result = calc.__eq__("not a calculation")
    assert eq_result is NotImplemented