"""
Production-ready logistics tools for Innovate Logistics (Activity 1.7).

This module applies the `@production_agent_function` decorator from
`1_7_START_production_wrapper.py` to remove repetitive try/except blocks and
standardize error handling/formatting.

Functions:
- `get_tracking_status(tracking_code: str)`
- `check_inventory(sku: str)`
- `calculate_delivery_days(zone: int, service_level: str)`

All functions raise `ValueError` for validation problems; the decorator
converts those into standardized validation error responses.
"""

import sys
import os
from importlib import import_module

# Ensure the activities directory is importable (allows import_module by name)
sys.path.insert(0, os.path.dirname(__file__))
_wrapper = import_module('1_7_START_production_wrapper')
production_agent_function = _wrapper.production_agent_function

import re
import math
from typing import Dict, Any

# Mock databases for educational/testing purposes
MOCK_TRACKING_DB = {
    "123456789": "In Transit",
    "987654321": "In Transit",
    "555555555": "In Transit",
    "111111111": "Delivered",
    "222222222": "Delivered",
}

MOCK_INVENTORY_DB = {
    "ABC1234": 150,
    "DEF5678": 3,
    "GHI9012": 0,
    "JKL3456": 42,
}

DELIVERY_DAYS_BASE = {
    1: 2,
    2: 4,
    3: 7,
    4: 14,
}


@production_agent_function
def get_tracking_status(tracking_code: str) -> Dict[str, Any]:
    """Return tracking status for a 9-digit tracking code.

    Raises ValueError on validation failures; decorator formats responses.
    """

    if not isinstance(tracking_code, str):
        raise ValueError(f"Tracking code must be a string, got {type(tracking_code).__name__}")

    if len(tracking_code) != 9:
        raise ValueError(f"Tracking code must be exactly 9 digits, got {len(tracking_code)} characters")

    if not tracking_code.isdigit():
        raise ValueError("Tracking code must contain only digits (0-9), no letters or symbols")

    status = MOCK_TRACKING_DB.get(tracking_code, "Unknown")

    return {"success": True, "result": status, "error": None}


@production_agent_function
def check_inventory(sku: str) -> Dict[str, Any]:
    """Return inventory details for SKU in format XXX#### (3 letters + 4 digits).

    Raises ValueError on validation failures; decorator formats responses.
    """

    if not isinstance(sku, str):
        raise ValueError(f"SKU must be a string, got {type(sku).__name__}")

    if len(sku) != 7:
        raise ValueError(f"SKU must be exactly 7 characters (3 letters + 4 digits), got {len(sku)} characters")

    sku_pattern = r'^[A-Z]{3}[0-9]{4}$'
    if not re.match(sku_pattern, sku):
        raise ValueError(f"SKU format must be 3 uppercase letters followed by 4 digits (e.g., 'ABC1234'), got '{sku}'")

    quantity = MOCK_INVENTORY_DB.get(sku, 0)
    in_stock = quantity > 0

    return {"success": True, "result": {"sku": sku, "quantity": quantity, "in_stock": in_stock}, "error": None}


@production_agent_function
def calculate_delivery_days(zone: int, service_level: str) -> Dict[str, Any]:
    """Return estimated delivery days for given zone and service level.

    Raises ValueError on validation failures; decorator formats responses.
    """

    if not isinstance(zone, int):
        raise ValueError(f"Zone must be an integer, got {type(zone).__name__}")

    if zone not in DELIVERY_DAYS_BASE:
        raise ValueError(f"Zone must be between 1 and 4, got {zone}")

    if not isinstance(service_level, str):
        raise ValueError(f"Service level must be a string, got {type(service_level).__name__}")

    valid_services = ["Standard", "Express"]
    if service_level not in valid_services:
        raise ValueError(f"Service level must be 'Standard' or 'Express' (case-sensitive), got '{service_level}'")

    base_days = DELIVERY_DAYS_BASE[zone]

    if service_level == "Express":
        delivery_days = math.ceil(base_days / 2)
    else:
        delivery_days = base_days

    return {"success": True, "result": {"zone": zone, "service_level": service_level, "delivery_days": delivery_days}, "error": None}


if __name__ == "__main__":
    print(get_tracking_status("123456789"))
    print(check_inventory("ABC1234"))
    print(calculate_delivery_days(3, "Express"))
