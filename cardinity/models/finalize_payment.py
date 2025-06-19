"""
Cardinity Finalize Payment Model

This module contains the FinalizePayment model for completing 3D Secure authentication.
"""

from typing import Any, Dict, Optional

from ..validation.constraints import Constraints
from .base import BaseModel


class FinalizePayment(BaseModel):
    """Model for finalizing payment after 3D Secure authentication.

    This model supports both 3D Secure v1 and v2 authentication flows:
    - 3DS v1: Uses authorize_data parameter
    - 3DS v2: Uses cres (Challenge Response) parameter
    """

    def __init__(self, payment_id: str, **kwargs: Any):
        """Initialize FinalizePayment model.

        Args:
            payment_id: The ID of the payment to finalize
            **kwargs: Finalization data as keyword arguments containing either cres or authorize_data
        """
        self._payment_id = str(payment_id)

        # Determine 3DS version based on the data provided
        self._is_threedsv2 = "cres" in kwargs

        super().__init__(**kwargs)

    def get_constraints(self) -> Dict[str, Any]:
        """Get validation constraints for payment finalization.

        Returns:
            Dict[str, Any]: Cerberus validation schema for finalization data
        """
        return Constraints.finalize_payment_schema(self._is_threedsv2)

    def get_endpoint(self) -> str:
        """Get the API endpoint for payment finalization.

        Returns:
            str: The payment-specific endpoint for PATCH operations
        """
        return f"/payments/{self._payment_id}"

    def get_method(self) -> str:
        """Get the HTTP method for payment finalization.

        Returns:
            str: Always returns PATCH for payment finalization
        """
        return "PATCH"

    def is_threedsv2(self) -> bool:
        """Check if this is a 3D Secure v2 flow.

        Returns:
            bool: True if 3DS v2, False if 3DS v1
        """
        return self._is_threedsv2

    def get_payment_id(self) -> str:
        """Get the payment ID being finalized.

        Returns:
            str: The payment ID
        """
        return self._payment_id

    def get_cres(self) -> Optional[str]:
        """Get the Challenge Response for 3DS v2.

        Returns:
            Optional[str]: The cres value or None if not 3DS v2
        """
        if self._is_threedsv2:
            return self.get_field("cres")
        return None

    def get_authorize_data(self) -> Optional[str]:
        """Get the authorization data for 3DS v1.

        Returns:
            Optional[str]: The authorize_data value or None if 3DS v2
        """
        if not self._is_threedsv2:
            return self.get_field("authorize_data")
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert finalization data to API-compatible dictionary.

        Returns:
            Dict[str, Any]: Only the relevant field based on 3DS version
        """
        data = super().to_dict()

        # Only include the relevant field for the 3DS version
        if self._is_threedsv2:
            return {k: v for k, v in data.items() if k == "cres"}
        else:
            return {k: v for k, v in data.items() if k == "authorize_data"}
