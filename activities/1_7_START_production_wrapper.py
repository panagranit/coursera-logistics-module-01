"""
Production-grade decorator for agent functions.

This decorator adds:
- Logging of function calls and results
- Execution timing for performance monitoring
- Standardized error handling and response formatting
- Automatic conversion of exceptions to agent-friendly format

Usage:
    from importlib import import_module
    _wrapper = import_module('1_7_START_production_wrapper')
    production_agent_function = _wrapper.production_agent_function

    @production_agent_function
    def my_function(param):
        if param <= 0:
            raise ValueError("Param must be positive")
        return {"success": True, "result": param * 2}

Learning Context:
    Provided in Activity 1.7 for learners to import and apply to their functions.
    Demonstrates the decorator pattern for cross-cutting concerns.

Benefits:
    - DRY (Don't Repeat Yourself): Write error handling once, use everywhere
    - Separation of Concerns: Business logic stays focused on business rules
    - Consistency: All functions handle errors the same way
    - Maintainability: Change logging/error handling in one place
"""

import functools
import logging
import time
from typing import Callable, Any, Dict

# WHAT: Configure logging for production agent functions
# WHY: Enable tracking of function calls and errors in production
# HOW: Set up basic logging configuration with INFO level

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def production_agent_function(func: Callable) -> Callable:
    """
    Decorator that adds production-grade infrastructure to agent functions.

    This decorator wraps agent-callable functions to provide:
    1. Automatic logging of function calls with parameters
    2. Execution timing for performance monitoring
    3. Standardized error handling (ValueError → validation errors)
    4. Consistent error response format

    The decorated function only needs to:
    - Implement business logic
    - Raise ValueError for validation errors
    - Return {"success": True, "result": ...} on success

    The decorator automatically handles:
    - Catching ValueError and formatting as validation error
    - Catching other exceptions and formatting as system error
    - Logging all calls and their outcomes
    - Measuring execution time

    Args:
        func: Function to decorate. Must return dict with "success" and "result" keys.
              Should raise ValueError for validation errors.

    Returns:
        Callable: Wrapped function with added production features

    Example:
        @production_agent_function
        def calculate_cost(weight):
            if weight <= 0:
                raise ValueError("Weight must be positive")
            return {"success": True, "result": weight * 2.5}

        # Function now automatically logs, times, and handles errors
        result = calculate_cost(10)  # Success case
        result = calculate_cost(-5)  # Validation error, handled gracefully

    Notes:
        - Decorated functions should NOT include their own try/except for ValueError
        - The decorator will catch and convert ValueError to validation error format
        - Other exceptions will be caught and converted to system error format
        - All functions return standardized {"success": ..., "result": ..., "error": ...}
    """

    # WHAT: Use functools.wraps to preserve original function metadata
    # WHY: Keeps function name, docstring, and signature intact
    # HOW: Apply @functools.wraps decorator to wrapper function

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        """
        Wrapper function that adds production features.

        Args:
            *args: Positional arguments to pass to wrapped function
            **kwargs: Keyword arguments to pass to wrapped function

        Returns:
            Dict with standardized format:
                {"success": bool, "result": Any, "error": str or None}
        """

        # WHAT: Log function invocation with all parameters
        # WHY: Track function usage for debugging and monitoring
        # HOW: Log function name with args and kwargs

        func_name = func.__name__
        logger.info(f"Calling {func_name} with args={args}, kwargs={kwargs}")

        # WHAT: Record start time for performance measurement
        # WHY: Monitor function execution time for optimization
        # HOW: Capture current timestamp before execution

        start_time = time.time()

        try:
            # WHAT: Execute the wrapped function with original arguments
            # WHY: Perform the actual business logic
            # HOW: Call function and capture result

            result = func(*args, **kwargs)

            # WHAT: Calculate execution time
            # WHY: Provide performance metrics
            # HOW: Subtract start time from current time

            execution_time = time.time() - start_time

            # WHAT: Log successful completion with timing
            # WHY: Track successful operations and performance
            # HOW: Log at INFO level with execution time

            logger.info(
                f"{func_name} completed successfully in {execution_time:.4f} seconds"
            )

            # WHAT: Return the function's result unchanged
            # WHY: Decorator should not modify successful responses
            # HOW: Pass through the result dictionary

            return result

        except ValueError as e:
            # WHAT: Handle validation errors (expected business rule violations)
            # WHY: Convert validation exceptions to standardized error responses
            # HOW: Return error dict with error_type="validation"

            execution_time = time.time() - start_time

            # WHAT: Log validation error with details
            # WHY: Track validation failures for debugging
            # HOW: Log at WARNING level (not an unexpected error)

            logger.warning(
                f"{func_name} validation error after {execution_time:.4f}s: {str(e)}"
            )

            # WHAT: Return standardized validation error response
            # WHY: Agents need consistent error format to handle failures
            # HOW: Return dict with success=False and error_type="validation"

            return {
                "success": False,
                "result": None,
                "error": str(e),
                "error_type": "validation"
            }

        except Exception as e:
            # WHAT: Handle unexpected system errors
            # WHY: Catch any unforeseen issues and return in standardized format
            # HOW: Return error dict with error_type="system"

            execution_time = time.time() - start_time

            # WHAT: Log unexpected error with details
            # WHY: Track system failures for debugging and fixing
            # HOW: Log at ERROR level (unexpected failure)

            logger.error(
                f"{func_name} system error after {execution_time:.4f}s: {str(e)}",
                exc_info=True  # Include stack trace in log
            )

            # WHAT: Return standardized system error response
            # WHY: Agents need to know this is an unexpected error, not validation
            # HOW: Return dict with success=False and error_type="system"

            return {
                "success": False,
                "result": None,
                "error": f"Unexpected error: {str(e)}",
                "error_type": "system"
            }

    # WHAT: Return the wrapper function
    # WHY: This is what replaces the original function when decorator is applied
    # HOW: Return wrapper that has original function's metadata

    return wrapper


