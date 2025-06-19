"""
Unit tests for the main Cardinity SDK class.
"""

from unittest.mock import patch

from cardinity import Cardinity
from cardinity.auth import CardinityAuth
from cardinity.client import CardinityClient


class TestCardinity:
    """Tests for the main Cardinity SDK class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.consumer_key = "test_consumer_key"
        self.consumer_secret = "test_consumer_secret"
        self.cardinity = Cardinity(self.consumer_key, self.consumer_secret)

    def test_initialization(self):
        """Test SDK initialization."""
        assert isinstance(self.cardinity._auth, CardinityAuth)
        assert isinstance(self.cardinity._client, CardinityClient)
        assert self.cardinity._client.base_url == "https://api.cardinity.com/v1"

    def test_initialization_with_custom_base_url(self):
        """Test SDK initialization with custom base URL."""
        custom_url = "https://sandbox.cardinity.com/v1"
        cardinity = Cardinity(
            self.consumer_key, self.consumer_secret, base_url=custom_url
        )
        assert cardinity._client.base_url == custom_url

    @patch.object(CardinityClient, "execute_request")
    def test_create_payment(self, mock_execute):
        """Test create_payment method."""
        mock_execute.return_value = {"id": "pay_123", "status": "pending"}

        result = self.cardinity.create_payment(
            amount="10.50",
            currency="EUR",
            description="Test payment",
            country="LT",
            payment_instrument={
                "pan": "4111111111111111",
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123",
                "holder": "John Doe",
            },
        )

        assert result == {"id": "pay_123", "status": "pending"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_payment_single(self, mock_execute):
        """Test get_payment method for single payment."""
        mock_execute.return_value = {"id": "pay_123", "amount": "10.50"}

        result = self.cardinity.get_payment("pay_123")

        assert result == {"id": "pay_123", "amount": "10.50"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_payment_list(self, mock_execute):
        """Test get_payment method for payment listing."""
        mock_execute.return_value = [{"id": "pay_123"}, {"id": "pay_456"}]

        result = self.cardinity.get_payment(limit=10)

        assert result == [{"id": "pay_123"}, {"id": "pay_456"}]
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_finalize_payment(self, mock_execute):
        """Test finalize_payment method."""
        mock_execute.return_value = {"id": "pay_123", "status": "approved"}

        result = self.cardinity.finalize_payment("pay_123", authorize_data="test_data")

        assert result == {"id": "pay_123", "status": "approved"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_create_recurring_payment(self, mock_execute):
        """Test create_recurring_payment method."""
        mock_execute.return_value = {"id": "pay_456", "status": "approved"}

        result = self.cardinity.create_recurring_payment(
            amount="25.00",
            currency="USD",
            description="Recurring payment",
            country="US",
            payment_instrument={"payment_id": "12345678-1234-1234-1234-123456789012"},
        )

        assert result == {"id": "pay_456", "status": "approved"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_create_refund(self, mock_execute):
        """Test create_refund method."""
        mock_execute.return_value = {"id": "ref_123", "amount": "5.25"}

        result = self.cardinity.create_refund(
            "pay_123", amount="5.25", description="Partial refund"
        )

        assert result == {"id": "ref_123", "amount": "5.25"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_refund_single(self, mock_execute):
        """Test get_refund method for single refund."""
        mock_execute.return_value = {"id": "ref_123", "amount": "5.25"}

        result = self.cardinity.get_refund("pay_123", "ref_123")

        assert result == {"id": "ref_123", "amount": "5.25"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_refund_list(self, mock_execute):
        """Test get_refund method for refund listing."""
        mock_execute.return_value = [{"id": "ref_123"}, {"id": "ref_456"}]

        result = self.cardinity.get_refund("pay_123")

        assert result == [{"id": "ref_123"}, {"id": "ref_456"}]
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_create_settlement(self, mock_execute):
        """Test create_settlement method."""
        mock_execute.return_value = {"id": "set_123", "amount": "10.50"}

        result = self.cardinity.create_settlement(
            "pay_123", amount="10.50", description="Full settlement"
        )

        assert result == {"id": "set_123", "amount": "10.50"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_settlement_single(self, mock_execute):
        """Test get_settlement method for single settlement."""
        mock_execute.return_value = {"id": "set_123", "amount": "10.50"}

        result = self.cardinity.get_settlement("pay_123", "set_123")

        assert result == {"id": "set_123", "amount": "10.50"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_settlement_list(self, mock_execute):
        """Test get_settlement method for settlement listing."""
        mock_execute.return_value = [{"id": "set_123"}]

        result = self.cardinity.get_settlement("pay_123")

        assert result == [{"id": "set_123"}]
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_create_void(self, mock_execute):
        """Test create_void method."""
        mock_execute.return_value = {"id": "void_123", "status": "approved"}

        result = self.cardinity.create_void("pay_123", description="Customer request")

        assert result == {"id": "void_123", "status": "approved"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_create_void_minimal(self, mock_execute):
        """Test create_void method with minimal data."""
        mock_execute.return_value = {"id": "void_123", "status": "approved"}

        result = self.cardinity.create_void("pay_123")

        assert result == {"id": "void_123", "status": "approved"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_void_single(self, mock_execute):
        """Test get_void method for single void."""
        mock_execute.return_value = {"id": "void_123", "status": "approved"}

        result = self.cardinity.get_void("pay_123", "void_123")

        assert result == {"id": "void_123", "status": "approved"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_void_list(self, mock_execute):
        """Test get_void method for void listing."""
        mock_execute.return_value = [{"id": "void_123"}]

        result = self.cardinity.get_void("pay_123")

        assert result == [{"id": "void_123"}]
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_chargeback_global(self, mock_execute):
        """Test get_chargeback method for global listing."""
        mock_execute.return_value = [{"id": "cb_123"}, {"id": "cb_456"}]

        result = self.cardinity.get_chargeback()

        assert result == [{"id": "cb_123"}, {"id": "cb_456"}]
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_chargeback_global_with_limit(self, mock_execute):
        """Test get_chargeback method for global listing with limit."""
        mock_execute.return_value = [{"id": "cb_123"}]

        result = self.cardinity.get_chargeback(10)

        assert result == [{"id": "cb_123"}]
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_chargeback_payment_specific(self, mock_execute):
        """Test get_chargeback method for payment-specific listing."""
        mock_execute.return_value = [{"id": "cb_123"}]

        result = self.cardinity.get_chargeback("pay_123")

        assert result == [{"id": "cb_123"}]
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_chargeback_single(self, mock_execute):
        """Test get_chargeback method for single chargeback."""
        mock_execute.return_value = {"id": "cb_123", "amount": "10.50"}

        result = self.cardinity.get_chargeback("pay_123", "cb_123")

        assert result == {"id": "cb_123", "amount": "10.50"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_create_payment_link(self, mock_execute):
        """Test create_payment_link method."""
        mock_execute.return_value = {"id": "link_123", "url": "https://example.com"}

        result = self.cardinity.create_payment_link(
            amount="50.00",
            currency="EUR",
            country="LT",
            description="Test payment link",
        )

        assert result == {"id": "link_123", "url": "https://example.com"}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_update_payment_link(self, mock_execute):
        """Test update_payment_link method."""
        mock_execute.return_value = {"id": "link_123", "enabled": False}

        result = self.cardinity.update_payment_link("link_123", enabled=False)

        assert result == {"id": "link_123", "enabled": False}
        mock_execute.assert_called_once()

    @patch.object(CardinityClient, "execute_request")
    def test_get_payment_link(self, mock_execute):
        """Test get_payment_link method."""
        mock_execute.return_value = {"id": "link_123", "amount": "50.00"}

        result = self.cardinity.get_payment_link("link_123")

        assert result == {"id": "link_123", "amount": "50.00"}
        mock_execute.assert_called_once()

    def test_get_client(self):
        """Test get_client method."""
        client = self.cardinity.get_client()
        assert isinstance(client, CardinityClient)
        assert client is self.cardinity._client

    def test_get_auth(self):
        """Test get_auth method."""
        auth = self.cardinity.get_auth()
        assert isinstance(auth, CardinityAuth)
        assert auth is self.cardinity._auth
