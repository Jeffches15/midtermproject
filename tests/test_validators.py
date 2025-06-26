import pytest
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator  # adjust as per your file structure

# Sample configuration with a max input value of 1 million for testing purposes
config = CalculatorConfig(max_input_value=Decimal('1000000'))

# Test cases for InputValidator.validate_number

# converts 128 into Decimal('123'), makes sure number is less than config value (1000000)
def test_validate_number_positive_integer():
    assert InputValidator.validate_number(128, config) == Decimal('128')

def test_validate_number_positive_decimal():
    assert InputValidator.validate_number(444.555, config) == Decimal('444.555').normalize()

def test_validate_number_positive_string_integer():
    assert InputValidator.validate_number("653", config) == Decimal('653')

def test_validate_number_positive_string_decimal():
    assert InputValidator.validate_number("221.784", config) == Decimal('221.784').normalize()

def test_validate_number_negative_integer():
    assert InputValidator.validate_number(-622, config) == Decimal('-622')

def test_validate_number_negative_decimal():
    assert InputValidator.validate_number(-888.12, config) == Decimal('-888.12').normalize()

def test_validate_number_negative_string_integer():
    assert InputValidator.validate_number("-221", config) == Decimal('-221')

def test_validate_number_negative_string_decimal():
    assert InputValidator.validate_number("-75.12", config) == Decimal('-75.12').normalize()

def test_validate_number_zero():
    assert InputValidator.validate_number(0, config) == Decimal('0')

# value = value.strip() strips the white space
def test_validate_number_trimmed_string():
    assert InputValidator.validate_number("  863  ", config) == Decimal('863')

# Negative test cases
def test_validate_number_invalid_string():
    with pytest.raises(ValidationError, match="Invalid number format: abc"):
        InputValidator.validate_number("abc", config)

def test_validate_number_exceeds_max_value():
    with pytest.raises(ValidationError, match="Value exceeds maximum allowed"):
        InputValidator.validate_number(Decimal('1000001'), config)

def test_validate_number_exceeds_max_value_string():
    with pytest.raises(ValidationError, match="Value exceeds maximum allowed"):
        InputValidator.validate_number("1000001", config)

def test_validate_number_exceeds_negative_max_value():
    with pytest.raises(ValidationError, match="Value exceeds maximum allowed"):
        InputValidator.validate_number(-Decimal('1000001'), config)

def test_validate_number_empty_string():
    with pytest.raises(ValidationError, match="Invalid number format: "):
        InputValidator.validate_number("", config)

def test_validate_number_whitespace_string():
    with pytest.raises(ValidationError, match="Invalid number format: "):
        InputValidator.validate_number("   ", config)

def test_validate_number_none_value():
    with pytest.raises(ValidationError, match="Invalid number format: None"):
        InputValidator.validate_number(None, config)

def test_validate_number_non_numeric_type():
    with pytest.raises(ValidationError, match="Invalid number format: "):
        InputValidator.validate_number([], config)