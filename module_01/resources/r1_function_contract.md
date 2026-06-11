# The Agent-Ready Function Contract

## Overview

An **agent-ready function contract** is a two-artifact approach that enables OpenAI agents to intelligently discover, select, and execute your custom business functions. Think of it as a binding agreement between your agent and your code:

1. **The Specification (JSON)**: A machine-readable description that tells the agent WHEN and HOW to use your function
2. **The Implementation (Python)**: A production-ready function that handles validation, executes business logic, and returns standardized results

This guide provides the complete template and best practices for creating reliable, agent-callable custom functions.

---

## Why Two Artifacts?

The separation of specification and implementation serves distinct purposes:

**The Specification** answers:
- "What does this function do?"
- "When should the agent use it?"
- "What parameters does it need?"
- "What constraints exist on those parameters?"

**The Implementation** answers:
- "How does the business logic work?"
- "What happens when inputs are invalid?"
- "How are errors reported to the agent?"
- "What format does the result take?"

By separating these concerns, you can:
- Update descriptions without modifying code
- Reuse specifications across different implementations
- Test agent selection behavior independently from function logic
- Maintain clear contracts that agents and developers both understand

---

## Part 1: The Specification (JSON)

### Purpose

The JSON specification is what the OpenAI agent "sees" when deciding whether to use your function. A well-written specification enables the agent to:
- Match user queries to the correct function
- Collect the required parameters from conversation context
- Understand constraints and format requirements
- Avoid selecting the wrong function for a task

### Structure

Every function specification must include three required fields:

```json
{
  "name": "function_name_here",
  "description": "Clear, conversational explanation of what this function does and when to use it.",
  "parameters": {
    "type": "object",
    "properties": {
      "parameter_name": {
        "type": "string|number|integer|boolean|array|object",
        "description": "Detailed explanation of what this parameter represents, with examples if helpful.",
        "enum": ["option1", "option2"]  // Optional: for constrained values
      }
    },
    "required": ["parameter_name"]
  }
}
```

### Required Fields Explained

#### 1. `name` (string)

The unique identifier for your function. Must match your Python function name exactly.

**Best Practices**:
- Use descriptive, action-oriented names: `calculate_shipping_cost`, `get_tracking_status`
- Use snake_case (lowercase with underscores)
- Avoid generic names: `process_request`, `handle_data`
- Be specific about the action: `check_inventory` not just `inventory`

**Examples**:
```json
// Good names
"name": "calculate_shipping_cost"
"name": "get_tracking_status"
"name": "check_inventory_availability"

// Avoid
"name": "process"           // Too generic
"name": "calculateCost"     // Wrong case convention
"name": "func1"             // Not descriptive
```

#### 2. `description` (string)

The most critical field for agent selection. This is your chance to explain WHEN and WHY the agent should choose this function.

**Best Practices**:
- Write conversationally, as if explaining to a colleague
- Start with what the function does
- Mention specific use cases or trigger phrases
- Include any important limitations or requirements
- Aim for 1-3 sentences
- Think about what the user might say that should trigger this function

**Good vs. Bad Descriptions**:

```json
// ❌ BAD: Too technical, no context
{
  "description": "Returns shipping cost based on weight, zone, and tier parameters."
}

// ✅ GOOD: Explains when to use, provides context
{
  "description": "Calculate the shipping cost for a package. Use this when customers ask about delivery pricing, shipping fees, or how much it costs to send an item. Requires package weight, delivery zone, and customer loyalty tier."
}

// ❌ BAD: Too brief, no use case guidance
{
  "description": "Gets package status."
}

// ✅ GOOD: Clear use cases, helpful examples
{
  "description": "Look up the current delivery status of a package using its tracking code. Use this when customers ask 'where is my package?', 'has my order shipped?', or provide a 9-digit tracking number. Returns status like 'In Transit', 'Delivered', or 'Unknown'."
}
```

#### 3. `parameters` (object)

The JSON Schema defining what inputs your function accepts. This follows the JSON Schema specification.

