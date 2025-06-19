"""
Unit tests for payment-related models.
"""

import pytest

from cardinity.exceptions import ValidationError
from cardinity.models import FinalizePayment, GetPayment, Payment, RecurringPayment


class TestPayment:
    """Tests for Payment model."""

    def test_payment_creation_valid(self):
        """Test creating a valid payment."""
        payment_data = {
            "amount": "10.50",
            "currency": "EUR",
            "country": "LT",
            "description": "Test payment",
            "order_id": "ORDER123",
            "payment_instrument": {
                "pan": "4111111111111111",
                "exp_year": 2025,
                "exp_month": 12,
                "cvc": "123",
                "holder": "John Doe",
            },
        }

        payment = Payment(**payment_data)
        assert payment.get_amount() == "10.50"
        assert payment.get_currency() == "EUR"
        assert payment.get_endpoint() == "/payments"
        assert payment.get_method() == "POST"

        # Check that payment method is automatically set to 'card'
        api_data = payment.to_dict()
        assert api_data["payment_method"] == "card"

    def test_payment_with_threeds2_data(self):
        """Test payment with 3D Secure v2 data."""
        payment_data = {
            "amount": "25.00",
            "currency": "USD",
            "country": "US",
            "description": "Test 3DS payment",
            "payment_instrument": {
                "pan": "4111111111111111",
                "exp_year": 2025,
                "exp_month": 12,
                "cvc": "123",
                "holder": "Jane Doe",
            },
            "threeds2_data": {
                "notification_url": "https://example.com/notification",
                "browser_info": {
                    "accept_header": "text/html,application/xhtml+xml",
                    "browser_language": "en-US",
                    "screen_width": 1920,
                    "screen_height": 1080,
                    "user_agent": "Mozilla/5.0",
                    "color_depth": 24,
                    "time_zone": -60,
                    "javascript_enabled": True,
                    "java_enabled": False,
                },
            },
        }

        payment = Payment(**payment_data)
        assert payment.has_threeds2_data() is True
        threeds2_data = payment.get_field("threeds2_data")
        assert threeds2_data["notification_url"] == "https://example.com/notification"

    def test_payment_invalid_amount(self):
        """Test payment with invalid amount."""
        payment_data = {
            "amount": "invalid",
            "currency": "EUR",
            "country": "DE",
            "description": "Test payment",
            "payment_instrument": {
                "pan": "4111111111111111",
                "exp_year": 2025,
                "exp_month": 12,
                "cvc": "123",
                "holder": "John Doe",
            },
        }

        with pytest.raises(ValidationError):
            Payment(**payment_data)

    def test_payment_missing_required_field(self):
        """Test payment with missing required field."""
        payment_data = {
            "currency": "EUR",
            "country": "DE",
            "description": "Test payment",
            # Missing amount
            "payment_instrument": {
                "pan": "4111111111111111",
                "exp_year": 2025,
                "exp_month": 12,
                "cvc": "123",
                "holder": "John Doe",
            },
        }

        with pytest.raises(ValidationError):
            Payment(**payment_data)


class TestGetPayment:
    """Tests for GetPayment model."""

    def test_get_payment_by_id(self):
        """Test getting a single payment by ID."""
        payment_id = "pay_12345"
        get_payment = GetPayment(payment_id)

        assert get_payment.get_payment_id() == payment_id
        assert get_payment.get_endpoint() == f"/payments/{payment_id}"
        assert get_payment.get_method() == "GET"
        assert get_payment.is_listing() is False
        assert get_payment.get_limit() is None

    def test_get_payment_list(self):
        """Test getting a list of payments."""
        limit = 10
        get_payment = GetPayment(limit=limit)

        assert get_payment.get_limit() == limit
        assert get_payment.get_endpoint() == f"/payments?limit={limit}"
        assert get_payment.get_method() == "GET"
        assert get_payment.is_listing() is True
        assert get_payment.get_payment_id() is None


