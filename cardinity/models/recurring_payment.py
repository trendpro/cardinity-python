"""
Cardinity Recurring Payment Model

This module contains the RecurringPayment model for creating recurring payments.
"""

from typing import Any, Dict

from ..validation.constraints import Constraints
from .base import BaseModel


class RecurringPayment(BaseModel):
    """Model for creating recurring payment requests.

    Recurring payments use a previously stored payment instrument
    from a successful payment to process new charges.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize RecurringPayment model.

        Args:
            **kwargs: Recurring payment data as keyword arguments
        """
        super().__init__(**kwargs)

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for recurring payment creation.

        Returns:
            Dict[str, Any]: Cerberus validation schema for recurring payment data
        """
        return Constraints.create_recurring_payment_schema()

    def get_endpoint(self) -> str:
        """Get the API endpoint for recurring payment creation.

        Returns:
            str: The payments endpoint (same as regular payments)
        """
        return "/payments"

    def get_method(self) -> str:
        """Get the HTTP method for recurring payment creation.

        Returns:
            str: Always returns POST for recurring payment creation
        """
        return "POST"

    def to_dict(self) -> Dict[str, Any]:
        """Convert recurring payment data to API-compatible dictionary.

        Returns:
            Dict[str, Any]: Recurring payment data formatted for API submission
        """
        data = super().to_dict()

        # Ensure payment method is set to 'recurring'
        data["payment_method"] = "recurring"

        return data

    def get_amount(self) -> str:
        """Get the payment amount.

        Returns:
            str: Payment amount in decimal format (e.g., "10.50")
        """
        return self.get_field("amount")

    def get_currency(self) -> str:
        """Get the payment currency.

        Returns:
            str: Three-letter ISO currency code (e.g., "EUR")
        """
        return self.get_field("currency")

    def get_payment_instrument(self) -> Dict[str, Any]:
        """Get the payment instrument reference.

        For recurring payments, this contains the reference to
        the previously stored payment instrument.

        Returns:
            Dict[str, Any]: Payment instrument reference data
        """
        return self.get_field("payment_instrument", {})

    def get_description(self) -> str:
        """Get the payment description.

        Returns:
            str: Payment description
        """
        return self.get_field("description", "")

    def get_order_id(self) -> str:
        """Get the order ID.

        Returns:
            str: Merchant's order identifier
        """
        return self.get_field("order_id", "")

    def is_settle(self) -> bool:
        """Check if payment should be automatically settled.

        Returns:
            bool: True if payment should be settled immediately
        """
        return self.get_field("settle", True)
