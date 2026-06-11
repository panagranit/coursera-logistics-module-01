"""
Module: shipping_tool.py
Purpose: Custom function to calculate shipping costs for Innovate Logistics

This module implements the calculate_shipping_cost function that handles
the company's proprietary pricing logic including weight zones, distance
tiers, and customer loyalty discounts.

Usage:
    from shipping_tool import calculate_shipping_cost

    result = calculate_shipping_cost(
        weight_kg=15.5,
        zone=4,
        customer_tier="Gold"
    )
    print(result)  # {"success": True, "result": 50.63, "error": None}

Learning Context:
    This is demonstrated in Screencast 1.1 "Creating Your First Custom Tool"
    as the first example of building an OpenAI-compatible agent function.

    Key concepts demonstrated:
    - Custom function design with business logic
    - Comprehensive input validation
    - Standardized return format for agent integration
    - Clear error messages for agent interpretation
"""

from typing import Dict, Any, Union

# WHAT: Define shipping cost calculation constants
# WHY: Centralize business logic parameters for easy adjustment and clarity
# HOW: Use descriptive names matching Innovate Logistics business terminology

BASE_RATE_PER_KG = 2.50  # Base shipping cost per kilogram in dollars

ZONE_MULTIPLIERS = {
    1: 1.0,   # Local delivery (within city) - no distance premium
    2: 1.5,   # Regional delivery (within state) - 50% distance premium
    3: 2.0,   # National delivery (across country) - 100% distance premium
    4: 3.0,   # International delivery - 200% distance premium
}

CUSTOMER_DISCOUNTS = {
    "Bronze": 0.0,   # No discount for bronze tier customers
    "Silver": 0.05,  # 5% discount for silver tier customers
    "Gold": 0.10,    # 10% discount for gold tier customers
    "Platinum": 0.15 # 15% discount for platinum tier customers
}