**Structure**:
```json
"parameters": {
  "type": "object",              // Always "object" for function parameters
  "properties": {                // Define each parameter here
    "parameter_name": {
      "type": "...",            // Data type
      "description": "..."       // What this parameter means
    }
  },
  "required": ["param1", "param2"]  // List of required parameters
}
```

**Parameter Types**:
- `"string"` - Text values
- `"number"` - Floating-point numbers (e.g., 15.5, 100.0)
- `"integer"` - Whole numbers only (e.g., 1, 2, 3)
- `"boolean"` - true or false
- `"array"` - List of values
- `"object"` - Nested structure

**Using `enum` for Constrained Values**:

When a parameter has a limited set of valid values, use `enum`:

```json
{
  "zone": {
    "type": "integer",
    "description": "Delivery zone: 1 (local), 2 (regional), 3 (national), 4 (international)",
    "enum": [1, 2, 3, 4]
  },
  "customer_tier": {
    "type": "string",
    "description": "Customer loyalty level: Bronze, Silver, Gold, or Platinum",
    "enum": ["Bronze", "Silver", "Gold", "Platinum"]
  }
}
```

**Parameter Descriptions**:

Be specific and include examples:

```json
// ❌ BAD: Too brief
{
  "weight_kg": {
    "type": "number",
    "description": "Package weight"
  }
}

// ✅ GOOD: Explains format and expectations
{
  "weight_kg": {
    "type": "number",
    "description": "Package weight in kilograms (e.g., 2.5, 15.0). Must be a positive number."
  }
}
```

### Complete Specification Example

Here's a production-ready specification for a shipping cost calculator:

```json
{
  "name": "calculate_shipping_cost",
  "description": "Calculate the shipping cost for a package based on weight, delivery zone, and customer loyalty tier. Use this when customers ask about delivery pricing, shipping fees, or how much it costs to send an item. The function applies zone-based multipliers and loyalty discounts to determine the final price.",
  "parameters": {
    "type": "object",
    "properties": {
      "weight_kg": {
        "type": "number",
        "description": "Package weight in kilograms (e.g., 2.5, 15.0). Must be a positive number."
      },
      "zone": {
        "type": "integer",
        "description": "Delivery zone: 1 (local), 2 (regional), 3 (national), 4 (international)",
        "enum": [1, 2, 3, 4]
      },
      "customer_tier": {
        "type": "string",
        "description": "Customer loyalty level affecting discount rate",
        "enum": ["Bronze", "Silver", "Gold", "Platinum"]
      }
    },
    "required": ["weight_kg", "zone", "customer_tier"]
  }
}
```

**What makes this specification effective**:
1. ✅ Descriptive function name (`calculate_shipping_cost`)
2. ✅ Clear description with use cases ("when customers ask about delivery pricing...")
3. ✅ Specific parameter types (`number`, `integer`, `string`)
4. ✅ Helpful parameter descriptions with examples
5. ✅ `enum` constraints for zone and tier (prevents invalid values)
6. ✅ All parameters marked as required

---

## Part 2: The Implementation (Python)

### Purpose

The Python implementation executes the actual business logic after the agent selects your function and provides the parameters. A production-ready implementation must:
- Validate all inputs thoroughly
- Handle errors gracefully
- Return results in a standardized format
- Provide clear error messages when things go wrong

### Standard Template

Every agent-callable function should follow this pattern:

