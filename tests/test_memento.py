import datetime
from unittest.mock import MagicMock
from app.calculator_memento import CalculatorMemento
from app.calculation import Calculation

# return cls(
        # history=[Calculation.from_dict(calc) for calc in data['history']],
        # timestamp=datetime.datetime.fromisoformat(data['timestamp'])
    # )
def test_calculator_memento_from_dict(monkeypatch):
    # This simulates what the saved history might look like in a file (as a dictionary).
    sample_data = {
        'history': [
            {
                'operation': 'Power',
                'operand1': '2',
                'operand2': '4',
                'result': '16',
                'timestamp': '2023-01-01T12:00:00'
            }
        ],
        'timestamp': '2023-01-01T12:00:00'
    }

    # Instead of creating a real Calculation object, we create a fake one 
        # (a "mock") so we can focus only on testing from_dict() for the memento.
    fake_calc = MagicMock(name="CalculationInstance")

    # This says: “Whenever Calculation.from_dict() is called during this test, 
        # just return the fake_calc — don’t run the real method.”
    monkeypatch.setattr(Calculation, "from_dict", lambda d: fake_calc)

    # It tries to create a CalculatorMemento from the dictionary. 
        # Internally, it would call Calculation.from_dict(...), but now it returns your fake_calc.
    memento = CalculatorMemento.from_dict(sample_data)

    # Checks that CalculatorMemento.from_dict() sets the timestamp and history correctly.
    assert isinstance(memento, CalculatorMemento)
    assert memento.timestamp == datetime.datetime.fromisoformat(sample_data['timestamp'])
    assert memento.history == [fake_calc]
    

# return {
            # 'history': [calc.to_dict() for calc in self.history],
            # 'timestamp': self.timestamp.isoformat()
        # }
def test_calculator_memento_to_dict():
    calc1 = Calculation(
        operation='Power',
        operand1=2,
        operand2=3,
        timestamp=datetime.datetime(2023, 1, 1, 12, 0, 0)
    )
    calc1.result = 8  # assign result attribute after init

    calc2 = Calculation(
        operation='Root',
        operand1=16,
        operand2=2,
        timestamp=datetime.datetime(2023, 1, 2, 13, 30, 0)
    )
    calc2.result = 4

    # creates a memento using the 2 Calculations created above, with one timestamp
    memento = CalculatorMemento(history=[calc1, calc2], timestamp=datetime.datetime(2023, 1, 3, 10, 0, 0))

    # coverts memento into dictionary
    d = memento.to_dict()

    # It has the expected top-level keys:
    assert 'history' in d
    assert 'timestamp' in d

    assert isinstance(d['history'], list) # history is a list
    assert all(isinstance(item, dict) for item in d['history']) # Each item in the history is a dictionary:
    assert d['timestamp'] == '2023-01-03T10:00:00' # The timestamp is correctly formatted as ISO:

    # Every calculation dict contains the required keys:
    expected_keys = {'operation', 'operand1', 'operand2', 'result', 'timestamp'}
    for calc_dict in d['history']:
        assert expected_keys.issubset(calc_dict.keys())
