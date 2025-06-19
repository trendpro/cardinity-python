"""
Cardinity Payment Model

This module contains the Payment model for creating payment requests.
"""

from typing import Any, Dict

from ..validation.constraints import Constraints
from .base import BaseModel


class Payment(BaseModel):
    """Model for creating payment requests.

    This model handles standard card payments with support for 3D Secure v2,
    billing addresses, and all required payment data validation.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize Payment model.

        Args:
            **kwargs: Payment data as keyword arguments
        """
        super().__init__(**kwargs)

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for payment creation.

        Returns:
            Dict[str, Any]: Cerberus validation schema for payment data
        """
        return Constraints.create_payment_schema()

    def get_endpoint(self) -> str:
        """Get the API endpoint for payment creation.

        Returns:
            str: The payments endpoint
        """
        return "/payments"

    def get_method(self) -> str:
        """Get the HTTP method for payment creation.

        Returns:
            str: Always returns POST for payment creation
        """
        return "POST"

    def to_dict(self) -> Dict[str, Any]:
        """Convert payment data to API-compatible dictionary.

        Returns:
            Dict[str, Any]: Payment data formatted for API submission
        """
        data = super().to_dict()

        # Ensure payment method is set to 'card' for standard payments
        data["payment_method"] = "card"

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
        """Get the payment instrument (card) data.

        Returns:
            Dict[str, Any]: Payment instrument data including PAN, expiry, etc.
        """
        return self.get_field("payment_instrument", {})

    def has_threeds2_data(self) -> bool:
        """Check if 3D Secure v2 data is present.

        Returns:
            bool: True if 3DS v2 data is present
        """
        return (
            self.has_field("threeds2_data")
            and self.get_field("threeds2_data") is not None
        )

    def has_billing_address(self) -> bool:
        """Check if billing address is present.

        Returns:
            bool: True if billing address is present
        """
        return (
            self.has_field("billing_address")
            and self.get_field("billing_address") is not None
        )
