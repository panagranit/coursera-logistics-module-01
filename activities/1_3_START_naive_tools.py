"""
Naive implementation of Innovate Logistics functions.

⚠️ WARNING: This code is intentionally simplified and NOT production-ready.

These functions lack:
- Input validation
- Error handling
- Standardized return formats
- Proper documentation
- Type safety

Your task in Activity 1.3: Refactor these into production-ready, agent-callable functions.

The problems with this code:
1. No validation - accepts any input, will crash on invalid data
2. No error handling - exceptions will propagate to caller
3. Inconsistent returns - different types (str, int, dict) instead of standardized format
4. No docstrings - unclear what inputs are expected
5. Magic values - hardcoded data with no explanation
6. Poor naming - unclear what functions do

DO NOT use this code in production. It's intentionally bad to demonstrate what NOT to do.
"""

def get_tracking_status(code):
    """Look up tracking status. (Minimal docstring - bad!)"""
    # Problem: No validation of input type, length, or format
    # This will return wrong data for invalid codes
    # Will crash if code is not a string (e.g., if given an integer)

    if code in ["123456789", "987654321", "555555555"]:
        return "In Transit"
    elif code in ["111111111", "222222222"]:
        return "Delivered"
    else:
        return "Unknown"
    # Problem: Returns raw string instead of standardized {"success": ..., "result": ...} format


def check_inventory(sku):
    """Check inventory. (Minimal docstring - bad!)"""
    # Problem: No validation of SKU format
    # Will return 0 for any invalid input, making it seem like item is just out of stock
    # Doesn't distinguish between "invalid SKU" and "valid SKU with zero stock"

    inventory = {
        "ABC1234": 150,
        "DEF5678": 3,
        "GHI9012": 0,
        "JKL3456": 42,
    }

    return inventory.get(sku, 0)
    # Problem: Returns raw integer instead of standardized format
    # Problem: No indication of whether SKU was valid or just out of stock


def calculate_delivery_days(zone, service_level):
    """Calculate delivery days. (Minimal docstring - bad!)"""
    # Problem: No validation of zone or service_level
    # Will crash if given invalid types
    # Logic bug: treats "express" as a zone instead of a service level modifier

    base_days = {
        1: 2,    # Local
        2: 4,    # Regional
        3: 7,    # National
        4: 14,   # International
    }

    days = base_days.get(zone, 5)  # Default to 5 if zone not found (arbitrary choice)

    # Bug: This logic is wrong! It treats service_level as if it might be "express" for zone
    # But service_level should be a separate parameter determining speed
    if service_level == "Express":
        return days // 2  # Integer division - doesn't round up correctly
    else:
        return days
    # Problem: Returns raw integer instead of standardized format
    # Problem: No error handling if zone or service_level is invalid


# If you run this file, you'll see the problems:
if __name__ == "__main__":
    print("Demonstrating problems with naive implementations:\n")

    # Problem 1: No validation
    print("Problem 1: No validation catches invalid inputs")
    print(f"get_tracking_status('123'): {get_tracking_status('123')}")  # Too short, but returns "Unknown"
    print(f"get_tracking_status('ABCDEFGHI'): {get_tracking_status('ABCDEFGHI')}")  # Letters, but returns "Unknown"
    print("^ Should have rejected invalid formats, but didn't!\n")

    # Problem 2: Type errors crash the program
    print("Problem 2: Wrong types cause crashes")
    try:
        result = get_tracking_status(123456789)  # Integer instead of string
        print(f"get_tracking_status(123456789): {result}")
    except Exception as e:
        print(f"get_tracking_status(123456789): CRASHED with error: {e}")
    print("^ Should have handled type error gracefully!\n")

    # Problem 3: Inconsistent return types
    print("Problem 3: Inconsistent return types")
    print(f"get_tracking_status returns: {type(get_tracking_status('123456789')).__name__} (should be dict)")
    print(f"check_inventory returns: {type(check_inventory('ABC1234')).__name__} (should be dict)")
    print(f"calculate_delivery_days returns: {type(calculate_delivery_days(1, 'Standard')).__name__} (should be dict)")
    print("^ Agents need consistent dict format with 'success', 'result', 'error' keys!\n")

    # Problem 4: Can't distinguish error types
    print("Problem 4: Can't distinguish between 'not found' and 'out of stock'")
    print(f"check_inventory('ABC1234'): {check_inventory('ABC1234')}")  # Valid SKU, in stock
    print(f"check_inventory('GHI9012'): {check_inventory('GHI9012')}")  # Valid SKU, out of stock
    print(f"check_inventory('INVALID'): {check_inventory('INVALID')}")  # Invalid SKU
    print(f"check_inventory('XYZ9999'): {check_inventory('XYZ9999')}")  # Unknown valid SKU
    print("^ All return integers, can't tell if SKU is valid or not!\n")

    # Problem 5: Calculation bugs
    print("Problem 5: Calculation bugs due to lack of validation")
    print(f"calculate_delivery_days(3, 'Express'): {calculate_delivery_days(3, 'Express')}")
    print("^ 7 days / 2 = 3.5, should round UP to 4, but // gives 3!")
    print(f"calculate_delivery_days(5, 'Standard'): {calculate_delivery_days(5, 'Standard')}")
    print("^ Zone 5 is invalid, but returns default of 5 days instead of error!\n")

    print("=" * 70)
    print("CONCLUSION: These naive implementations have serious problems!")
    print("=" * 70)
    print("""
Your task: Refactor these into production-ready functions that:
✓ Validate all inputs
✓ Handle errors gracefully
✓ Return standardized {"success": ..., "result": ..., "error": ...} format
✓ Provide clear error messages
✓ Are safe for agent use

See START_requirements.md for detailed specifications.
    """)
