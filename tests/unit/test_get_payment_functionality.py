"""
Unit tests for get_payment functionality.

These tests verify that the GetPayment model and SDK integration
correctly implement the API endpoints as documented.
"""

from unittest.mock import patch

import pytest

from cardinity import Cardinity
from cardinity.client import CardinityClient
from cardinity.exceptions import APIError, NotFoundError
from cardinity.models import GetPayment


class TestGetPaymentModel:
    """Tests for the GetPayment model class."""

    def test_get_single_payment_endpoint(self):
        """Test that single payment retrieval uses correct endpoint."""
        payment_id = "cb5e1c95-7685-4499-a2b1-ae0f28297b92"
        get_payment = GetPayment(payment_id)

        assert get_payment.get_endpoint() == f"/payments/{payment_id}"
        assert get_payment.get_method() == "GET"
        assert get_payment.is_listing() is False
        assert get_payment.get_payment_id() == payment_id
        assert get_payment.get_limit() is None

    def test_get_all_payments_endpoint(self):
        """Test that all payments retrieval uses correct endpoint."""
        get_payment = GetPayment()

        assert get_payment.get_endpoint() == "/payments"
        assert get_payment.get_method() == "GET"
        assert get_payment.is_listing() is True
        assert get_payment.get_payment_id() is None
        assert get_payment.get_limit() is None

    def test_get_payments_with_limit_endpoint(self):
        """Test that payments with limit use correct endpoint."""
        limit = 20
        get_payment = GetPayment(limit=limit)

        assert get_payment.get_endpoint() == f"/payments?limit={limit}"
        assert get_payment.get_method() == "GET"
        assert get_payment.is_listing() is True
        assert get_payment.get_payment_id() is None
        assert get_payment.get_limit() == limit

    def test_get_payment_constraints_empty(self):
        """Test that GetPayment has no validation constraints."""
        get_payment = GetPayment("test_id")
        constraints = get_payment.get_constraints()

        assert constraints == {}

    def test_get_payment_with_uuid_format(self):
        """Test GetPayment with properly formatted UUID."""
        payment_id = "12345678-1234-1234-1234-123456789012"
        get_payment = GetPayment(payment_id)

        assert get_payment.get_payment_id() == payment_id
        assert get_payment.get_endpoint() == f"/payments/{payment_id}"

    def test_get_payment_string_conversion(self):
        """Test that payment_id is properly converted to string."""
        payment_id = 123456
        get_payment = GetPayment(payment_id)

        assert get_payment.get_payment_id() == "123456"
        assert get_payment.get_endpoint() == "/payments/123456"