def calculate_shipping_cost(
    weight_kg: Union[int, float],
    zone: int,
    customer_tier: str
) -> Dict[str, Any]:
    """
    Calculate shipping cost using Innovate Logistics proprietary pricing rules.

    This function implements a three-factor pricing model:
    1. Base cost: weight in kg × base rate per kg
    2. Distance multiplier: based on shipping zone
    3. Loyalty discount: based on customer tier

    Final formula: (weight × base_rate × zone_multiplier) × (1 - discount)

    Args:
        weight_kg: Package weight in kilograms. Must be a positive number.
            Typical range: 0.1 to 500 kg.
        zone: Shipping destination zone (1=local, 2=regional, 3=national, 4=international).
            Must be an integer from 1 to 4.
        customer_tier: Customer loyalty tier ("Bronze", "Silver", "Gold", or "Platinum").
            Determines discount percentage applied to final cost.

    Returns:
        Dict with standardized agent-friendly format:
            {
                "success": bool,      # True if calculation succeeded
                "result": float,      # Calculated cost in dollars (if success=True)
                "error": str or None, # Error message (if success=False)
                "error_type": str     # Error category: "validation" or "system" (if success=False)
            }

    Raises:
        ValueError: When input validation fails (caught and returned as error response)

    Examples:
        >>> # Successful calculation
        >>> result = calculate_shipping_cost(15.0, 2, "Gold")
        >>> print(result)
        {'success': True, 'result': 50.63, 'error': None}

        >>> # Validation error
        >>> result = calculate_shipping_cost(-5, 2, "Gold")
        >>> print(result)
        {'success': False, 'result': None, 'error': 'Weight must be positive, got: -5',
         'error_type': 'validation'}
    """

    try:
        # WHAT: Validate weight_kg is numeric and positive
        # WHY: Prevent invalid weights from causing incorrect calculations or crashes
        # HOW: Check type first, then value range with specific error messages

        # Check if weight is a number (int or float)
        if not isinstance(weight_kg, (int, float)):
            raise ValueError(
                f"Weight must be a number (int or float), got type: {type(weight_kg).__name__}"
            )

        # Check if weight is positive
        if weight_kg <= 0:
            raise ValueError(
                f"Weight must be positive, got: {weight_kg}"
            )

        # WHAT: Validate zone is an integer in valid range
        # WHY: Ensure zone corresponds to defined pricing multipliers
        # HOW: Check type first, then membership in valid zone set

        # Check if zone is an integer
        if not isinstance(zone, int):
            raise ValueError(
                f"Zone must be an integer, got type: {type(zone).__name__}"
            )

        # Check if zone is in valid range (1-4)
        if zone not in ZONE_MULTIPLIERS:
            valid_zones = sorted(ZONE_MULTIPLIERS.keys())
            raise ValueError(
                f"Zone must be one of {valid_zones}, got: {zone}"
            )

        # WHAT: Validate customer_tier is a valid tier name
        # WHY: Ensure tier corresponds to defined discount rates
        # HOW: Check type first, then membership in valid tier set

        # Check if customer_tier is a string
        if not isinstance(customer_tier, str):
            raise ValueError(
                f"Customer tier must be a string, got type: {type(customer_tier).__name__}"
            )

        # Check if customer_tier is in valid tier list
        if customer_tier not in CUSTOMER_DISCOUNTS:
            valid_tiers = sorted(CUSTOMER_DISCOUNTS.keys())
            raise ValueError(
                f"Customer tier must be one of {valid_tiers}, got: '{customer_tier}'"
            )

        # WHAT: Calculate base shipping cost from weight
        # WHY: Foundation of pricing model - cost scales with package weight
        # HOW: Multiply weight by base rate to get pre-adjustment cost

        base_cost = weight_kg * BASE_RATE_PER_KG

        # WHAT: Apply zone multiplier for distance-based pricing
        # WHY: Longer distances cost more to ship
        # HOW: Multiply base cost by zone-specific multiplier

        zone_multiplier = ZONE_MULTIPLIERS[zone]
        cost_with_zone = base_cost * zone_multiplier

        # WHAT: Apply customer loyalty discount
        # WHY: Reward repeat customers with lower prices
        # HOW: Reduce cost by discount percentage (multiply by 1 - discount_rate)

        discount_rate = CUSTOMER_DISCOUNTS[customer_tier]
        final_cost = cost_with_zone * (1 - discount_rate)

        # WHAT: Round final cost to 2 decimal places
        # WHY: Currency amounts should have exactly 2 decimal places
        # HOW: Use round() function with precision of 2

        final_cost = round(final_cost, 2)

        # WHAT: Return standardized success response
        # WHY: Provides consistent format that agents can reliably parse
        # HOW: Return dictionary with success=True and result containing calculated cost

        return {
            "success": True,
            "result": final_cost,
            "error": None
        }

    except ValueError as e:
        # WHAT: Handle validation errors
        # WHY: Convert validation failures into agent-parseable error responses
        # HOW: Return standardized error format with error_type="validation"

        return {
            "success": False,
            "result": None,
            "error": str(e),
            "error_type": "validation"
        }

    except Exception as e:
        # WHAT: Handle unexpected system errors
        # WHY: Catch any unforeseen issues and return in standardized format
        # HOW: Return error format with error_type="system" for non-validation issues

        return {
            "success": False,
            "result": None,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "system"
        }


# WHAT: Provide example usage when module is run directly
# WHY: Demonstrates function usage and expected output format
# HOW: Execute sample calls with various inputs when __name__ == "__main__"

if __name__ == "__main__":
    print("Innovate Logistics Shipping Cost Calculator")
    print("=" * 50)

    # Example 1: Standard calculation
    print("\nExample 1: 15kg package to zone 2 for Gold customer")
    result = calculate_shipping_cost(15.0, 2, "Gold")
    print(f"Result: {result}")

    # Expected output:
    # {'success': True, 'result': 50.63, 'error': None}

    # Example 2: International shipping with Platinum discount
    print("\nExample 2: 25kg package to zone 4 for Platinum customer")
    result = calculate_shipping_cost(25.0, 4, "Platinum")
    print(f"Result: {result}")

    # Expected output:
    # {'success': True, 'result': 159.38, 'error': None}

    # Example 3: Validation error - negative weight
    print("\nExample 3: Invalid input - negative weight")
    result = calculate_shipping_cost(-5.0, 2, "Gold")
    print(f"Result: {result}")

    # Expected output:
    # {'success': False, 'result': None,
    #  'error': 'Weight must be positive, got: -5.0',
    #  'error_type': 'validation'}

    # Example 4: Validation error - invalid zone
    print("\nExample 4: Invalid input - zone out of range")
    result = calculate_shipping_cost(10.0, 5, "Silver")
    print(f"Result: {result}")

    # Expected output:
    # {'success': False, 'result': None,
    #  'error': 'Zone must be one of [1, 2, 3, 4], got: 5',
    #  'error_type': 'validation'}
