# Purpose: Logs every calculation to the logging system (usually a file).
# How it works: It gets called with a Calculation object and writes the operation, operands, 
    # and result using logging.info(...).
# Validation: Raises AttributeError if calculation is None.
import logging
from app.calculation import Calculation
from app.history import HistoryObserver


class LoggingObserver(HistoryObserver):
    """
    Observer that logs calculations to a file.

    Implements the Observer pattern by listening for new calculations and logging
    their details to a log file.
    """

    def update(self, calculation: Calculation) -> None:
        """
        Log calculation details.

        This method is called whenever a new calculation is performed. It records
        the operation, operands, and result in the log file

        Args:
            calculation (Calculation): the calculation that was performed
        """

        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        logging.info(
            f"Calculation performed: {calculation.operation} "
            f"({calculation.operand1}, {calculation.operand2}) = "
            f"{calculation.result}"
        )