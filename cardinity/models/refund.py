"""
Cardinity Refund Models

This module contains models for refund operations.
"""

from typing import Any, Dict, Optional

from ..validation.constraints import Constraints
from .base import BaseModel, ReadOnlyModel


class Refund(BaseModel):
    """Model for creating refund requests.

    Refunds allow merchants to return funds to customers for
    previously processed payments.
    """

    def __init__(self, payment_id: str, **kwargs: Any) -> None:
        """Initialize Refund model.

        Args:
            payment_id: The ID of the payment to refund
            **kwargs: Refund data as keyword arguments containing amount and description
        """
        self._payment_id = str(payment_id)
        super().__init__(**kwargs)

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for refund creation.

        Returns:
            Dict[str, Any]: Cerberus validation schema for refund data
        """
        return Constraints.create_refund_schema()

    def get_endpoint(self) -> str:
        """Get the API endpoint for refund creation.

        Returns:
            str: The payment-specific refund endpoint
        """
        return f"/payments/{self._payment_id}/refunds"

    def get_method(self) -> str:
        """Get the HTTP method for refund creation.

        Returns:
            str: Always returns POST for refund creation
        """
        return "POST"

    def get_payment_id(self) -> str:
        """Get the payment ID being refunded.

        Returns:
            str: The payment ID
        """
        return self._payment_id

    def get_amount(self) -> str:
        """Get the refund amount.

        Returns:
            str: Refund amount in decimal format (e.g., "10.50")
        """
        return self.get_field("amount")

    def get_description(self) -> str:
        """Get the refund description.

        Returns:
            str: Refund description
        """
        return self.get_field("description", "")


class GetRefund(ReadOnlyModel):
    """Model for retrieving refund information.

    This model supports both single refund retrieval and listing
    all refunds for a payment.
    """

    def __init__(self, payment_id: str, refund_id: Optional[str] = None) -> None:
        """Initialize GetRefund model.

        Args:
            payment_id: The ID of the payment
            refund_id: Optional specific refund ID to retrieve
        """
        self._payment_id = str(payment_id)
        self._refund_id = refund_id
        super().__init__()

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for refund retrieval.

        Returns:
            Dict[str, Any]: Empty constraints for read-only operations
        """
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint for refund retrieval.

        Returns:
            str: The appropriate endpoint based on retrieval mode
        """
        if self._refund_id:
            return f"/payments/{self._payment_id}/refunds/{self._refund_id}"
        else:
            return f"/payments/{self._payment_id}/refunds/"

    def get_method(self) -> str:
        """Get the HTTP method for refund retrieval.

        Returns:
            str: Always returns GET for refund retrieval
        """
        return "GET"

    def get_payment_id(self) -> str:
        """Get the payment ID.

        Returns:
            str: The payment ID
        """
        return self._payment_id

    def get_refund_id(self) -> Optional[str]:
        """Get the refund ID for single refund retrieval.

        Returns:
            Optional[str]: Refund ID or None if listing mode
        """
        return self._refund_id

    def is_listing(self) -> bool:
        """Check if this is a refund listing request.

        Returns:
            bool: True if listing refunds, False if retrieving single refund
        """
        return self._refund_id is None
