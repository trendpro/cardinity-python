"""
Unit tests for additional API models (Phase 5).
"""

from datetime import datetime

import pytest

from cardinity.exceptions import ValidationError
from cardinity.models import (
    GetChargeback,
    GetPaymentLink,
    GetRefund,
    GetSettlement,
    GetVoid,
    PaymentLink,
    Refund,
    Settlement,
    UpdatePaymentLink,
    Void,
)


class TestRefund:
    """Tests for Refund model."""

    def test_refund_creation_valid(self):
        """Test creating a valid refund."""
        payment_id = "pay_12345"
        refund_data = {"amount": "10.50", "description": "Customer return"}

        refund = Refund(payment_id, **refund_data)
        assert refund.get_payment_id() == payment_id
        assert refund.get_amount() == "10.50"
        assert refund.get_description() == "Customer return"
        assert refund.get_endpoint() == f"/payments/{payment_id}/refunds"
        assert refund.get_method() == "POST"

    def test_refund_invalid_amount(self):
        """Test refund with invalid amount."""
        payment_id = "pay_12345"
        refund_data = {"amount": "invalid", "description": "Test refund"}

        with pytest.raises(ValidationError):
            Refund(payment_id, **refund_data)

    def test_refund_missing_amount(self):
        """Test refund with missing amount."""
        payment_id = "pay_12345"
        refund_data = {"description": "Test refund"}

        with pytest.raises(ValidationError):
            Refund(payment_id, **refund_data)


class TestGetRefund:
    """Tests for GetRefund model."""

    def test_get_refund_single(self):
        """Test getting a single refund."""
        payment_id = "pay_12345"
        refund_id = "ref_67890"

        get_refund = GetRefund(payment_id, refund_id)
        assert get_refund.get_payment_id() == payment_id
        assert get_refund.get_refund_id() == refund_id
        assert (
            get_refund.get_endpoint() == f"/payments/{payment_id}/refunds/{refund_id}"
        )
        assert get_refund.get_method() == "GET"
        assert get_refund.is_listing() is False

    def test_get_refund_list(self):
        """Test getting all refunds for a payment."""
        payment_id = "pay_12345"

        get_refund = GetRefund(payment_id)
        assert get_refund.get_payment_id() == payment_id
        assert get_refund.get_refund_id() is None
        assert get_refund.get_endpoint() == f"/payments/{payment_id}/refunds/"
        assert get_refund.get_method() == "GET"
        assert get_refund.is_listing() is True


class TestSettlement:
    """Tests for Settlement model."""

    def test_settlement_creation_valid(self):
        """Test creating a valid settlement."""
        payment_id = "pay_12345"
        settlement_data = {"amount": "25.75", "description": "Partial settlement"}

        settlement = Settlement(payment_id, **settlement_data)
        assert settlement.get_payment_id() == payment_id
        assert settlement.get_amount() == "25.75"
        assert settlement.get_description() == "Partial settlement"
        assert settlement.get_endpoint() == f"/payments/{payment_id}/settlements"
        assert settlement.get_method() == "POST"

    def test_settlement_invalid_amount(self):
        """Test settlement with invalid amount."""
        payment_id = "pay_12345"
        settlement_data = {"amount": "invalid", "description": "Test settlement"}

        with pytest.raises(ValidationError):
            Settlement(payment_id, **settlement_data)


class TestGetSettlement:
    """Tests for GetSettlement model."""

    def test_get_settlement_single(self):
        """Test getting a single settlement."""
        payment_id = "pay_12345"
        settlement_id = "set_67890"

        get_settlement = GetSettlement(payment_id, settlement_id)
        assert get_settlement.get_payment_id() == payment_id
        assert get_settlement.get_settlement_id() == settlement_id
        assert (
            get_settlement.get_endpoint()
            == f"/payments/{payment_id}/settlements/{settlement_id}"
        )
        assert get_settlement.get_method() == "GET"
        assert get_settlement.is_listing() is False

    def test_get_settlement_list(self):
        """Test getting all settlements for a payment."""
        payment_id = "pay_12345"

        get_settlement = GetSettlement(payment_id)
        assert get_settlement.get_payment_id() == payment_id
        assert get_settlement.get_settlement_id() is None
        assert get_settlement.get_endpoint() == f"/payments/{payment_id}/settlements/"
        assert get_settlement.get_method() == "GET"
        assert get_settlement.is_listing() is True


