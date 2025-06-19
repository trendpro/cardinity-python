"""
Unit tests for Cardinity validation functions.

This module tests the validation functions and CardinityValidator class.
"""

from cardinity.validation import (
    CardinityValidator,
    validate_amount_format,
    validate_card_number,
    validate_country_code,
    validate_currency_code,
    validate_data,
    validate_required_fields,
)


class TestValidationFunctions:
    """Test validation functions."""

    def test_validate_amount_format_valid(self):
        """Test valid amount formats."""
        valid_amounts = ["10.50", "0.50", "999.99", "1000.00"]

        for amount in valid_amounts:
            result = validate_amount_format(amount)
            assert result is None, f"Amount {amount} should be valid"

    def test_validate_amount_format_invalid(self):
        """Test invalid amount formats."""
        invalid_amounts = [
            "10.5",  # Wrong decimal places
            "10",  # No decimal places
            "10.500",  # Too many decimal places
            "0.49",  # Below minimum
            "abc",  # Not a number
            123.45,  # Not a string
            None,  # None value
        ]

        for amount in invalid_amounts:
            result = validate_amount_format(amount)
            assert result is not None, f"Amount {amount} should be invalid"

    def test_validate_card_number_valid(self):
        """Test valid card numbers."""
        valid_cards = [
            "4111111111111111",  # 16 digits
            "411111111111",  # 12 digits (minimum)
            "41111111111111111111",  # 20 digits (maximum)
            "4111 1111 1111 1111",  # With spaces
            "4111-1111-1111-1111",  # With dashes
        ]

        for card in valid_cards:
            result = validate_card_number(card)
            assert result is None, f"Card {card} should be valid"

    def test_validate_card_number_invalid(self):
        """Test invalid card numbers."""
        invalid_cards = [
            "411111111",  # Too short
            "411111111111111111111",  # Too long
            "4111-1111-1111-abcd",  # Contains letters
            123456789012,  # Not a string
            None,  # None value
        ]

        for card in invalid_cards:
            result = validate_card_number(card)
            assert result is not None, f"Card {card} should be invalid"

    def test_validate_currency_code_valid(self):
        """Test valid currency codes."""
        valid_currencies = ["EUR", "USD", "GBP"]

        for currency in valid_currencies:
            result = validate_currency_code(currency)
            assert result is None, f"Currency {currency} should be valid"

    def test_validate_currency_code_invalid(self):
        """Test invalid currency codes."""
        invalid_currencies = [
            "eur",  # Lowercase
            "EU",  # Too short
            "EURO",  # Too long
            "E1R",  # Contains number
            123,  # Not a string
            None,  # None value
        ]

        for currency in invalid_currencies:
            result = validate_currency_code(currency)
            assert result is not None, f"Currency {currency} should be invalid"

    def test_validate_country_code_valid(self):
        """Test valid country codes."""
        valid_countries = ["US", "GB", "DE", "FR"]

        for country in valid_countries:
            result = validate_country_code(country)
            assert result is None, f"Country {country} should be valid"

    def test_validate_country_code_invalid(self):
        """Test invalid country codes."""
        invalid_countries = [
            "us",  # Lowercase
            "U",  # Too short
            "USA",  # Too long
            "U1",  # Contains number
            123,  # Not a string
            None,  # None value
        ]

        for country in invalid_countries:
            result = validate_country_code(country)
            assert result is not None, f"Country {country} should be invalid"

    def test_validate_required_fields_valid(self):
        """Test required fields validation with valid data."""
        data = {"amount": "10.50", "currency": "EUR"}
        required = ["amount", "currency"]

        result = validate_required_fields(data, required)
        assert result is None

    def test_validate_required_fields_missing(self):
        """Test required fields validation with missing fields."""
        data = {"amount": "10.50"}
        required = ["amount", "currency"]

        result = validate_required_fields(data, required)
        assert result is not None
        assert "currency" in result
        assert "is required" in result["currency"][0]

    def test_validate_required_fields_empty(self):
        """Test required fields validation with empty fields."""
        data = {"amount": "10.50", "currency": ""}
        required = ["amount", "currency"]

        result = validate_required_fields(data, required)
        assert result is not None
        assert "currency" in result
        assert "cannot be empty" in result["currency"][0]


class TestCardinityValidator:
    """Test the custom Cerberus validator."""

    def test_amount_validation(self):
        """Test custom amount validation."""
        validator = CardinityValidator()

        # Valid amount
        data = {"amount": "10.50"}
        schema = {"amount": {"check_with": "validate_amount"}}
        assert validator.validate(data, schema)

        # Invalid amount (too low)
        data = {"amount": "0.49"}
        assert not validator.validate(data, schema)
        assert "amount" in validator.errors

    def test_payment_id_validation(self):
        """Test custom payment ID validation."""
        validator = CardinityValidator()

        # Valid UUID-like string
        data = {"payment_id": "550e8400-e29b-41d4-a716-446655440000"}
        schema = {"payment_id": {"check_with": "validate_payment_id"}}
        assert validator.validate(data, schema)

        # Invalid payment ID (wrong length)
        data = {"payment_id": "invalid-id"}
        assert not validator.validate(data, schema)
        assert "payment_id" in validator.errors


class TestValidateData:
    """Test the validate_data function."""

    def test_validate_with_missing_required_fields(self):
        """Test validation with missing required fields."""
        schema = {"amount": {"type": "string", "required": True}}
        data = {}

        result = validate_data(data, schema)
        assert result is not None
        assert "amount" in result

    def test_validate_with_valid_data(self):
        """Test validation with valid data."""
        schema = {
            "amount": {"type": "string", "required": True},
            "currency": {"type": "string", "required": True},
        }
        data = {"amount": "10.50", "currency": "EUR"}

        result = validate_data(data, schema)
        assert result is None
