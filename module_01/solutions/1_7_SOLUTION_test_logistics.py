"""
Complete test suite for Innovate Logistics refactored functions - SOLUTION

This is the exemplar solution for Activity 1.7 Part B: Build Test Suite.

This test suite demonstrates best practices for testing agent-callable functions:
1. Happy path scenarios (correct inputs produce correct outputs)
2. Input validation (invalid inputs produce clear error messages)
3. Edge cases (boundary conditions, special values)
4. Standardized return format (all functions return consistent dict structure)

Run with:
    pytest 1_7_SOLUTION_test_logistics.py -v

Learning Context:
    This is the complete solution file showing what learners should produce
    in Activity 1.7. It demonstrates comprehensive testing patterns including:

    - Test organization with classes
    - pytest fixtures for reusable test data
    - Parametrized tests for multiple scenarios
    - Clear test names and docstrings
    - Validation of both success and error cases
    - Testing of standardized response format

Expected Result: All tests PASS when run against logistics_tools.py or logistics_tools_with_decorator.py
"""

import pytest
from logistics_tools import get_tracking_status, check_inventory, calculate_delivery_days


# ============================================================================
# TEST FIXTURES
# ============================================================================

# WHAT: Define reusable test data for valid inputs
# WHY: Avoid repetition and ensure consistency across tests
# HOW: Use pytest fixtures to provide standard valid values

@pytest.fixture
def valid_tracking_code():
    """Provide a standard valid tracking code for tests."""
    return "123456789"


@pytest.fixture
def valid_sku():
    """Provide a standard valid SKU for tests."""
    return "ABC1234"


@pytest.fixture
def valid_zone():
    """Provide a standard valid zone for tests."""
    return 2  # Regional


@pytest.fixture
def valid_service_level():
    """Provide a standard valid service level for tests."""
    return "Standard"


# ============================================================================
# TESTS FOR get_tracking_status
# ============================================================================

class TestGetTrackingStatusHappyPath:
    """Test get_tracking_status with valid inputs."""

    def test_tracking_status_in_transit(self):
        """Test tracking lookup returns 'In Transit' for active shipments."""
        # WHAT: Call get_tracking_status with a code that should be in transit
        # WHY: Verify function correctly retrieves and returns status from database
        # HOW: Use known tracking code and assert success=True with correct status

        result = get_tracking_status("123456789")

        # Validate return format
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "success" in result, "Result must have 'success' key"
        assert "result" in result, "Result must have 'result' key"
        assert "error" in result, "Result must have 'error' key"

        # Validate success response
        assert result["success"] is True, "Should succeed for valid tracking code"
        assert result["result"] == "In Transit", "Should return 'In Transit' status"
        assert result["error"] is None, "Error should be None for successful calls"

    def test_tracking_status_delivered(self):
        """Test tracking lookup returns 'Delivered' for completed shipments."""
        # WHAT: Call get_tracking_status with a code that should be delivered
        # WHY: Verify function handles different status values correctly
        # HOW: Use known delivered tracking code and assert correct status

        result = get_tracking_status("111111111")

        assert result["success"] is True
        assert result["result"] == "Delivered", "Should return 'Delivered' status"
        assert result["error"] is None

    def test_tracking_status_unknown(self):
        """Test tracking lookup returns 'Unknown' for unrecognized codes."""
        # WHAT: Call get_tracking_status with valid format but unknown code
        # WHY: Verify function distinguishes between invalid format and unknown code
        # HOW: Use valid format but unrecognized code, expect success with 'Unknown'

        result = get_tracking_status("999999999")

        assert result["success"] is True, "Should succeed even if code not found"
        assert result["result"] == "Unknown", "Should return 'Unknown' for unrecognized codes"
        assert result["error"] is None