class TestVoid:
    """Tests for Void model."""

    def test_void_creation_valid(self):
        """Test creating a valid void."""
        payment_id = "pay_12345"

        void = Void(payment_id, description="Customer cancellation")
        assert void.get_payment_id() == payment_id
        assert void.get_description() == "Customer cancellation"
        assert void.get_endpoint() == f"/payments/{payment_id}/voids"
        assert void.get_method() == "POST"

    def test_void_creation_minimal(self):
        """Test creating a void with minimal data."""
        payment_id = "pay_12345"

        void = Void(payment_id)
        assert void.get_payment_id() == payment_id
        assert void.get_description() == ""
        assert void.get_endpoint() == f"/payments/{payment_id}/voids"
        assert void.get_method() == "POST"

    def test_void_with_empty_data(self):
        """Test creating a void with empty data dict."""
        payment_id = "pay_12345"

        void = Void(payment_id)
        assert void.get_payment_id() == payment_id
        assert void.get_description() == ""


class TestGetVoid:
    """Tests for GetVoid model."""

    def test_get_void_single(self):
        """Test getting a single void."""
        payment_id = "pay_12345"
        void_id = "void_67890"

        get_void = GetVoid(payment_id, void_id)
        assert get_void.get_payment_id() == payment_id
        assert get_void.get_void_id() == void_id
        assert get_void.get_endpoint() == f"/payments/{payment_id}/voids/{void_id}"
        assert get_void.get_method() == "GET"
        assert get_void.is_listing() is False

    def test_get_void_list(self):
        """Test getting all voids for a payment."""
        payment_id = "pay_12345"

        get_void = GetVoid(payment_id)
        assert get_void.get_payment_id() == payment_id
        assert get_void.get_void_id() is None
        assert get_void.get_endpoint() == f"/payments/{payment_id}/voids/"
        assert get_void.get_method() == "GET"
        assert get_void.is_listing() is True


class TestGetChargeback:
    """Tests for GetChargeback model."""

    def test_get_chargeback_global_with_limit(self):
        """Test getting global chargebacks with limit."""
        limit = 10

        get_chargeback = GetChargeback(limit)
        assert get_chargeback.get_limit() == limit
        assert get_chargeback.get_payment_id() is None
        assert get_chargeback.get_chargeback_id() is None
        assert get_chargeback.get_endpoint() == f"/payments/chargebacks?limit={limit}"
        assert get_chargeback.get_method() == "GET"
        assert get_chargeback.is_global_listing() is True
        assert get_chargeback.is_payment_specific() is False

    def test_get_chargeback_global_without_limit(self):
        """Test getting all global chargebacks."""
        get_chargeback = GetChargeback()
        assert get_chargeback.get_limit() is None
        assert get_chargeback.get_payment_id() is None
        assert get_chargeback.get_chargeback_id() is None
        assert get_chargeback.get_endpoint() == "/payments/chargebacks"
        assert get_chargeback.get_method() == "GET"
        assert get_chargeback.is_global_listing() is True
        assert get_chargeback.is_payment_specific() is False

    def test_get_chargeback_payment_specific_single(self):
        """Test getting a specific chargeback for a payment."""
        payment_id = "pay_12345"
        chargeback_id = "cb_67890"

        get_chargeback = GetChargeback(payment_id, chargeback_id)
        assert get_chargeback.get_payment_id() == payment_id
        assert get_chargeback.get_chargeback_id() == chargeback_id
        assert get_chargeback.get_limit() is None
        assert (
            get_chargeback.get_endpoint()
            == f"/payments/{payment_id}/chargebacks/{chargeback_id}"
        )
        assert get_chargeback.get_method() == "GET"
        assert get_chargeback.is_global_listing() is False
        assert get_chargeback.is_payment_specific() is True
        assert get_chargeback.is_single_chargeback() is True

    def test_get_chargeback_payment_specific_list(self):
        """Test getting all chargebacks for a specific payment."""
        payment_id = "pay_12345"

        get_chargeback = GetChargeback(payment_id)
        assert get_chargeback.get_payment_id() == payment_id
        assert get_chargeback.get_chargeback_id() is None
        assert get_chargeback.get_limit() is None
        assert get_chargeback.get_endpoint() == f"/payments/{payment_id}/chargebacks/"
        assert get_chargeback.get_method() == "GET"
        assert get_chargeback.is_global_listing() is False
        assert get_chargeback.is_payment_specific() is True
        assert get_chargeback.is_single_chargeback() is False


