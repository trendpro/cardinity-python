"""
Cardinity Chargeback Models

This module contains models for chargeback operations.
"""

from typing import Any, Dict, Optional, Union

from .base import ReadOnlyModel


class GetChargeback(ReadOnlyModel):
    """Model for retrieving chargeback information.

    This model supports multiple chargeback retrieval modes:
    1. Single chargeback retrieval by payment_id and chargeback_id
    2. All chargebacks for a specific payment
    3. Global chargeback listing with optional limit
    """

    def __init__(
        self,
        payment_id_or_limit: Optional[Union[str, int]] = None,
        chargeback_id: Optional[str] = None,
    ) -> None:
        """Initialize GetChargeback model.

        Args:
            payment_id_or_limit: Either a payment ID (str) for payment-specific
                                chargebacks, or limit (int) for global listing,
                                or None for all global chargebacks
            chargeback_id: Optional specific chargeback ID to retrieve
        """
        if isinstance(payment_id_or_limit, int):
            # Global chargeback listing with limit
            self._mode = "global_with_limit"
            self._limit: Optional[int] = payment_id_or_limit
            self._payment_id: Optional[str] = None
            self._chargeback_id: Optional[str] = None
        elif payment_id_or_limit is None:
            # Global chargeback listing without limit
            self._mode = "global"
            self._limit = None
            self._payment_id = None
            self._chargeback_id = None
        else:
            # Payment-specific chargeback operations
            self._mode = "payment_specific"
            self._payment_id = str(payment_id_or_limit)
            self._chargeback_id = chargeback_id
            self._limit = None

        super().__init__()

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for chargeback retrieval.

        Returns:
            Dict[str, Any]: Empty constraints for read-only operations
        """
        return {}

    def get_endpoint(self) -> str:
        """Get the API endpoint for chargeback retrieval.

        Returns:
            str: The appropriate endpoint based on retrieval mode
        """
        if self._mode == "global_with_limit":
            return f"/payments/chargebacks?limit={self._limit}"
        elif self._mode == "global":
            return "/payments/chargebacks"
        else:
            # Payment-specific mode
            if self._chargeback_id:
                return f"/payments/{self._payment_id}/chargebacks/{self._chargeback_id}"
            else:
                return f"/payments/{self._payment_id}/chargebacks/"

    def get_method(self) -> str:
        """Get the HTTP method for chargeback retrieval.

        Returns:
            str: Always returns GET for chargeback retrieval
        """
        return "GET"

    def get_payment_id(self) -> Optional[str]:
        """Get the payment ID for payment-specific chargebacks.

        Returns:
            Optional[str]: Payment ID or None if global mode
        """
        return self._payment_id

    def get_chargeback_id(self) -> Optional[str]:
        """Get the chargeback ID for single chargeback retrieval.

        Returns:
            Optional[str]: Chargeback ID or None if listing mode
        """
        return self._chargeback_id

    def get_limit(self) -> Optional[int]:
        """Get the limit for global chargeback listing.

        Returns:
            Optional[int]: Limit value or None if not applicable
        """
        return self._limit

    def is_global_listing(self) -> bool:
        """Check if this is a global chargeback listing request.

        Returns:
            bool: True if global listing, False if payment-specific
        """
        return self._mode in ["global", "global_with_limit"]

    def is_payment_specific(self) -> bool:
        """Check if this is a payment-specific chargeback request.

        Returns:
            bool: True if payment-specific, False if global
        """
        return self._mode == "payment_specific"

    def is_single_chargeback(self) -> bool:
        """Check if this is a single chargeback retrieval request.

        Returns:
            bool: True if retrieving single chargeback, False if listing
        """
        return self._chargeback_id is not None