class TestGetTrackingStatusValidation:
    """Test get_tracking_status input validation."""

    def test_tracking_code_wrong_type(self):
        """Test that non-string tracking codes are rejected."""
        # WHAT: Call get_tracking_status with integer instead of string
        # WHY: Ensure type validation catches incorrect input types
        # HOW: Pass integer, expect validation error

        result = get_tracking_status(123456789)  # Integer instead of string

        # Validate error response format
        assert isinstance(result, dict), "Result should be a dictionary"
        assert result["success"] is False, "Should fail for non-string input"
        assert result["result"] is None, "Result should be None on error"
        assert result["error"] is not None, "Error message should be provided"
        assert "error_type" in result, "Must include error_type"
        assert result["error_type"] == "validation", "Should be validation error"
        assert "string" in result["error"].lower(), "Error should mention string type"

    def test_tracking_code_too_short(self):
        """Test that tracking codes shorter than 9 digits are rejected."""
        # WHAT: Call get_tracking_status with code that's too short
        # WHY: Ensure length validation works correctly
        # HOW: Pass short code, expect validation error mentioning length

        result = get_tracking_status("123")

        assert result["success"] is False
        assert result["result"] is None
        assert result["error_type"] == "validation"
        assert "9" in result["error"] or "length" in result["error"].lower()

    def test_tracking_code_too_long(self):
        """Test that tracking codes longer than 9 digits are rejected."""
        # WHAT: Call get_tracking_status with code that's too long
        # WHY: Ensure length validation catches codes that are too long
        # HOW: Pass long code, expect validation error

        result = get_tracking_status("1234567890123")

        assert result["success"] is False
        assert result["result"] is None
        assert result["error_type"] == "validation"
        assert "9" in result["error"] or "length" in result["error"].lower()

    @pytest.mark.parametrize("invalid_code", [
        "12345678X",      # Contains letter at end
        "X23456789",      # Contains letter at start
        "123X56789",      # Contains letter in middle
        "ABCDEFGHI",      # All letters
        "123-45-678",     # Contains hyphens
        "123 456 789",    # Contains spaces
        "12345678!",      # Contains symbol
        "",               # Empty string
        "         ",      # Only spaces (9 spaces)
    ])
    def test_tracking_code_invalid_format(self, invalid_code):
        """Test that tracking codes with non-digit characters are rejected."""
        # WHAT: Call get_tracking_status with various invalid formats
        # WHY: Ensure format validation catches all non-numeric codes
        # HOW: Use parametrize to test multiple invalid formats

        result = get_tracking_status(invalid_code)

        assert result["success"] is False, f"Should fail for invalid code: '{invalid_code}'"
        assert result["result"] is None
        assert result["error_type"] == "validation"
        assert result["error"] is not None


# ============================================================================
# TESTS FOR check_inventory
# ============================================================================

