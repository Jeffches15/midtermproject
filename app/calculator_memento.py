### Calculator Memento ###

from dataclasses import dataclass, field
import datetime
from typing import Any, Dict, List

from app.calculation import Calculation

# to_dict() is an instance method because it needs access 
    # to self — it works on an existing object.

# from_dict() is a class method because it creates a new object from a dictionary, 
    # and doesn’t require an existing instance.

# to_dict() → Take a machine and draw blueprints from it
# from_dict() → Take blueprints and build a machine from them

@dataclass
class CalculatorMemento:
    """
    Stores calculator state for undo/redo functionality.

    The Memento pattern allows the Calculator to save its current state (history)
    so that it can be restored later. This enables features like undo and redo.
    """

    history: List[Calculation] # list of Calculation instances representing the calculator's history

    # When a new instance of the dataclass is created without specifying timestamp,
        # it will automatically set it to the current time using datetime.datetime.now().
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts memento to dictionary. This method serializes the memento's state into a
        dictionary format, making it easy to store or transmit
        """

        # self.history is a collection (like a list) of Calculation objects (or similar).
        # For each calc (which is a Calculation instance), it calls calc.to_dict().
        # This code returns one overall timestamp, like when the entire history snapshot was created or saved.
        return {
            'history': [calc.to_dict() for calc in self.history],
            'timestamp': self.timestamp.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Calculation':
        """
        Create memento from dictionary. This class method deserializes a dictionary to
        recreate a CalculatorMemento instance, restoring the calculator's history and timestamp
        """

        # Create a new instance of the class (CalculatorMemento).
        # history=[Calculation.from_dict(calc) for calc in data['history']]:
        # For each item in the data['history'] list (which is itself a dictionary representing a calculation), 
            # call Calculation.from_dict(calc) recursively to turn each dict back into a Calculation object.
        return cls(
            history=[Calculation.from_dict(calc) for calc in data['history']],
            timestamp=datetime.datetime.fromisoformat(data['timestamp'])
        )