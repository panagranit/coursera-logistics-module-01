# Innovate Logistics Function Requirements

## Business Context

Welcome to your first project at Praxis AI consultancy! You've been assigned to **Innovate Logistics**, a shipping company with internal Python functions that need to be refactored for agent integration.

The client has three legacy functions that "work" for basic use cases but have serious problems:
- No input validation
- No error handling
- Inconsistent return formats
- Not safe for agent use

Your task: Transform these naive implementations into production-ready, agent-callable functions.

---

## Function 1: `get_tracking_status`

### Purpose
Look up the delivery status of a package using its tracking code.

### Current Implementation Issues
- ❌ No validation of tracking code format
- ❌ Returns raw string instead of standardized format
- ❌ No error handling for invalid inputs
- ❌ Will crash if given non-string input

### Business Logic Requirements

**Input Parameter**:
- `tracking_code`: A string containing exactly 9 digits
- Examples: "123456789", "987654321"
- Invalid examples: "123" (too short), "12345678X" (contains letter), "123-456-789" (contains hyphens)

**Validation Rules**:
1. Must be a string (reject if not)
2. Must be exactly 9 characters long (reject if shorter or longer)
3. Must contain only numeric digits 0-9 (reject if contains letters or symbols)

**Business Logic**:
- Query the tracking database (mock data for this exercise)
- Return one of three statuses:
  - "In Transit" - Package is currently being shipped
  - "Delivered" - Package has reached its destination
  - "Unknown" - Tracking code not found in system

**Required Return Format**:
```python
# Success case
{
    "success": True,
    "result": "In Transit",  # or "Delivered" or "Unknown"
    "error": None
}

# Validation error case
{
    "success": False,
    "result": None,
    "error": "Tracking code must be exactly 9 digits",
    "error_type": "validation"
}
```

**Error Messages** (must be clear and specific):
- Non-string input: "Tracking code must be a string"
- Wrong length: "Tracking code must be exactly 9 digits"
- Non-numeric: "Tracking code must contain only digits"

---

## Function 2: `check_inventory`

### Purpose
Check if a product SKU is in stock and return the available quantity.

### Current Implementation Issues
- ❌ No validation of SKU format
- ❌ Returns raw integer instead of standardized format
- ❌ No distinction between "not found" and "out of stock"
- ❌ No error handling

### Business Logic Requirements

**Input Parameter**:
- `sku`: A string in format "3 letters + 4 digits"
- Examples: "ABC1234", "DEF5678", "GHI9012"
- Invalid examples: "ABC123" (too short), "12341234" (no letters), "abc1234" (lowercase)

**Validation Rules**:
1. Must be a string (reject if not)
2. Must be exactly 7 characters long (reject if not)
3. First 3 characters must be uppercase letters A-Z (reject if lowercase or numbers)
4. Last 4 characters must be digits 0-9 (reject if letters)

**Business Logic**:
- Query the inventory database (mock data for this exercise)
- Return the quantity available
- If SKU not found, treat as quantity = 0

**Required Return Format**:
```python
# Success case (in stock)
{
    "success": True,
    "result": {
        "sku": "ABC1234",
        "quantity": 150,
        "in_stock": True
    },
    "error": None
}

# Success case (out of stock)
{
    "success": True,
    "result": {
        "sku": "GHI9012",
        "quantity": 0,
        "in_stock": False
    },
    "error": None
}

# Validation error case
{
    "success": False,
    "result": None,
    "error": "SKU format must be 3 uppercase letters followed by 4 digits (e.g., 'ABC1234')",
    "error_type": "validation"
}
```

**Error Messages**:
- Non-string input: "SKU must be a string"
- Wrong length: "SKU must be exactly 7 characters (3 letters + 4 digits)"
- Wrong format: "SKU format must be 3 uppercase letters followed by 4 digits (e.g., 'ABC1234')"

---

## Function 3: `calculate_delivery_days`

### Purpose
Estimate delivery time in days based on destination zone and service level.

### Current Implementation Issues
- ❌ No validation of zone or service level
- ❌ Returns raw integer instead of standardized format
- ❌ Logic bug with "express" zone handling
- ❌ No error handling

### Business Logic Requirements

**Input Parameters**:
- `zone`: An integer from 1 to 4 representing distance
  - 1 = Local (within city)
  - 2 = Regional (within state)
  - 3 = National (across country)
  - 4 = International
- `service_level`: A string, either "Standard" or "Express"
  - "Standard" = Normal delivery speed
  - "Express" = Expedited delivery (half the standard days, rounded up)

**Validation Rules**:
1. Zone must be an integer (reject if not)
2. Zone must be in range 1-4 (reject if outside)
3. Service level must be a string (reject if not)
4. Service level must be exactly "Standard" or "Express" (case-sensitive)

**Business Logic - Base Delivery Days**:
- Zone 1 (Local): 2 days standard
- Zone 2 (Regional): 4 days standard
- Zone 3 (National): 7 days standard
- Zone 4 (International): 14 days standard

**Express Calculation**:
- Express service: Divide standard days by 2, round UP to nearest integer
- Examples:
  - Zone 1 Standard: 2 days → Express: 1 day
  - Zone 2 Standard: 4 days → Express: 2 days
  - Zone 3 Standard: 7 days → Express: 4 days (7/2 = 3.5, rounds up to 4)

**Required Return Format**:
```python
# Success case
{
    "success": True,
    "result": {
        "zone": 3,
        "service_level": "Express",
        "delivery_days": 4
    },
    "error": None
}

# Validation error case
{
    "success": False,
    "result": None,
    "error": "Zone must be between 1 and 4",
    "error_type": "validation"
}
```

**Error Messages**:
- Zone not integer: "Zone must be an integer"
- Zone out of range: "Zone must be between 1 and 4, got: {zone}"
- Service level not string: "Service level must be a string"
- Invalid service level: "Service level must be 'Standard' or 'Express', got: '{service_level}'"

---

## Your Deliverables

### 1. `logistics_specs.json`
Create a JSON file with OpenAI function specifications for all three functions. Each specification must include:
- Clear `name` matching the function name
- Detailed `description` explaining when the agent should use this function
- Complete `parameters` schema with types, descriptions, and constraints
- List of `required` parameters

### 2. `logistics_tools.py`
Create a Python file with refactored implementations of all three functions. Each function must include:
- Comprehensive docstring with Args, Returns, Raises, and Example
- "What-Why-How" comments explaining the code
- Complete input validation with specific error messages
- Try/except error handling
- Standardized return format as specified above

---

## Success Criteria

Your code is ready when:

✅ All functions pass the tests in `1_3_START_function_tests.py`
✅ Each function has comprehensive input validation
✅ All functions return standardized `{"success": ..., "result": ..., "error": ...}` format
✅ Error messages are clear and specific
✅ Code includes "What-Why-How" comments
✅ Functions have complete docstrings

---

## Testing Your Work

Run the provided test suite:
```bash
pytest 1_3_START_function_tests.py -v
```

Expected outcome:
- ❌ Tests FAIL when run against `1_3_START_naive_tools.py` (the "before" code)
- ✅ Tests PASS when run against your refactored `logistics_tools.py`

---

## Tips

1. **Start with validation**: Get the validation working first, then add business logic
2. **Use specific error messages**: Don't just say "invalid input" - explain what's wrong
3. **Test as you go**: Run individual tests while developing
4. **Follow the pattern**: Look at `1_1_shipping_tool.py` from the screencast as an example
5. **Copy the return format exactly**: The tests expect specific keys and structure

Good luck! This is your first step toward becoming a custom agent function expert. 🚀