class TestCheckInventoryHappyPath:
    """Test check_inventory with valid inputs."""

    def test_inventory_in_stock(self):
        """Test inventory check for SKU with available quantity."""
        # WHAT: Call check_inventory with SKU that has stock
        # WHY: Verify function correctly retrieves and reports inventory
        # HOW: Use known in-stock SKU and assert success with correct quantity

        result = check_inventory("ABC1234")

        # Validate return format
        assert isinstance(result, dict), "Result should be a dictionary"
        assert "success" in result
        assert "result" in result
        assert "error" in result

        # Validate success response
        assert result["success"] is True
        assert result["error"] is None

        # Validate result structure
        assert isinstance(result["result"], dict), "Result should contain dict with inventory details"
        assert "sku" in result["result"], "Result should include SKU"
        assert "quantity" in result["result"], "Result should include quantity"
        assert "in_stock" in result["result"], "Result should include in_stock flag"

        # Validate result values
        assert result["result"]["sku"] == "ABC1234"
        assert result["result"]["quantity"] == 150, "Should return correct quantity"
        assert result["result"]["in_stock"] is True, "Should indicate item is in stock"

    def test_inventory_low_stock(self):
        """Test inventory check for SKU with low quantity."""
        # WHAT: Call check_inventory with SKU that has minimal stock
        # WHY: Verify function correctly handles low quantity scenarios
        # HOW: Use SKU with quantity 3, assert in_stock is still True

        result = check_inventory("DEF5678")

        assert result["success"] is True
        assert result["result"]["sku"] == "DEF5678"
        assert result["result"]["quantity"] == 3
        assert result["result"]["in_stock"] is True, "Even low quantity should show in_stock=True"

    def test_inventory_out_of_stock(self):
        """Test inventory check for SKU with zero quantity."""
        # WHAT: Call check_inventory with SKU that has zero quantity
        # WHY: Verify function distinguishes between zero stock and unknown SKU
        # HOW: Use SKU with quantity 0, expect success but in_stock=False

        result = check_inventory("GHI9012")

        assert result["success"] is True, "Should succeed even for zero quantity"
        assert result["result"]["sku"] == "GHI9012"
        assert result["result"]["quantity"] == 0
        assert result["result"]["in_stock"] is False, "Should indicate item is not in stock"

    def test_inventory_unknown_sku(self):
        """Test inventory check for unknown but valid-format SKU."""
        # WHAT: Call check_inventory with valid format but unknown SKU
        # WHY: Verify function handles unknown SKUs appropriately
        # HOW: Use valid format unknown SKU, expect success with quantity 0

        result = check_inventory("XYZ9999")

        assert result["success"] is True, "Should succeed for valid format even if SKU unknown"
        assert result["result"]["sku"] == "XYZ9999"
        assert result["result"]["quantity"] == 0, "Unknown SKUs should return quantity 0"
        assert result["result"]["in_stock"] is False


class TestCheckInventoryValidation:
    """Test check_inventory input validation."""

    def test_sku_wrong_type(self):
        """Test that non-string SKUs are rejected."""
        # WHAT: Call check_inventory with integer instead of string
        # WHY: Ensure type validation catches incorrect input types
        # HOW: Pass integer, expect validation error

        result = check_inventory(1234567)

        assert result["success"] is False
        assert result["result"] is None
        assert result["error_type"] == "validation"
        assert "string" in result["error"].lower()

    def test_sku_wrong_length(self):
        """Test that SKUs with incorrect length are rejected."""
        # WHAT: Call check_inventory with SKU that's wrong length
        # WHY: Ensure length validation works correctly
        # HOW: Pass short SKU, expect validation error mentioning length

        result = check_inventory("ABC123")  # Too short (6 chars instead of 7)

        assert result["success"] is False
        assert result["result"] is None
        assert result["error_type"] == "validation"
        assert "7" in result["error"] or "length" in result["error"].lower()

    def test_sku_lowercase_letters(self):
        """Test that SKUs with lowercase letters are rejected."""
        # WHAT: Call check_inventory with lowercase SKU
        # WHY: Ensure format validation requires uppercase letters
        # HOW: Pass lowercase SKU, expect validation error

        result = check_inventory("abc1234")

        assert result["success"] is False
        assert result["result"] is None
        assert result["error_type"] == "validation"
        assert "uppercase" in result["error"].lower() or "format" in result["error"].lower()

    @pytest.mark.parametrize("invalid_sku", [
        "AB1234",        # Only 2 letters
        "ABCD1234",      # 4 letters instead of 3
        "ABC12345",      # 5 digits instead of 4
        "ABC123",        # Only 3 digits
        "123ABCD",       # Digits first, letters second (reversed)
        "A1C2D3F",       # Mixed letters and digits
        "ABC-1234",      # Contains hyphen
        "ABC 1234",      # Contains space
        "",              # Empty string
        "       ",       # Only spaces
    ])
    def test_sku_invalid_format(self, invalid_sku):
        """Test that SKUs with invalid format are rejected."""
        # WHAT: Call check_inventory with various invalid formats
        # WHY: Ensure format validation catches all non-conforming SKUs
        # HOW: Use parametrize to test multiple invalid formats

        result = check_inventory(invalid_sku)

        assert result["success"] is False, f"Should fail for invalid SKU: '{invalid_sku}'"
        assert result["result"] is None
        assert result["error_type"] == "validation"


