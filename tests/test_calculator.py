import datetime
from pathlib import Path
from sys import exc_info
import pandas as pd
import pytest
from unittest.mock import Mock, patch, PropertyMock, MagicMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.calculation import Calculation
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver
from app.operations import OperationFactory, IntegerDivision
from app.logger import LoggingObserver
import logging

# Fixture to initialize Calculator with a temporary directory for file paths
@pytest.fixture
def calculator():
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        config = CalculatorConfig(base_dir=temp_path)

        # Patch properties to use the temporary directory paths
        with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
             patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file, \
             patch.object(CalculatorConfig, 'history_dir', new_callable=PropertyMock) as mock_history_dir, \
             patch.object(CalculatorConfig, 'history_file', new_callable=PropertyMock) as mock_history_file:
            
            # Set return values to use paths within the temporary directory
            mock_log_dir.return_value = temp_path / "logs"
            mock_log_file.return_value = temp_path / "logs/calculator.log"
            mock_history_dir.return_value = temp_path / "history"
            mock_history_file.return_value = temp_path / "history/calculator_history.csv"
            
            # Return an instance of Calculator with the mocked config
            yield Calculator(config=config)


# Test Calculator Initialization
def test_calculator_initialization(calculator):
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []
    assert calculator.operation_strategy is None


# Test Logging Setup
@patch('app.calculator.logging.info')
def test_logging_setup(logging_info_mock):
    with patch.object(CalculatorConfig, 'log_dir', new_callable=PropertyMock) as mock_log_dir, \
         patch.object(CalculatorConfig, 'log_file', new_callable=PropertyMock) as mock_log_file:
        mock_log_dir.return_value = Path('/tmp/logs')
        mock_log_file.return_value = Path('/tmp/logs/calculator.log')
        
        # Instantiate calculator to trigger logging
        calculator = Calculator(CalculatorConfig())
        logging_info_mock.assert_any_call("Calculator initialized with configuration")


# Test Adding and Removing Observers
def test_add_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    assert observer in calculator.observers

def test_remove_observer(calculator):
    observer = LoggingObserver()
    calculator.add_observer(observer)
    calculator.remove_observer(observer)
    assert observer not in calculator.observers

# Test Setting Operations
def test_set_operation(calculator):
    operation = OperationFactory.create_operation('percentage-calculation')
    calculator.set_operation(operation)
    assert calculator.operation_strategy == operation


# Test Performing Operations
def test_perform_operation_addition(calculator):
    operation = OperationFactory.create_operation('power')
    calculator.set_operation(operation)
    result = calculator.perform_operation(6, 2)
    assert result == Decimal('36')

def test_perform_operation_validation_error(calculator):
    calculator.set_operation(OperationFactory.create_operation('power'))
    with pytest.raises(ValidationError):
        calculator.perform_operation('invalid', 7)

def test_perform_operation_operation_error(calculator):
    with pytest.raises(OperationError, match="No operation set"):
        calculator.perform_operation(3, 8)


# Test Undo/Redo Functionality

def test_undo(calculator):
    operation = OperationFactory.create_operation('power')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 5)
    calculator.undo()
    assert calculator.history == []

def test_redo(calculator):
    operation = OperationFactory.create_operation('power')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 5)
    calculator.undo()
    calculator.redo()
    assert len(calculator.history) == 1


# Test History Management

@patch('app.calculator.pd.DataFrame.to_csv')
def test_save_history(mock_to_csv, calculator):
    operation = OperationFactory.create_operation('root')
    calculator.set_operation(operation)
    calculator.perform_operation(16, 4)
    calculator.save_history()
    mock_to_csv.assert_called_once()



@patch('app.calculator.pd.read_csv')
@patch('app.calculator.Path.exists', return_value=True)
def test_load_history(mock_exists, mock_read_csv, calculator):
    # Mock CSV data to match the expected format in from_dict
    # So when calculator.load_history() runs and tries to read the CSV, 
        # it receives that fake DataFrame as if it had been read from a real file.
    mock_read_csv.return_value = pd.DataFrame({
        'operation': ['Power'],
        'operand1': ['2'],
        'operand2': ['5'],
        'result': ['32'],
        'timestamp': [datetime.datetime.now().isoformat()]
    })
    
    # Test the load_history functionality
    try:
        calculator.load_history()
        # Verify history length after loading
        assert len(calculator.history) == 1
        # Verify the loaded values
        assert calculator.history[0].operation == "Power"
        assert calculator.history[0].operand1 == Decimal("2")
        assert calculator.history[0].operand2 == Decimal("5")
        assert calculator.history[0].result == Decimal("32")
    except OperationError:
        pytest.fail("Loading history failed due to OperationError")


