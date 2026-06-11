"""
Test suite for 1_1_shipping_tool.py

This test suite validates the calculate_shipping_cost function for:
- Happy path: Valid inputs return correct calculations
- Validation: Invalid inputs return proper error messages
- Edge cases: Boundary values and all tier/zone combinations
- Error format: Standardized response structure

Learning Context:
    Demonstrated in Screencast 1.1 to show proper testing from the start.
    Emphasizes test-driven development and comprehensive validation testing.

Run with: pytest 1_1_test_shipping_tool.py -v
"""

import pytest
from importlib import import_module

# Import from numbered module using importlib
_shipping_tool = import_module('1_1_shipping_tool')
calculate_shipping_cost = _shipping_tool.calculate_shipping_cost
BASE_RATE_PER_KG = _shipping_tool.BASE_RATE_PER_KG
ZONE_MULTIPLIERS = _shipping_tool.ZONE_MULTIPLIERS
CUSTOMER_DISCOUNTS = _shipping_tool.CUSTOMER_DISCOUNTS


# WHAT: Define test fixtures for common test data
# WHY: Avoid repeating test data setup across multiple test functions
# HOW: Use pytest fixtures with @pytest.fixture decorator

@pytest.fixture
def valid_request():
    """Standard valid request for baseline testing."""
    return {
        "weight_kg": 15.0,
        "zone": 2,
        "customer_tier": "Gold"
    }


@pytest.fixture
def expected_cost_valid_request():
    """Expected cost for the valid_request fixture."""
    # Calculation: 15.0 kg * $2.50/kg * 1.5 (zone 2) * 0.9 (10% Gold discount)
    base = 15.0 * BASE_RATE_PER_KG
    with_zone = base * ZONE_MULTIPLIERS[2]
    with_discount = with_zone * (1 - CUSTOMER_DISCOUNTS["Gold"])
    return round(with_discount, 2)


# WHAT: Test happy path scenarios with valid inputs
# WHY: Verify correct calculation logic with known inputs and outputs
# HOW: Call function with valid data, assert expected calculations

def test_basic_calculation(valid_request, expected_cost_valid_request):
    """Test calculation with valid inputs returns correct cost."""
    result = calculate_shipping_cost(**valid_request)

    # WHAT: Verify success response structure
    # WHY: Ensure standardized format for agent parsing
    # HOW: Assert each key has expected type and value

    assert result["success"] is True, "Should return success=True"
    assert result["error"] is None, "Should have no error message"
    assert isinstance(result["result"], (int, float)), "Result should be numeric"

    # WHAT: Verify calculation accuracy
    # WHY: Ensure pricing formula is implemented correctly
    # HOW: Compare result to manually calculated expected value

    assert abs(result["result"] - expected_cost_valid_request) < 0.01, \
        f"Expected {expected_cost_valid_request}, got {result['result']}"


def test_minimum_weight():
    """Test calculation with very small weight."""
    result = calculate_shipping_cost(0.1, 1, "Bronze")

    assert result["success"] is True
    assert result["result"] > 0, "Cost should be positive"

    # Expected: 0.1 * 2.5 * 1.0 * 1.0 = 0.25
    expected = 0.25
    assert abs(result["result"] - expected) < 0.01


def test_large_weight():
    """Test calculation with large weight (500kg)."""
    result = calculate_shipping_cost(500.0, 4, "Bronze")

    assert result["success"] is True

    # Expected: 500 * 2.5 * 3.0 * 1.0 = 3750.0
    expected = 3750.0
    assert abs(result["result"] - expected) < 0.01


def test_international_platinum():
    """Test highest cost scenario: international with Platinum discount."""
    result = calculate_shipping_cost(25.0, 4, "Platinum")

    assert result["success"] is True

    # Expected: 25 * 2.5 * 3.0 * 0.85 = 159.38
    expected = 159.38
    assert abs(result["result"] - expected) < 0.01


# WHAT: Test all customer tier combinations
# WHY: Ensure discount calculations work for every tier
# HOW: Use parametrize to test all four tiers with same base inputs

