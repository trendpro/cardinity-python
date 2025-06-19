"""
Integration tests for SDK workflows.

These tests verify that the complete workflows work end-to-end,
using mocked HTTP responses to simulate real API interactions.
"""

from unittest.mock import patch

import pytest

from cardinity import Cardinity
from cardinity.exceptions import APIError, ValidationError


class TestSDKWorkflows:
    """Integration tests for complete SDK workflows."""

    def setup_method(self):
        """Set up test fixtures."""
        self.cardinity = Cardinity("test_key", "test_secret")

    @patch("cardinity.client.CardinityClient._request")
    def test_complete_payment_workflow(self, mock_request):
        """Test complete payment workflow: create -> get -> finalize."""
        # Mock responses for each step
        mock_request.side_effect = [
            # Create payment response
            {
                "id": "pay_123",
                "status": "pending",
                "amount": "10.50",
                "currency": "EUR",
                "authorization_information": {
                    "url": "https://3ds.example.com",
                    "data": "auth_data_123",
                },
            },
            # Get payment response
            {
                "id": "pay_123",
                "status": "pending",
                "amount": "10.50",
                "currency": "EUR",
            },
            # Finalize payment response
            {"id": "pay_123", "status": "approved", "amount": "10.50"},
        ]

        # Step 1: Create payment
        payment_result = self.cardinity.create_payment(
            amount="10.50",
            currency="EUR",
            description="Test payment",
            payment_instrument={
                "pan": "4111111111111111",
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123",
                "holder": "John Doe",
            },
            country="LT",
        )

        assert payment_result["id"] == "pay_123"
        assert payment_result["status"] == "pending"

        # Step 2: Get payment details
        payment_details = self.cardinity.get_payment("pay_123")
        assert payment_details["id"] == "pay_123"
        assert payment_details["status"] == "pending"

        # Step 3: Finalize payment (3DS v1)
        finalized_payment = self.cardinity.finalize_payment(
            "pay_123", authorize_data="finalized_auth_data"
        )
        assert finalized_payment["status"] == "approved"

        # Verify all requests were made
        assert mock_request.call_count == 3

    @patch("cardinity.client.CardinityClient._request")
    def test_refund_workflow(self, mock_request):
        """Test refund workflow: create refund -> get refund."""
        # Mock responses
        mock_request.side_effect = [
            # Create refund response
            {"id": "ref_123", "amount": "5.25", "status": "approved"},
            # Get refund response
            {"id": "ref_123", "amount": "5.25", "status": "approved"},
        ]

        # Create refund
        refund_result = self.cardinity.create_refund(
            "pay_123", amount="5.25", description="Partial refund"
        )
        assert refund_result["id"] == "ref_123"
        assert refund_result["amount"] == "5.25"

        # Get refund details
        refund_details = self.cardinity.get_refund("pay_123", "ref_123")
        assert refund_details["id"] == "ref_123"

        assert mock_request.call_count == 2

    @patch("cardinity.client.CardinityClient._request")
    def test_settlement_workflow(self, mock_request):
        """Test settlement workflow: create settlement -> get settlement."""
        # Mock responses
        mock_request.side_effect = [
            # Create settlement response
            {"id": "set_123", "amount": "10.50", "status": "approved"},
            # Get settlement response
            {"id": "set_123", "amount": "10.50", "status": "approved"},
        ]

        # Create settlement
        settlement_result = self.cardinity.create_settlement(
            "pay_123", amount="10.50", description="Full settlement"
        )
        assert settlement_result["id"] == "set_123"

        # Get settlement details
        settlement_details = self.cardinity.get_settlement("pay_123", "set_123")
        assert settlement_details["id"] == "set_123"

        assert mock_request.call_count == 2

    @patch("cardinity.client.CardinityClient._request")
    def test_void_workflow(self, mock_request):
        """Test void workflow: create void -> get void."""
        # Mock responses
        mock_request.side_effect = [
            # Create void response
            {"id": "void_123", "status": "approved"},
            # Get void response
            {"id": "void_123", "status": "approved"},
        ]

        # Create void
        void_result = self.cardinity.create_void(
            "pay_123", description="Cancel payment"
        )
        assert void_result["id"] == "void_123"

        # Get void details
        void_details = self.cardinity.get_void("pay_123", "void_123")
        assert void_details["id"] == "void_123"

        assert mock_request.call_count == 2

    @patch("cardinity.client.CardinityClient._request")
    def test_payment_link_workflow(self, mock_request):
        """Test payment link workflow: create -> update -> get."""
        # Mock responses
        mock_request.side_effect = [
            # Create payment link response
            {
                "id": "link_123",
                "url": "https://checkout.cardinity.com/link_123",
                "amount": "50.00",
                "currency": "EUR",
                "enabled": True,
            },
            # Update payment link response
            {"id": "link_123", "enabled": False},
            # Get payment link response
            {
                "id": "link_123",
                "url": "https://checkout.cardinity.com/link_123",
                "enabled": False,
            },
        ]

        # Create payment link
        link_result = self.cardinity.create_payment_link(
            amount="50.00",
            currency="EUR",
            country="LT",
            description="Test payment link",
            multiple_use=True,
        )
        assert link_result["id"] == "link_123"
        assert link_result["enabled"] is True

        # Update payment link
        update_result = self.cardinity.update_payment_link("link_123", enabled=False)
        assert update_result["enabled"] is False

        # Get payment link
        link_details = self.cardinity.get_payment_link("link_123")
        assert link_details["id"] == "link_123"
        assert link_details["enabled"] is False

        assert mock_request.call_count == 3

    @patch("cardinity.client.CardinityClient._request")
    def test_chargeback_retrieval_modes(self, mock_request):
        """Test different chargeback retrieval modes."""
        # Mock responses for different modes
        mock_request.side_effect = [
            # Global chargebacks
            [{"id": "cb_123"}, {"id": "cb_456"}],
            # Global with limit
            [{"id": "cb_123"}],
            # Payment-specific chargebacks
            [{"id": "cb_789"}],
            # Single chargeback
            {"id": "cb_789", "amount": "10.50", "reason": "fraud"},
        ]

        # Test global chargeback listing
        global_chargebacks = self.cardinity.get_chargeback()
        assert len(global_chargebacks) == 2

        # Test global with limit
        limited_chargebacks = self.cardinity.get_chargeback(1)
        assert len(limited_chargebacks) == 1

        # Test payment-specific chargebacks
        payment_chargebacks = self.cardinity.get_chargeback("pay_123")
        assert len(payment_chargebacks) == 1

        # Test single chargeback
        single_chargeback = self.cardinity.get_chargeback("pay_123", "cb_789")
        assert single_chargeback["id"] == "cb_789"

        assert mock_request.call_count == 4

    @patch("cardinity.client.CardinityClient._request")
    def test_recurring_payment_workflow(self, mock_request):
        """Test recurring payment workflow."""
        # Mock responses
        mock_request.side_effect = [
            # Initial payment
            {"id": "pay_123", "status": "approved", "payment_method": "card"},
            # Recurring payment
            {"id": "pay_456", "status": "approved", "payment_method": "recurring"},
        ]

        # Create initial payment (would be done separately)
        initial_payment = self.cardinity.create_payment(
            amount="25.00",
            currency="USD",
            description="Initial payment",
            payment_instrument={
                "pan": "4111111111111111",
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123",
                "holder": "Jane Smith",
            },
            country="US",
        )
        assert initial_payment["id"] == "pay_123"

        # Create recurring payment using the initial payment
        recurring_payment = self.cardinity.create_recurring_payment(
            amount="25.00",
            currency="USD",
            description="Monthly subscription",
            payment_instrument={"payment_id": "12345678-1234-1234-1234-123456789012"},
            country="US",
        )
        assert recurring_payment["id"] == "pay_456"
        assert recurring_payment["payment_method"] == "recurring"

        assert mock_request.call_count == 2

    @patch("cardinity.client.CardinityClient._request")
    def test_error_handling_workflow(self, mock_request):
        """Test error handling across different operations."""
        # Mock error response
        mock_request.side_effect = [
            APIError("Payment failed", status_code=400, response_data={}),
        ]

        # Test that API errors are properly propagated
        with pytest.raises(APIError) as exc_info:
            self.cardinity.create_payment(
                amount="10.50",
                currency="EUR",
                description="Test payment",
                country="LT",
                payment_instrument={
                    "pan": "4111111111111111",
                    "exp_month": 12,
                    "exp_year": 2025,
                    "cvc": "123",
                    "holder": "Test User",
                },
            )

        assert exc_info.value.status_code == 400
        assert "Payment failed" in str(exc_info.value)

    def test_validation_error_workflow(self):
        """Test validation error handling."""
        # Test that validation errors are raised for invalid data
        with pytest.raises(ValidationError):
            self.cardinity.create_payment(
                amount="invalid",  # Invalid amount format
                currency="EUR",
                description="Test payment",
            )

        with pytest.raises(ValidationError):
            self.cardinity.create_payment_link(
                amount="50.00",
                currency="INVALID",  # Invalid currency
                country="LT",
                description="Test link",
            )

    @patch("cardinity.client.CardinityClient._request")
    def test_3ds_v2_workflow(self, mock_request):
        """Test 3D Secure v2 workflow."""
        # Mock responses
        mock_request.side_effect = [
            # Create payment with 3DS v2
            {
                "id": "pay_123",
                "status": "pending",
                "authorization_information": {
                    "url": "https://3ds2.example.com",
                    "data": "3ds2_data",
                },
            },
            # Finalize with cres
            {"id": "pay_123", "status": "approved"},
        ]

        # Create payment with 3DS v2 data
        payment_result = self.cardinity.create_payment(
            amount="15.75",
            currency="EUR",
            description="3DS v2 test",
            payment_instrument={
                "pan": "4111111111111111",
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123",
                "holder": "Test User",
            },
            threeds2_data={
                "notification_url": "https://example.com/notify",
                "browser_info": {
                    "accept_header": "text/html",
                    "language": "en-US",
                    "screen_height": 1080,
                    "screen_width": 1920,
                    "user_agent": "Mozilla/5.0...",
                    "java_enabled": False,
                    "javascript_enabled": True,
                    "time_zone": -120,
                    "color_depth": 24,
                },
            },
            country="LT",
        )
        assert payment_result["status"] == "pending"

        # Finalize with 3DS v2 cres
        finalized = self.cardinity.finalize_payment(
            "pay_123", cres="cres_response_data"
        )
        assert finalized["status"] == "approved"

        assert mock_request.call_count == 2
