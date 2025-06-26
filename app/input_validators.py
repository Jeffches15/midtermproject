### Input Validation Class ###

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError

# The purpose of a @dataclass in Python is to simplify 
    # the creation of classes that primarily store data 
@dataclass
class InputValidator:
    """Validates and sanitizes calculator inputs."""
    
    # static methods:
        # Does not receive self or cls as the first argument.
        # Does not depend on the instance or the class — it’s just grouped with the class logically.
        # You can call it with either the class or an instance
        # most limited amount of scope: (only has access to data you import through parameters)
    @staticmethod
    def validate_number(value: Any, config: CalculatorConfig) -> Decimal:
        """
        Validate and convert input to Decimal.
        
        Args:
            value: Input value to validate
            config: Calculator configuration
            
        Returns:
            Decimal: Validated and converted number
            
        Raises:
            ValidationError: If input is invalid
        """
        try:
            if isinstance(value, str): # if value is a string, remove extra white space
                value = value.strip()
            number = Decimal(str(value)) # converts to Decimal

            # if |number| exceeds max input length defined in config, raise ValidationError
            if abs(number) > config.max_input_value:
                raise ValidationError(f"Value exceeds maximum allowed: {config.max_input_value}")
            
            # removes trailing zeros and adjusts the exponent to make the number’s 
                # representation more compact and clean.
            return number.normalize()
        
        except InvalidOperation as e:
            raise ValidationError(f"Invalid number format: {value}") from e