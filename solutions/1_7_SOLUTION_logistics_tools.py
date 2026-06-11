"""
Module: logistics_tools_with_decorator.py
Purpose: Logistics functions with production decorator pattern - SOLUTION

This is the exemplar solution for Activity 1.7 Part A: Apply Production Decorator.

Key Changes from logistics_tools.py:
1. Imports @production_agent_function decorator
2. Applies decorator to all three functions
3. Removes manual try/except blocks (decorator handles this)
4. Functions now just raise ValueError for validation errors
5. Decorator automatically formats errors into standardized response

Benefits:
- DRY principle: Error handling written once in decorator
- Cleaner code: Functions focus on business logic
- Consistency: All functions handle errors identically
- Maintainability: Change error handling in one place
"""

import sys
import os
from importlib import import_module

# WHAT: Add activity directory to path
# WHY: Need to import decorator from activity directory
# HOW: Insert parent../activities path before imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../activities'))

# Import from numbered module using importlib
_wrapper = import_module('1_7_START_production_wrapper')
production_agent_function = _wrapper.production_agent_function

import re
import math
from typing import Dict, Any, Union


# WHAT: Define mock tracking database for educational purposes
# WHY: Simulate database lookups without needing actual database
# HOW: Use dictionary mapping tracking codes to statuses

# NOTE: In production, this would query a real tracking database
MOCK_TRACKING_DB = {
    "123456789": "In Transit",
    "987654321": "In Transit",
    "555555555": "In Transit",
    "111111111": "Delivered",
    "222222222": "Delivered",
}

# WHAT: Define mock inventory database for educational purposes
# WHY: Simulate warehouse inventory without needing actual database
# HOW: Use dictionary mapping SKUs to quantities

# NOTE: In production, this would query a real inventory system
MOCK_INVENTORY_DB = {
    "ABC1234": 150,
    "DEF5678": 3,
    "GHI9012": 0,
    "JKL3456": 42,
}

# WHAT: Define base delivery days by zone
# WHY: Centralize business logic for delivery time calculations
# HOW: Use dictionary mapping zones to standard delivery days

DELIVERY_DAYS_BASE = {
    1: 2,   # Local delivery (within city)
    2: 4,   # Regional delivery (within state)
    3: 7,   # National delivery (across country)
    4: 14,  # International delivery
}



@production_agent_function
def get_tracking_status(tracking_code: str) -> Dict[str, Any]:
    """
    Look up the current delivery status of a package.

    This function queries the tracking database (mocked for education) and
    returns the current status of a package. The function performs comprehensive
    validation to ensure the tracking code is in the correct format before
    attempting the lookup.

    Args:
        tracking_code: 9-digit tracking code (string of numeric characters only)
            Examples: "123456789", "987654321"

    Returns:
        Dict with standardized agent-friendly format:
            Success case:
                {
                    "success": True,
                    "result": str,  # "In Transit", "Delivered", or "Unknown"
                    "error": None
                }
            Error case:
                {
                    "success": False,
                    "result": None,
                    "error": str,  # Clear error message
                    "error_type": "validation" or "system"
                }

    Raises:
        ValueError: When validation fails (caught and returned as error response)

    Examples:
        >>> result = get_tracking_status("123456789")
        >>> print(result)
        {'success': True, 'result': 'In Transit', 'error': None}

        >>> result = get_tracking_status("123")
        >>> print(result)
        {'success': False, 'result': None,
         'error': 'Tracking code must be exactly 9 digits', 'error_type': 'validation'}
    """

        # WHAT: Validate tracking_code is a string
        # WHY: Function expects string input, other types will cause errors
        # HOW: Check type using isinstance

        if not isinstance(tracking_code, str):
            raise ValueError(
                f"Tracking code must be a string, got {type(tracking_code).__name__}"
            )

        # WHAT: Validate tracking_code length is exactly 9 characters
        # WHY: Tracking codes are always 9 digits in Innovate Logistics system
        # HOW: Check length using len()

        if len(tracking_code) != 9:
            raise ValueError(
                f"Tracking code must be exactly 9 digits, got {len(tracking_code)} characters"
            )

        # WHAT: Validate tracking_code contains only numeric digits
        # WHY: Tracking codes must be numeric only, no letters or symbols
        # HOW: Use string method isdigit() to check all characters are 0-9

        if not tracking_code.isdigit():
            raise ValueError(
                "Tracking code must contain only digits (0-9), no letters or symbols"
            )

        # WHAT: Look up tracking code in database
        # WHY: Retrieve current package status
        # HOW: Query mock database (in production, would query real database)

        # NOTE: In production, this would be:
        # status = database.query("SELECT status FROM tracking WHERE code = ?", tracking_code)

        status = MOCK_TRACKING_DB.get(tracking_code, "Unknown")

        # WHAT: Return success response with status
        # WHY: Provide standardized format that agents can reliably parse
        # HOW: Return dictionary with success=True and result containing status

        return {
            "success": True,
            "result": status,
            "error": None
        }