# ============================================================================
# TESTS FOR calculate_delivery_days
# ============================================================================

class TestCalculateDeliveryDaysHappyPath:
    """Test calculate_delivery_days with valid inputs."""

    def test_delivery_zone1_standard(self):
        """Test delivery calculation for local zone with standard service."""
        # WHAT: Call calculate_delivery_days for zone 1 standard
        # WHY: Verify basic calculation works correctly
        # HOW: Pass zone 1 and Standard, expect 2 days

        result = calculate_delivery_days(1, "Standard")

        # Validate return format
        assert isinstance(result, dict)
        assert "success" in result
        assert "result" in result
        assert "error" in result

        # Validate success response
        assert result["success"] is True
        assert result["error"] is None

        # Validate result structure
        assert isinstance(result["result"], dict)
        assert "zone" in result["result"]
        assert "service_level" in result["result"]
        assert "delivery_days" in result["result"]

        # Validate result values
        assert result["result"]["zone"] == 1
        assert result["result"]["service_level"] == "Standard"
        assert result["result"]["delivery_days"] == 2, "Zone 1 standard should be 2 days"

    def test_delivery_zone2_standard(self):
        """Test delivery calculation for regional zone with standard service."""
        result = calculate_delivery_days(2, "Standard")

        assert result["success"] is True
        assert result["result"]["delivery_days"] == 4, "Zone 2 standard should be 4 days"

    def test_delivery_zone3_standard(self):
        """Test delivery calculation for national zone with standard service."""
        result = calculate_delivery_days(3, "Standard")

        assert result["success"] is True
        assert result["result"]["delivery_days"] == 7, "Zone 3 standard should be 7 days"

    def test_delivery_zone4_standard(self):
        """Test delivery calculation for international zone with standard service."""
        result = calculate_delivery_days(4, "Standard")

        assert result["success"] is True
        assert result["result"]["delivery_days"] == 14, "Zone 4 standard should be 14 days"

    def test_delivery_zone1_express(self):
        """Test delivery calculation for local zone with express service."""
        # WHAT: Call calculate_delivery_days for zone 1 express
        # WHY: Verify express calculation divides by 2 and rounds up
        # HOW: Pass zone 1 and Express, expect 1 day (2 / 2 = 1)

        result = calculate_delivery_days(1, "Express")

        assert result["success"] is True
        assert result["result"]["zone"] == 1
        assert result["result"]["service_level"] == "Express"
        assert result["result"]["delivery_days"] == 1, "Zone 1 express should be 1 day (2/2=1)"

    def test_delivery_zone2_express(self):
        """Test delivery calculation for regional zone with express service."""
        result = calculate_delivery_days(2, "Express")

        assert result["success"] is True
        assert result["result"]["delivery_days"] == 2, "Zone 2 express should be 2 days (4/2=2)"

    def test_delivery_zone3_express_rounds_up(self):
        """Test that express delivery rounds up correctly (7 days / 2 = 3.5 -> 4)."""
        # WHAT: Call calculate_delivery_days for zone 3 express
        # WHY: Verify function rounds up fractional days (critical business logic)
        # HOW: Pass zone 3 Express, expect 4 days not 3 (7/2=3.5 rounds to 4)

        result = calculate_delivery_days(3, "Express")

        assert result["success"] is True
        assert result["result"]["delivery_days"] == 4, "Zone 3 express should round up: 7/2=3.5->4 days"

    def test_delivery_zone4_express(self):
        """Test delivery calculation for international zone with express service."""
        result = calculate_delivery_days(4, "Express")

        assert result["success"] is True
        assert result["result"]["delivery_days"] == 7, "Zone 4 express should be 7 days (14/2=7)"


