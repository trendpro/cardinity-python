"""
Real API integration tests for Cardinity SDK.

These tests use real Cardinity API endpoints with test credentials
to verify complete end-to-end functionality.

Test credentials are provided by Cardinity for sandbox testing.
"""

import time

import pytest

from cardinity import Cardinity
from cardinity.exceptions import APIError
from tests.fixtures.test_data import (
    CardinityTestCredentials,
    TestPaymentData,
    TestPaymentLinkData,
)


class TestRealAPIIntegration:
    """Integration tests using real Cardinity API."""

    def setup_method(self):
        """Set up test fixtures with real credentials."""
        self.cardinity = Cardinity(
            CardinityTestCredentials.CONSUMER_KEY,
            CardinityTestCredentials.CONSUMER_SECRET,
            base_url=CardinityTestCredentials.BASE_URL,
        )

        # Store created resources for cleanup
        self.created_payments = []
        self.created_payment_links = []

    def teardown_method(self):
        """Clean up any created resources."""
        # Note: In test environment, cleanup is automatic
        # but we track resources for reference
        pass

    @pytest.mark.integration
    def test_successful_payment_creation(self):
        """Test creating a successful payment with real API."""
        payment_data = TestPaymentData.successful_payment()

        result = self.cardinity.create_payment(**payment_data)

        assert result is not None
        assert "id" in result
        assert result["status"] in ["approved", "pending"]
        assert result["amount"] == payment_data["amount"]
        assert result["currency"] == payment_data["currency"]

        self.created_payments.append(result["id"])

    @pytest.mark.integration
    def test_successful_mastercard_payment(self):
        """Test creating a successful MasterCard payment."""
        payment_data = TestPaymentData.successful_mastercard_payment()

        result = self.cardinity.create_payment(**payment_data)

        assert result is not None
        assert "id" in result
        assert result["status"] in ["approved", "pending"]
        assert result["currency"] == "USD"

        self.created_payments.append(result["id"])

    @pytest.mark.integration
    def test_declined_payment(self):
        """Test payment that should be declined due to amount > 150.00."""
        payment_data = TestPaymentData.declined_payment()

        result = self.cardinity.create_payment(**payment_data)

        assert result is not None
        assert "id" in result
        assert result["status"] == "declined"

        self.created_payments.append(result["id"])

    @pytest.mark.integration
    def test_get_payment(self):
        """Test retrieving a payment after creation."""
        # Create a payment first
        payment_data = TestPaymentData.successful_payment()
        created_payment = self.cardinity.create_payment(**payment_data)
        payment_id = created_payment["id"]
        self.created_payments.append(payment_id)

        # Retrieve the payment
        retrieved_payment = self.cardinity.get_payment(payment_id)

        assert retrieved_payment["id"] == payment_id
        assert retrieved_payment["amount"] == payment_data["amount"]
        assert retrieved_payment["currency"] == payment_data["currency"]

    @pytest.mark.integration
    def test_get_payments_list(self):
        """Test retrieving a list of payments."""
        result = self.cardinity.get_payment(limit=5)

        assert isinstance(result, list)
        assert len(result) <= 5

        # Verify each payment has required fields
        for payment in result:
            assert "id" in payment
            assert "amount" in payment
            assert "currency" in payment
            assert "status" in payment

    @pytest.mark.integration
    def test_3ds_v2_payment_flow(self):
        """Test complete 3D Secure v2 payment flow."""
        payment_data = TestPaymentData.payment_3ds_v2_pass()

        # Create payment that requires 3DS
        result = self.cardinity.create_payment(**payment_data)

        assert result is not None
        assert "id" in result
        payment_id = result["id"]
        self.created_payments.append(payment_id)

        # Should be pending and have authorization_information
        assert result["status"] == "pending"
        assert "authorization_information" in result

        # Finalize the payment with successful cres
        finalized = self.cardinity.finalize_payment(payment_id, cres="3ds2-pass")

        assert finalized["id"] == payment_id
        assert finalized["status"] == "approved"

    @pytest.mark.integration
    def test_3ds_v2_payment_failure(self):
        """Test 3D Secure v2 payment failure flow."""
        payment_data = TestPaymentData.payment_3ds_v2_fail()

        # Create payment that requires 3DS
        result = self.cardinity.create_payment(**payment_data)

        assert result is not None
        payment_id = result["id"]
        self.created_payments.append(payment_id)

        # Should be pending
        assert result["status"] == "pending"

        # Finalize the payment with failed cres
        finalized = self.cardinity.finalize_payment(payment_id, cres="3ds2-fail")

        assert finalized["id"] == payment_id
        assert finalized["status"] == "declined"

    @pytest.mark.integration
    def test_payment_link_workflow(self):
        """Test complete payment link workflow."""
        # Create a payment link
        link_data = TestPaymentLinkData.payment_link()
        link = self.cardinity.create_payment_link(**link_data)

        assert link is not None
        assert "id" in link
        assert "url" in link
        assert link["amount"] == link_data["amount"]
        assert link["enabled"] is True

        link_id = link["id"]
        self.created_payment_links.append(link_id)

        # Update the payment link
        update_data = TestPaymentLinkData.payment_link_update()
        updated_link = self.cardinity.update_payment_link(link_id, **update_data)

        assert updated_link["id"] == link_id
        assert updated_link["enabled"] is False

        # Retrieve the payment link
        retrieved_link = self.cardinity.get_payment_link(link_id)

        assert retrieved_link["id"] == link_id
        assert retrieved_link["enabled"] is False

    @pytest.mark.integration
    def test_chargeback_retrieval(self):
        """Test chargeback retrieval operations."""
        # Test global chargeback listing
        global_chargebacks = self.cardinity.get_chargeback()
        assert isinstance(global_chargebacks, list)

        # Test global with limit
        limited_chargebacks = self.cardinity.get_chargeback(5)
        assert isinstance(limited_chargebacks, list)
        assert len(limited_chargebacks) <= 5

    @pytest.mark.integration
    def test_oauth_authentication(self):
        """Test OAuth authentication is working correctly."""
        # If we can make any successful API call, OAuth is working
        payments = self.cardinity.get_payment(limit=1)
        assert isinstance(payments, list)

    @pytest.mark.integration
    def test_performance_metrics(self):
        """Test basic performance metrics."""
        start_time = time.time()

        # Create a payment
        payment_data = TestPaymentData.successful_payment()
        result = self.cardinity.create_payment(**payment_data)

        end_time = time.time()
        response_time = end_time - start_time

        # Payment should complete within reasonable time (5 seconds)
        assert response_time < 5.0
        assert result is not None

        self.created_payments.append(result["id"])


