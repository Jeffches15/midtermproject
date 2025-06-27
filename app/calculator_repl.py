### Calculator REPL ###

from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver
from app.logger import LoggingObserver
from app.operations import OperationFactory

def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
    try:
        # initialize the Calculator instance
        calc = Calculator()

        # register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print("Calculator started. Type 'help' for commands.")

        while True:
            try:
                # prompt the user for a command
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    # display available commands
                    print("\nAvailable commands:")
                    print("  power, root, modulus, integer-division, percentage-calculation, absolute-difference - Perform calculations")
                    print("  history - Show calculation history")
                    print("  clear - Clear calculation history")
                    print("  undo - Undo the last calculation")
                    print("  redo - Redo the last undone calculation")
                    print("  save - Save calculation history to file")
                    print("  load - Load calculation history from file")
                    print("  exit - Exit the calculator")
                    continue
                if command == 'exit':
                    # attempt to save history before exiting
                    try:
                        calc.save_history()
                        print("History saved successfully.")
                    except Exception as e:
                        print(f"Warning: Could not save history: {e}")
                    print("Goodbye!")
                    break
                if command == 'history':
                    # display calculation history
                    history = calc.show_history()
                    if not history:
                        print("No calculations in history")
                    else:
                        print("\nCalculation History:")
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue
                if command == 'clear':
                    # clear calculation history
                    calc.clear_history()
                    print("History cleared")
                    continue
                if command == 'undo':
                    # undo the last calculation
                    if calc.undo():
                        print("Operation undone")
                    else:
                        print("Nothing to undo")
                    continue
                if command == 'redo':
                    # redo the last undone calculation
                    if calc.redo():
                        print("Operation redone")
                    else:
                        print("Nothing to redo")
                    continue
                if command == 'save':
                    # save calculation history to file
                    try:
                        calc.save_history()
                        print("History saved successfully")
                    except Exception as e:
                        print(f"Error saving history: {e}")
                    continue
                if command == 'load':
                    # load calculation history from file
                    try:
                        calc.load_history()
                        print("History loaded successfully")
                    except Exception as e:
                        print(f"Error loading history: {e}")
                    continue

                if command in ['power', 'root', 'modulus', 'integer-division', 
                               'percentage-calculation', 'absolute-difference']:
                    # perform the specified arithmetic operation
                    try:
                        print("\nEnter numbers (or 'cancel' to abort):")
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print("Operation cancelled")
                            continue

                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print("Operation cancelled")
                            continue

                        # create the appropriate operation instance using the factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # perform the calculation
                        result = calc.perform_operation(a,b)

                        # normalize the result if its a Decimal
                        if isinstance(result, Decimal): # pragma: no cover
                            result = result.normalize()

                        print(f"\nResult: {result}")
                    except (ValidationError, OperationError) as e:
                        # handle known exceptions related to validation or operation errors
                        print(f"Error: {e}")
                    except Exception as e:
                        # handle any unexpected exceptions
                        print(f"Unexpected error: {e}")
                    continue

                # handle unknown commands
                print(f"Unknown command: '{command}'. Type 'help' for available commands")

            except KeyboardInterrupt:
                # handle Ctrl+C interruption gracefully
                print("\nOperation cancelled")
                continue
            except EOFError:
                # handle end of file (Ctrl+D) gracefully
                print("\nInput terminated. Exiting...")
                break
            except Exception as e: # pragma: no cover
                # handle any other unexpected exceptions
                print(f"Error: {e}")
                continue

    except Exception as e:
        # handle fatal errors during initialization
        print(f"Fatal error: {e}")
        logging.error(f"fatal error in calculator REPL: {e}")
        raise