class TestFinalizePayment:
    """Tests for FinalizePayment model."""

    def test_finalize_payment_3ds_v1(self):
        """Test finalizing payment with 3D Secure v1."""
        payment_id = "pay_12345"
        authorize_data = "auth_data_123"

        finalize = FinalizePayment(payment_id, authorize_data=authorize_data)

        assert finalize.get_payment_id() == payment_id
        assert finalize.is_threedsv2() is False
        assert finalize.get_authorize_data() == authorize_data
        assert finalize.get_cres() is None
        assert finalize.get_endpoint() == f"/payments/{payment_id}"
        assert finalize.get_method() == "PATCH"

        # Check that only authorize_data is in the output
        api_data = finalize.to_dict()
        assert "authorize_data" in api_data
        assert "cres" not in api_data

    def test_finalize_payment_3ds_v2(self):
        """Test finalizing payment with 3D Secure v2."""
        payment_id = "pay_12345"
        cres = "cres_data_123"

        finalize = FinalizePayment(payment_id, cres=cres)

        assert finalize.get_payment_id() == payment_id
        assert finalize.is_threedsv2() is True
        assert finalize.get_cres() == cres
        assert finalize.get_authorize_data() is None
        assert finalize.get_endpoint() == f"/payments/{payment_id}"
        assert finalize.get_method() == "PATCH"

        # Check that only cres is in the output
        api_data = finalize.to_dict()
        assert "cres" in api_data
        assert "authorize_data" not in api_data

    def test_finalize_payment_v1_validation(self):
        """Test finalize payment v1 validation."""
        payment_id = "pay_12345"

        with pytest.raises(ValidationError):
            FinalizePayment(
                payment_id,
                authorize_data="",  # Empty string should fail
            )

    def test_finalize_payment_v2_validation(self):
        """Test finalize payment v2 validation."""
        payment_id = "pay_12345"

        with pytest.raises(ValidationError):
            FinalizePayment(
                payment_id,
                cres="",  # Empty string should fail
            )


class TestRecurringPayment:
    """Tests for RecurringPayment model."""

    def test_recurring_payment_creation(self):
        """Test creating a recurring payment."""
        payment_data = {
            "amount": "15.75",
            "currency": "GBP",
            "country": "GB",
            "description": "Recurring payment",
            "order_id": "REC_ORDER123",
            "payment_instrument": {
                "payment_id": "12345678-1234-1234-1234-123456789012"
            },
        }

        recurring = RecurringPayment(**payment_data)
        assert recurring.get_amount() == "15.75"
        assert recurring.get_currency() == "GBP"
        assert recurring.get_description() == "Recurring payment"
        assert recurring.get_order_id() == "REC_ORDER123"
        assert recurring.get_endpoint() == "/payments"
        assert recurring.get_method() == "POST"

        # Check that payment method is automatically set to 'recurring'
        api_data = recurring.to_dict()
        assert api_data["payment_method"] == "recurring"

    def test_recurring_payment_with_payment_instrument(self):
        """Test recurring payment with payment instrument reference."""
        payment_data = {
            "amount": "20.00",
            "currency": "EUR",
            "country": "DE",
            "description": "Subscription payment",
            "payment_instrument": {
                "payment_id": "12345678-1234-1234-1234-123456789012"
            },
        }

        recurring = RecurringPayment(**payment_data)
        payment_instrument = recurring.get_payment_instrument()
        assert (
            payment_instrument["payment_id"] == "12345678-1234-1234-1234-123456789012"
        )

    def test_recurring_payment_settle_flag(self):
        """Test recurring payment settle flag."""
        payment_data = {
            "amount": "10.00",
            "currency": "USD",
            "country": "US",
            "description": "Test payment",
            "settle": False,
        }

        recurring = RecurringPayment(**payment_data)
        assert recurring.is_settle() is False

        # Test default value
        payment_data_default = {
            "amount": "10.00",
            "currency": "USD",
            "country": "US",
            "description": "Test payment",
        }

        recurring_default = RecurringPayment(**payment_data_default)
        assert recurring_default.is_settle() is True

    def test_recurring_payment_invalid_data(self):
        """Test recurring payment with invalid data."""
        payment_data = {
            "amount": "invalid_amount",
            "currency": "INVALID",
            "description": "Test payment",
        }

        with pytest.raises(ValidationError):
            RecurringPayment(**payment_data)
