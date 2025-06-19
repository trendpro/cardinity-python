"""
Cardinity Settlement Models

This module contains models for settlement operations.
"""

from typing import Any, Dict, Optional

from ..validation.constraints import Constraints
from .base import BaseModel, ReadOnlyModel


class Settlement(BaseModel):
    """Model for creating settlement requests.

    Settlements allow merchants to capture funds from previously
    authorized payments.
    """

    def __init__(self, payment_id: str, **kwargs: Any) -> None:
        """Initialize Settlement model.

        Args:
            payment_id: The ID of the payment to settle
            **kwargs: Settlement data as keyword arguments containing amount and description
        """
        self._payment_id = str(payment_id)
        super().__init__(**kwargs)

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for settlement creation.

        Returns:
            Dict[str, Any]: Cerberus validation schema for settlement data
        """
        return Constraints.create_settlement_schema()

    def get_endpoint(self) -> str:
        """Get the API endpoint for settlement creation.

        Returns:
            str: The payment-specific settlement endpoint
        """
        return f"/payments/{self._payment_id}/settlements"

    def get_method(self) -> str:
        """Get the HTTP method for settlement creation.

        Returns:
            str: Always returns POST for settlement creation
        """
        return "POST"

    def get_payment_id(self) -> str:
        """Get the payment ID being settled.

        Returns:
            str: The payment ID
        """
        return self._payment_id

    def get_amount(self) -> str:
        """Get the settlement amount.

        Returns:
            str: Settlement amount in decimal format (e.g., "10.50")
        """
        return self.get_field("amount")

    def get_description(self) -> str:
        """Get the settlement description.

        Returns:
            str: Settlement description
        """
        return self.get_field("description", "")


class GetSettlement(ReadOnlyModel):
    """Model for retrieving settlement information.

    This model supports both single settlement retrieval and listing
    all settlements for a payment.
    """

    def __init__(self, payment_id: str, settlement_id: Optional[str] = None) -> None:
        """Initialize GetSettlement model.

        Args:
            payment_id: The ID of the payment
            settlement_id: Optional specific settlement ID to retrieve
        """
        self._payment_id = str(payment_id)
        self._settlement_id = settlement_id
        super().__init__()

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for settlement retrieval.

        Returns:
            Dict[str, Any]: Empty constraints for read-only operations
        """
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint for settlement retrieval.

        Returns:
            str: The appropriate endpoint based on retrieval mode
        """
        if self._settlement_id:
            return f"/payments/{self._payment_id}/settlements/{self._settlement_id}"
        else:
            return f"/payments/{self._payment_id}/settlements/"

    def get_method(self) -> str:
        """Get the HTTP method for settlement retrieval.

        Returns:
            str: Always returns GET for settlement retrieval
        """
        return "GET"

    def get_payment_id(self) -> str:
        """Get the payment ID.

        Returns:
            str: The payment ID
        """
        return self._payment_id

    def get_settlement_id(self) -> Optional[str]:
        """Get the settlement ID for single settlement retrieval.

        Returns:
            Optional[str]: Settlement ID or None if listing mode
        """
        return self._settlement_id

    def is_listing(self) -> bool:
        """Check if this is a settlement listing request.

        Returns:
            bool: True if listing settlements, False if retrieving single settlement
        """
        return self._settlement_id is None