# WHAT: Provide usage examples when module is run directly
# WHY: Demonstrate decorator usage and benefits
# HOW: Show before/after comparison and test cases

if __name__ == "__main__":
    print("=" * 70)
    print("PRODUCTION DECORATOR USAGE EXAMPLES")
    print("=" * 70)

    # WHAT: Example function using the decorator
    # WHY: Show how to apply decorator to agent functions
    # HOW: Use @production_agent_function syntax

    @production_agent_function
    def calculate_simple_cost(weight: float) -> Dict[str, Any]:
        """
        Calculate simple cost with validation.

        This function demonstrates decorator usage.
        Notice: No try/except needed! Decorator handles errors.
        """
        # WHAT: Validate input
        # WHY: Ensure weight is valid
        # HOW: Raise ValueError for invalid input

        if not isinstance(weight, (int, float)):
            raise ValueError(f"Weight must be a number, got {type(weight).__name__}")

        if weight <= 0:
            raise ValueError(f"Weight must be positive, got {weight}")

        # WHAT: Calculate cost
        # WHY: Apply business logic
        # HOW: Simple multiplication

        cost = weight * 2.5

        # WHAT: Return success response
        # WHY: Standard format for agent
        # HOW: Return dict with success=True

        return {
            "success": True,
            "result": round(cost, 2),
            "error": None
        }

    # Test the decorated function
    print("\nTest 1: Valid input (weight=10)")
    result1 = calculate_simple_cost(10.0)
    print(f"Result: {result1}\n")

    print("Test 2: Validation error (weight=-5)")
    result2 = calculate_simple_cost(-5.0)
    print(f"Result: {result2}\n")

    print("Test 3: Type error (weight='invalid')")
    result3 = calculate_simple_cost("invalid")
    print(f"Result: {result3}\n")

    print("=" * 70)
    print("KEY BENEFITS")
    print("=" * 70)
    print("""
    1. No try/except needed in function
    2. Automatic logging of all calls
    3. Automatic timing of execution
    4. Consistent error format
    5. Easier to maintain and test

    Your task in Activity 1.7:
    - Import this decorator
    - Apply it to your logistics functions
    - Remove try/except blocks from your functions
    - Functions will be cleaner and more maintainable!
    """)
