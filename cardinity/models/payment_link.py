"""
Cardinity Payment Link Models

This module contains models for payment link operations.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from ..validation.constraints import Constraints
from .base import BaseModel, ReadOnlyModel


class PaymentLink(BaseModel):
    """Model for creating payment link requests.

    Payment links allow merchants to generate URLs that customers
    can use to complete payments without direct integration.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Initialize PaymentLink model.

        Args:
            data: Payment link data dictionary
        """
        # Handle expiration_date conversion to ISO format if needed
        if "expiration_date" in data and data["expiration_date"]:
            if isinstance(data["expiration_date"], datetime):
                data["expiration_date"] = data["expiration_date"].isoformat() + "Z"

        super().__init__(**data)

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for payment link creation.

        Returns:
            Dict[str, Any]: Cerberus validation schema for payment link data
        """
        return Constraints.create_payment_link_schema()

    def get_endpoint(self) -> str:
        """Get the API endpoint for payment link creation.

        Returns:
            str: The payment links endpoint
        """
        return "/paymentLinks"

    def get_method(self) -> str:
        """Get the HTTP method for payment link creation.

        Returns:
            str: Always returns POST for payment link creation
        """
        return "POST"

    def get_amount(self) -> str:
        """Get the payment link amount.

        Returns:
            str: Payment amount in decimal format (e.g., "10.50")
        """
        return self.get_field("amount")

    def get_currency(self) -> str:
        """Get the payment link currency.

        Returns:
            str: Three-letter ISO currency code (e.g., "EUR")
        """
        return self.get_field("currency")

    def get_country(self) -> str:
        """Get the payment link country.

        Returns:
            str: Two-letter ISO country code (e.g., "LT")
        """
        return self.get_field("country")

    def get_description(self) -> str:
        """Get the payment link description.

        Returns:
            str: Payment link description
        """
        return self.get_field("description", "")

    def get_expiration_date(self) -> Optional[str]:
        """Get the payment link expiration date.

        Returns:
            Optional[str]: Expiration date in ISO 8601 format or None
        """
        return self.get_field("expiration_date")

    def is_multiple_use(self) -> bool:
        """Check if payment link allows multiple uses.

        Returns:
            bool: True if multiple use is allowed
        """
        return self.get_field("multiple_use", False)


class UpdatePaymentLink(BaseModel):
    """Model for updating existing payment links.

    This model allows updating the expiration date and enabled status
    of existing payment links.
    """

    def __init__(self, link_id: str, data: Dict[str, Any]) -> None:
        """Initialize UpdatePaymentLink model.

        Args:
            link_id: The ID of the payment link to update
            data: Update data dictionary
        """
        self._link_id = str(link_id)

        # Handle expiration_date conversion to ISO format if needed
        if "expiration_date" in data and data["expiration_date"]:
            if isinstance(data["expiration_date"], datetime):
                data["expiration_date"] = data["expiration_date"].isoformat() + "Z"

        super().__init__(**data)

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for payment link updates.

        Returns:
            Dict[str, Any]: Cerberus validation schema for payment link updates
        """
        return Constraints.update_payment_link_schema()

    def get_endpoint(self) -> str:
        """Get the API endpoint for payment link updates.

        Returns:
            str: The payment link-specific endpoint
        """
        return f"/paymentLinks/{self._link_id}"

    def get_method(self) -> str:
        """Get the HTTP method for payment link updates.

        Returns:
            str: Always returns PATCH for payment link updates
        """
        return "PATCH"

    def get_link_id(self) -> str:
        """Get the payment link ID being updated.

        Returns:
            str: The payment link ID
        """
        return self._link_id

    def get_expiration_date(self) -> Optional[str]:
        """Get the updated expiration date.

        Returns:
            Optional[str]: Expiration date in ISO 8601 format or None
        """
        return self.get_field("expiration_date")

    def is_enabled(self) -> Optional[bool]:
        """Get the enabled status.

        Returns:
            Optional[bool]: Enabled status or None if not set
        """
        return self.get_field("enabled")


class GetPaymentLink(ReadOnlyModel):
    """Model for retrieving payment link information.

    This model retrieves information about a specific payment link.
    """

    def __init__(self, link_id: str) -> None:
        """Initialize GetPaymentLink model.

        Args:
            link_id: The ID of the payment link to retrieve
        """
        self._link_id = str(link_id)
        super().__init__()

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for payment link retrieval.

        Returns:
            Dict[str, Any]: Empty constraints for read-only operations
        """
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint for payment link retrieval.

        Returns:
            str: The payment link-specific endpoint
        """
        return f"/paymentLinks/{self._link_id}"

    def get_method(self) -> str:
        """Get the HTTP method for payment link retrieval.

        Returns:
            str: Always returns GET for payment link retrieval
        """
        return "GET"

    def get_link_id(self) -> str:
        """Get the payment link ID being retrieved.

        Returns:
            str: The payment link ID
        """
        return self._link_id