@pytest.mark.parametrize("tier,discount", [
    ("Bronze", 0.0),
    ("Silver", 0.05),
    ("Gold", 0.10),
    ("Platinum", 0.15),
])
def test_all_customer_tiers(tier, discount):
    """Test that all valid customer tiers are accepted and discounts applied."""
    weight = 10.0
    zone = 2

    result = calculate_shipping_cost(weight, zone, tier)

    assert result["success"] is True, f"Failed for tier: {tier}"

    # Calculate expected cost with this tier's discount
    base = weight * BASE_RATE_PER_KG
    with_zone = base * ZONE_MULTIPLIERS[zone]
    expected = round(with_zone * (1 - discount), 2)

    assert abs(result["result"] - expected) < 0.01, \
        f"Incorrect calculation for {tier} tier"


# WHAT: Test all zone combinations
# WHY: Ensure zone multipliers work for every zone
# HOW: Use parametrize to test all four zones

@pytest.mark.parametrize("zone,multiplier", [
    (1, 1.0),
    (2, 1.5),
    (3, 2.0),
    (4, 3.0),
])
def test_all_zones(zone, multiplier):
    """Test that all valid zones are accepted and multipliers applied."""
    weight = 10.0
    tier = "Bronze"

    result = calculate_shipping_cost(weight, zone, tier)

    assert result["success"] is True, f"Failed for zone: {zone}"

    # Calculate expected cost with this zone's multiplier
    expected = round(weight * BASE_RATE_PER_KG * multiplier, 2)

    assert abs(result["result"] - expected) < 0.01, \
        f"Incorrect calculation for zone {zone}"


# WHAT: Test validation error handling for weight parameter
# WHY: Ensure invalid weights are rejected with clear error messages
# HOW: Test each validation rule (type, positive value) separately

def test_negative_weight():
    """Test that negative weight is rejected with clear error."""
    result = calculate_shipping_cost(-5.0, 2, "Gold")

    # WHAT: Verify error response structure
    # WHY: Ensure standardized error format for agents
    # HOW: Assert success=False and error_type="validation"

    assert result["success"] is False, "Should reject negative weight"
    assert result["result"] is None, "Should have no result on error"
    assert result["error_type"] == "validation", "Should be validation error"
    assert "positive" in result["error"].lower(), "Error should mention 'positive'"
    assert "-5" in result["error"], "Error should include the invalid value"


def test_zero_weight():
    """Test that zero weight is rejected."""
    result = calculate_shipping_cost(0, 2, "Gold")

    assert result["success"] is False
    assert result["error_type"] == "validation"
    assert "positive" in result["error"].lower()


def test_weight_wrong_type_string():
    """Test that string weight is rejected."""
    result = calculate_shipping_cost("15.5", 2, "Gold")

    assert result["success"] is False
    assert result["error_type"] == "validation"
    assert "number" in result["error"].lower() or "int or float" in result["error"].lower()


def test_weight_wrong_type_none():
    """Test that None weight is rejected."""
    result = calculate_shipping_cost(None, 2, "Gold")

    assert result["success"] is False
    assert result["error_type"] == "validation"


# WHAT: Test validation error handling for zone parameter
# WHY: Ensure invalid zones are rejected with clear error messages
# HOW: Test out-of-range zones and wrong types

@pytest.mark.parametrize("invalid_zone", [0, 5, -1, 100])
def test_invalid_zone_out_of_range(invalid_zone):
    """Test that zones outside 1-4 range are rejected."""
    result = calculate_shipping_cost(15.0, invalid_zone, "Gold")

    assert result["success"] is False, f"Should reject zone: {invalid_zone}"
    assert result["error_type"] == "validation"
    assert "zone" in result["error"].lower()
    assert str(invalid_zone) in result["error"], "Error should include the invalid value"


def test_zone_wrong_type_float():
    """Test that float zone is rejected (must be integer)."""
    result = calculate_shipping_cost(15.0, 2.5, "Gold")

    assert result["success"] is False
    assert result["error_type"] == "validation"
    assert "integer" in result["error"].lower()


def test_zone_wrong_type_string():
    """Test that string zone is rejected."""
    result = calculate_shipping_cost(15.0, "2", "Gold")

    assert result["success"] is False
    assert result["error_type"] == "validation"


# WHAT: Test validation error handling for customer_tier parameter
# WHY: Ensure invalid tiers are rejected with clear error messages
# HOW: Test misspellings, wrong case, and invalid values