@production_agent_function
def check_inventory(sku: str) -> Dict[str, Any]:
    """
    Check if a product SKU is in stock and return available quantity.

    This function queries the warehouse inventory system (mocked for education)
    and returns the quantity available and stock status. The function performs
    comprehensive validation to ensure the SKU is in the correct format before
    attempting the lookup.

    SKU Format: 3 uppercase letters + 4 digits (e.g., "ABC1234")

    Args:
        sku: Product SKU code in format "XXX####" where X = letter, # = digit
            Examples: "ABC1234", "DEF5678", "GHI9012"

    Returns:
        Dict with standardized agent-friendly format:
            Success case:
                {
                    "success": True,
                    "result": {
                        "sku": str,          # The queried SKU
                        "quantity": int,     # Available quantity
                        "in_stock": bool     # True if quantity > 0
                    },
                    "error": None
                }
            Error case:
                {
                    "success": False,
                    "result": None,
                    "error": str,
                    "error_type": "validation" or "system"
                }

    Raises:
        ValueError: When validation fails (caught and returned as error response)

    Examples:
        >>> result = check_inventory("ABC1234")
        >>> print(result)
        {'success': True, 'result': {'sku': 'ABC1234', 'quantity': 150, 'in_stock': True}, 'error': None}

        >>> result = check_inventory("abc1234")
        >>> print(result)
        {'success': False, 'result': None,
         'error': 'SKU format must be 3 uppercase letters followed by 4 digits', ...}
    """

        # WHAT: Validate SKU is a string
        # WHY: Function expects string input
        # HOW: Check type using isinstance

        if not isinstance(sku, str):
            raise ValueError(
                f"SKU must be a string, got {type(sku).__name__}"
            )

        # WHAT: Validate SKU length is exactly 7 characters
        # WHY: SKU format is always 3 letters + 4 digits = 7 characters
        # HOW: Check length using len()

        if len(sku) != 7:
            raise ValueError(
                f"SKU must be exactly 7 characters (3 letters + 4 digits), got {len(sku)} characters"
            )

        # WHAT: Validate SKU format using regex pattern
        # WHY: Ensure SKU matches required format: 3 uppercase letters + 4 digits
        # HOW: Use regular expression to match pattern

        # Pattern: ^[A-Z]{3}[0-9]{4}$
        # ^ = start of string
        # [A-Z]{3} = exactly 3 uppercase letters
        # [0-9]{4} = exactly 4 digits
        # $ = end of string

        sku_pattern = r'^[A-Z]{3}[0-9]{4}$'

        if not re.match(sku_pattern, sku):
            raise ValueError(
                f"SKU format must be 3 uppercase letters followed by 4 digits (e.g., 'ABC1234'), got '{sku}'"
            )

        # WHAT: Look up SKU in inventory database
        # WHY: Retrieve current stock quantity
        # HOW: Query mock database (in production, would query real inventory system)

        # NOTE: In production, this would be:
        # quantity = database.query("SELECT quantity FROM inventory WHERE sku = ?", sku)

        quantity = MOCK_INVENTORY_DB.get(sku, 0)

        # WHAT: Determine if item is in stock
        # WHY: Provide clear availability status
        # HOW: Check if quantity is greater than zero

        in_stock = quantity > 0

        # WHAT: Return success response with inventory information
        # WHY: Provide standardized format with detailed inventory data
        # HOW: Return dictionary with success=True and result containing inventory details

        return {
            "success": True,
            "result": {
                "sku": sku,
                "quantity": quantity,
                "in_stock": in_stock
            },
            "error": None
        }


