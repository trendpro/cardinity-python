"""
Cardinity Validation Constraints

This module defines all validation constraints for the Cardinity API data structures.
It uses Cerberus schema format for consistent validation across the SDK.
"""

from typing import Any, Dict

# 3D Secure v2 challenge window sizes
CHALLENGE_WINDOW_SIZES = ["01", "02", "03", "04", "05"]

# Supported currencies (ISO 4217)
SUPPORTED_CURRENCIES = [
    "EUR",
    "USD",
    "GBP",
    "PLN",
    "CZK",
    "DKK",
    "SEK",
    "NOK",
    "CHF",
    "CAD",
    "AUD",
]

# Common country codes (ISO 3166-1 alpha-2)
SUPPORTED_COUNTRIES = [
    "AD",
    "AE",
    "AF",
    "AG",
    "AI",
    "AL",
    "AM",
    "AO",
    "AQ",
    "AR",
    "AS",
    "AT",
    "AU",
    "AW",
    "AX",
    "AZ",
    "BA",
    "BB",
    "BD",
    "BE",
    "BF",
    "BG",
    "BH",
    "BI",
    "BJ",
    "BL",
    "BM",
    "BN",
    "BO",
    "BQ",
    "BR",
    "BS",
    "BT",
    "BV",
    "BW",
    "BY",
    "BZ",
    "CA",
    "CC",
    "CD",
    "CF",
    "CG",
    "CH",
    "CI",
    "CK",
    "CL",
    "CM",
    "CN",
    "CO",
    "CR",
    "CU",
    "CV",
    "CW",
    "CX",
    "CY",
    "CZ",
    "DE",
    "DJ",
    "DK",
    "DM",
    "DO",
    "DZ",
    "EC",
    "EE",
    "EG",
    "EH",
    "ER",
    "ES",
    "ET",
    "FI",
    "FJ",
    "FK",
    "FM",
    "FO",
    "FR",
    "GA",
    "GB",
    "GD",
    "GE",
    "GF",
    "GG",
    "GH",
    "GI",
    "GL",
    "GM",
    "GN",
    "GP",
    "GQ",
    "GR",
    "GS",
    "GT",
    "GU",
    "GW",
    "GY",
    "HK",
    "HM",
    "HN",
    "HR",
    "HT",
    "HU",
    "ID",
    "IE",
    "IL",
    "IM",
    "IN",
    "IO",
    "IQ",
    "IR",
    "IS",
    "IT",
    "JE",
    "JM",
    "JO",
    "JP",
    "KE",
    "KG",
    "KH",
    "KI",
    "KM",
    "KN",
    "KP",
    "KR",
    "KW",
    "KY",
    "KZ",
    "LA",
    "LB",
    "LC",
    "LI",
    "LK",
    "LR",
    "LS",
    "LT",
    "LU",
    "LV",
    "LY",
    "MA",
    "MC",
    "MD",
    "ME",
    "MF",
    "MG",
    "MH",
    "MK",
    "ML",
    "MM",
    "MN",
    "MO",
    "MP",
    "MQ",
    "MR",
    "MS",
    "MT",
    "MU",
    "MV",
    "MW",
    "MX",
    "MY",
    "MZ",
    "NA",
    "NC",
    "NE",
    "NF",
    "NG",
    "NI",
    "NL",
    "NO",
    "NP",
    "NR",
    "NU",
    "NZ",
    "OM",
    "PA",
    "PE",
    "PF",
    "PG",
    "PH",
    "PK",
    "PL",
    "PM",
    "PN",
    "PR",
    "PS",
    "PT",
    "PW",
    "PY",
    "QA",
    "RE",
    "RO",
    "RS",
    "RU",
    "RW",
    "SA",
    "SB",
    "SC",
    "SD",
    "SE",
    "SG",
    "SH",
    "SI",
    "SJ",
    "SK",
    "SL",
    "SM",
    "SN",
    "SO",
    "SR",
    "SS",
    "ST",
    "SV",
    "SX",
    "SY",
    "SZ",
    "TC",
    "TD",
    "TF",
    "TG",
    "TH",
    "TJ",
    "TK",
    "TL",
    "TM",
    "TN",
    "TO",
    "TR",
    "TT",
    "TV",
    "TW",
    "TZ",
    "UA",
    "UG",
    "UM",
    "US",
    "UY",
    "UZ",
    "VA",
    "VC",
    "VE",
    "VG",
    "VI",
    "VN",
    "VU",
    "WF",
    "WS",
    "YE",
    "YT",
    "ZA",
    "ZM",
    "ZW",
]