@pytest.mark.parametrize("invalid_tier", [
    "gold",        # Wrong case
    "GOLD",        # Wrong case
    "Diamond",     # Invalid tier
    "Basic",       # Invalid tier
    "Premium",     # Invalid tier
])
def test_invalid_customer_tier(invalid_tier):
    """Test that invalid customer tiers are rejected."""
    result = calculate_shipping_cost(15.0, 2, invalid_tier)

    assert result["success"] is False, f"Should reject tier: {invalid_tier}"
    assert result["error_type"] == "validation"
    assert "tier" in result["error"].lower() or "customer" in result["error"].lower()
    assert invalid_tier in result["error"], "Error should include the invalid value"


def test_customer_tier_wrong_type():
    """Test that non-string customer_tier is rejected."""
    result = calculate_shipping_cost(15.0, 2, 123)

    assert result["success"] is False
    assert result["error_type"] == "validation"
    assert "string" in result["error"].lower()


# WHAT: Test edge case combinations
# WHY: Ensure function handles unusual but valid input combinations
# HOW: Test boundary scenarios that combine multiple factors

def test_minimum_possible_cost():
    """Test minimum cost scenario: small weight, local, Bronze."""
    result = calculate_shipping_cost(0.1, 1, "Bronze")

    assert result["success"] is True
    # 0.1 * 2.5 * 1.0 * 1.0 = 0.25
    assert result["result"] == 0.25


def test_maximum_discount_scenario():
    """Test maximum discount: Platinum tier (15% off)."""
    result = calculate_shipping_cost(100.0, 1, "Platinum")

    assert result["success"] is True
    # 100 * 2.5 * 1.0 * 0.85 = 212.5
    expected = 212.50
    assert abs(result["result"] - expected) < 0.01


# WHAT: Test that result is properly rounded to 2 decimal places
# WHY: Currency amounts must have exactly 2 decimal places
# HOW: Use calculation that would produce more decimals without rounding

def test_result_rounded_to_two_decimals():
    """Test that results are properly rounded to 2 decimal places."""
    # Use inputs that produce repeating decimals
    result = calculate_shipping_cost(10.0, 2, "Gold")

    assert result["success"] is True

    # Verify result has at most 2 decimal places
    result_str = str(result["result"])
    if "." in result_str:
        decimal_places = len(result_str.split(".")[1])
        assert decimal_places <= 2, f"Result should have at most 2 decimal places, got {decimal_places}"


# WHAT: Test response structure consistency
# WHY: Agents depend on consistent response format
# HOW: Verify all required keys present in both success and error cases

def test_success_response_structure():
    """Test that success response has all required keys."""
    result = calculate_shipping_cost(15.0, 2, "Gold")

    # WHAT: Verify required keys are present
    # WHY: Agents expect specific keys to be present
    # HOW: Assert each key exists and has correct type

    assert "success" in result, "Response must have 'success' key"
    assert "result" in result, "Response must have 'result' key"
    assert "error" in result, "Response must have 'error' key"

    assert isinstance(result["success"], bool), "'success' must be boolean"
    assert result["error"] is None, "'error' should be None on success"


def test_error_response_structure():
    """Test that error response has all required keys."""
    result = calculate_shipping_cost(-5.0, 2, "Gold")

    # WHAT: Verify error response structure
    # WHY: Agents need consistent error format to handle failures
    # HOW: Assert required keys and types for error responses

    assert "success" in result, "Response must have 'success' key"
    assert "result" in result, "Response must have 'result' key"
    assert "error" in result, "Response must have 'error' key"
    assert "error_type" in result, "Error response must have 'error_type' key"

    assert result["success"] is False, "'success' must be False on error"
    assert result["result"] is None, "'result' should be None on error"
    assert isinstance(result["error"], str), "'error' must be string"
    assert result["error_type"] in ["validation", "system"], \
        "'error_type' must be 'validation' or 'system'"


# WHAT: Test multiple validation errors (only first should be caught)
# WHY: Understand validation order and error priority
# HOW: Provide inputs with multiple issues, verify which error is returned

def test_multiple_validation_errors():
    """Test that validation catches first error in order."""
    # Provide invalid weight AND invalid zone
    result = calculate_shipping_cost(-5.0, 10, "Gold")

    # Should catch weight validation first (it's checked first in code)
    assert result["success"] is False
    assert result["error_type"] == "validation"
    assert "weight" in result["error"].lower(), \
        "First validation (weight) should be caught first"


if __name__ == "__main__":
    # WHAT: Run tests with verbose output when executed directly
    # WHY: Allow quick test execution without pytest command
    # HOW: Use pytest.main() with verbose flag

    import sys
    sys.exit(pytest.main([__file__, "-v"]))
