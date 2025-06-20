"""
Test data fixtures for Cardinity SDK testing.

This module contains test data based on Cardinity's official testing guidelines.
See: https://developers.cardinity.com/api/v1/?javascript#oauth-parameters
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict


class CardinityTestCredentials:
    """Test credentials provided by Cardinity for sandbox testing."""

    CONSUMER_KEY = "test_jlol6sogrlvje2zwwsfb6kjajuyy7h"
    CONSUMER_SECRET = "1h7j6rvwlpvuwbzrobo6bjbcqv1m3khnlqojpkkwh9wzbrlkmu"
    BASE_URL = "https://api.cardinity.com/v1"  # Same endpoint as production


class TestCards:
    """Test card numbers provided by Cardinity for testing different scenarios."""

    # Standard test cards that should pass
    VISA_SUCCESS = "4111111111111111"
    VISA_SUCCESS_ALT = "4222222222222"
    MASTERCARD_SUCCESS = "5555555555554444"

    # 3D Secure test cards
    VISA_3DS_FAILED = "4200000000000000"  # 3D-Secure enrolled, authorization failed
    MASTERCARD_3DS_PASSED = (
        "5454545454545454"  # 3D-Secure enrolled, authorization passed
    )
    MASTERCARD_3DS_FAILED = "5454545454540109"  # 3D-Secure authorization failed

    # Special behavior cards
    MASTERCARD_MERCHANT_ADVICE = "5454545454540018"  # Returns merchant_advice_code

    # Invalid cards for failure testing
    INVALID_LUHN = "4242424242424241"  # Fails Luhn check


class TestAmounts:
    """Test amounts for different scenarios."""

    SUCCESS_AMOUNT = "50.00"  # < 150.00, should be approved
    LARGE_SUCCESS_AMOUNT = "149.99"  # Just under limit
    DECLINED_AMOUNT = "150.01"  # > 150.00, should be declined
    INVALID_SMALL_AMOUNT = "0.49"  # < 0.50, should be invalid
    MINIMUM_VALID_AMOUNT = "0.50"  # Minimum valid amount


class TestPaymentInstruments:
    """Test payment instrument data for different scenarios."""

    @staticmethod
    def valid_visa() -> Dict[str, Any]:
        """Valid Visa card data."""
        return {
            "pan": TestCards.VISA_SUCCESS,
            "exp_month": 12,
            "exp_year": 2025,
            "cvc": "123",
            "holder": "John Doe",
        }

    @staticmethod
    def valid_mastercard() -> Dict[str, Any]:
        """Valid MasterCard data."""
        return {
            "pan": TestCards.MASTERCARD_SUCCESS,
            "exp_month": 6,
            "exp_year": 2026,
            "cvc": "456",
            "holder": "Jane Smith",
        }

    @staticmethod
    def visa_3ds_failed() -> Dict[str, Any]:
        """Visa card that will fail 3DS authorization."""
        return {
            "pan": TestCards.VISA_3DS_FAILED,
            "exp_month": 8,
            "exp_year": 2025,
            "cvc": "789",
            "holder": "Test User",
        }

    @staticmethod
    def mastercard_3ds_passed() -> Dict[str, Any]:
        """MasterCard that will pass 3DS authorization."""
        return {
            "pan": TestCards.MASTERCARD_3DS_PASSED,
            "exp_month": 3,
            "exp_year": 2027,
            "cvc": "321",
            "holder": "Secure User",
        }

    @staticmethod
    def invalid_luhn() -> Dict[str, Any]:
        """Card with invalid Luhn checksum."""
        return {
            "pan": TestCards.INVALID_LUHN,
            "exp_month": 12,
            "exp_year": 2025,
            "cvc": "123",
            "holder": "Invalid Card",
        }

    @staticmethod
    def invalid_month() -> Dict[str, Any]:
        """Card with invalid expiry month."""
        return {
            "pan": TestCards.VISA_SUCCESS,
            "exp_month": 13,  # Invalid month
            "exp_year": 2025,
            "cvc": "123",
            "holder": "Invalid Month",
        }

    @staticmethod
    def expired_year() -> Dict[str, Any]:
        """Card with expired year."""
        return {
            "pan": TestCards.VISA_SUCCESS,
            "exp_month": 12,
            "exp_year": 2020,  # Past year
            "cvc": "123",
            "holder": "Expired Card",
        }

    @staticmethod
    def invalid_cvc() -> Dict[str, Any]:
        """Card with invalid CVC."""
        return {
            "pan": TestCards.VISA_SUCCESS,
            "exp_month": 12,
            "exp_year": 2025,
            "cvc": "99",  # Invalid 2-digit CVC
            "holder": "Invalid CVC",
        }


class Test3DSData:
    """Test data for 3D Secure v2 flows."""

    @staticmethod
    def browser_info() -> Dict[str, Any]:
        """Standard browser info for 3DS v2."""
        return {
            "accept_header": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "browser_language": "en-US",
            "screen_height": 1040,
            "screen_width": 1920,
            "challenge_window_size": "500x600",
            "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0",
            "color_depth": 24,
            "time_zone": -60,
            "ip_address": "216.58.207.35",
            "java_enabled": True,
            "javascript_enabled": True,
        }

    @staticmethod
    def threeds2_data(
        notification_url: str = "https://example.com/3ds-callback",
    ) -> Dict[str, Any]:
        """Complete 3DS v2 data."""
        return {
            "notification_url": notification_url,
            "browser_info": Test3DSData.browser_info(),
        }


class TestPaymentData:
    """Complete payment data for different test scenarios."""

    @staticmethod
    def successful_payment() -> Dict[str, Any]:
        """Data for a successful payment."""
        return {
            "amount": TestAmounts.SUCCESS_AMOUNT,
            "currency": "EUR",
            "description": "Test successful payment",
            "country": "LT",
            "payment_instrument": TestPaymentInstruments.valid_visa(),
        }

    @staticmethod
    def successful_mastercard_payment() -> Dict[str, Any]:
        """Data for a successful MasterCard payment."""
        return {
            "amount": TestAmounts.SUCCESS_AMOUNT,
            "currency": "USD",
            "description": "Test MasterCard payment",
            "country": "US",
            "payment_instrument": TestPaymentInstruments.valid_mastercard(),
        }

    @staticmethod
    def declined_payment() -> Dict[str, Any]:
        """Data for a payment that should be declined."""
        return {
            "amount": TestAmounts.DECLINED_AMOUNT,
            "currency": "EUR",
            "description": "Test declined payment",
            "country": "LT",
            "payment_instrument": TestPaymentInstruments.valid_visa(),
        }

    @staticmethod
    def payment_3ds_v2_pass() -> Dict[str, Any]:
        """Data for 3DS v2 payment that should pass."""
        return {
            "amount": TestAmounts.SUCCESS_AMOUNT,
            "currency": "EUR",
            "description": "3ds2-pass",  # Special description for 3DS testing
            "country": "LT",
            "payment_instrument": TestPaymentInstruments.mastercard_3ds_passed(),
            "threeds2_data": Test3DSData.threeds2_data(),
        }

    @staticmethod
    def payment_3ds_v2_fail() -> Dict[str, Any]:
        """Data for 3DS v2 payment that should fail."""
        return {
            "amount": TestAmounts.SUCCESS_AMOUNT,
            "currency": "EUR",
            "description": "3ds2-fail",  # Special description for 3DS testing
            "country": "LT",
            "payment_instrument": TestPaymentInstruments.visa_3ds_failed(),
            "threeds2_data": Test3DSData.threeds2_data(),
        }

    @staticmethod
    def recurring_payment_data(payment_id: str) -> Dict[str, Any]:
        """Data for recurring payment."""
        return {
            "amount": "25.00",
            "currency": "EUR",
            "description": "Monthly subscription",
            "country": "LT",
            "payment_instrument": {"payment_id": payment_id},
        }


class TestRefundData:
    """Test data for refund operations."""

    @staticmethod
    def successful_refund() -> Dict[str, Any]:
        """Data for successful refund."""
        return {"amount": "25.00", "description": "Customer requested refund"}

    @staticmethod
    def failed_refund() -> Dict[str, Any]:
        """Data for refund that should fail."""
        return {
            "amount": "10.00",
            "description": "fail",  # Special description to trigger failure
        }


class TestSettlementData:
    """Test data for settlement operations."""

    @staticmethod
    def successful_settlement() -> Dict[str, Any]:
        """Data for successful settlement."""
        return {"amount": "50.00", "description": "Full settlement"}

    @staticmethod
    def failed_settlement() -> Dict[str, Any]:
        """Data for settlement that should fail."""
        return {
            "amount": "25.00",
            "description": "fail",  # Special description to trigger failure
        }


class TestVoidData:
    """Test data for void operations."""

    @staticmethod
    def successful_void() -> Dict[str, Any]:
        """Data for successful void."""
        return {"description": "Customer cancelled order"}

    @staticmethod
    def failed_void() -> Dict[str, Any]:
        """Data for void that should fail."""
        return {
            "description": "fail"  # Special description to trigger failure
        }


class TestPaymentLinkData:
    """Test data for payment link operations."""

    @staticmethod
    def payment_link() -> Dict[str, Any]:
        """Data for creating payment link."""
        return {
            "amount": "75.00",
            "currency": "EUR",
            "description": "Test payment link",
            "country": "LT",
            "multiple_use": True,
        }

    @staticmethod
    def single_use_payment_link() -> Dict[str, Any]:
        """Data for single-use payment link."""
        return {
            "amount": "100.00",
            "currency": "USD",
            "description": "Single use payment link",
            "country": "US",
            "expiration_date": (
                datetime.now(timezone.utc) + timedelta(days=1)
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "multiple_use": False,
        }

    @staticmethod
    def payment_link_update() -> Dict[str, Any]:
        """Data for updating payment link."""
        return {
            "enabled": False,
            "expiration_date": (
                datetime.now(timezone.utc) + timedelta(days=14)
            ).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