@production_agent_function
def calculate_delivery_days(zone: int, service_level: str) -> Dict[str, Any]:
    """
    Calculate estimated delivery time in days based on zone and service level.

    This function applies Innovate Logistics delivery time formulas based on
    shipping distance (zone) and selected service speed. Express service provides
    expedited delivery at approximately half the standard time (rounded up).

    Zone Definitions:
        1 = Local (within city, 2 days standard)
        2 = Regional (within state, 4 days standard)
        3 = National (across country, 7 days standard)
        4 = International (14 days standard)

    Service Levels:
        Standard = Normal delivery speed
        Express = Expedited delivery (half time, rounded up)

    Args:
        zone: Destination zone (integer from 1 to 4)
        service_level: Service speed ("Standard" or "Express", case-sensitive)

    Returns:
        Dict with standardized agent-friendly format:
            Success case:
                {
                    "success": True,
                    "result": {
                        "zone": int,
                        "service_level": str,
                        "delivery_days": int
                    },
                    "error": None
                }
            Error case:
                {
                    "success": False,
                    "result": None,
                    "error": str,
                    "error_type": "validation" or "system"
                }

    Raises:
        ValueError: When validation fails (caught and returned as error response)

    Examples:
        >>> result = calculate_delivery_days(2, "Standard")
        >>> print(result)
        {'success': True, 'result': {'zone': 2, 'service_level': 'Standard', 'delivery_days': 4}, ...}

        >>> result = calculate_delivery_days(3, "Express")
        >>> print(result)
        {'success': True, 'result': {'zone': 3, 'service_level': 'Express', 'delivery_days': 4}, ...}
        # Note: 7 days / 2 = 3.5, rounds up to 4
    """

        # WHAT: Validate zone is an integer
        # WHY: Zone must be integer type for business logic
        # HOW: Check type using isinstance

        if not isinstance(zone, int):
            raise ValueError(
                f"Zone must be an integer, got {type(zone).__name__}"
            )

        # WHAT: Validate zone is in valid range (1-4)
        # WHY: Only zones 1-4 are defined in Innovate Logistics system
        # HOW: Check if zone is in DELIVERY_DAYS_BASE dictionary keys

        if zone not in DELIVERY_DAYS_BASE:
            valid_zones = sorted(DELIVERY_DAYS_BASE.keys())
            raise ValueError(
                f"Zone must be between 1 and 4, got {zone}"
            )

        # WHAT: Validate service_level is a string
        # WHY: Service level must be string for comparison
        # HOW: Check type using isinstance

        if not isinstance(service_level, str):
            raise ValueError(
                f"Service level must be a string, got {type(service_level).__name__}"
            )

        # WHAT: Validate service_level is either "Standard" or "Express"
        # WHY: Only these two service levels are supported
        # HOW: Check if service_level matches exactly (case-sensitive)

        valid_services = ["Standard", "Express"]

        if service_level not in valid_services:
            raise ValueError(
                f"Service level must be 'Standard' or 'Express' (case-sensitive), got '{service_level}'"
            )

        # WHAT: Get base delivery days for the zone
        # WHY: Start with standard delivery time for distance
        # HOW: Look up zone in DELIVERY_DAYS_BASE dictionary

        base_days = DELIVERY_DAYS_BASE[zone]

        # WHAT: Calculate delivery days based on service level
        # WHY: Express service is faster than standard
        # HOW: For Express, divide by 2 and round up; for Standard, use base days

        if service_level == "Express":
            # WHAT: Calculate express delivery time
            # WHY: Express is approximately half the standard time
            # HOW: Divide base days by 2 and round UP to nearest integer

            # Use math.ceil() to round up (e.g., 3.5 becomes 4, not 3)
            delivery_days = math.ceil(base_days / 2)
        else:
            # Standard service uses base days with no modification
            delivery_days = base_days

        # WHAT: Return success response with delivery estimate
        # WHY: Provide standardized format with detailed delivery information
        # HOW: Return dictionary with success=True and result containing all details

        return {
            "success": True,
            "result": {
                "zone": zone,
                "service_level": service_level,
                "delivery_days": delivery_days
            },
            "error": None
        }

