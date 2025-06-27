### Calculator Config ###

from dataclasses import dataclass
from decimal import Decimal
from numbers import Number
from pathlib import Path
import os
from typing import Optional

from dotenv import load_dotenv

from app.exceptions import ConfigurationError

# Load environment variables from a .env file into the program's environment
load_dotenv()

def get_project_root() -> Path:
    """
    Get project root directory.
    This function determines the root directory of the project by navigating up
    the directory hierarchy from the current file's location.

    Returns:
        Path: The root directory of the project
    """

    # this is the current directory (app/calculator_config.py)
    current_file = Path(__file__)

    # navigate up two directories to reach project root
    return current_file.parent.parent

@dataclass
class CalculatorConfig:
    """
    Calculator configuration settings.

    Manages all configuration parameters required by the calculator application,
    including directory paths, history size, auto-save preferences, calculation precision,
    maximum input values, and default encoding

    Configuration can be set via environment variables,
    or by passing parameters directly to the class constructor
    """

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        max_history_size: Optional[int] = None,
        auto_save: Optional[bool] = None,
        precision: Optional[int] = None,
        max_input_value: Optional[Number] = None,
        default_encoding: Optional[str] = None
    ):
        """
        Initialize configuration with environment variables and defaults.

        Args:
            base_dir (Optional[Path], optional): Base directory for the calculator. Defaults to None.
            max_history_size (Optional[int], optional): Maximum number of history entries. Defaults to None.
            auto_save (Optional[bool], optional): Whether to auto-save history. Defaults to None.
            precision (Optional[int], optional): Number of decimal places for calculations. Defaults to None.
            max_input_value (Optional[Number], optional): Maximum allowed input value. Defaults to None.
            default_encoding (Optional[str], optional): Default encoding for file operations. Defaults to None.
        """

        # set base directory to project root by default
        project_root = get_project_root()

        # If base_dir is None or any "falsy" value (like an empty string), Python will use the fallback (Path)
        # For paths, "truthiness" is enough — None, '', or Path("") are all treated as falsy.
        self.base_dir = base_dir or Path(
            # uses str(project_root) if CALCULATOR_BASE_DIR doesnt exit
            os.getenv('CALCULATOR_BASE_DIR', str(project_root))
        ).resolve()

        # maximum history size
        self.max_history_size = max_history_size or int(
            os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '1000')
        )

        # auto save preference
        auto_save_env = os.getenv('CALCULATOR_AUTO_SAVE', 'true').lower()

        # if auto_save is true or false, use that
        # otherwise if auto_save is None, use fallback
        self.auto_save = auto_save if auto_save is not None else (
            auto_save_env == 'true' or auto_save_env == '1'
        )

        # calculation precision
        self.precision = precision or int(
            os.getenv('CALCULATOR_PRECISION', '10')
        )

        # max input value allowed
        self.max_input_value = max_input_value or Decimal(
            os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999')
        )

        # default encoding for file operations
        self.default_encoding = default_encoding or os.getenv(
            'CALCULATOR_DEFAULT_ENCODING', 'utf-8'
        )
    
    # decorator that turns a method into a read only property
    # can access this without paranthesis (___.log_dir)
    # Purpose:
        # To encapsulate logic behind a simple attribute interface.
        # To hide internal data but still expose results.
    @property
    def log_dir(self) -> Path:
        """
        Get log directory path. Determines the path where log files will be stored

        Returns:
            Path: the log directory path
        """

        # uses env variable CALCULATOR_LOG_DIR or
            # uses subdirectory called log from base_dir
        return Path(os.getenv(
            'CALCULATOR_LOG_DIR',
            str(self.base_dir / "logs")
        )).resolve()

    @property
    def history_dir(self) -> Path:
        """
        Get history file path. 
        Determines the path where calculation history will be stored

        Returns:
            Path: the history directory path
        """

        # .resolve() gives you the clean, absolute, real path on the filesystem.
        return Path(os.getenv(
            'CALCULATOR_HISTORY_DIR',
            str(self.base_dir / "history")
        )).resolve()
    
    @property
    def history_file(self) -> Path:
        """
        Get history file path. Determines the file path for storing
        calculation history in CSV format

        Returns:
            Path: the history file path
        """

        return Path(os.getenv(
            'CALCULATOR_HISTORY_FILE',
            str(self.history_dir / "calculator_history.csv")
        )).resolve()
    
    @property
    def log_file(self) -> Path:
        """
        Get log file path. Determines the file path for storing log entries

        Returns:
            Path: the log file path
        """

        return Path(os.getenv(
            'CALCULATOR_LOG_FILE',
            str(self.log_dir / "calculator.log")
        )).resolve()
    
    def validate(self) -> None:
        """
        Validate configuration settings

        Ensures that all configuration parameters meet the required criteria.
        Raises ConfigurationError if any validation fails
        """

        if self.max_history_size <= 0:
            raise ConfigurationError("max_history_size must be positive")
        if self.precision <= 0:
            raise ConfigurationError("precision must be positive")
        if self.max_input_value <= 0:
            raise ConfigurationError("max_input_value must be positive")