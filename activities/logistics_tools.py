import re
import math
from typing import Dict, Any, Union

# NOTE: In production, this would query a real tracking database
MOCK_TRACKING_DB = {
    "123456789": "In Transit",
    "987654321": "In Transit",
    "555555555": "In Transit",
    "111111111": "Delivered",
    "222222222": "Delivered",
}

# NOTE: In production, this would query a real inventory system
MOCK_INVENTORY_DB = {
    "ABC1234": 150,
    "DEF5678": 3,
    "GHI9012": 0,
    "JKL3456": 42,
}

DELIVERY_DAYS_BASE = {
    1: 2,   # Local delivery (within city)
    2: 4,   # Regional delivery (within state)
    3: 7,   # National delivery (across country)
    4: 14,  # International delivery
}


def get_tracking_status(tracking_code: str) -> Dict[str, Any]:
    try:
        if not isinstance(tracking_code, str):
            raise ValueError(
                f"Tracking code must be a string, got {type(tracking_code).__name__}"
            )

        if len(tracking_code) != 9:
            raise ValueError(
                f"Tracking code must be exactly 9 digits, got {len(tracking_code)} characters"
            )

        if not tracking_code.isdigit():
            raise ValueError(
                "Tracking code must contain only digits (0-9), no letters or symbols"
            )

        status = MOCK_TRACKING_DB.get(tracking_code, "Unknown")

        return {
            "success": True,
            "result": status,
            "error": None
        }

    except ValueError as e:
        return {
            "success": False,
            "result": None,
            "error": str(e),
            "error_type": "validation"
        }

    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "system"
        }


def check_inventory(sku: str) -> Dict[str, Any]:
    try:
        if not isinstance(sku, str):
            raise ValueError(
                f"SKU must be a string, got {type(sku).__name__}"
            )

        if len(sku) != 7:
            raise ValueError(
                f"SKU must be exactly 7 characters (3 letters + 4 digits), got {len(sku)} characters"
            )

        sku_pattern = r'^[A-Z]{3}[0-9]{4}$'

        if not re.match(sku_pattern, sku):
            raise ValueError(
                f"SKU format must be 3 uppercase letters followed by 4 digits (e.g., 'ABC1234'), got '{sku}'"
            )

        quantity = MOCK_INVENTORY_DB.get(sku, 0)
        in_stock = quantity > 0

        return {
            "success": True,
            "result": {
                "sku": sku,
                "quantity": quantity,
                "in_stock": in_stock
            },
            "error": None
        }

    except ValueError as e:
        return {
            "success": False,
            "result": None,
            "error": str(e),
            "error_type": "validation"
        }

    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "system"
        }


def calculate_delivery_days(zone: int, service_level: str) -> Dict[str, Any]:
    try:
        if not isinstance(zone, int):
            raise ValueError(
                f"Zone must be an integer, got {type(zone).__name__}"
            )

        if zone not in DELIVERY_DAYS_BASE:
            valid_zones = sorted(DELIVERY_DAYS_BASE.keys())
            raise ValueError(
                f"Zone must be between 1 and 4, got {zone}"
            )

        if not isinstance(service_level, str):
            raise ValueError(
                f"Service level must be a string, got {type(service_level).__name__}"
            )

        valid_services = ["Standard", "Express"]

        if service_level not in valid_services:
            raise ValueError(
                f"Service level must be 'Standard' or 'Express' (case-sensitive), got '{service_level}'"
            )

        base_days = DELIVERY_DAYS_BASE[zone]

        if service_level == "Express":
            delivery_days = math.ceil(base_days / 2)
        else:
            delivery_days = base_days

        return {
            "success": True,
            "result": {
                "zone": zone,
                "service_level": service_level,
                "delivery_days": delivery_days
            },
            "error": None
        }

    except ValueError as e:
        return {
            "success": False,
            "result": None,
            "error": str(e),
            "error_type": "validation"
        }

    except Exception as e:
        return {
            "success": False,
            "result": None,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "system"
        }
