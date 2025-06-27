### History Management

from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculation import Calculation


# Purpose: Define a common interface (update) for all observers.
# Why? This enforces that any class claiming to be a HistoryObserver must implement update.
# Pattern: This is the Observer Design Pattern, which supports extensibility and modularity.
class HistoryObserver(ABC):
    """
    abstract base class for calculator observers.

    This class defines the interface for observers that monitor and react to
    new calculation events. Implementing classes must provide an update method
    to handle the received Calculation instance.
    """

    @abstractmethod
    def update(self, calculation: Calculation) -> None:
        """
        Handle new calculation event.

        Args:
            calculation (Calculation): the calculation that was performed
        """
        pass # pragma: no cover
    

# Purpose: Automatically saves the calculator's history if auto_save is enabled.
# How it works:
    # Takes a calculator instance that must have:
    # .config with an auto_save flag.
    # .save_history() method to save the history.

# Behavior:
    # On each new calculation, checks the config.auto_save setting.
    # If true, calls save_history() and logs that the history was saved
class AutoSaveObserver(HistoryObserver):
    """
    Observer that automatically saves calculations.

    implements the observer pattern by listening for new calculations and
    triggering an automatic save of the calculation history if the auto-save
    feature is enabled in the configuration
    """

    def __init__(self, calculator: Any):
        """
        Initialize the AutoSaveObserver.

        Args:
            calculator (Any): the calculator instance to interact with.
                Must have 'config' and 'save_history' attributes
        Raises:
            TypeError: If the calculator does not have the required attributes.
        """
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        """
        Trigger auto-save.

        This method is called whenever a new calculation is performed. If the
        auto-save feature is enabled, it saves the current calculation history

        Args:
            calculation (Calculation): The calculation that was performed
        """
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")
