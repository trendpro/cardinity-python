"""
Cardinity SDK Main Interface

This module provides the main Cardinity class for interacting with the Cardinity API.
"""

from typing import Any, Dict, Optional, Union

from .auth import CardinityAuth
from .client import CardinityClient
from .models import (
    FinalizePayment,
    GetChargeback,
    GetPayment,
    GetPaymentLink,
    GetRefund,
    GetSettlement,
    GetVoid,
    Payment,
    PaymentLink,
    RecurringPayment,
    Refund,
    Settlement,
    UpdatePaymentLink,
    Void,
)


class Cardinity:
    """Main Cardinity SDK class.

    This class provides a convenient interface for all Cardinity API operations.
    It handles authentication, HTTP communication, and provides methods for
    all supported payment operations.

    Example:
        Basic usage example::

            cardinity = Cardinity(
                consumer_key="your_consumer_key",
                consumer_secret="your_consumer_secret"
            )

            # Create a payment
            payment = cardinity.create_payment(
                amount="10.50",
                currency="EUR",
                description="Test payment"
            )
    """

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        base_url: str = "https://api.cardinity.com/v1",
    ) -> None:
        """Initialize the Cardinity SDK.

        Args:
            consumer_key: Your Cardinity consumer key
            consumer_secret: Your Cardinity consumer secret
            base_url: Base URL for the Cardinity API (default: production)
        """
        self._auth = CardinityAuth(consumer_key, consumer_secret)
        self._client = CardinityClient(self._auth, base_url)

    # Payment Operations

    def create_payment(self, **kwargs: Any) -> Dict[str, Any]:
        """Create a new payment.

        Args:
            **kwargs: Payment data including amount, currency, description, etc.

        Returns:
            Dict[str, Any]: Payment response from the API

        Raises:
            ValidationError: If payment data is invalid
            APIError: If the API request fails
        """
        payment = Payment(**kwargs)
        return self._client.execute_request(payment)

    def get_payment(
        self, payment_id: Optional[str] = None, limit: Optional[int] = None
    ) -> Dict[str, Any]:
        """Get payment information.

        Args:
            payment_id: Specific payment ID to retrieve (optional)
            limit: Limit for payment listing (optional, used when payment_id is None)

        Returns:
            Dict[str, Any]: Payment data or list of payments

        Raises:
            APIError: If the API request fails
        """
        get_payment = GetPayment(payment_id, limit)
        return self._client.execute_request(get_payment)

    def finalize_payment(self, payment_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Finalize a payment (complete 3D Secure authentication).

        Args:
            payment_id: ID of the payment to finalize
            **kwargs: Finalization data (authorize_data or cres)

        Returns:
            Dict[str, Any]: Finalized payment response

        Raises:
            ValidationError: If finalization data is invalid
            APIError: If the API request fails
        """
        finalize = FinalizePayment(payment_id, **kwargs)
        return self._client.execute_request(finalize)

    def create_recurring_payment(self, **kwargs: Any) -> Dict[str, Any]:
        """Create a recurring payment.

        Args:
            **kwargs: Recurring payment data including payment_id reference

        Returns:
            Dict[str, Any]: Recurring payment response

        Raises:
            ValidationError: If recurring payment data is invalid
            APIError: If the API request fails
        """
        recurring = RecurringPayment(**kwargs)
        return self._client.execute_request(recurring)

    # Refund Operations

    def create_refund(self, payment_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Create a refund for a payment.

        Args:
            payment_id: ID of the payment to refund
            **kwargs: Refund data including amount and description

        Returns:
            Dict[str, Any]: Refund response

        Raises:
            ValidationError: If refund data is invalid
            APIError: If the API request fails
        """
        refund = Refund(payment_id, **kwargs)
        return self._client.execute_request(refund)

    def get_refund(
        self, payment_id: str, refund_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get refund information.

        Args:
            payment_id: ID of the payment
            refund_id: Specific refund ID (optional, lists all if None)

        Returns:
            Dict[str, Any]: Refund data or list of refunds

        Raises:
            APIError: If the API request fails
        """
        get_refund = GetRefund(payment_id, refund_id)
        return self._client.execute_request(get_refund)

    # Settlement Operations

    def create_settlement(self, payment_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Create a settlement for a payment.

        Args:
            payment_id: ID of the payment to settle
            **kwargs: Settlement data including amount and description

        Returns:
            Dict[str, Any]: Settlement response

        Raises:
            ValidationError: If settlement data is invalid
            APIError: If the API request fails
        """
        settlement = Settlement(payment_id, **kwargs)
        return self._client.execute_request(settlement)

    def get_settlement(
        self, payment_id: str, settlement_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get settlement information.

        Args:
            payment_id: ID of the payment
            settlement_id: Specific settlement ID (optional, lists all if None)

        Returns:
            Dict[str, Any]: Settlement data or list of settlements

        Raises:
            APIError: If the API request fails
        """
        get_settlement = GetSettlement(payment_id, settlement_id)
        return self._client.execute_request(get_settlement)

    # Void Operations

    def create_void(self, payment_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Create a void for a payment.

        Args:
            payment_id: ID of the payment to void
            **kwargs: Optional void data including description

        Returns:
            Dict[str, Any]: Void response

        Raises:
            APIError: If the API request fails
        """
        void = Void(payment_id, **kwargs if kwargs else {})
        return self._client.execute_request(void)

    def get_void(
        self, payment_id: str, void_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get void information.

        Args:
            payment_id: ID of the payment
            void_id: Specific void ID (optional, lists all if None)

        Returns:
            Dict[str, Any]: Void data or list of voids

        Raises:
            APIError: If the API request fails
        """
        get_void = GetVoid(payment_id, void_id)
        return self._client.execute_request(get_void)

    # Chargeback Operations

    def get_chargeback(
        self,
        payment_id_or_limit: Optional[Union[str, int]] = None,
        chargeback_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get chargeback information.

        This method supports multiple modes:
        - Global chargeback listing: get_chargeback() or get_chargeback(limit=10)
        - Payment-specific chargebacks: get_chargeback("payment_id")
        - Single chargeback: get_chargeback("payment_id", "chargeback_id")

        Args:
            payment_id_or_limit: Payment ID (str) or limit (int) for global listing
            chargeback_id: Specific chargeback ID (optional)

        Returns:
            Dict[str, Any]: Chargeback data or list of chargebacks

        Raises:
            APIError: If the API request fails
        """
        get_chargeback = GetChargeback(payment_id_or_limit, chargeback_id)
        return self._client.execute_request(get_chargeback)

    # Payment Link Operations

    def create_payment_link(self, **kwargs: Any) -> Dict[str, Any]:
        """Create a payment link.

        Args:
            **kwargs: Payment link data including amount, currency, description, etc.

        Returns:
            Dict[str, Any]: Payment link response

        Raises:
            ValidationError: If payment link data is invalid
            APIError: If the API request fails
        """
        payment_link = PaymentLink(kwargs)
        return self._client.execute_request(payment_link)

    def update_payment_link(self, link_id: str, **kwargs: Any) -> Dict[str, Any]:
        """Update an existing payment link.

        Args:
            link_id: ID of the payment link to update
            **kwargs: Update data including expiration_date and enabled status

        Returns:
            Dict[str, Any]: Updated payment link response

        Raises:
            ValidationError: If update data is invalid
            APIError: If the API request fails
        """
        update_link = UpdatePaymentLink(link_id, kwargs)
        return self._client.execute_request(update_link)

    def get_payment_link(self, link_id: str) -> Dict[str, Any]:
        """Get payment link information.

        Args:
            link_id: ID of the payment link to retrieve

        Returns:
            Dict[str, Any]: Payment link data

        Raises:
            APIError: If the API request fails
        """
        get_link = GetPaymentLink(link_id)
        return self._client.execute_request(get_link)

    # Utility Methods

    def get_client(self) -> CardinityClient:
        """Get the underlying HTTP client for advanced usage.

        Returns:
            CardinityClient: The HTTP client instance
        """
        return self._client

    def get_auth(self) -> CardinityAuth:
        """Get the authentication instance.

        Returns:
            CardinityAuth: The authentication instance
        """
        return self._auth