class TestAPIErrorScenarios:
    """Tests for various API error scenarios."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cardinity = Cardinity(
            CardinityTestCredentials.CONSUMER_KEY,
            CardinityTestCredentials.CONSUMER_SECRET,
            base_url=CardinityTestCredentials.BASE_URL,
        )

    @pytest.mark.integration
    def test_invalid_credentials(self):
        """Test behavior with invalid credentials."""
        invalid_cardinity = Cardinity(
            "invalid_key", "invalid_secret", base_url=CardinityTestCredentials.BASE_URL
        )

        with pytest.raises(APIError) as exc_info:
            invalid_cardinity.get_payment(limit=1)

        assert exc_info.value.status_code == 401

    @pytest.mark.integration
    def test_nonexistent_payment(self):
        """Test retrieving non-existent payment."""
        fake_payment_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(APIError) as exc_info:
            self.cardinity.get_payment(fake_payment_id)

        assert exc_info.value.status_code == 404


# Test configuration for pytest
@pytest.mark.integration
class TestConfiguration:
    """Test configuration and setup verification."""

    def test_test_credentials_valid(self):
        """Verify test credentials are valid."""
        cardinity = Cardinity(
            CardinityTestCredentials.CONSUMER_KEY,
            CardinityTestCredentials.CONSUMER_SECRET,
            base_url=CardinityTestCredentials.BASE_URL,
        )

        # Should be able to make a basic API call
        result = cardinity.get_payment(limit=1)
        assert isinstance(result, list)

    def test_base_url_configuration(self):
        """Test that base URL is configured correctly."""
        cardinity = Cardinity(
            CardinityTestCredentials.CONSUMER_KEY,
            CardinityTestCredentials.CONSUMER_SECRET,
            base_url="https://api.cardinity.com/v1",
        )

        assert cardinity._client.base_url == "https://api.cardinity.com/v1"
