"""
Cardinity Validation Engine

This module provides the validation functionality using Cerberus validator.
"""

from typing import Any, Dict, List, Optional

from cerberus import Validator


class CardinityValidator(Validator):
    """Custom Cerberus validator for Cardinity API data.

    This extends the base Cerberus validator with custom validation methods
    specific to Cardinity API requirements.
    """

    def _check_with_validate_amount(self, field: str, value: Any) -> None:
        """Custom validator for amount field.

        Validates that the amount is >= 0.50 and in the correct format.
        """
        try:
            if isinstance(value, str):
                amount_value = float(value)
                if amount_value < 0.50:
                    self._error(field, "Amount must be at least 0.50")
        except (ValueError, TypeError):
            self._error(field, "Amount must be a valid number")

    def _check_with_validate_payment_id(self, field: str, value: Any) -> None:
        """Custom validator for payment ID field.

        Validates UUID format for payment IDs.
        """
        if not isinstance(value, str):
            self._error(field, "Payment ID must be a string")
            return

        # Basic UUID format check (can be enhanced later)
        if len(value) != 36:
            self._error(field, "Payment ID must be 36 characters long")

    def _check_with_validate_expiry_date(self, field: str, value: Any) -> None:
        """Custom validator for card expiry date.

        Validates that the expiry date is not in the past.
        """
        if not isinstance(value, dict):
            return

        year = value.get("exp_year")
        month = value.get("exp_month")

        if year and month:
            from datetime import datetime

            current_date = datetime.now()
            if year < current_date.year or (
                year == current_date.year and month < current_date.month
            ):
                self._error(field, "Expiry date cannot be in the past")


def validate_data(
    data: Dict[str, Any], schema: Dict[str, Any]
) -> Optional[Dict[str, List[str]]]:
    """Validate data against a schema using Cerberus.

    Args:
        data: The data to validate
        schema: The validation schema

    Returns:
        Dictionary of validation errors if any, None if validation passes
    """
    validator = CardinityValidator(schema)

    if validator.validate(data):
        return None
    else:
        return validator.errors


def validate_required_fields(
    data: Dict[str, Any], required_fields: List[str]
) -> Optional[Dict[str, List[str]]]:
    """Validate that all required fields are present.

    Args:
        data: The data to validate
        required_fields: List of required field names

    Returns:
        Dictionary of validation errors if any, None if validation passes
    """
    errors = {}

    for field in required_fields:
        if field not in data or data[field] is None:
            errors[field] = [f"{field} is required"]
        elif isinstance(data[field], str) and not data[field].strip():
            errors[field] = [f"{field} cannot be empty"]

    return errors if errors else None


def validate_amount_format(amount: Any) -> Optional[str]:
    """Validate amount format specifically.

    Args:
        amount: The amount value to validate

    Returns:
        Error message if validation fails, None if validation passes
    """
    if not isinstance(amount, str):
        return "Amount must be a string"

    import re

    if not re.match(r"^\d+\.\d{2}$", amount):
        return "Amount must be in format #.## (e.g., 10.50)"

    try:
        amount_value = float(amount)
        if amount_value < 0.50:
            return "Amount must be at least 0.50"
    except ValueError:
        return "Amount must be a valid number"

    return None


def validate_card_number(pan: Any) -> Optional[str]:
    """Validate credit card number format.

    Args:
        pan: Primary Account Number (card number)

    Returns:
        Error message if validation fails, None if validation passes
    """
    if not isinstance(pan, str):
        return "Card number must be a string"

    # Remove spaces and dashes
    clean_pan = pan.replace(" ", "").replace("-", "")

    if not clean_pan.isdigit():
        return "Card number must contain only digits"

    if len(clean_pan) < 12 or len(clean_pan) > 20:
        return "Card number must be between 12 and 20 digits"

    return None


def validate_currency_code(currency: Any) -> Optional[str]:
    """Validate ISO currency code.

    Args:
        currency: Currency code to validate

    Returns:
        Error message if validation fails, None if validation passes
    """
    if not isinstance(currency, str):
        return "Currency must be a string"

    if len(currency) != 3:
        return "Currency must be a 3-letter ISO code"

    if not currency.isupper():
        return "Currency must be uppercase"

    if not currency.isalpha():
        return "Currency must contain only letters"

    return None


def validate_country_code(country: Any) -> Optional[str]:
    """Validate ISO country code.

    Args:
        country: Country code to validate

    Returns:
        Error message if validation fails, None if validation passes
    """
    if not isinstance(country, str):
        return "Country must be a string"

    if len(country) != 2:
        return "Country must be a 2-letter ISO code"

    if not country.isupper():
        return "Country must be uppercase"

    if not country.isalpha():
        return "Country must contain only letters"

    return None