```python
def function_name(param1, param2, param3):
    """
    Brief description of what this function does.

    Args:
        param1 (type): Description of parameter 1
        param2 (type): Description of parameter 2
        param3 (type): Description of parameter 3

    Returns:
        dict: Standardized response with keys:
            - success (bool): True if operation succeeded, False otherwise
            - result (any): The actual result value (None if error)
            - error (str): Error message if success=False, None otherwise
            - error_type (str): "validation" or "system" (only present if error)

    Raises:
        None: Function catches all exceptions and returns error dict

    Example:
        >>> result = function_name(value1, value2, value3)
        >>> print(result)
        {'success': True, 'result': 42.50, 'error': None}
    """

    try:
        # WHAT: Validate param1
        # WHY: Ensure param1 meets business requirements before processing
        # HOW: Check type and value constraints, raise ValueError if invalid
        if not isinstance(param1, expected_type):
            raise ValueError(f"param1 must be {expected_type}")
        if param1 <= 0:  # Example constraint
            raise ValueError("param1 must be positive")

        # WHAT: Validate param2
        # WHY: Prevent invalid data from reaching business logic
        # HOW: Check against allowed values
        if param2 not in ALLOWED_VALUES:
            raise ValueError(f"param2 must be one of {ALLOWED_VALUES}")

        # WHAT: Execute core business logic
        # WHY: Perform the actual calculation/operation this function provides
        # HOW: Use validated inputs to compute result
        result = perform_calculation(param1, param2, param3)

        # WHAT: Return success response
        # WHY: Standardized format allows agent to handle result consistently
        # HOW: Dictionary with success=True and result value
        return {
            "success": True,
            "result": result,
            "error": None
        }

    except ValueError as e:
        # WHAT: Handle validation errors
        # WHY: Return clear error message to agent without crashing
        # HOW: Catch ValueError (from our validation), return error dict
        return {
            "success": False,
            "result": None,
            "error": str(e),
            "error_type": "validation"
        }

    except Exception as e:
        # WHAT: Handle unexpected errors
        # WHY: Prevent crashes, log issues for debugging
        # HOW: Catch all other exceptions, return system error
        return {
            "success": False,
            "result": None,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "system"
        }
```

### Template Components Explained

#### 1. Function Signature

```python
def function_name(param1, param2, param3):
```

**Best Practices**:
- Name must exactly match the `name` in your JSON specification
- Use descriptive parameter names (not `x`, `y`, `data`)
- Order parameters logically (most important first)

#### 2. Docstring

```python
"""
Brief description.

Args:
    param1 (type): Description
    ...

Returns:
    dict: Description of return format

Example:
    >>> code example
"""
```

**Best Practices**:
- Start with a clear one-sentence summary
- Document every parameter with type and purpose
- Explicitly describe the return format
- Include a usage example showing expected output

#### 3. Validation Section

```python
try:
    # WHAT: Validate weight_kg
    # WHY: Ensure positive number to prevent calculation errors
    # HOW: Check type and value, raise ValueError if invalid
    if not isinstance(weight_kg, (int, float)):
        raise ValueError("weight_kg must be a number")
    if weight_kg <= 0:
        raise ValueError("weight_kg must be positive")
```

**Validation Checklist**:
- ✅ Type checking (`isinstance()`)
- ✅ Range validation (min/max values)
- ✅ Format validation (for strings: length, pattern)
- ✅ Enum validation (check against allowed values)
- ✅ Clear error messages explaining what's wrong

**Example Validation Patterns**:

```python
# Type validation
if not isinstance(tracking_code, str):
    raise ValueError("tracking_code must be a string")

# Range validation
if zone < 1 or zone > 4:
    raise ValueError("zone must be between 1 and 4")

# Format validation (tracking code example)
if len(tracking_code) != 9:
    raise ValueError("tracking_code must be exactly 9 digits")
if not tracking_code.isdigit():
    raise ValueError("tracking_code must contain only digits")

# Enum validation
VALID_TIERS = ["Bronze", "Silver", "Gold", "Platinum"]
if customer_tier not in VALID_TIERS:
    raise ValueError(f"customer_tier must be one of {VALID_TIERS}")

# Empty string validation
if not sku or not sku.strip():
    raise ValueError("sku cannot be empty")
```

#### 4. Business Logic Section

```python
# WHAT: Calculate base cost
# WHY: Apply per-kilogram rate as foundation for pricing
# HOW: Multiply weight by base rate constant
base_cost = weight_kg * BASE_RATE_PER_KG

# WHAT: Apply zone multiplier
# WHY: Adjust cost based on delivery distance
# HOW: Multiply by zone-specific multiplier from lookup table
zone_cost = base_cost * ZONE_MULTIPLIERS[zone]

# WHAT: Apply customer discount
# WHY: Reward loyalty with reduced pricing
# HOW: Reduce cost by tier-specific discount percentage
discount_rate = CUSTOMER_DISCOUNTS[customer_tier]
final_cost = zone_cost * (1 - discount_rate)
```