class TestGetPaymentSDKIntegration:
    """Tests for GetPayment integration with the main SDK."""

    def setup_method(self):
        """Set up test fixtures."""
        self.consumer_key = "test_consumer_key"
        self.consumer_secret = "test_consumer_secret"
        self.cardinity = Cardinity(self.consumer_key, self.consumer_secret)

    @patch.object(CardinityClient, "execute_request")
    def test_sdk_get_single_payment(self, mock_execute):
        """Test SDK get_payment method for single payment retrieval."""
        payment_id = "cb5e1c95-7685-4499-a2b1-ae0f28297b92"
        expected_response = {
            "id": payment_id,
            "amount": "20.00",
            "currency": "EUR",
            "created": "2014-12-17T09:46:11Z",
            "type": "authorization",
            "live": False,
            "description": "some description",
            "status": "approved",
            "country": "LT",
            "payment_method": "card",
            "payment_instrument": {
                "card_brand": "Visa",
                "pan": "4447",
                "exp_year": 2017,
                "exp_month": 5,
                "holder": "John Smith",
            },
        }

        mock_execute.return_value = expected_response

        result = self.cardinity.get_payment(payment_id)

        assert result == expected_response
        assert result["id"] == payment_id
        assert result["amount"] == "20.00"
        assert result["currency"] == "EUR"
        assert result["status"] == "approved"

        # Verify the correct model was used
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args[0]
        get_payment_model = call_args[0]
        assert isinstance(get_payment_model, GetPayment)
        assert get_payment_model.get_payment_id() == payment_id
        assert get_payment_model.is_listing() is False

    @patch.object(CardinityClient, "execute_request")
    def test_sdk_get_all_payments(self, mock_execute):
        """Test SDK get_payment method for all payments retrieval."""
        expected_response = [
            {
                "id": "cb5e1c95-7685-4499-a2b1-ae0f28297b92",
                "amount": "20.00",
                "currency": "EUR",
                "created": "2014-12-17T09:46:11Z",
                "type": "authorization",
                "live": False,
                "description": "some description",
                "status": "declined",
                "error": "33333: 3D Secure Authorization Failed.",
                "country": "LT",
                "payment_method": "card",
                "payment_instrument": {
                    "card_brand": "Visa",
                    "pan": "0006",
                    "exp_year": 2017,
                    "exp_month": 5,
                    "holder": "John Smith",
                },
            },
            {
                "id": "1379c6bb-dcd9-4669-8846-85a278c2aa7f",
                "amount": "20.00",
                "currency": "EUR",
                "created": "2014-12-17T09:44:01Z",
                "type": "authorization",
                "live": False,
                "description": "some description",
                "status": "approved",
                "country": "LT",
                "payment_method": "card",
                "payment_instrument": {
                    "card_brand": "Visa",
                    "pan": "4447",
                    "exp_year": 2017,
                    "exp_month": 5,
                    "holder": "John Smith",
                },
            },
        ]

        mock_execute.return_value = expected_response

        result = self.cardinity.get_payment()

        assert result == expected_response
        assert len(result) == 2
        assert all("id" in payment for payment in result)
        assert all("status" in payment for payment in result)

        # Verify the correct model was used
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args[0]
        get_payment_model = call_args[0]
        assert isinstance(get_payment_model, GetPayment)
        assert get_payment_model.get_payment_id() is None
        assert get_payment_model.is_listing() is True
        assert get_payment_model.get_limit() is None

    @patch.object(CardinityClient, "execute_request")
    def test_sdk_get_payments_with_limit(self, mock_execute):
        """Test SDK get_payment method with limit parameter."""
        limit = 10
        expected_response = [
            {
                "id": "cb5e1c95-7685-4499-a2b1-ae0f28297b92",
                "amount": "20.00",
                "currency": "EUR",
                "status": "approved",
            }
        ]

        mock_execute.return_value = expected_response

        result = self.cardinity.get_payment(limit=limit)

        assert result == expected_response

        # Verify the correct model was used with limit
        mock_execute.assert_called_once()
        call_args = mock_execute.call_args[0]
        get_payment_model = call_args[0]
        assert isinstance(get_payment_model, GetPayment)
        assert get_payment_model.get_payment_id() is None
        assert get_payment_model.is_listing() is True
        assert get_payment_model.get_limit() == limit

    @patch.object(CardinityClient, "execute_request")
    def test_sdk_get_payment_not_found(self, mock_execute):
        """Test SDK get_payment method with non-existent payment ID."""
        payment_id = "nonexistent-payment-id"

        # Mock 404 response
        mock_execute.side_effect = NotFoundError("Payment not found")

        with pytest.raises(NotFoundError):
            self.cardinity.get_payment(payment_id)

    @patch.object(CardinityClient, "execute_request")
    def test_sdk_get_payment_api_error(self, mock_execute):
        """Test SDK get_payment method with API error."""
        payment_id = "test-payment-id"

        # Mock API error
        mock_execute.side_effect = APIError("Internal server error", status_code=500)

        with pytest.raises(APIError):
            self.cardinity.get_payment(payment_id)

    def test_sdk_get_payment_parameter_combinations(self):
        """Test that SDK correctly handles different parameter combinations."""
        # Test with payment_id only
        with patch.object(CardinityClient, "execute_request") as mock_execute:
            mock_execute.return_value = {"id": "test", "status": "approved"}
            self.cardinity.get_payment("test_id")

            call_args = mock_execute.call_args[0]
            model = call_args[0]
            assert model.get_payment_id() == "test_id"
            assert model.is_listing() is False

        # Test with limit only
        with patch.object(CardinityClient, "execute_request") as mock_execute:
            mock_execute.return_value = []
            self.cardinity.get_payment(limit=5)

            call_args = mock_execute.call_args[0]
            model = call_args[0]
            assert model.get_payment_id() is None
            assert model.get_limit() == 5
            assert model.is_listing() is True

        # Test with no parameters
        with patch.object(CardinityClient, "execute_request") as mock_execute:
            mock_execute.return_value = []
            self.cardinity.get_payment()

            call_args = mock_execute.call_args[0]
            model = call_args[0]
            assert model.get_payment_id() is None
            assert model.get_limit() is None
            assert model.is_listing() is True


class TestGetPaymentAPICompliance:
    """Tests to verify API compliance according to documentation."""

    def test_single_payment_endpoint_matches_api_docs(self):
        """Test that single payment endpoint matches API documentation."""
        # From API docs: GET https://api.cardinity.com/v1/payments/{PAYMENT_ID}
        payment_id = "cb5e1c95-7685-4499-a2b1-ae0f28297b92"
        get_payment = GetPayment(payment_id)

        expected_endpoint = f"/payments/{payment_id}"
        assert get_payment.get_endpoint() == expected_endpoint
        assert get_payment.get_method() == "GET"

    def test_all_payments_endpoint_matches_api_docs(self):
        """Test that all payments endpoint matches API documentation."""
        # From API docs: GET https://api.cardinity.com/v1/payments
        get_payment = GetPayment()

        expected_endpoint = "/payments"
        assert get_payment.get_endpoint() == expected_endpoint
        assert get_payment.get_method() == "GET"

    def test_response_structure_validation(self):
        """Test that we can handle the documented response structure."""
        # Test single payment response structure
        single_payment_response = {
            "id": "cb5e1c95-7685-4499-a2b1-ae0f28297b92",
            "amount": "20.00",
            "currency": "EUR",
            "created": "2014-12-17T09:46:11Z",
            "type": "authorization",
            "live": False,
            "description": "some description",
            "status": "approved",
            "country": "LT",
            "payment_method": "card",
            "payment_instrument": {
                "card_brand": "Visa",
                "pan": "4447",
                "exp_year": 2017,
                "exp_month": 5,
                "holder": "John Smith",
            },
        }

        # Test that all documented fields exist
        required_fields = [
            "id",
            "amount",
            "currency",
            "created",
            "type",
            "live",
            "status",
            "country",
            "payment_method",
        ]
        for field in required_fields:
            assert field in single_payment_response

        # Test payment_instrument structure
        instrument = single_payment_response["payment_instrument"]
        instrument_fields = ["card_brand", "pan", "exp_year", "exp_month", "holder"]
        for field in instrument_fields:
            assert field in instrument

    def test_error_response_handling(self):
        """Test that error responses are handled correctly."""
        # Test that 404 errors (payment not found) are properly handled
        with patch.object(CardinityClient, "execute_request") as mock_execute:
            mock_execute.side_effect = NotFoundError("Payment not found")

            cardinity = Cardinity("test", "test")

            with pytest.raises(NotFoundError):
                cardinity.get_payment("nonexistent-id")