# Test Clearing History

def test_clear_history(calculator):
    operation = OperationFactory.create_operation('power')
    calculator.set_operation(operation)
    calculator.perform_operation(2, 6)
    calculator.clear_history()
    assert calculator.history == []
    assert calculator.undo_stack == []
    assert calculator.redo_stack == []


# Test REPL Commands (using patches for input/output handling)

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Goodbye!")


@patch('builtins.input', side_effect=['help', 'exit'])
@patch('builtins.print')
def test_calculator_repl_help(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nAvailable commands:")


@patch('builtins.input', side_effect=['integer-division', '14.4', '3.1', 'exit'])
@patch('builtins.print')
def test_calculator_repl_integer_division(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nResult: 4")


# except Exception as e:
#   # Log a warning if history could not be loaded
#   logging.warning(f"Could not load existing history: {e}")
def test_load_history_logs_warning_on_failure(monkeypatch, caplog):
    def mock_load_history(self):
        raise IOError("Simulated load failure")

    monkeypatch.setattr(Calculator, "load_history", mock_load_history)
    monkeypatch.setattr(Calculator, "_setup_logging", lambda self: None)  # disable logging setup

    caplog.set_level(logging.WARNING)

    _ = Calculator()

    assert "Could not load existing history: Simulated load failure" in caplog.text

# except Exception as e:
#   # Print an error message and re-raise the exception if logging setup fails
#   print(f"Error setting up logging: {e}")
#   raise
def test_setup_logging_exception(monkeypatch, capsys):
    calc = Calculator.__new__(Calculator)  # create instance without calling __init__
    calc.config = type('Config', (), {})()  # dummy config object

    # Provide a dummy log_dir and log_file
    calc.config.log_dir = "/some/fake/dir"
    calc.config.log_file = Path("/some/fake/dir/logfile.log")

    # Mock os.makedirs to raise an exception
    def mock_makedirs_fail(path, exist_ok=True):
        raise PermissionError("No permission to create directory")

    monkeypatch.setattr("os.makedirs", mock_makedirs_fail)

    # Call _setup_logging and expect it to print error and raise
    with pytest.raises(PermissionError) as excinfo:
        calc._setup_logging()

    # Capture the stdout
    captured = capsys.readouterr()

    # Check printed error message
    assert "Error setting up logging: No permission to create directory" in captured.out

    # Check exception was re-raised
    assert "No permission to create directory" in str(excinfo.value)

# Ensure the history does not exceed the maximum size
# if len(self.history) > self.config.max_history_size:
    # self.history.pop(0)
def test_history_pop_when_max_history_exceeded():
    config = CalculatorConfig(max_history_size=3)
    calc = Calculator(config=config)
    calc.set_operation(IntegerDivision())
    calc.history.clear()

    # Use "1" only in the first operation
    calc.perform_operation("1", "1")        # Should be removed
    calc.perform_operation("6.2", "2")      # 3
    calc.perform_operation("7.23", "3.4")   # 2
    calc.perform_operation("8", "4")        # 2 → triggers pop

    assert len(calc.history) == 3
    assert all("1" not in str(c) for c in calc.history)


# # If history is empty, create an empty CSV with headers
# pd.DataFrame(columns=['operation', 'operand1', 'operand2', 'result', 'timestamp']
#                      ).to_csv(self.config.history_file, index=False)
# logging.info("Empty history saved")
def test_save_history_saves_empty_csv_and_logs(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)
    calc.history.clear()

    with patch('logging.info') as mock_log_info:
        calc.save_history()
        # Check if logging.info was called with "Empty history saved"
        mock_log_info.assert_any_call("Empty history saved")

    history_file = calc.config.history_file
    assert history_file.exists()
    content = history_file.read_text()
    assert content.startswith("operation,operand1,operand2,result,timestamp")
    assert len(content.strip().splitlines()) == 1

# except Exception as e:
    # Log and raise an OperationError if saving fails
    # logging.error(f"Failed to save history: {e}")
    # raise OperationError(f"Failed to save history: {e}")
def test_save_history_raises_operation_error_and_logs(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)

    # Create a MagicMock for a calculation with to_dict and timestamp
    mock_calc = MagicMock()
    mock_calc.to_dict.return_value = {
        'operation': 'add',
        'operand1': '1',
        'operand2': '2',
        'result': '3',
        'timestamp': datetime.datetime.now().isoformat()
    }
    mock_calc.timestamp = datetime.datetime.now()

    calc.history.append(mock_calc)

    with patch('pandas.DataFrame.to_csv', side_effect=Exception("Simulated failure")), \
         patch('logging.error') as mock_log_error:

        with pytest.raises(OperationError) as exc_info:
            calc.save_history()

        assert "Failed to save history" in str(exc_info.value)
        mock_log_error.assert_any_call("Failed to save history: Simulated failure")


# except Exception as e:
#             # Log and raise an OperationError if loading fails
#             logging.error(f"Failed to load history: {e}")
#             raise OperationError(f"Failed to load history: {e}")
def test_load_history_exception_logging_and_reraise(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)

    # Create empty file so .exists() returns True and code tries to read CSV
    calc.config.history_file.touch()

    # Patch pandas.read_csv to raise an exception to simulate load failure
    with patch('pandas.read_csv', side_effect=Exception("Simulated load failure")), \
         patch('logging.error') as mock_log_error:

        with pytest.raises(OperationError) as exc_info:
            calc.load_history()

        # Check OperationError message contains expected substring
        assert "Failed to load history" in str(exc_info.value)

        # Confirm logging.error was called with correct error message
        mock_log_error.assert_any_call("Failed to load history: Simulated load failure")


# history_data = []
# for calc in self.history:
#   history_data.append({
#         'operation': str(calc.operation),
#         'operand1': str(calc.operand1),
#         'operand2': str(calc.operand2),
#         'result': str(calc.result),
#         'timestamp': calc.timestamp
#     })
# return pd.DataFrame(history_data)
def test_history_data_list_and_dataframe(tmp_path):
    config = CalculatorConfig(base_dir=tmp_path)
    calc = Calculator(config=config)

    # Add Calculation instances to history
    calc1 = Calculation(
        operation='Power',
        operand1=Decimal('5'),
        operand2=Decimal('2'),
        timestamp=datetime.datetime(2023, 5, 10, 15, 30, 0)
    )
    calc1.result = Decimal('25.0')  # assign result attribute after init

    calc2 = Calculation(
        operation='Root',
        operand1=Decimal('64'),
        operand2=Decimal('2'),
        timestamp=datetime.datetime(2023, 5, 11, 16, 45, 0)
    )
    calc2.result = Decimal('8')
    calc.history = [calc1, calc2]


    # Call method that contains those lines
    df = calc.get_history_dataframe()

    # Check type and shape of resulting DataFrame
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2
    assert set(df.columns) == {'operation', 'operand1', 'operand2', 'result', 'timestamp'}

    # Check data was converted to strings except timestamp
    assert df.loc[0, 'operation'] == 'Power'
    assert df.loc[0, 'operand1'] == '5'
    assert df.loc[0, 'operand2'] == '2'
    assert df.loc[0, 'result'] == '25.0'
    assert df.loc[0, 'timestamp'] == datetime.datetime(2023, 5, 10, 15, 30, 0)

    assert df.loc[1, 'operation'] == 'Root'
    assert df.loc[1, 'operand1'] == '64'
    assert df.loc[1, 'operand2'] == '2'
    assert df.loc[1, 'result'] == '8'
    assert df.loc[1, 'timestamp'] == datetime.datetime(2023, 5, 11, 16, 45, 0)

# return [
#   f"{calc.operation}({calc.operand1}, {calc.operand2}) = {calc.result}"
#   for calc in self.history
# ]
def test_show_history_returns_correct_strings():

    # Setup a Calculator instance (with config if needed)
    calc = Calculator()

    # Create Calculation instances and set their attributes
    calc1 = Calculation(
        operation="Power",
        operand1=Decimal('4'),
        operand2=Decimal('3'),
        timestamp=datetime.datetime.now()
    )
    calc1.result = Decimal('64')

    calc2 = Calculation(
        operation="Root",
        operand1=Decimal('100'),
        operand2=Decimal('2'),
        timestamp=datetime.datetime.now()
    )
    calc2.result = Decimal('10')

    # Assign to history
    calc.history = [calc1, calc2]

    # Call show_history
    history_strings = calc.show_history()

    # Assert the output is a list of correct formatted strings
    assert history_strings == [
        "Power(4, 3) = 64",
        "Root(100, 2) = 10"
    ]

# if not self.undo_stack:
#     return False
def test_undo_returns_false_when_undo_stack_empty():
    calc = Calculator()  # new instance, undo_stack should be empty
    calc.undo_stack.clear()  # explicitly clear to be sure

    result = calc.undo()

    assert result is False

# if not self.redo_stack:
#   return False
def test_redo_returns_false_when_redo_stack_empty():
    calc = Calculator() # new instance of Calculator, redo_stack should be empty
    calc.redo_stack.clear()

    result = calc.redo()

    assert result is False