**Best Practices**:
- Break complex calculations into explicit steps
- Use descriptive variable names for intermediate values
- Add "What-Why-How" comments for each step
- Use constants for business rules (don't hardcode magic numbers)

#### 5. Return Format

**Every function must return a dictionary with this exact structure:**

**Success Response**:
```python
{
    "success": True,
    "result": <the actual value>,
    "error": None
}
```

**Error Response (Validation)**:
```python
{
    "success": False,
    "result": None,
    "error": "Descriptive error message",
    "error_type": "validation"
}
```

**Error Response (System)**:
```python
{
    "success": False,
    "result": None,
    "error": "Unexpected error: <details>",
    "error_type": "system"
}
```

**Why this format?**
- `success` - Agent can check if operation worked without parsing error messages
- `result` - Holds the actual return value when successful
- `error` - Provides human-readable error message for debugging
- `error_type` - Distinguishes user errors (validation) from system failures

#### 6. Error Handling Structure

```python
try:
    # Validation and business logic here
    return {"success": True, "result": value, "error": None}

except ValueError as e:
    # Catch validation errors (raised by our code)
    return {
        "success": False,
        "result": None,
        "error": str(e),
        "error_type": "validation"
    }

except Exception as e:
    # Catch unexpected errors (system issues)
    return {
        "success": False,
        "result": None,
        "error": f"Unexpected error: {str(e)}",
        "error_type": "system"
    }
```

**Best Practices**:
- Always catch `ValueError` separately (your validation errors)
- Catch general `Exception` last (unexpected issues)
- Never let exceptions propagate to the agent
- Include original error message in response: `str(e)`

### Complete Implementation Example

Here's the full implementation matching our specification:

```python
"""
Shipping cost calculator for Innovate Logistics.

This module provides an agent-callable function to calculate shipping costs
based on package weight, delivery zone, and customer loyalty tier.
"""

# WHAT: Define business constants
# WHY: Centralize pricing rules for easy maintenance
# HOW: Constants at module level, referenced by calculation function
BASE_RATE_PER_KG = 2.50

ZONE_MULTIPLIERS = {
    1: 1.0,    # Local
    2: 1.5,    # Regional
    3: 2.0,    # National
    4: 3.0     # International
}

CUSTOMER_DISCOUNTS = {
    "Bronze": 0.00,      # No discount
    "Silver": 0.05,      # 5% discount
    "Gold": 0.10,        # 10% discount
    "Platinum": 0.15     # 15% discount
}


def calculate_shipping_cost(weight_kg, zone, customer_tier):
    """
    Calculate shipping cost based on weight, zone, and customer loyalty tier.

    Applies Innovate Logistics pricing rules: base rate per kg, zone-based
    multipliers for delivery distance, and loyalty tier discounts.

    Args:
        weight_kg (float): Package weight in kilograms. Must be positive.
        zone (int): Delivery zone (1=local, 2=regional, 3=national, 4=international)
        customer_tier (str): Loyalty tier ("Bronze", "Silver", "Gold", "Platinum")

    Returns:
        dict: Standardized response with keys:
            - success (bool): True if calculation succeeded, False otherwise
            - result (float): Calculated cost in dollars (None if error)
            - error (str): Error message if success=False, None otherwise
            - error_type (str): "validation" or "system" (only if error)

    Example:
        >>> calculate_shipping_cost(15.0, 3, "Gold")
        {'success': True, 'result': 67.50, 'error': None}

        >>> calculate_shipping_cost(-5, 1, "Bronze")
        {'success': False, 'result': None, 'error': 'weight_kg must be positive', 'error_type': 'validation'}
    """

    try:
        # WHAT: Validate weight_kg parameter
        # WHY: Ensure we have a positive number to prevent nonsensical calculations
        # HOW: Check type and value constraints, raise ValueError if invalid
        if not isinstance(weight_kg, (int, float)):
            raise ValueError("weight_kg must be a number")
        if weight_kg <= 0:
            raise ValueError("weight_kg must be positive")

        # WHAT: Validate zone parameter
        # WHY: Ensure zone is a valid integer in our supported range (1-4)
        # HOW: Check type and value against allowed zones
        if not isinstance(zone, int):
            raise ValueError("zone must be an integer")
        if zone not in [1, 2, 3, 4]:
            raise ValueError("zone must be 1 (local), 2 (regional), 3 (national), or 4 (international)")

        # WHAT: Validate customer_tier parameter
        # WHY: Ensure tier is one of our recognized loyalty levels
        # HOW: Check against allowed tier values
        valid_tiers = ["Bronze", "Silver", "Gold", "Platinum"]
        if customer_tier not in valid_tiers:
            raise ValueError(f"customer_tier must be one of {valid_tiers}")

        # WHAT: Calculate base cost
        # WHY: Apply per-kilogram rate as foundation for all shipping costs
        # HOW: Multiply weight by standard base rate constant
        base_cost = weight_kg * BASE_RATE_PER_KG

        # WHAT: Apply zone multiplier
        # WHY: Adjust cost based on delivery distance (longer = more expensive)
        # HOW: Multiply base cost by zone-specific multiplier from lookup table
        zone_cost = base_cost * ZONE_MULTIPLIERS[zone]

        # WHAT: Apply customer loyalty discount
        # WHY: Reward repeat customers with reduced pricing
        # HOW: Reduce cost by tier-specific discount percentage
        discount_rate = CUSTOMER_DISCOUNTS[customer_tier]
        final_cost = zone_cost * (1 - discount_rate)

        # WHAT: Return success response
        # WHY: Provide standardized result format for agent to parse
        # HOW: Dictionary with success=True and calculated cost
        return {
            "success": True,
            "result": round(final_cost, 2),  # Round to 2 decimal places
            "error": None
        }

    except ValueError as e:
        # WHAT: Handle validation errors
        # WHY: Return clear error message instead of crashing
        # HOW: Catch ValueError from our validation, return standardized error dict
        return {
            "success": False,
            "result": None,
            "error": str(e),
            "error_type": "validation"
        }

    except Exception as e:
        # WHAT: Handle unexpected errors
        # WHY: Catch system issues, provide debugging information
        # HOW: Catch all other exceptions, return system error with details
        return {
            "success": False,
            "result": None,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "system"
        }
```

**What makes this implementation production-ready**:
1. ✅ Complete docstring with examples
2. ✅ "What-Why-How" comments throughout
3. ✅ Thorough input validation (type, range, enum)
4. ✅ Clear error messages
5. ✅ Standardized return format
6. ✅ Separate handling for validation vs. system errors
7. ✅ Business constants defined at module level
8. ✅ Explicit variable names for intermediate calculations
9. ✅ Never crashes - always returns a dict

---

## Best Practices

### 1. Write Agent-Friendly Descriptions

**Think about what users will say:**

```json
// ❌ BAD: Technical, no context
{
  "description": "Returns package status from database lookup"
}

// ✅ GOOD: User-focused, includes trigger phrases
{
  "description": "Look up package delivery status using tracking code. Use when customers ask 'where is my package?', 'has my order shipped?', or provide a 9-digit tracking number."
}
```

### 2. Validate Everything

**Never trust inputs, even from an agent:**

```python
# ❌ BAD: No validation
def check_inventory(sku):
    return INVENTORY_DB[sku]  # Will crash if sku not in DB or wrong type

# ✅ GOOD: Comprehensive validation
def check_inventory(sku):
    try:
        if not isinstance(sku, str):
            raise ValueError("sku must be a string")
        if not sku or not sku.strip():
            raise ValueError("sku cannot be empty")

        quantity = INVENTORY_DB.get(sku, 0)
        return {"success": True, "result": quantity, "error": None}
    except ValueError as e:
        return {"success": False, "result": None, "error": str(e), "error_type": "validation"}
```

### 3. Use Enum for Constrained Values

**Help the agent and your code:**

```json
// ✅ Specify allowed values in spec
{
  "service_level": {
    "type": "string",
    "description": "Delivery speed: Standard, Express, or Overnight",
    "enum": ["Standard", "Express", "Overnight"]
  }
}
```

```python
# ✅ Validate against same values in code
VALID_SERVICE_LEVELS = ["Standard", "Express", "Overnight"]
if service_level not in VALID_SERVICE_LEVELS:
    raise ValueError(f"service_level must be one of {VALID_SERVICE_LEVELS}")
```

### 4. Provide Clear Error Messages

**Help debugging and user understanding:**

```python
# ❌ BAD: Vague error
if zone > 4:
    raise ValueError("Invalid zone")

# ✅ GOOD: Specific, actionable error
if zone not in [1, 2, 3, 4]:
    raise ValueError("zone must be 1 (local), 2 (regional), 3 (national), or 4 (international)")
```

### 5. Use Constants for Business Rules

**Make rules easy to update:**

```python
# ❌ BAD: Magic numbers in code
cost = weight * 2.50
zone_cost = cost * 1.5

# ✅ GOOD: Named constants
BASE_RATE_PER_KG = 2.50
ZONE_MULTIPLIERS = {1: 1.0, 2: 1.5, 3: 2.0, 4: 3.0}

cost = weight * BASE_RATE_PER_KG
zone_cost = cost * ZONE_MULTIPLIERS[zone]
```

### 6. Always Return the Same Format

**Consistency is critical for agents:**

```python
# ❌ BAD: Inconsistent returns
def bad_function(x):
    if x < 0:
        return "Error: negative value"  # String
    return {"result": x * 2}           # Dict with different keys

# ✅ GOOD: Always same structure
def good_function(x):
    try:
        if x < 0:
            raise ValueError("x must be non-negative")
        return {"success": True, "result": x * 2, "error": None}
    except ValueError as e:
        return {"success": False, "result": None, "error": str(e), "error_type": "validation"}
```

### 7. Include Usage Examples

**In both docstrings and descriptions:**

```python
"""
Example:
    >>> calculate_shipping_cost(15.0, 3, "Gold")
    {'success': True, 'result': 67.50, 'error': None}
"""
```

```json
{
  "description": "Calculate shipping cost. Example: 15kg to zone 3 for Gold customer."
}
```

---

## Common Pitfalls to Avoid

### ❌ Pitfall 1: Specification Doesn't Match Implementation

**Problem**: JSON says zone is 1-4, but code accepts 1-5

```json
// Specification says
"enum": [1, 2, 3, 4]
```

```python
# But code allows
if zone < 1 or zone > 5:  # WRONG!
    raise ValueError("Invalid zone")
```

**Solution**: Keep spec and validation in sync. Copy enum values directly.

### ❌ Pitfall 2: Vague Function Descriptions

**Problem**: Agent can't determine when to use function

```json
{
  "description": "Processes logistics data"  // Too vague!
}
```

**Solution**: Be specific about use cases and triggers

```json
{
  "description": "Calculate shipping cost for a package. Use when customers ask about delivery pricing or shipping fees."
}
```

### ❌ Pitfall 3: Returning Raw Values Instead of Dicts

**Problem**: Inconsistent return types break agent parsing

```python
def bad_function(x):
    return x * 2  # Returns number
```

**Solution**: Always return standardized dict

```python
def good_function(x):
    try:
        result = x * 2
        return {"success": True, "result": result, "error": None}
    except Exception as e:
        return {"success": False, "result": None, "error": str(e), "error_type": "system"}
```

### ❌ Pitfall 4: Missing Validation

**Problem**: Crashes instead of returning error

```python
def bad_function(zone):
    return ZONE_MULTIPLIERS[zone]  # KeyError if zone invalid!
```

**Solution**: Validate before using

```python
def good_function(zone):
    try:
        if zone not in [1, 2, 3, 4]:
            raise ValueError("zone must be 1, 2, 3, or 4")
        return {"success": True, "result": ZONE_MULTIPLIERS[zone], "error": None}
    except ValueError as e:
        return {"success": False, "result": None, "error": str(e), "error_type": "validation"}
```

### ❌ Pitfall 5: Unclear Error Messages

**Problem**: Error doesn't help debugging

```python
raise ValueError("Invalid input")  // What's invalid?
```

**Solution**: Be specific

```python
raise ValueError("tracking_code must be exactly 9 digits, received 5")
```

---

## Quick Reference: Copy-Paste Templates

### Minimal Specification Template

```json
{
  "name": "your_function_name",
  "description": "What this function does and when to use it. Include typical user queries that should trigger this function.",
  "parameters": {
    "type": "object",
    "properties": {
      "param_name": {
        "type": "string|number|integer|boolean",
        "description": "What this parameter represents, with examples"
      }
    },
    "required": ["param_name"]
  }
}
```

### Minimal Implementation Template

```python
def your_function_name(param_name):
    """
    Brief description.

    Args:
        param_name (type): Description

    Returns:
        dict: {"success": bool, "result": any, "error": str|None}

    Example:
        >>> your_function_name("value")
        {'success': True, 'result': 42, 'error': None}
    """

    try:
        # WHAT: Validate param_name
        # WHY: Ensure valid input before processing
        # HOW: Check type and constraints
        if not isinstance(param_name, expected_type):
            raise ValueError("param_name must be <expected_type>")

        # WHAT: Execute business logic
        # WHY: Perform the core operation
        # HOW: Process validated input
        result = perform_operation(param_name)

        # WHAT: Return success response
        # WHY: Provide standardized result to agent
        # HOW: Dict with success=True and result
        return {"success": True, "result": result, "error": None}

    except ValueError as e:
        return {"success": False, "result": None, "error": str(e), "error_type": "validation"}

    except Exception as e:
        return {"success": False, "result": None, "error": f"Unexpected error: {str(e)}", "error_type": "system"}
```

---

## Testing Your Contract

### 1. Test the Specification Independently

**Load and validate your JSON:**

```python
import json

# Load specification
with open("your_spec.json", "r") as f:
    spec = json.load(f)

# Verify required fields
assert "name" in spec
assert "description" in spec
assert "parameters" in spec

print(f"Function name: {spec['name']}")
print(f"Description: {spec['description']}")
```

### 2. Test the Implementation

**Create test cases for validation:**

```python
# Test happy path
result = your_function(valid_param)
assert result["success"] is True
assert result["result"] is not None
assert result["error"] is None

# Test validation errors
result = your_function(invalid_param)
assert result["success"] is False
assert result["error_type"] == "validation"
assert result["error"] is not None
```

### 3. Test Specification-Implementation Alignment

**Verify parameter names match:**

```python
import json
import inspect

# Load spec
with open("your_spec.json", "r") as f:
    spec = json.load(f)

# Get function signature
sig = inspect.signature(your_function)
param_names = list(sig.parameters.keys())

# Compare to spec
spec_params = list(spec["parameters"]["properties"].keys())
assert set(param_names) == set(spec_params), "Parameter names don't match!"
```

---

## Summary

A complete agent-ready function contract consists of:

**Specification (JSON)**:
- `name` - Exact function name
- `description` - When and why to use this function
- `parameters` - JSON Schema defining inputs with types, descriptions, and constraints

**Implementation (Python)**:
- Matching function name
- Comprehensive input validation
- "What-Why-How" commented business logic
- Standardized return format: `{"success": bool, "result": any, "error": str|None}`
- Separate error handling for validation vs. system errors

**Key Success Factors**:
1. ✅ Specification and implementation stay in sync
2. ✅ Descriptions help agents select the right function
3. ✅ Validation prevents crashes and provides clear error messages
4. ✅ Consistent return format enables reliable agent integration
5. ✅ "What-Why-How" comments make code maintainable

By following this template and best practices, your custom functions will be reliable, agent-friendly, and production-ready.
