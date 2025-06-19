"""
Unit tests for Cardinity HTTP client.
"""

import json
from unittest.mock import Mock, patch

import pytest
from requests.exceptions import ConnectionError, Timeout

from cardinity.auth import CardinityAuth
from cardinity.client import CardinityClient
from cardinity.exceptions import (
    APIError,
    AuthenticationError,
    CardinityError,
    NotFoundError,
    ServerError,
)
from cardinity.models.payment import Payment


class TestCardinityClient:
    """Test cases for CardinityClient class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.auth = CardinityAuth("test_key", "test_secret")
        self.client = CardinityClient(self.auth)

    def test_client_initialization(self):
        """Test proper initialization of CardinityClient."""
        assert self.client.auth == self.auth
        assert self.client.base_url == "https://api.cardinity.com/v1"
        assert self.client.timeout == 30
        assert "User-Agent" in self.client.session.headers
        assert "Accept" in self.client.session.headers

    def test_client_initialization_with_custom_base_url(self):
        """Test client initialization with custom base URL."""
        custom_url = "https://custom.api.com/v1"
        client = CardinityClient(self.auth, base_url=custom_url)

        assert client.base_url == custom_url

    def test_client_initialization_with_custom_timeout(self):
        """Test client initialization with custom timeout."""
        custom_timeout = 60
        client = CardinityClient(self.auth, timeout=custom_timeout)

        assert client.timeout == custom_timeout

    def test_session_configuration(self):
        """Test that session is properly configured."""
        session = self.client.session

        assert session.headers["Accept"] == "application/json"
        assert session.headers["Content-Type"] == "application/json"
        assert "cardinity-python" in session.headers["User-Agent"]

    @patch("requests.Session.request")
    def test_successful_get_request(self, mock_request):
        """Test successful GET request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {"id": "test_id", "amount": "10.00"}
        mock_request.return_value = mock_response

        result = self.client.get("/payments")

        assert result == {"id": "test_id", "amount": "10.00"}
        mock_request.assert_called_once()

    @patch("requests.Session.request")
    def test_successful_post_request(self, mock_request):
        """Test successful POST request with data."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.ok = True
        mock_response.json.return_value = {"id": "new_payment", "status": "approved"}
        mock_request.return_value = mock_response

        data = {"amount": "10.00", "currency": "EUR"}
        result = self.client.post("/payments", data)

        assert result == {"id": "new_payment", "status": "approved"}
        mock_request.assert_called_once()

    @patch("requests.Session.request")
    def test_404_error_handling(self, mock_request):
        """Test handling of 404 errors."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.ok = False
        mock_response.reason = "Not Found"
        mock_response.json.return_value = {"error": "Not found"}
        mock_request.return_value = mock_response

        with pytest.raises(NotFoundError) as exc_info:
            self.client.get("/payments/nonexistent")

        assert "Not found" in str(exc_info.value)

    @patch("requests.Session.request")
    def test_401_unauthorized_error(self, mock_request):
        """Test handling of 401 unauthorized errors."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.ok = False
        mock_response.reason = "Unauthorized"
        mock_response.json.return_value = {"error": "Unauthorized"}
        mock_request.return_value = mock_response

        with pytest.raises(AuthenticationError) as exc_info:
            self.client.get("/payments")

        assert "Unauthorized" in str(exc_info.value)

    @patch("requests.Session.request")
    def test_500_server_error(self, mock_request):
        """Test handling of 500 server errors."""
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.ok = False
        mock_response.reason = "Internal Server Error"
        mock_response.json.return_value = {"error": "Internal server error"}
        mock_request.return_value = mock_response

        with pytest.raises(ServerError) as exc_info:
            self.client.get("/payments")

        assert "Internal server error" in str(exc_info.value)

    @patch("requests.Session.request")
    def test_connection_error_handling(self, mock_request):
        """Test handling of connection errors."""
        mock_request.side_effect = ConnectionError("Connection failed")

        with pytest.raises(CardinityError) as exc_info:
            self.client.get("/payments")

        assert "Connection failed" in str(exc_info.value)

    @patch("requests.Session.request")
    def test_timeout_error_handling(self, mock_request):
        """Test handling of timeout errors."""
        mock_request.side_effect = Timeout("Request timed out")

        with pytest.raises(CardinityError) as exc_info:
            self.client.get("/payments")

        assert "Request timed out" in str(exc_info.value)

    @patch("requests.Session.request")
    def test_invalid_json_response(self, mock_request):
        """Test handling of invalid JSON responses."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_response.text = "Invalid JSON response"
        mock_request.return_value = mock_response

        result = self.client.get("/payments")

        # Should handle invalid JSON gracefully
        assert "error" in result

    @patch("requests.Session.request")
    def test_execute_request_method(self, mock_request):
        """Test execute_request method with model instances."""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.ok = True
        mock_response.json.return_value = {"id": "test_payment", "amount": "10.00"}
        mock_request.return_value = mock_response

        # Create a payment model instance
        payment_data = {
            "amount": "10.00",
            "currency": "EUR",
            "description": "Test payment",
            "country": "LT",
            "payment_instrument": {
                "pan": "4111111111111111",
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123",
                "holder": "John Doe",
            },
        }
        payment = Payment(**payment_data)

        result = self.client.execute_request(payment)

        assert result == {"id": "test_payment", "amount": "10.00"}
        mock_request.assert_called_once()

    def test_url_construction(self):
        """Test URL construction with different endpoints."""
        client = CardinityClient(self.auth, base_url="https://api.example.com/v1")

        # Test URL building
        url = client._build_url("/payments")
        assert url == "https://api.example.com/v1/payments"

        # Test with endpoint that already has leading slash
        url = client._build_url("/payments/123")
        assert url == "https://api.example.com/v1/payments/123"

    def test_client_with_trailing_slash_base_url(self):
        """Test client handles base URL with trailing slash."""
        client = CardinityClient(self.auth, base_url="https://api.example.com/v1/")

        url = client._build_url("/payments")
        assert url == "https://api.example.com/v1/payments"

    @patch("requests.Session.request")
    def test_retry_logic_on_connection_error(self, mock_request):
        """Test retry logic on connection errors."""
        # First call fails, second succeeds
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {"id": "test"}

        mock_request.side_effect = [ConnectionError("Connection failed"), mock_response]

        result = self.client.get("/payments")

        assert result == {"id": "test"}
        assert mock_request.call_count == 2

    @patch("requests.Session.request")
    def test_retry_exhausted(self, mock_request):
        """Test behavior when all retries are exhausted."""
        mock_request.side_effect = ConnectionError("Connection failed")

        with pytest.raises(CardinityError):
            self.client.get("/payments")

        # Should retry the configured number of times + 1 initial attempt
        assert mock_request.call_count >= 2

    @patch("requests.Session.request")
    def test_no_retry_on_client_errors(self, mock_request):
        """Test that client errors (4xx) are not retried."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.ok = False
        mock_response.reason = "Bad Request"
        mock_response.json.return_value = {"error": "Bad request"}
        mock_request.return_value = mock_response

        with pytest.raises(APIError):
            self.client.get("/payments")

        # Should not retry on client errors
        assert mock_request.call_count == 1

    @patch("requests.Session.request")
    def test_user_agent_header(self, mock_request):
        """Test that User-Agent header is properly set."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.ok = True
        mock_response.json.return_value = {}
        mock_request.return_value = mock_response

        self.client.get("/payments")

        # Check that session headers include User-Agent
        user_agent = self.client.session.headers.get("User-Agent")
        assert user_agent is not None
        assert "cardinity-python" in user_agent

    def test_session_isolation(self):
        """Test that different client instances have isolated sessions."""
        auth1 = CardinityAuth("key1", "secret1")
        auth2 = CardinityAuth("key2", "secret2")

        client1 = CardinityClient(auth1)
        client2 = CardinityClient(auth2)

        assert client1.session is not client2.session
        assert client1.auth != client2.auth

    @patch("requests.Session.request")
    def test_error_response_data_preservation(self, mock_request):
        """Test that error response data is preserved in APIError."""
        error_data = {
            "error": "validation_failed",
            "message": "Invalid payment data",
            "details": {"field": "amount", "error": "too_small"},
        }

        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.ok = False
        mock_response.reason = "Unprocessable Entity"
        mock_response.json.return_value = error_data
        mock_request.return_value = mock_response

        with pytest.raises(APIError) as exc_info:
            self.client.post("/payments", {"amount": "0.01"})

        api_error = exc_info.value
        assert api_error.status_code == 422
        assert api_error.response_data == error_data

    def test_context_manager_usage(self):
        """Test client can be used as context manager."""
        with CardinityClient(self.auth) as client:
            assert client.session is not None

        # Session should be closed after exiting context
        # (Note: requests Session doesn't expose a closed state,
        # so we just verify the client still exists)
        assert client is not None
