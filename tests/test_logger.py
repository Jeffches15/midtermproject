from unittest.mock import Mock, patch

import pytest

from app.calculation import Calculation
from app.logger import LoggingObserver

# Sample setup for mock calculation
calculation_mock = Mock(spec=Calculation)
calculation_mock.operation = "power"
calculation_mock.operand1 = 3
calculation_mock.operand2 = 4
calculation_mock.result = 81


@patch('logging.info')
def test_logging_observer_logs_calculation(logging_info_mock):
    observer = LoggingObserver()
    observer.update(calculation_mock)
    logging_info_mock.assert_called_once_with(
        "Calculation performed: power (3, 4) = 81"
    )

def test_logging_observer_no_calculation():
    observer = LoggingObserver()
    with pytest.raises(AttributeError):
        observer.update(None)  # Passing None should raise an exception as there's no calculation