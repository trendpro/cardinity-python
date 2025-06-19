"""
Cardinity Get Payment Model

This module contains the GetPayment model for retrieving payment information.
"""

from typing import Any, Dict, Optional

from .base import ReadOnlyModel


class GetPayment(ReadOnlyModel):
    """Model for retrieving payment information.

    This model supports two retrieval modes:
    1. Single payment retrieval by payment ID
    2. Payment listing with optional limit parameter
    """

    def __init__(self, payment_id: Optional[str] = None, limit: Optional[int] = None):
        """Initialize GetPayment model.

        Args:
            payment_id: Specific payment ID to retrieve (optional)
            limit: Limit for payment listing (optional, used when payment_id is None)
        """
        if payment_id is not None:
            # Single payment retrieval mode
            self._payment_id = str(payment_id)
            self._limit = None
            self._is_listing = False
        else:
            # Payment listing mode
            self._payment_id = None
            self._limit = limit
            self._is_listing = True

        super().__init__()

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for payment retrieval.

        For retrieval operations, minimal validation is needed.

        Returns:
            Dict[str, Any]: Empty constraints for read-only operations
        """
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint for payment retrieval.

        Returns:
            str: The appropriate endpoint based on retrieval mode
        """
        if self._is_listing:
            if self._limit is not None:
                return f"/payments?limit={self._limit}"
            else:
                return "/payments"
        else:
            return f"/payments/{self._payment_id}"

    def get_method(self) -> str:
        """Get the HTTP method for payment retrieval.

        Returns:
            str: Always returns GET for payment retrieval
        """
        return "GET"

    def is_listing(self) -> bool:
        """Check if this is a payment listing request.

        Returns:
            bool: True if listing payments, False if retrieving single payment
        """
        return self._is_listing

    def get_payment_id(self) -> Optional[str]:
        """Get the payment ID for single payment retrieval.

        Returns:
            Optional[str]: Payment ID or None if listing mode
        """
        return self._payment_id

    def get_limit(self) -> Optional[int]:
        """Get the limit for payment listing.

        Returns:
            Optional[int]: Limit value or None if single retrieval mode
        """
        return self._limit
