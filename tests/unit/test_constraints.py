"""
Unit tests for Cardinity validation constraints.

This module tests the validation constraints functionality.
"""

from cardinity.validation.constraints import (
    CHALLENGE_WINDOW_SIZES,
    SUPPORTED_COUNTRIES,
    SUPPORTED_CURRENCIES,
    Constraints,
)


class TestConstraints:
    """Test the Constraints class methods."""

    def test_amount_constraint(self):
        """Test amount validation constraint."""
        constraint = Constraints.amount()

        assert constraint["type"] == "string"
        assert constraint["required"] is True
        assert constraint["regex"] == r"^\d+\.\d{2}$"
        assert constraint["check_with"] == "validate_amount"

    def test_currency_constraint(self):
        """Test currency validation constraint."""
        constraint = Constraints.currency()

        assert constraint["type"] == "string"
        assert constraint["required"] is True
        assert constraint["minlength"] == 3
        assert constraint["maxlength"] == 3
        assert constraint["allowed"] == SUPPORTED_CURRENCIES
        assert constraint["regex"] == r"^[A-Z]{3}$"

    def test_country_constraint(self):
        """Test country validation constraint."""
        constraint = Constraints.country()

        assert constraint["type"] == "string"
        assert constraint["required"] is True
        assert constraint["minlength"] == 2
        assert constraint["maxlength"] == 2
        assert constraint["allowed"] == SUPPORTED_COUNTRIES
        assert constraint["regex"] == r"^[A-Z]{2}$"

    def test_payment_instrument_constraint(self):
        """Test payment instrument validation constraint."""
        constraint = Constraints.payment_instrument()

        assert constraint["type"] == "dict"
        assert constraint["required"] is True

        schema = constraint["schema"]
        assert "pan" in schema
        assert "exp_month" in schema
        assert "exp_year" in schema
        assert "cvc" in schema
        assert "holder" in schema

        # Test PAN constraints
        assert schema["pan"]["type"] == "string"
        assert schema["pan"]["minlength"] == 12
        assert schema["pan"]["maxlength"] == 20
        assert schema["pan"]["regex"] == r"^\d{12,20}$"

        # Test expiry month constraints
        assert schema["exp_month"]["type"] == "integer"
        assert schema["exp_month"]["min"] == 1
        assert schema["exp_month"]["max"] == 12

        # Test expiry year constraints
        assert schema["exp_year"]["type"] == "integer"
        assert schema["exp_year"]["min"] == 2000
        assert schema["exp_year"]["max"] == 2099

    def test_complete_payment_schema(self):
        """Test complete payment creation schema."""
        schema = Constraints.create_payment_schema()

        required_fields = ["amount", "currency"]
        optional_fields = [
            "description",
            "order_id",
            "payment_instrument",
            "billing_address",
            "threeds2_data",
        ]

        for field in required_fields + optional_fields:
            assert field in schema

    def test_supported_currencies_list(self):
        """Test that supported currencies list is not empty."""
        assert len(SUPPORTED_CURRENCIES) > 0
        assert "EUR" in SUPPORTED_CURRENCIES
        assert "USD" in SUPPORTED_CURRENCIES

    def test_supported_countries_list(self):
        """Test that supported countries list is not empty."""
        assert len(SUPPORTED_COUNTRIES) > 0
        assert "US" in SUPPORTED_COUNTRIES
        assert "GB" in SUPPORTED_COUNTRIES

    def test_challenge_window_sizes(self):
        """Test challenge window sizes for 3DS v2."""
        assert len(CHALLENGE_WINDOW_SIZES) == 5
        assert "01" in CHALLENGE_WINDOW_SIZES
        assert "05" in CHALLENGE_WINDOW_SIZES
