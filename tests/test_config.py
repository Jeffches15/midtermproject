import pytest
import os
from decimal import Decimal
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError

# Set up temporary environment variables for testing
os.environ['CALCULATOR_MAX_HISTORY_SIZE'] = '500'
os.environ['CALCULATOR_AUTO_SAVE'] = 'false'
os.environ['CALCULATOR_PRECISION'] = '8'
os.environ['CALCULATOR_MAX_INPUT_VALUE'] = '1000'
os.environ['CALCULATOR_DEFAULT_ENCODING'] = 'utf-16'
os.environ['CALCULATOR_LOG_DIR'] = './test_logs'
os.environ['CALCULATOR_HISTORY_DIR'] = './test_history'
os.environ['CALCULATOR_HISTORY_FILE'] = './test_history/test_history.csv'
os.environ['CALCULATOR_LOG_FILE'] = './test_logs/test_log.log'

# Helper function to clear specific environment variables
def clear_env_vars(*args):
    for var in args:
        os.environ.pop(var, None)

# Your current test covers default value assignment inside __init__
def test_default_configuration():
    config = CalculatorConfig()
    assert config.max_history_size == 500
    assert config.auto_save is False
    assert config.precision == 8
    assert config.max_input_value == Decimal("1000")
    assert config.default_encoding == 'utf-16'
    assert config.log_dir == Path('./test_logs').resolve()
    assert config.history_dir == Path('./test_history').resolve()
    assert config.history_file == Path('./test_history/test_history.csv').resolve()
    assert config.log_file == Path('./test_logs/test_log.log').resolve()


# log_dir defaults to base_dir / "logs" when CALCULATOR_LOG_DIR is not set.
# history_dir defaults to base_dir / "history" when CALCULATOR_HISTORY_DIR is not set.
def test_directory_properties():
    clear_env_vars('CALCULATOR_LOG_DIR', 'CALCULATOR_HISTORY_DIR')
    config = CalculatorConfig(base_dir=Path('/custom_base_dir'))
    assert config.log_dir == Path('/custom_base_dir/logs').resolve()
    assert config.history_dir == Path('/custom_base_dir/history').resolve()

# history_file defaults to base_dir / "history" / "calculator_history" when
    # CALCULATOR_HISTORY_FILE is not set
# log_file defaults to base_dir / "logs" / "calculator_log" when
    # CALCULATOR_LOG_FILE is not set
def test_file_properties():
    clear_env_vars('CALCULATOR_HISTORY_FILE', 'CALCULATOR_LOG_FILE')
    config = CalculatorConfig(base_dir=Path('/custom_base_dir'))
    assert config.history_file == Path('/custom_base_dir/history/calculator_history.csv').resolve()
    assert config.log_file == Path('/custom_base_dir/logs/calculator.log').resolve()

# if self.max_history_size <= 0:
    # raise ConfigurationError("max_history_size must be positive")
def test_invalid_max_history_size():
    with pytest.raises(ConfigurationError, match="max_history_size must be positive"):
        config = CalculatorConfig(max_history_size=-1)
        config.validate()

# if self.precision <= 0:
    # raise ConfigurationError("precision must be positive")
def test_invalid_precision():
    with pytest.raises(ConfigurationError, match="precision must be positive"):
        config = CalculatorConfig(precision=-1)
        config.validate()

# if self.max_input_value <= 0:
    # raise ConfigurationError("max_input_value must be positive")
# def test_invalid_max_input_value():
#     with pytest.raises(ConfigurationError, match="max_input_value must be positive"):
#         config = CalculatorConfig(max_input_value=Decimal("-2"))
#         config.validate()

import pytest
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError

# not getting covered at the moment
def test_invalid_max_input_value():
    config = CalculatorConfig(max_input_value=Decimal("-2"))
    with pytest.raises(ConfigurationError, match="max_input_value must be positive"):
        config.validate()