class TestCalculateDeliveryDaysValidation:
    """Test calculate_delivery_days input validation."""

    def test_zone_wrong_type(self):
        """Test that non-integer zones are rejected."""
        # WHAT: Call calculate_delivery_days with string zone instead of integer
        # WHY: Ensure type validation catches incorrect zone types
        # HOW: Pass string zone, expect validation error

        result = calculate_delivery_days("2", "Standard")  # String instead of int

        assert result["success"] is False
        assert result["result"] is None
        assert result["error_type"] == "validation"
        assert "integer" in result["error"].lower()

    @pytest.mark.parametrize("invalid_zone", [0, 5, -1, 100])
    def test_zone_out_of_range(self, invalid_zone):
        """Test that zones outside 1-4 range are rejected."""
        # WHAT: Call calculate_delivery_days with out-of-range zones
        # WHY: Ensure zone validation only accepts valid zones (1-4)
        # HOW: Use parametrize to test multiple invalid zones

        result = calculate_delivery_days(invalid_zone, "Standard")

        assert result["success"] is False, f"Should fail for zone {invalid_zone}"
        assert result["result"] is None
        assert result["error_type"] == "validation"
        assert "zone" in result["error"].lower()

    def test_service_level_wrong_type(self):
        """Test that non-string service levels are rejected."""
        # WHAT: Call calculate_delivery_days with integer service level
        # WHY: Ensure type validation catches incorrect service level types
        # HOW: Pass integer, expect validation error

        result = calculate_delivery_days(2, 123)  # Integer instead of string

        assert result["success"] is False
        assert result["result"] is None
        assert result["error_type"] == "validation"
        assert "string" in result["error"].lower()

    @pytest.mark.parametrize("invalid_service", [
        "standard",      # Wrong case (lowercase)
        "STANDARD",      # Wrong case (uppercase)
        "express",       # Wrong case (lowercase)
        "EXPRESS",       # Wrong case (uppercase)
        "Premium",       # Invalid service level
        "Overnight",     # Invalid service level
        "Economy",       # Invalid service level
        "",              # Empty string
        "Standard ",     # Trailing space
        " Standard",     # Leading space
    ])
    def test_service_level_invalid(self, invalid_service):
        """Test that invalid service levels are rejected."""
        # WHAT: Call calculate_delivery_days with invalid service levels
        # WHY: Ensure service level validation only accepts "Standard" or "Express" (case-sensitive)
        # HOW: Use parametrize to test various invalid service levels

        result = calculate_delivery_days(2, invalid_service)

        assert result["success"] is False, f"Should fail for service level: '{invalid_service}'"
        assert result["result"] is None
        assert result["error_type"] == "validation"
        assert "service" in result["error"].lower() or "Standard" in result["error"] or "Express" in result["error"]


# ============================================================================
# CROSS-FUNCTION TESTS
# ============================================================================

