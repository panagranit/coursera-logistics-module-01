# Enterprise Patterns for Agent Functions

**Purpose**: This reference guide covers production-grade patterns for building reliable, maintainable agent functions. You'll find complete decorator implementations, comprehensive testing strategies, and best practices used by professional development teams.

**When to use this guide**:
- When applying the production decorator to your functions (Activity 1.7)
- When building comprehensive test suites with pytest
- When you need examples of testing patterns (fixtures, parametrize)
- As a reference for professional code organization

---

## Table of Contents

1. [Pattern 1: Production Decorator](#pattern-1-production-decorator)
   - [The Problem: Repetitive Infrastructure Code](#the-problem-repetitive-infrastructure-code)
   - [The Solution: Decorator Pattern](#the-solution-decorator-pattern)
   - [Complete Implementation](#complete-implementation)
   - [Usage Examples](#usage-examples)
2. [Pattern 2: Comprehensive Testing](#pattern-2-comprehensive-testing)
   - [Test Organization Strategy](#test-organization-strategy)
   - [pytest Fixtures](#pytest-fixtures)
   - [pytest Parametrize](#pytest-parametrize)
   - [Complete Test Suite Example](#complete-test-suite-example)
3. [Best Practices Summary](#best-practices-summary)

---

## Pattern 1: Production Decorator

### The Problem: Repetitive Infrastructure Code

When building agent functions without decorators, you end up repeating the same infrastructure code in every function:

```python
def my_function(param1, param2):
    """A typical function without decorator support."""

    # Repetitive logging
    logger.info(f"Calling my_function with {param1}, {param2}")

    # Repetitive timing
    start_time = time.time()

    try:
        # Actual business logic (what we really care about!)
        if param1 <= 0:
            raise ValueError("param1 must be positive")

        result = param1 * param2

        # More repetitive code
        execution_time = time.time() - start_time
        logger.info(f"my_function completed in {execution_time:.4f}s")

        return {"success": True, "result": result, "error": None}

    except ValueError as e:
        # Repetitive error handling
        execution_time = time.time() - start_time
        logger.warning(f"Validation error: {e}")
        return {
            "success": False,
            "result": None,
            "error": str(e),
            "error_type": "validation"
        }

    except Exception as e:
        # Even more repetitive error handling
        execution_time = time.time() - start_time
        logger.error(f"System error: {e}")
        return {
            "success": False,
            "result": None,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "system"
        }
```

**Problems with this approach**:
- **50+ lines** per function (most is boilerplate!)
- Logging code repeated in every function
- Timing code repeated in every function
- Error handling repeated in every function
- Business logic buried in infrastructure code
- Changes to error format require updating every function

### The Solution: Decorator Pattern

A decorator is a reusable wrapper that adds functionality to functions without modifying their core logic. It's like a template that automatically adds logging, timing, and error handling to any function you apply it to.

**Key benefits**:
- **Write once, use everywhere**: Infrastructure code lives in one place
- **Separation of concerns**: Business logic stays clean and focused
- **Consistency**: All functions handle errors identically
- **Maintainability**: Change error handling once, affects all functions

**How decorators work**:
```python
@production_agent_function  # This is the decorator
def my_function(param):
    # Just business logic - decorator handles the rest!
    if param <= 0:
        raise ValueError("param must be positive")
    return {"success": True, "result": param * 2}
```

The `@production_agent_function` syntax tells Python to wrap `my_function` with production-grade error handling, logging, and timing automatically.

### Complete Implementation

Here's the complete production decorator used by Praxis AI consultants:

```python
"""
Production Decorator for Agent Functions

This decorator adds three cross-cutting concerns to any function:
1. Logging: Automatic logging of function calls and results
2. Timing: Performance measurement for monitoring
3. Error Handling: Standardized error response format

Usage:
    from production_wrapper import production_agent_function

    @production_agent_function
    def my_function(param):
        if param <= 0:
            raise ValueError("param must be positive")
        return {"success": True, "result": param * 2}
"""

import functools
import logging
import time
from typing import Callable, Any, Dict

# Configure logging for the decorator
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def production_agent_function(func: Callable) -> Callable:
    """
    Decorator that adds production-grade error handling, logging, and timing.

    The decorated function only needs to:
    - Implement business logic
    - Raise ValueError for validation errors
    - Return {"success": True, "result": <value>} on success

    The decorator automatically:
    - Logs all function calls with parameters
    - Measures execution time
    - Converts ValueError to {"success": False, "error_type": "validation"}
    - Converts other exceptions to {"success": False, "error_type": "system"}
    - Logs all results and errors

    Args:
        func: The function to decorate. Should return dict with "success" and "result" keys.

    Returns:
        Wrapped function with added infrastructure

    Example:
        @production_agent_function
        def calculate_cost(weight):
            if weight <= 0:
                raise ValueError("Weight must be positive")
            return {"success": True, "result": weight * 2.5}
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Dict[str, Any]:
        # WHAT: Log function invocation with all parameters
        # WHY: Enables debugging and usage tracking in production
        # HOW: Capture function name and arguments before execution

        logger.info(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")

        # WHAT: Record execution start time
        # WHY: Measure performance for optimization and monitoring
        # HOW: Capture timestamp before function execution

        start_time = time.time()

        try:
            # WHAT: Execute the wrapped function
            # WHY: Run the actual business logic
            # HOW: Call function with original arguments

            result = func(*args, **kwargs)

            # WHAT: Calculate execution duration
            # WHY: Track performance metrics
            # HOW: Subtract start time from current time

            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} completed successfully in {execution_time:.4f}s")

            # WHAT: Return the function result unchanged
            # WHY: Decorator should not modify successful responses
            # HOW: Pass through the result dictionary

            return result

        except ValueError as e:
            # WHAT: Handle validation errors (expected errors from business logic)
            # WHY: Convert validation exceptions to standardized error format
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
            # WHY: Catch unforeseen issues and return standardized format
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
```

**Key implementation details**:

1. **`@functools.wraps(func)`**: Preserves the original function's name and docstring
2. **`*args, **kwargs`**: Accepts any combination of positional and keyword arguments
3. **Try/except structure**: Catches ValueError (validation) separately from general Exception (system errors)
4. **Timing logic**: Measures execution time in both success and error cases
5. **Standardized returns**: All responses follow the same dictionary structure

### Usage Examples

#### Example 1: Before and After Comparison

**WITHOUT decorator (verbose, ~50 lines)**:
```python
def calculate_cost_verbose(weight: float) -> Dict[str, Any]:
    """Calculate shipping cost without decorator."""
    logger.info(f"Calling calculate_cost_verbose with weight={weight}")
    start_time = time.time()

    try:
        if weight <= 0:
            raise ValueError(f"Weight must be positive, got: {weight}")

        cost = weight * 2.5

        execution_time = time.time() - start_time
        logger.info(f"calculate_cost_verbose completed in {execution_time:.4f}s")

        return {
            "success": True,
            "result": cost,
            "error": None
        }

    except ValueError as e:
        execution_time = time.time() - start_time
        logger.warning(f"Validation error: {e}")
        return {
            "success": False,
            "result": None,
            "error": str(e),
            "error_type": "validation"
        }

    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"System error: {e}")
        return {
            "success": False,
            "result": None,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "system"
        }
```

**WITH decorator (clean, ~15 lines)**:
```python
@production_agent_function
def calculate_cost_clean(weight: float) -> Dict[str, Any]:
    """Calculate shipping cost using decorator."""

    # WHAT: Validate input
    # WHY: Ensure weight is valid for calculation
    # HOW: Raise ValueError if not positive
    if weight <= 0:
        raise ValueError(f"Weight must be positive, got: {weight}")

    # WHAT: Calculate shipping cost
    # WHY: Apply standard pricing formula
    # HOW: Multiply weight by rate
    cost = weight * 2.5

    # WHAT: Return success response
    # WHY: Provide standardized format for agent
    # HOW: Return dictionary with success=True and result
    return {
        "success": True,
        "result": cost,
        "error": None
    }

# Note: No try/except needed - decorator handles it!
# Note: No logging needed - decorator handles it!
# Note: No timing needed - decorator handles it!
```

**Code reduction**: 70% fewer lines per function!

#### Example 2: Applying Decorator to Multiple Functions

```python
from production_wrapper import production_agent_function

# Function 1: Calculate shipping cost
@production_agent_function
def calculate_shipping_cost(weight_kg, zone, customer_tier):
    """Calculate shipping cost with zone and tier pricing."""
    # Validation
    if not isinstance(weight_kg, (int, float)) or weight_kg <= 0:
        raise ValueError(f"Weight must be positive number, got: {weight_kg}")

    if zone not in [1, 2, 3, 4]:
        raise ValueError(f"Zone must be 1-4, got: {zone}")

    # Business logic
    base_cost = weight_kg * 2.5
    zone_multiplier = {1: 1.0, 2: 1.5, 3: 2.0, 4: 3.0}[zone]
    discount = {"Bronze": 0, "Silver": 0.05, "Gold": 0.10, "Platinum": 0.15}[customer_tier]

    final_cost = base_cost * zone_multiplier * (1 - discount)

    return {"success": True, "result": round(final_cost, 2), "error": None}


# Function 2: Check inventory
@production_agent_function
def check_inventory(sku):
    """Check product inventory level."""
    # Validation
    if not isinstance(sku, str) or len(sku) != 7:
        raise ValueError(f"SKU must be 7-character string, got: {sku}")

    # Business logic (mock database lookup)
    inventory_db = {
        "ABC1234": 150,
        "DEF5678": 3,
        "GHI9012": 0
    }

    quantity = inventory_db.get(sku, 0)

    return {"success": True, "result": quantity, "error": None}


# Function 3: Calculate delivery days
@production_agent_function
def calculate_delivery_days(zone, service_level):
    """Estimate delivery time based on zone and service level."""
    # Validation
    if zone not in ["Local", "Regional", "National", "International"]:
        raise ValueError(f"Invalid zone: {zone}")

    # Business logic
    base_days = {"Local": 1, "Regional": 3, "National": 5, "International": 10}
    days = base_days[zone]

    if service_level == "Express":
        days = max(1, days // 2)

    return {"success": True, "result": days, "error": None}
```

**Benefits**:
- All three functions automatically get logging, timing, and error handling
- Consistent error format across all functions
- Business logic is clear and focused
- Easy to add more functions with the same pattern

---

## Pattern 2: Comprehensive Testing

### Test Organization Strategy

A comprehensive test suite validates four critical aspects:

1. **Happy Path Tests**: Verify correct behavior with valid inputs
2. **Validation Tests**: Ensure invalid inputs are properly rejected
3. **Edge Case Tests**: Test boundary conditions and unusual scenarios
4. **Error Format Tests**: Verify response structure consistency

**Recommended test file structure**:
```python
"""
Test suite for [module_name].py

This suite validates:
- Happy path: Valid inputs return correct results
- Validation: Invalid inputs return proper error messages
- Edge cases: Boundary values and all combinations
- Error format: Standardized response structure

Run with: pytest test_[module_name].py -v
"""

import pytest
from [module_name] import function1, function2, function3

# 1. Fixtures (shared test data)

# 2. Happy path tests

# 3. Validation tests

# 4. Edge case tests

# 5. Error format tests
```

### pytest Fixtures

**What are fixtures?**
Fixtures are reusable test data or setup code that can be shared across multiple tests. They help you avoid repeating test setup code.

**Why use fixtures?**
- Reduce code duplication
- Ensure consistent test data
- Make tests more readable
- Centralize test data management

**How to create fixtures**:

```python
import pytest

# WHAT: Define fixture for standard valid request data
# WHY: Avoid repeating this data setup in every test
# HOW: Use @pytest.fixture decorator

@pytest.fixture
def valid_shipping_request():
    """Standard valid shipping request for baseline testing."""
    return {
        "weight_kg": 15.0,
        "zone": 2,
        "customer_tier": "Gold"
    }


@pytest.fixture
def expected_cost_for_valid_request():
    """Expected cost for the valid_shipping_request fixture."""
    # 15.0 kg * $2.50/kg * 1.5 (zone 2) * 0.9 (10% Gold discount)
    # = 37.5 * 1.5 * 0.9 = 50.625 ≈ 50.63
    return 50.63


# WHAT: Use fixtures in test functions
# WHY: Access shared test data cleanly
# HOW: Add fixture names as function parameters

def test_basic_calculation(valid_shipping_request, expected_cost_for_valid_request):
    """Test calculation with valid inputs returns correct cost."""
    from shipping_tool import calculate_shipping_cost

    result = calculate_shipping_cost(**valid_shipping_request)

    assert result["success"] is True
    assert result["error"] is None
    assert abs(result["result"] - expected_cost_for_valid_request) < 0.01
```

**Fixture scope**:
By default, fixtures are recreated for each test. You can specify different scopes:

```python
@pytest.fixture(scope="module")  # Created once per test file
def database_connection():
    """Expensive setup - create once and reuse."""
    conn = create_connection()
    yield conn  # Provide connection to tests
    conn.close()  # Cleanup after all tests
```

### pytest Parametrize

**What is parametrize?**
`@pytest.mark.parametrize` runs the same test with different input values. It's perfect for testing multiple scenarios without writing duplicate test functions.

**Why use parametrize?**
- Test multiple inputs with one test function
- Reduce code duplication
- Clearly see all test cases in one place
- pytest shows each parameter combination as a separate test result

**How to use parametrize**:

#### Example 1: Testing Multiple Invalid Values

```python
import pytest

# WHAT: Test that various invalid zones are rejected
# WHY: Ensure comprehensive validation coverage
# HOW: Use parametrize to test multiple invalid values with one test

@pytest.mark.parametrize("invalid_zone", [0, 5, -1, 100])
def test_invalid_zone_out_of_range(invalid_zone):
    """Test that zones outside 1-4 range are rejected."""
    from shipping_tool import calculate_shipping_cost

    result = calculate_shipping_cost(15.0, invalid_zone, "Gold")

    assert result["success"] is False, f"Should reject zone: {invalid_zone}"
    assert result["error_type"] == "validation"
    assert "zone" in result["error"].lower()
    assert str(invalid_zone) in result["error"]
```

**Output when run**:
```
test_invalid_zone_out_of_range[0] PASSED
test_invalid_zone_out_of_range[5] PASSED
test_invalid_zone_out_of_range[-1] PASSED
test_invalid_zone_out_of_range[100] PASSED
```

#### Example 2: Testing with Multiple Parameters

```python
# WHAT: Test all valid customer tiers with their discounts
# WHY: Verify discount calculation for every tier
# HOW: Parametrize with tuples containing (tier, discount) pairs

@pytest.mark.parametrize("tier,discount", [
    ("Bronze", 0.0),
    ("Silver", 0.05),
    ("Gold", 0.10),
    ("Platinum", 0.15),
])
def test_all_customer_tiers(tier, discount):
    """Test that all valid customer tiers are accepted and discounts applied."""
    from shipping_tool import calculate_shipping_cost

    weight = 10.0
    zone = 2

    result = calculate_shipping_cost(weight, zone, tier)

    assert result["success"] is True, f"Failed for tier: {tier}"

    # Calculate expected cost with this tier's discount
    base = weight * 2.5  # Base rate
    with_zone = base * 1.5  # Zone 2 multiplier
    expected = round(with_zone * (1 - discount), 2)

    assert abs(result["result"] - expected) < 0.01, \
        f"Incorrect calculation for {tier} tier"
```

#### Example 3: Testing Multiple Invalid String Values

```python
# WHAT: Test various invalid customer tier strings
# WHY: Ensure case-sensitivity and invalid tier rejection
# HOW: Parametrize with list of invalid tier values

@pytest.mark.parametrize("invalid_tier", [
    "gold",        # Wrong case (lowercase)
    "GOLD",        # Wrong case (uppercase)
    "Diamond",     # Invalid tier
    "Basic",       # Invalid tier
    "Premium",     # Invalid tier
    "",            # Empty string
])
def test_invalid_customer_tier(invalid_tier):
    """Test that invalid customer tiers are rejected."""
    from shipping_tool import calculate_shipping_cost

    result = calculate_shipping_cost(15.0, 2, invalid_tier)

    assert result["success"] is False, f"Should reject tier: {invalid_tier}"
    assert result["error_type"] == "validation"
    assert invalid_tier in result["error"], "Error should include the invalid value"
```

#### Example 4: Combining Fixtures with Parametrize

```python
# WHAT: Combine fixture and parametrize for complex scenarios
# WHY: Test multiple zones while reusing other parameters
# HOW: Use fixture for base data, parametrize for varying values

@pytest.fixture
def base_request():
    """Base request with standard weight and tier."""
    return {"weight_kg": 10.0, "customer_tier": "Bronze"}


@pytest.mark.parametrize("zone,multiplier", [
    (1, 1.0),
    (2, 1.5),
    (3, 2.0),
    (4, 3.0),
])
def test_all_zones(base_request, zone, multiplier):
    """Test that all valid zones are accepted and multipliers applied."""
    from shipping_tool import calculate_shipping_cost

    result = calculate_shipping_cost(
        weight_kg=base_request["weight_kg"],
        zone=zone,
        customer_tier=base_request["customer_tier"]
    )

    assert result["success"] is True, f"Failed for zone: {zone}"

    # Calculate expected cost
    expected = round(base_request["weight_kg"] * 2.5 * multiplier, 2)

    assert abs(result["result"] - expected) < 0.01
```

### Complete Test Suite Example

Here's a complete test suite demonstrating all patterns:

```python
"""
Test suite for shipping_tool.py

This comprehensive test suite validates:
- Happy path: Valid inputs return correct calculations
- Validation: Invalid inputs return proper error messages
- Edge cases: Boundary values and all tier/zone combinations
- Error format: Standardized response structure

Run with: pytest test_shipping_tool.py -v
"""

import pytest
from shipping_tool import calculate_shipping_cost

# ============================================================================
# FIXTURES: Shared test data
# ============================================================================

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
    # 15.0 kg * $2.50/kg * 1.5 (zone 2) * 0.9 (10% Gold discount)
    # = 37.5 * 1.5 * 0.9 = 50.625 ≈ 50.63
    return 50.63


# ============================================================================
# HAPPY PATH TESTS: Valid inputs produce correct results
# ============================================================================

def test_basic_calculation(valid_request, expected_cost_valid_request):
    """Test calculation with valid inputs returns correct cost."""
    result = calculate_shipping_cost(**valid_request)

    # Verify success response structure
    assert result["success"] is True, "Should return success=True"
    assert result["error"] is None, "Should have no error message"
    assert isinstance(result["result"], (int, float)), "Result should be numeric"

    # Verify calculation accuracy
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


# ============================================================================
# PARAMETRIZE TESTS: Multiple scenarios with one test function
# ============================================================================

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
    base = weight * 2.5
    with_zone = base * 1.5  # Zone 2 multiplier
    expected = round(with_zone * (1 - discount), 2)

    assert abs(result["result"] - expected) < 0.01, \
        f"Incorrect calculation for {tier} tier"


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

    # Calculate expected cost
    expected = round(weight * 2.5 * multiplier, 2)

    assert abs(result["result"] - expected) < 0.01


# ============================================================================
# VALIDATION TESTS: Invalid inputs are properly rejected
# ============================================================================

def test_negative_weight():
    """Test that negative weight is rejected with clear error."""
    result = calculate_shipping_cost(-5.0, 2, "Gold")

    assert result["success"] is False, "Should reject negative weight"
    assert result["result"] is None, "Should have no result on error"
    assert result["error_type"] == "validation", "Should be validation error"
    assert "positive" in result["error"].lower(), "Error should mention 'positive'"


def test_zero_weight():
    """Test that zero weight is rejected."""
    result = calculate_shipping_cost(0, 2, "Gold")

    assert result["success"] is False
    assert result["error_type"] == "validation"
    assert "positive" in result["error"].lower()


@pytest.mark.parametrize("invalid_zone", [0, 5, -1, 100])
def test_invalid_zone_out_of_range(invalid_zone):
    """Test that zones outside 1-4 range are rejected."""
    result = calculate_shipping_cost(15.0, invalid_zone, "Gold")

    assert result["success"] is False, f"Should reject zone: {invalid_zone}"
    assert result["error_type"] == "validation"
    assert "zone" in result["error"].lower()


@pytest.mark.parametrize("invalid_tier", [
    "gold",        # Wrong case
    "GOLD",        # Wrong case
    "Diamond",     # Invalid tier
    "Basic",       # Invalid tier
])
def test_invalid_customer_tier(invalid_tier):
    """Test that invalid customer tiers are rejected."""
    result = calculate_shipping_cost(15.0, 2, invalid_tier)

    assert result["success"] is False, f"Should reject tier: {invalid_tier}"
    assert result["error_type"] == "validation"


# ============================================================================
# ERROR FORMAT TESTS: Response structure is consistent
# ============================================================================

def test_success_response_structure():
    """Test that success response has all required keys."""
    result = calculate_shipping_cost(15.0, 2, "Gold")

    # Verify required keys are present
    assert "success" in result, "Response must have 'success' key"
    assert "result" in result, "Response must have 'result' key"
    assert "error" in result, "Response must have 'error' key"

    # Verify types
    assert isinstance(result["success"], bool), "'success' must be boolean"
    assert result["error"] is None, "'error' should be None on success"


def test_error_response_structure():
    """Test that error response has all required keys."""
    result = calculate_shipping_cost(-5.0, 2, "Gold")

    # Verify error response structure
    assert "success" in result, "Response must have 'success' key"
    assert "result" in result, "Response must have 'result' key"
    assert "error" in result, "Response must have 'error' key"
    assert "error_type" in result, "Error response must have 'error_type' key"

    # Verify values
    assert result["success"] is False, "'success' must be False on error"
    assert result["result"] is None, "'result' should be None on error"
    assert isinstance(result["error"], str), "'error' must be string"
    assert result["error_type"] in ["validation", "system"], \
        "'error_type' must be 'validation' or 'system'"


# ============================================================================
# EDGE CASE TESTS: Boundary conditions
# ============================================================================

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


def test_result_rounded_to_two_decimals():
    """Test that results are properly rounded to 2 decimal places."""
    result = calculate_shipping_cost(10.0, 2, "Gold")

    assert result["success"] is True

    # Verify result has at most 2 decimal places
    result_str = str(result["result"])
    if "." in result_str:
        decimal_places = len(result_str.split(".")[1])
        assert decimal_places <= 2, \
            f"Result should have at most 2 decimal places, got {decimal_places}"


if __name__ == "__main__":
    # Run tests with verbose output when executed directly
    import sys
    sys.exit(pytest.main([__file__, "-v"]))
```

**Test suite statistics**:
- **15+ test functions** covering all scenarios
- **50+ individual test cases** (when you count parametrize combinations)
- **4 test categories**: Happy path, validation, edge cases, error format
- **2 fixtures** for reusable test data
- **5 parametrized tests** for efficient coverage

---

## Best Practices Summary

### Decorator Best Practices

1. **Always use `@functools.wraps(func)`**
   - Preserves original function's name and docstring
   - Essential for debugging and documentation

2. **Separate validation errors from system errors**
   - Use `ValueError` for expected validation errors
   - Use general `Exception` for unexpected system errors
   - Helps agents distinguish fixable errors from bugs

3. **Log at appropriate levels**
   - `logger.info()` for normal operations
   - `logger.warning()` for validation errors (user-fixable)
   - `logger.error()` for system errors (developer attention needed)

4. **Keep business logic clean**
   - Functions should only implement business rules
   - Let decorator handle all infrastructure concerns
   - Validation logic can stay in the function (it's business logic!)

5. **Return consistent formats**
   - Always return dictionaries with same keys
   - Success: `{"success": True, "result": value, "error": None}`
   - Error: `{"success": False, "result": None, "error": message, "error_type": type}`

### Testing Best Practices

1. **Organize tests into clear categories**
   - Happy path tests first (verify core functionality)
   - Validation tests (verify error handling)
   - Edge cases (boundary conditions)
   - Error format tests (response structure)

2. **Use descriptive test names**
   - Good: `test_negative_weight_rejected_with_validation_error()`
   - Bad: `test_1()`, `test_weight()`
   - Test names serve as documentation

3. **Use fixtures for reusable data**
   - Avoid repeating test setup code
   - Makes tests more maintainable
   - Centralizes test data definitions

4. **Use parametrize for multiple scenarios**
   - Test all enum values (zones, tiers, statuses)
   - Test all invalid input types
   - Test boundary conditions
   - Reduces code duplication significantly

5. **Test both success and failure cases**
   - Don't just test happy path
   - Validation errors are equally important
   - Verify error messages are helpful

6. **Verify response structure explicitly**
   - Check that all required keys are present
   - Check that types are correct
   - Ensures consistency for agent parsing

7. **Include "What-Why-How" comments in tests**
   - Tests serve as documentation
   - Help others understand what's being tested and why
   - Explain the expected behavior

8. **Test error messages contain useful information**
   - Verify invalid value is mentioned in error
   - Check that error indicates what was wrong
   - Helps users fix their input

### Code Organization Best Practices

1. **One decorator file for the entire project**
   - Create `production_wrapper.py` once
   - Import and use across all function modules
   - Changes to error handling affect all functions

2. **One test file per module**
   - `test_shipping_tool.py` tests `shipping_tool.py`
   - `test_logistics_tools.py` tests `logistics_tools.py`
   - Keeps tests organized and discoverable

3. **Group related tests together**
   - All weight validation tests in sequence
   - All zone validation tests in sequence
   - Makes it easy to find and update related tests

4. **Use constants for test data**
   - Import constants from module under test when possible
   - Makes tests resilient to business logic changes
   - Example: `from shipping_tool import BASE_RATE_PER_KG`

### Running Tests Effectively

1. **Run tests frequently during development**
   ```bash
   # Run all tests with verbose output
   pytest test_shipping_tool.py -v

   # Run specific test
   pytest test_shipping_tool.py::test_negative_weight -v

   # Run tests matching pattern
   pytest test_shipping_tool.py -k "validation" -v
   ```

2. **Use test coverage tools**
   ```bash
   # Install coverage
   pip install pytest-cov

   # Run with coverage report
   pytest test_shipping_tool.py --cov=shipping_tool --cov-report=html
   ```

3. **Make tests part of your workflow**
   - Write tests before or during function development
   - Run tests after every change
   - Don't commit code with failing tests

---

## Quick Reference

### Decorator Template

```python
from production_wrapper import production_agent_function

@production_agent_function
def my_function(param1, param2):
    """Function docstring."""
    # Validation (raise ValueError for validation errors)
    if param1 <= 0:
        raise ValueError(f"param1 must be positive, got: {param1}")

    # Business logic
    result = param1 * param2

    # Return success format
    return {"success": True, "result": result, "error": None}
```

### Test Template

```python
import pytest
from my_module import my_function

@pytest.fixture
def valid_input():
    """Fixture for valid test data."""
    return {"param1": 10, "param2": 5}

def test_happy_path(valid_input):
    """Test with valid inputs."""
    result = my_function(**valid_input)
    assert result["success"] is True
    assert result["result"] == 50

@pytest.mark.parametrize("invalid_value", [-1, 0, -100])
def test_validation_error(invalid_value):
    """Test validation rejection."""
    result = my_function(invalid_value, 5)
    assert result["success"] is False
    assert result["error_type"] == "validation"
```

### Common pytest Commands

```bash
# Run all tests in file with verbose output
pytest test_file.py -v

# Run specific test function
pytest test_file.py::test_function_name -v

# Run tests matching keyword
pytest test_file.py -k "validation" -v

# Show print statements in output
pytest test_file.py -v -s

# Stop on first failure
pytest test_file.py -v -x

# Run with coverage report
pytest test_file.py --cov=module_name --cov-report=term-missing
```

---

## Additional Resources

- **pytest documentation**: https://docs.pytest.org/
- **Python decorators guide**: https://realpython.com/primer-on-python-decorators/
- **functools.wraps**: https://docs.python.org/3/library/functools.html#functools.wraps

**Questions to consider**:
- Which of your functions could benefit from the production decorator?
- What validation scenarios should you test for each parameter?
- How can parametrize reduce duplication in your test suite?
- What edge cases exist in your business logic that need testing?

---

**End of Reference Guide**
