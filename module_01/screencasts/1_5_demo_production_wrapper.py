"""
Module: production_wrapper_demo.py
Purpose: Demonstrate the production decorator pattern using Innovate Logistics functions

This module shows the "before and after" of using a production decorator
to handle cross-cutting concerns like logging, timing, and error standardization.

Uses get_tracking_status from Innovate Logistics as a real-world example.

Learning Context:
    Demonstrated in Screencast 1.6 "From 'Working' to 'Production-Ready'"
    Shows how decorators reduce boilerplate and separate concerns using
    actual functions from the Innovate Logistics toolkit.

Key Concepts:
    - Decorator pattern for code reuse
    - Separation of concerns (business logic vs. infrastructure)
    - DRY principle (Don't Repeat Yourself)
    - Standardized error handling across functions
"""

import functools
import logging
import time
from typing import Callable, Any, Dict

# WHAT: Configure logging for demonstration
# WHY: Show how decorator can add logging without cluttering business logic
# HOW: Set up basic logging configuration with INFO level

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# WHAT: Define production decorator for agent functions
# WHY: Eliminate repetitive error handling, logging, and timing code
# HOW: Create decorator that wraps functions with standard infrastructure code

def production_agent_function(func: Callable) -> Callable:
    """
    Decorator that adds production-grade error handling, logging, and timing.

    This decorator handles three cross-cutting concerns:
    1. Logging: Logs function calls with parameters and results
    2. Timing: Measures and logs execution time
    3. Error Handling: Standardizes error responses

    The decorated function only needs to:
    - Implement business logic
    - Raise ValueError for validation errors
    - Return success dictionary on success

    Args:
        func: Function to decorate. Should return dict with {"success": ..., "result": ...}

    Returns:
        Wrapped function with added infrastructure

    Example:
        @production_agent_function
        def my_function(param):
            if param <= 0:
                raise ValueError("Param must be positive")
            return {"success": True, "result": param * 2}
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        # WHAT: Log function invocation with parameters
        # WHY: Track function usage for debugging and monitoring
        # HOW: Log function name and all arguments

        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")

        # WHAT: Record start time for performance measurement
        # WHY: Track function execution time for optimization
        # HOW: Capture time before execution

        start_time = time.time()

        try:
            # WHAT: Execute the wrapped function
            # WHY: Perform the actual business logic
            # HOW: Call function with original arguments

            result = func(*args, **kwargs)

            # WHAT: Calculate and log execution time
            # WHY: Provide performance metrics for monitoring
            # HOW: Subtract start time from current time

            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} completed successfully in {execution_time:.4f}s")

            # WHAT: Return the function's result unchanged
            # WHY: Decorator should not modify successful responses
            # HOW: Pass through the result dictionary

            return result

        except ValueError as e:
            # WHAT: Handle validation errors
            # WHY: Convert validation exceptions to standardized error responses
            # HOW: Return error dictionary with error_type="validation"

            execution_time = time.time() - start_time
            logger.warning(f"{func.__name__} validation error after {execution_time:.4f}s: {e}")

            return {
                "success": False,
                "result": None,
                "error": str(e),
                "error_type": "validation"
            }

        except Exception as e:
            # WHAT: Handle unexpected system errors
            # WHY: Catch any unforeseen issues and return standardized format
            # HOW: Return error dictionary with error_type="system"

            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} system error after {execution_time:.4f}s: {e}")

            return {
                "success": False,
                "result": None,
                "error": f"Unexpected error: {str(e)}",
                "error_type": "system"
            }

    return wrapper


# WHAT: Define mock tracking database for demonstration
# WHY: Need data for tracking status lookups
# HOW: Simple dictionary mapping codes to statuses

MOCK_TRACKING_DB = {
    "123456789": "In Transit",
    "987654321": "In Transit",
    "111111111": "Delivered",
}


# ============================================================================
# DEMONSTRATION: Before Decorator (Verbose)
# ============================================================================

def get_tracking_status_verbose(tracking_code: str) -> Dict[str, Any]:
    """
    Look up package tracking status WITHOUT using decorator.

    This is an Innovate Logistics function showing the verbose approach
    with manual logging, timing, and error handling throughout.

    Notice how the infrastructure code (logging, timing, error handling)
    obscures the simple business logic!
    """
    # WHAT: Manual logging of function call
    # WHY: Need to track usage for monitoring
    # HOW: Explicit logger.info() call

    logger.info(f"Calling get_tracking_status_verbose with tracking_code={tracking_code}")

    # WHAT: Manual timing start
    # WHY: Need to measure performance
    # HOW: Capture start time

    start_time = time.time()

    try:
        # WHAT: Validate tracking code is a string (BUSINESS LOGIC)
        # WHY: Ensure correct type before processing
        # HOW: Check type with isinstance

        if not isinstance(tracking_code, str):
            raise ValueError(
                f"Tracking code must be a string, got {type(tracking_code).__name__}"
            )

        # WHAT: Validate tracking code length (BUSINESS LOGIC)
        # WHY: Innovate Logistics codes are always 9 digits
        # HOW: Check length

        if len(tracking_code) != 9:
            raise ValueError(
                f"Tracking code must be exactly 9 digits, got {len(tracking_code)} characters"
            )

        # WHAT: Validate tracking code format (BUSINESS LOGIC)
        # WHY: Must be numeric only
        # HOW: Use isdigit() method

        if not tracking_code.isdigit():
            raise ValueError(
                "Tracking code must contain only digits (0-9)"
            )

        # WHAT: Look up status in database (BUSINESS LOGIC)
        # WHY: Retrieve current package status
        # HOW: Query mock database

        status = MOCK_TRACKING_DB.get(tracking_code, "Unknown")

        # WHAT: Manual timing end and logging
        # WHY: Record performance metric
        # HOW: Calculate duration and log

        execution_time = time.time() - start_time
        logger.info(f"get_tracking_status_verbose completed successfully in {execution_time:.4f}s")

        # WHAT: Return success response
        # WHY: Standard format for agent
        # HOW: Return dictionary

        return {
            "success": True,
            "result": status,
            "error": None
        }

    except ValueError as e:
        # WHAT: Manual validation error handling
        # WHY: Standardize error format
        # HOW: Return error dictionary

        execution_time = time.time() - start_time
        logger.warning(f"get_tracking_status_verbose validation error after {execution_time:.4f}s: {e}")

        return {
            "success": False,
            "result": None,
            "error": str(e),
            "error_type": "validation"
        }

    except Exception as e:
        # WHAT: Manual system error handling
        # WHY: Catch unexpected errors
        # HOW: Return error dictionary

        execution_time = time.time() - start_time
        logger.error(f"get_tracking_status_verbose system error after {execution_time:.4f}s: {e}")

        return {
            "success": False,
            "result": None,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "system"
        }


# ============================================================================
# DEMONSTRATION: After Decorator (Clean)
# ============================================================================

@production_agent_function
def get_tracking_status_clean(tracking_code: str) -> Dict[str, Any]:
    """
    Look up package tracking status USING decorator.

    This is the SAME Innovate Logistics function, but with decorator applied.

    Notice how much cleaner this is! The decorator handles:
    - Logging function calls
    - Timing execution
    - Catching and formatting errors

    This version focuses ONLY on business logic!
    """

    # WHAT: Validate tracking code is a string (BUSINESS LOGIC ONLY)
    # WHY: Ensure correct type before processing
    # HOW: Raise ValueError if not - decorator will handle it!

    if not isinstance(tracking_code, str):
        raise ValueError(
            f"Tracking code must be a string, got {type(tracking_code).__name__}"
        )

    # WHAT: Validate tracking code length (BUSINESS LOGIC ONLY)
    # WHY: Innovate Logistics codes are always 9 digits
    # HOW: Raise ValueError if not valid

    if len(tracking_code) != 9:
        raise ValueError(
            f"Tracking code must be exactly 9 digits, got {len(tracking_code)} characters"
        )

    # WHAT: Validate tracking code format (BUSINESS LOGIC ONLY)
    # WHY: Must be numeric only
    # HOW: Raise ValueError if not valid

    if not tracking_code.isdigit():
        raise ValueError(
            "Tracking code must contain only digits (0-9)"
        )

    # WHAT: Look up status in database (BUSINESS LOGIC ONLY)
    # WHY: Retrieve current package status
    # HOW: Query mock database

    status = MOCK_TRACKING_DB.get(tracking_code, "Unknown")

    # WHAT: Return success response (BUSINESS LOGIC ONLY)
    # WHY: Standard format for agent
    # HOW: Return dictionary - decorator will log it!

    return {
        "success": True,
        "result": status,
        "error": None
    }

# Note: No try/except needed! The decorator handles all error conversion.
# Note: No logging needed! The decorator handles all logging.
# Note: No timing needed! The decorator handles performance measurement.


# ============================================================================
# DEMONSTRATION: Comparison
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PRODUCTION DECORATOR DEMONSTRATION")
    print("Innovate Logistics - Tracking Status Function")
    print("=" * 70)

    print("\n" + "=" * 70)
    print("VERBOSE VERSION (Without Decorator)")
    print("=" * 70)
    print("\nNotice the cluttered code with manual logging, timing, and error handling.\n")

    # Test 1: Valid input
    print("Test 1: Valid tracking code")
    result1 = get_tracking_status_verbose("123456789")
    print(f"Result: {result1}\n")

    # Test 2: Invalid input (wrong length)
    print("Test 2: Invalid input (wrong length)")
    result2 = get_tracking_status_verbose("123")
    print(f"Result: {result2}\n")

    print("\n" + "=" * 70)
    print("CLEAN VERSION (With Decorator)")
    print("=" * 70)
    print("\nNotice the clean code - business logic is clear and focused!\n")

    # Test 3: Valid input
    print("Test 3: Valid tracking code")
    result3 = get_tracking_status_clean("111111111")
    print(f"Result: {result3}\n")

    # Test 4: Invalid input (non-numeric)
    print("Test 4: Invalid input (contains letters)")
    result4 = get_tracking_status_clean("12345678X")
    print(f"Result: {result4}\n")

    print("\n" + "=" * 70)
    print("KEY BENEFITS OF DECORATOR APPROACH")
    print("=" * 70)
    print("""
    1. DRY (Don't Repeat Yourself):
       - Logging code written once, used everywhere
       - Timing code written once, used everywhere
       - Error handling written once, used everywhere

    2. Separation of Concerns:
       - Business logic stays focused on business rules
       - Infrastructure concerns handled separately
       - Easier to read and maintain

    3. Consistency:
       - All functions handle errors the same way
       - All functions log the same way
       - Guaranteed standardized responses

    4. Maintainability:
       - Change logging once, affects all functions
       - Change error handling once, affects all functions
       - Add new features (like metrics) in one place

    Line Count Comparison (Innovate Logistics example):
    - Verbose get_tracking_status: ~102 lines (with all infrastructure)
    - Clean get_tracking_status: ~45 lines (just business logic)
    - 56% reduction in code per function!

    For Innovate's 3 logistics functions:
    - Without decorator: ~300+ lines of repetitive infrastructure code
    - With decorator: ~30 lines (decorator) + ~135 lines (business logic) = 165 lines
    - 45% overall reduction in repository size!
    """)

    print("\n" + "=" * 70)
    print("CODE COMPARISON - Innovate Logistics Function")
    print("=" * 70)

    print("\nVERBOSE (Without Decorator) - get_tracking_status:")
    print("""
    def get_tracking_status_verbose(tracking_code):
        logger.info(f"Calling get_tracking_status_verbose...")
        start_time = time.time()
        try:
            if not isinstance(tracking_code, str):
                raise ValueError("Must be string")
            if len(tracking_code) != 9:
                raise ValueError("Must be 9 digits")
            if not tracking_code.isdigit():
                raise ValueError("Must be numeric")

            status = MOCK_TRACKING_DB.get(tracking_code, "Unknown")

            execution_time = time.time() - start_time
            logger.info(f"completed in {execution_time:.4f}s")
            return {"success": True, "result": status, "error": None}
        except ValueError as e:
            execution_time = time.time() - start_time
            logger.warning(f"validation error: {e}")
            return {"success": False, "result": None, "error": str(e), "error_type": "validation"}
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"system error: {e}")
            return {"success": False, "result": None, "error": ..., "error_type": "system"}
    """)

    print("\nCLEAN (With Decorator) - get_tracking_status:")
    print("""
    @production_agent_function
    def get_tracking_status_clean(tracking_code):
        if not isinstance(tracking_code, str):
            raise ValueError("Must be string")
        if len(tracking_code) != 9:
            raise ValueError("Must be 9 digits")
        if not tracking_code.isdigit():
            raise ValueError("Must be numeric")

        status = MOCK_TRACKING_DB.get(tracking_code, "Unknown")
        return {"success": True, "result": status, "error": None}

    # All logging, timing, and error handling done by decorator!
    """)

    print("\n" + "=" * 70)
