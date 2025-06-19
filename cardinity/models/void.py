"""
Cardinity Void Models

This module contains models for void operations.
"""

from typing import Any, Dict, Optional

from .base import BaseModel, ReadOnlyModel


class Void(BaseModel):
    """Model for creating void requests.

    Voids allow merchants to cancel previously authorized payments
    before they are settled.
    """

    def __init__(self, payment_id: str, **kwargs: Any) -> None:
        """Initialize Void model.

        Args:
            payment_id: The ID of the payment to void
            **kwargs: Optional void data as keyword arguments containing description
        """
        self._payment_id = str(payment_id)
        super().__init__(**kwargs)

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for void creation.

        Returns:
            Dict[str, Any]: Cerberus validation schema for void data
        """
        return {
            "description": {
                "type": "string",
                "required": False,
                "maxlength": 255,
                "nullable": True,
            }
        }

    def get_endpoint(self) -> str:
        """Get the API endpoint for void creation.

        Returns:
            str: The payment-specific void endpoint
        """
        return f"/payments/{self._payment_id}/voids"

    def get_method(self) -> str:
        """Get the HTTP method for void creation.

        Returns:
            str: Always returns POST for void creation
        """
        return "POST"

    def get_payment_id(self) -> str:
        """Get the payment ID being voided.

        Returns:
            str: The payment ID
        """
        return self._payment_id

    def get_description(self) -> str:
        """Get the void description.

        Returns:
            str: Void description
        """
        return self.get_field("description", "")


class GetVoid(ReadOnlyModel):
    """Model for retrieving void information.

    This model supports both single void retrieval and listing
    all voids for a payment.
    """

    def __init__(self, payment_id: str, void_id: Optional[str] = None) -> None:
        """Initialize GetVoid model.

        Args:
            payment_id: The ID of the payment
            void_id: Optional specific void ID to retrieve
        """
        self._payment_id = str(payment_id)
        self._void_id = void_id
        super().__init__()

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for void retrieval.

        Returns:
            Dict[str, Any]: Empty constraints for read-only operations
        """
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint for void retrieval.

        Returns:
            str: The appropriate endpoint based on retrieval mode
        """
        if self._void_id:
            return f"/payments/{self._payment_id}/voids/{self._void_id}"
        else:
            return f"/payments/{self._payment_id}/voids/"

    def get_method(self) -> str:
        """Get the HTTP method for void retrieval.

        Returns:
            str: Always returns GET for void retrieval
        """
        return "GET"

    def get_payment_id(self) -> str:
        """Get the payment ID.

        Returns:
            str: The payment ID
        """
        return self._payment_id

    def get_void_id(self) -> Optional[str]:
        """Get the void ID for single void retrieval.

        Returns:
            Optional[str]: Void ID or None if listing mode
        """
        return self._void_id

    def is_listing(self) -> bool:
        """Check if this is a void listing request.

        Returns:
            bool: True if listing voids, False if retrieving single void
        """
        return self._void_id is None