class TestReturnFormatConsistency:
    """Test that all functions return consistent format."""

    def test_all_functions_return_dict(self):
        """Test that all functions return dictionary type."""
        # WHAT: Call each function and verify return type is dict
        # WHY: Ensure agents can reliably parse all function responses
        # HOW: Call each function with valid inputs and check type

        result1 = get_tracking_status("123456789")
        result2 = check_inventory("ABC1234")
        result3 = calculate_delivery_days(2, "Standard")

        assert isinstance(result1, dict), "get_tracking_status must return dict"
        assert isinstance(result2, dict), "check_inventory must return dict"
        assert isinstance(result3, dict), "calculate_delivery_days must return dict"

    def test_all_functions_have_required_keys_on_success(self):
        """Test that all successful responses have required keys."""
        # WHAT: Verify all success responses contain success, result, error keys
        # WHY: Ensure standardized response format across all functions
        # HOW: Call each function successfully and check keys

        result1 = get_tracking_status("123456789")
        result2 = check_inventory("ABC1234")
        result3 = calculate_delivery_days(2, "Standard")

        required_keys = {"success", "result", "error"}

        assert set(result1.keys()) >= required_keys, "get_tracking_status missing required keys"
        assert set(result2.keys()) >= required_keys, "check_inventory missing required keys"
        assert set(result3.keys()) >= required_keys, "calculate_delivery_days missing required keys"

    def test_all_functions_have_required_keys_on_error(self):
        """Test that all error responses have required keys including error_type."""
        # WHAT: Verify all error responses contain success, result, error, error_type keys
        # WHY: Ensure standardized error format across all functions
        # HOW: Trigger validation errors and check keys

        result1 = get_tracking_status("123")  # Invalid
        result2 = check_inventory("ABC")       # Invalid
        result3 = calculate_delivery_days(5, "Standard")  # Invalid

        required_keys = {"success", "result", "error", "error_type"}

        assert set(result1.keys()) >= required_keys, "get_tracking_status error missing required keys"
        assert set(result2.keys()) >= required_keys, "check_inventory error missing required keys"
        assert set(result3.keys()) >= required_keys, "calculate_delivery_days error missing required keys"

    def test_success_true_means_result_not_none(self):
        """Test that success=True always means result is not None."""
        # WHAT: Verify success responses have non-None result values
        # WHY: Ensure agents can reliably extract results from successful calls
        # HOW: Call each function successfully and verify result is not None

        result1 = get_tracking_status("123456789")
        result2 = check_inventory("ABC1234")
        result3 = calculate_delivery_days(2, "Standard")

        assert result1["success"] is True
        assert result1["result"] is not None, "Successful call must have result"

        assert result2["success"] is True
        assert result2["result"] is not None, "Successful call must have result"

        assert result3["success"] is True
        assert result3["result"] is not None, "Successful call must have result"

    def test_success_false_means_result_is_none(self):
        """Test that success=False always means result is None."""
        # WHAT: Verify error responses have None as result value
        # WHY: Ensure consistent error format - no partial results on failure
        # HOW: Trigger errors and verify result is None

        result1 = get_tracking_status("123")  # Invalid
        result2 = check_inventory("ABC")       # Invalid
        result3 = calculate_delivery_days(5, "Standard")  # Invalid

        assert result1["success"] is False
        assert result1["result"] is None, "Failed call must have result=None"

        assert result2["success"] is False
        assert result2["result"] is None, "Failed call must have result=None"

        assert result3["success"] is False
        assert result3["result"] is None, "Failed call must have result=None"

    def test_all_validation_errors_have_type_validation(self):
        """Test that all validation errors have error_type='validation'."""
        # WHAT: Verify validation errors are properly categorized
        # WHY: Ensure agents can distinguish validation vs system errors
        # HOW: Trigger validation errors and check error_type

        result1 = get_tracking_status("INVALID")
        result2 = check_inventory("invalid")
        result3 = calculate_delivery_days(999, "Invalid")

        assert result1["error_type"] == "validation"
        assert result2["error_type"] == "validation"
        assert result3["error_type"] == "validation"


# ============================================================================
# SUMMARY
# ============================================================================

# WHAT: This test suite provides comprehensive validation of refactored functions
# WHY: Ensures learner implementations meet all requirements for agent use
# HOW: Tests cover happy path, validation, edge cases, and format consistency

# Test Coverage Summary:
# - get_tracking_status: 11 tests (3 happy path, 8 validation)
# - check_inventory: 12 tests (4 happy path, 8 validation)
# - calculate_delivery_days: 16 tests (8 happy path, 8 validation)
# - Cross-function: 6 consistency tests
# Total: 45 comprehensive tests

# When run against 1_3_START_naive_tools.py: Many tests will FAIL
# When run against proper logistics_tools.py: All tests should PASS