# WHAT: Provide example usage when module is run directly
# WHY: Demonstrate function usage and expected outputs
# HOW: Execute sample calls when __name__ == "__main__"

if __name__ == "__main__":
    print("=" * 70)
    print("INNOVATE LOGISTICS FUNCTIONS - SOLUTION")
    print("=" * 70)

    # Test get_tracking_status
    print("\n### Testing get_tracking_status ###\n")

    print("Test 1: Valid tracking code (in transit)")
    result = get_tracking_status("123456789")
    print(f"Result: {result}")
    # Expected: {"success": True, "result": "In Transit", "error": None}

    print("\nTest 2: Valid tracking code (delivered)")
    result = get_tracking_status("111111111")
    print(f"Result: {result}")

    print("\nTest 3: Valid tracking code (unknown)")
    result = get_tracking_status("999999999")
    print(f"Result: {result}")

    print("\nTest 4: Invalid - too short")
    result = get_tracking_status("123")
    print(f"Result: {result}")

    print("\nTest 5: Invalid - contains letter")
    result = get_tracking_status("12345678X")
    print(f"Result: {result}")

    # Test check_inventory
    print("\n\n### Testing check_inventory ###\n")

    print("Test 1: Valid SKU (in stock)")
    result = check_inventory("ABC1234")
    print(f"Result: {result}")

    print("\nTest 2: Valid SKU (out of stock)")
    result = check_inventory("GHI9012")
    print(f"Result: {result}")

    print("\nTest 3: Valid SKU (unknown)")
    result = check_inventory("XYZ9999")
    print(f"Result: {result}")

    print("\nTest 4: Invalid - lowercase")
    result = check_inventory("abc1234")
    print(f"Result: {result}")

    print("\nTest 5: Invalid - too short")
    result = check_inventory("ABC123")
    print(f"Result: {result}")

    # Test calculate_delivery_days
    print("\n\n### Testing calculate_delivery_days ###\n")

    print("Test 1: Zone 2 Standard")
    result = calculate_delivery_days(2, "Standard")
    print(f"Result: {result}")

    print("\nTest 2: Zone 3 Express (rounds up)")
    result = calculate_delivery_days(3, "Express")
    print(f"Result: {result}")
    print("Note: 7 days / 2 = 3.5, rounds UP to 4")

    print("\nTest 3: Zone 1 Express")
    result = calculate_delivery_days(1, "Express")
    print(f"Result: {result}")

    print("\nTest 4: Invalid - zone out of range")
    result = calculate_delivery_days(5, "Standard")
    print(f"Result: {result}")

    print("\nTest 5: Invalid - wrong service level")
    result = calculate_delivery_days(2, "Premium")
    print(f"Result: {result}")

    print("\n" + "=" * 70)
    print("All functions demonstrated successfully!")
    print("=" * 70)