class Constraints:
    """Collection of validation constraints for Cardinity API fields."""

    @staticmethod
    def amount() -> Dict[str, Any]:
        """Constraint for monetary amounts.

        Returns:
            Dict: Cerberus schema for amount validation
        """
        return {
            "type": "string",
            "required": True,
            "regex": r"^\d+\.\d{2}$",  # Format: 10.50
            "check_with": "validate_amount",
        }

    @staticmethod
    def currency() -> Dict[str, Any]:
        """Constraint for currency codes.

        Returns:
            Dict: Cerberus schema for currency validation
        """
        return {
            "type": "string",
            "required": True,
            "minlength": 3,
            "maxlength": 3,
            "allowed": SUPPORTED_CURRENCIES,
            "regex": r"^[A-Z]{3}$",
        }

    @staticmethod
    def country() -> Dict[str, Any]:
        """Constraint for country codes.

        Returns:
            Dict: Cerberus schema for country validation
        """
        return {
            "type": "string",
            "required": True,
            "minlength": 2,
            "maxlength": 2,
            "allowed": SUPPORTED_COUNTRIES,
            "regex": r"^[A-Z]{2}$",
        }

    @staticmethod
    def description() -> Dict[str, Any]:
        """Constraint for payment descriptions.

        Returns:
            Dict: Cerberus schema for description validation
        """
        return {"type": "string", "required": False, "maxlength": 255, "nullable": True}

    @staticmethod
    def order_id() -> Dict[str, Any]:
        """Constraint for order IDs.

        Returns:
            Dict: Cerberus schema for order_id validation
        """
        return {
            "type": "string",
            "required": False,
            "maxlength": 100,
            "regex": r"^[a-zA-Z0-9_-]+$",  # Alphanumeric with underscores and hyphens
            "nullable": True,
        }

    @staticmethod
    def payment_id() -> Dict[str, Any]:
        """Constraint for payment IDs (UUIDs).

        Returns:
            Dict: Cerberus schema for payment_id validation
        """
        return {"type": "string", "required": True, "check_with": "validate_payment_id"}

    @staticmethod
    def payment_instrument() -> Dict[str, Any]:
        """Constraint for payment instrument (card) data.

        Returns:
            Dict: Cerberus schema for payment instrument validation
        """
        return {
            "type": "dict",
            "required": True,
            "schema": {
                "pan": {
                    "type": "string",
                    "required": True,
                    "minlength": 12,
                    "maxlength": 20,
                    "regex": r"^\d{12,20}$",
                },
                "exp_month": {"type": "integer", "required": True, "min": 1, "max": 12},
                "exp_year": {
                    "type": "integer",
                    "required": True,
                    "min": 2000,
                    "max": 2099,
                },
                "cvc": {
                    "type": "string",
                    "required": True,
                    "minlength": 3,
                    "maxlength": 4,
                    "regex": r"^\d{3,4}$",
                },
                "holder": {
                    "type": "string",
                    "required": True,
                    "maxlength": 100,
                    "regex": r"^[a-zA-Z\s]+$",  # Only letters and spaces
                },
            },
        }

    @staticmethod
    def billing_address() -> Dict[str, Any]:
        """Constraint for billing address data.

        Returns:
            Dict: Cerberus schema for billing address validation
        """
        return {
            "type": "dict",
            "required": False,
            "nullable": True,
            "schema": {
                "address_line1": {"type": "string", "required": True, "maxlength": 100},
                "address_line2": {
                    "type": "string",
                    "required": False,
                    "maxlength": 100,
                    "nullable": True,
                },
                "city": {"type": "string", "required": True, "maxlength": 50},
                "state": {
                    "type": "string",
                    "required": False,
                    "maxlength": 50,
                    "nullable": True,
                },
                "zip": {"type": "string", "required": True, "maxlength": 20},
                "country": Constraints.country(),
            },
        }

    @staticmethod
    def threeds2_data() -> Dict[str, Any]:
        """Constraint for 3D Secure v2 data.

        Returns:
            Dict: Cerberus schema for 3DS v2 validation
        """
        return {
            "type": "dict",
            "required": False,
            "nullable": True,
            "schema": {
                "notification_url": {
                    "type": "string",
                    "required": False,
                    "maxlength": 2000,
                    "regex": r"^https?://.+",
                    "nullable": True,
                },
                "browser_info": {
                    "type": "dict",
                    "required": False,
                    "nullable": True,
                    "schema": {
                        "accept_header": {
                            "type": "string",
                            "required": True,
                            "maxlength": 2048,
                        },
                        "color_depth": {
                            "type": "integer",
                            "required": True,
                            "allowed": [1, 4, 8, 15, 16, 24, 32, 48],
                        },
                        "java_enabled": {"type": "boolean", "required": True},
                        "javascript_enabled": {"type": "boolean", "required": True},
                        "browser_language": {
                            "type": "string",
                            "required": True,
                            "maxlength": 8,
                        },
                        "screen_height": {
                            "type": "integer",
                            "required": True,
                            "min": 1,
                        },
                        "screen_width": {"type": "integer", "required": True, "min": 1},
                        "time_zone": {
                            "type": "integer",
                            "required": True,
                            "min": -720,
                            "max": 840,
                        },
                        "user_agent": {
                            "type": "string",
                            "required": True,
                            "maxlength": 2048,
                        },
                        "challenge_window_size": {
                            "type": "string",
                            "required": False,
                            "regex": r"^\d+x\d+$",  # Format like "500x600"
                            "nullable": True,
                        },
                        "ip_address": {
                            "type": "string",
                            "required": False,
                            "nullable": True,
                        },
                    },
                },
            },
        }

    @staticmethod
    def recurring_data() -> Dict[str, Any]:
        """Constraint for recurring payment data.

        Returns:
            Dict: Cerberus schema for recurring payment validation
        """
        return {
            "type": "dict",
            "required": False,
            "nullable": True,
            "schema": {"payment_id": Constraints.payment_id()},
        }

    @staticmethod
    def refund_amount() -> Dict[str, Any]:
        """Constraint for refund amounts.

        Returns:
            Dict: Cerberus schema for refund amount validation
        """
        return {
            "type": "string",
            "required": True,
            "regex": r"^\d+\.\d{2}$",
            "check_with": "validate_amount",
        }

    @staticmethod
    def settlement_amount() -> Dict[str, Any]:
        """Constraint for settlement amounts.

        Returns:
            Dict: Cerberus schema for settlement amount validation
        """
        return {
            "type": "string",
            "required": True,
            "regex": r"^\d+\.\d{2}$",
            "check_with": "validate_amount",
        }

    @staticmethod
    def payment_link_data() -> Dict[str, Any]:
        """Constraint for payment link creation data.

        Returns:
            Dict: Cerberus schema for payment link validation
        """
        return {
            "type": "dict",
            "required": False,
            "nullable": True,
            "schema": {
                "expiration_date": {
                    "type": "string",
                    "required": False,
                    "regex": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",  # ISO 8601
                    "nullable": True,
                },
                "multiple_use": {
                    "type": "boolean",
                    "required": False,
                    "nullable": True,
                },
            },
        }

    @staticmethod
    def finalize_payment() -> Dict[str, Any]:
        """Constraint for payment finalization data.

        Returns:
            Dict: Cerberus schema for payment finalization
        """
        return {
            "type": "dict",
            "required": True,
            "schema": {
                "authorize_data": {
                    "type": "string",
                    "required": False,
                    "nullable": True,
                    "excludes": "cres",  # Either authorize_data OR cres, not both
                },
                "cres": {
                    "type": "string",
                    "required": False,
                    "nullable": True,
                    "excludes": "authorize_data",  # Either authorize_data OR cres
                },
            },
        }

    @staticmethod
    def create_payment_schema() -> Dict[str, Any]:
        """Complete schema for payment creation.

        Returns:
            Dict: Complete Cerberus schema for payment creation
        """
        return {
            "amount": Constraints.amount(),
            "currency": Constraints.currency(),
            "description": Constraints.description(),
            "order_id": Constraints.order_id(),
            "payment_instrument": Constraints.payment_instrument(),
            "billing_address": Constraints.billing_address(),
            "threeds2_data": Constraints.threeds2_data(),
            "settle": {"type": "boolean", "required": False, "nullable": True},
            "country": Constraints.country(),
        }

    @staticmethod
    def create_recurring_payment_schema() -> Dict[str, Any]:
        """Complete schema for recurring payment creation.

        Returns:
            Dict: Complete Cerberus schema for recurring payment
        """
        return {
            "amount": Constraints.amount(),
            "currency": Constraints.currency(),
            "description": Constraints.description(),
            "order_id": Constraints.order_id(),
            "payment_instrument": Constraints.recurring_data(),
            "settle": {"type": "boolean", "required": False, "nullable": True},
            "country": Constraints.country(),
        }

    @staticmethod
    def create_refund_schema() -> Dict[str, Any]:
        """Complete schema for refund creation.

        Returns:
            Dict: Complete Cerberus schema for refund creation
        """
        return {
            "amount": Constraints.refund_amount(),
            "description": Constraints.description(),
        }

    @staticmethod
    def create_settlement_schema() -> Dict[str, Any]:
        """Complete schema for settlement creation.

        Returns:
            Dict: Complete Cerberus schema for settlement creation
        """
        return {
            "amount": Constraints.settlement_amount(),
            "description": Constraints.description(),
        }

    @staticmethod
    def finalize_payment_schema(is_threedsv2: bool = False) -> Dict[str, Any]:
        """Complete schema for payment finalization.

        Args:
            is_threedsv2: Whether this is a 3D Secure v2 flow

        Returns:
            Dict: Complete Cerberus schema for payment finalization
        """
        if is_threedsv2:
            return {"cres": {"type": "string", "required": True, "empty": False}}
        else:
            return {
                "authorize_data": {"type": "string", "required": True, "empty": False}
            }

    @staticmethod
    def create_payment_link_schema() -> Dict[str, Any]:
        """Complete schema for payment link creation.

        Returns:
            Dict: Complete Cerberus schema for payment link creation
        """
        return {
            "amount": Constraints.amount(),
            "currency": Constraints.currency(),
            "country": Constraints.country(),
            "description": Constraints.description(),
            "expiration_date": {
                "type": "string",
                "required": False,
                "regex": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",  # ISO 8601
                "nullable": True,
            },
            "multiple_use": {"type": "boolean", "required": False, "nullable": True},
        }

    @staticmethod
    def update_payment_link_schema() -> Dict[str, Any]:
        """Complete schema for payment link updates.

        Returns:
            Dict: Complete Cerberus schema for payment link updates
        """
        return {
            "expiration_date": {
                "type": "string",
                "required": False,
                "regex": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",  # ISO 8601
                "nullable": True,
            },
            "enabled": {"type": "boolean", "required": False, "nullable": True},
        }