class TestPaymentLink:
    """Tests for PaymentLink model."""

    def test_payment_link_creation_valid(self):
        """Test creating a valid payment link."""
        link_data = {
            "amount": "50.00",
            "currency": "EUR",
            "country": "LT",
            "description": "Test payment link",
            "multiple_use": True,
        }

        payment_link = PaymentLink(link_data)
        assert payment_link.get_amount() == "50.00"
        assert payment_link.get_currency() == "EUR"
        assert payment_link.get_country() == "LT"
        assert payment_link.get_description() == "Test payment link"
        assert payment_link.is_multiple_use() is True
        assert payment_link.get_endpoint() == "/paymentLinks"
        assert payment_link.get_method() == "POST"

    def test_payment_link_with_expiration_date_string(self):
        """Test payment link with expiration date as string."""
        link_data = {
            "amount": "30.00",
            "currency": "USD",
            "country": "US",
            "description": "Test payment link",
            "expiration_date": "2024-12-31T23:59:59Z",
        }

        payment_link = PaymentLink(link_data)
        assert payment_link.get_expiration_date() == "2024-12-31T23:59:59Z"

    def test_payment_link_with_expiration_date_datetime(self):
        """Test payment link with expiration date as datetime object."""
        expiration = datetime(2024, 12, 31, 23, 59, 59)
        link_data = {
            "amount": "30.00",
            "currency": "USD",
            "country": "US",
            "description": "Test payment link",
            "expiration_date": expiration,
        }

        payment_link = PaymentLink(link_data)
        assert payment_link.get_expiration_date() == "2024-12-31T23:59:59Z"

    def test_payment_link_invalid_amount(self):
        """Test payment link with invalid amount."""
        link_data = {
            "amount": "invalid",
            "currency": "EUR",
            "country": "LT",
            "description": "Test payment link",
        }

        with pytest.raises(ValidationError):
            PaymentLink(link_data)

    def test_payment_link_missing_required_fields(self):
        """Test payment link with missing required fields."""
        link_data = {"amount": "30.00"}  # Missing currency, country, description

        with pytest.raises(ValidationError):
            PaymentLink(link_data)


class TestUpdatePaymentLink:
    """Tests for UpdatePaymentLink model."""

    def test_update_payment_link_valid(self):
        """Test updating a payment link."""
        link_id = "link_12345"
        update_data = {
            "expiration_date": "2024-12-31T23:59:59Z",
            "enabled": False,
        }

        update_link = UpdatePaymentLink(link_id, update_data)
        assert update_link.get_link_id() == link_id
        assert update_link.get_expiration_date() == "2024-12-31T23:59:59Z"
        assert update_link.is_enabled() is False
        assert update_link.get_endpoint() == f"/paymentLinks/{link_id}"
        assert update_link.get_method() == "PATCH"

    def test_update_payment_link_with_datetime(self):
        """Test updating payment link with datetime object."""
        link_id = "link_12345"
        expiration = datetime(2024, 12, 31, 23, 59, 59)
        update_data = {"expiration_date": expiration, "enabled": True}

        update_link = UpdatePaymentLink(link_id, update_data)
        assert update_link.get_expiration_date() == "2024-12-31T23:59:59Z"
        assert update_link.is_enabled() is True

    def test_update_payment_link_minimal(self):
        """Test updating payment link with minimal data."""
        link_id = "link_12345"
        update_data = {"enabled": True}

        update_link = UpdatePaymentLink(link_id, update_data)
        assert update_link.get_link_id() == link_id
        assert update_link.get_expiration_date() is None
        assert update_link.is_enabled() is True


class TestGetPaymentLink:
    """Tests for GetPaymentLink model."""

    def test_get_payment_link(self):
        """Test getting a payment link."""
        link_id = "link_12345"

        get_link = GetPaymentLink(link_id)
        assert get_link.get_link_id() == link_id
        assert get_link.get_endpoint() == f"/paymentLinks/{link_id}"
        assert get_link.get_method() == "GET"
