### Calculator Class ###

from decimal import Decimal
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pandas as pd

from app.calculation import Calculation
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorMemento
from app.exceptions import OperationError, ValidationError
from app.history import HistoryObserver
from app.input_validators import InputValidator
from app.operations import Operation

# type aliases for better readability
Number = Union[int, float, Decimal]
CalculationResult = Union[Number, str]

class Calculator:
    """
    Main calculator class implementing multiple design patterns to enhance
    flexibility, maintainability and scalability.

    Core of calculator application, managing operations, calculation history,
    observers, configuration settings, and data persistence
    """

    def __init__(self, config: Optional[CalculatorConfig] = None):
        """
        Initialize calculator with configuration.

        Args:
            config (Optional[CalculatorConfig], optional): Configuration settings for the calculator
            if not provided, default settings are loaded based on env variables
        """

        if config is None:
            # determine the project root directory if no configuration is provided
            # __file__ contains the path to the current Python file being executed.
            current_file = Path(__file__)
            project_root = current_file.parent.parent
            config = CalculatorConfig(base_dir=project_root)
        
        # Assign the configuration and validate its parameters
        self.config = config
        self.config.validate()

        # Ensure that the log directory exists
        os.makedirs(self.config.log_dir, exist_ok=True)

        # Set up the logging system
        self._setup_logging()

        # Initialize calculation history and operation strategy
        self.history: List[Calculation] = []
        self.operation_strategy: Optional[Operation] = None

        # Initialize observer list for the Observer pattern
        self.observers: List[HistoryObserver] = []

        # Initialize stacks for undo and redo functionality using the Memento pattern
        self.undo_stack: List[CalculatorMemento] = []
        self.redo_stack: List[CalculatorMemento] = []

        # Create required directories for history management
        self._setup_directories()

        try:
            # Attempt to load existing calculation history from file
            self.load_history()
        except Exception as e:
            # Log a warning if history could not be loaded
            logging.warning(f"Could not load existing history: {e}")

        # Log the successful initialization of the calculator
        logging.info("Calculator initialized with configuration")

    def _setup_logging(self) -> None:
        """
        Configure the logging system.

        Sets up logging to a file with a specified format and log level.
        """
        try:
            # Ensure the log directory exists
            os.makedirs(self.config.log_dir, exist_ok=True)
            log_file = self.config.log_file.resolve()

            # Configure the basic logging settings
            # how your log messages look when they're written to a file 
                # or printed to the console using Python’s logging module:
                # %(asctime)s	Timestamp of when the log entry was created
                # %(levelname)s	The severity level of the log (e.g., INFO, ERROR, etc.)
                # %(message)s	The actual log message text that you passed in
            logging.basicConfig(
                filename=str(log_file),
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                force=True  # Overwrite any existing logging configuration
            )
            logging.info(f"Logging initialized at: {log_file}")
        except Exception as e:
            # Print an error message and re-raise the exception if logging setup fails
            print(f"Error setting up logging: {e}")
            raise

    def _setup_directories(self) -> None:
        """
        Create required directories.

        Ensures that all necessary directories for history management exist.
        """
        self.config.history_dir.mkdir(parents=True, exist_ok=True)

    def add_observer(self, observer: HistoryObserver) -> None:
        """
        Register a new observer.

        Adds an observer to the list, allowing it to receive updates when new
        calculations are performed.

        Args:
            observer (HistoryObserver): The observer to be added.
        """
        self.observers.append(observer)
        logging.info(f"Added observer: {observer.__class__.__name__}")

    def remove_observer(self, observer: HistoryObserver) -> None:
        """
        Remove an existing observer.

        Removes an observer from the list, preventing it from receiving further updates.

        Args:
            observer (HistoryObserver): The observer to be removed.
        """
        self.observers.remove(observer)
        logging.info(f"Removed observer: {observer.__class__.__name__}")

    def notify_observers(self, calculation: Calculation) -> None:
        """
        Notify all observers of a new calculation.

        Iterates through the list of observers and calls their update method,
        passing the new calculation as an argument.

        Args:
            calculation (Calculation): The latest calculation performed.
        """
        for observer in self.observers:
            observer.update(calculation)

    def set_operation(self, operation: Operation) -> None:
        """
        Set the current operation strategy.

        Assigns the operation strategy that will be used for performing calculations.
        This is part of the Strategy pattern, allowing the calculator to switch between
        different operation algorithms dynamically.

        Args:
            operation (Operation): The operation strategy to be set.
        """
        self.operation_strategy = operation # Root, Power, Modulus, PercentageCalculation, etc.
        logging.info(f"Set operation: {operation}")

    