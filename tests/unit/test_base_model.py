"""
Unit tests for Cardinity base model classes.

This module tests the BaseModel and ReadOnlyModel abstract base classes.
"""

from typing import Any, Dict

import pytest

from cardinity.exceptions import ValidationError
from cardinity.models.base import BaseModel, ReadOnlyModel


class TestModel(BaseModel):
    """Concrete test model for testing BaseModel functionality."""

    def get_constraints(self) -> Dict[str, Any]:
        return {
            "amount": {"type": "string", "required": True},
            "currency": {"type": "string", "required": True},
            "description": {"type": "string", "required": False},
        }

    def get_endpoint(self) -> str:
        return "/test-payments"

    def get_method(self) -> str:
        return "POST"


class TestReadOnlyModel(ReadOnlyModel):
    """Concrete test read-only model for testing ReadOnlyModel functionality."""

    def get_constraints(self) -> Dict[str, Any]:
        return {
            "id": {"type": "string", "required": True},
            "status": {"type": "string", "required": True},
        }

    def get_endpoint(self) -> str:
        return "/test-payments"


class TestBaseModelFunctionality:
    """Test the BaseModel functionality."""

    def test_model_creation_with_valid_data(self):
        """Test creating a model with valid data."""
        model = TestModel(amount="10.50", currency="EUR")

        assert model.get_field("amount") == "10.50"
        assert model.get_field("currency") == "EUR"
        assert model.get_endpoint() == "/test-payments"
        assert model.get_method() == "POST"

    def test_model_creation_with_optional_fields(self):
        """Test creating a model with optional fields."""
        model = TestModel(amount="10.50", currency="EUR", description="Test payment")

        assert model.get_field("amount") == "10.50"
        assert model.get_field("currency") == "EUR"
        assert model.get_field("description") == "Test payment"

    def test_model_creation_missing_required_field(self):
        """Test creating a model with missing required field raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            TestModel(amount="10.50")  # Missing required currency

        assert "Validation failed" in str(exc_info.value)
        assert exc_info.value.errors is not None
        assert "currency" in exc_info.value.errors

    def test_model_creation_with_invalid_data_type(self):
        """Test creating a model with invalid data type."""
        with pytest.raises(ValidationError) as exc_info:
            TestModel(amount=10.50, currency="EUR")  # amount should be string

        assert "Validation failed" in str(exc_info.value)

    def test_to_dict_method(self):
        """Test converting model to dictionary."""
        model = TestModel(amount="10.50", currency="EUR", description="Test")
        data = model.to_dict()

        expected = {"amount": "10.50", "currency": "EUR", "description": "Test"}
        assert data == expected

    def test_get_data_returns_copy(self):
        """Test that get_data returns a copy, not the original."""
        model = TestModel(amount="10.50", currency="EUR")
        data = model.get_data()

        # Modify the returned data
        data["amount"] = "20.00"

        # Original model should be unchanged
        assert model.get_field("amount") == "10.50"

    def test_update_data_with_valid_values(self):
        """Test updating model data with valid values."""
        model = TestModel(amount="10.50", currency="EUR")

        model.update_data(amount="20.00", description="Updated payment")

        assert model.get_field("amount") == "20.00"
        assert model.get_field("currency") == "EUR"  # Should remain unchanged
        assert model.get_field("description") == "Updated payment"

    def test_update_data_with_invalid_values(self):
        """Test updating model data with invalid values raises ValidationError."""
        model = TestModel(amount="10.50", currency="EUR")

        with pytest.raises(ValidationError):
            model.update_data(currency=None)  # Setting required field to None

    def test_get_field_with_existing_field(self):
        """Test getting an existing field value."""
        model = TestModel(amount="10.50", currency="EUR")

        assert model.get_field("amount") == "10.50"
        assert model.get_field("currency") == "EUR"

    def test_get_field_with_default_value(self):
        """Test getting a non-existing field with default value."""
        model = TestModel(amount="10.50", currency="EUR")

        assert model.get_field("description") is None
        assert model.get_field("missing_field", "default") == "default"

    def test_has_field_method(self):
        """Test checking if fields exist."""
        model = TestModel(amount="10.50", currency="EUR")

        assert model.has_field("amount") is True
        assert model.has_field("currency") is True
        assert model.has_field("description") is False
        assert model.has_field("missing_field") is False

    def test_validate_method(self):
        """Test the validate method."""
        # Valid model
        model = TestModel(amount="10.50", currency="EUR")
        errors = model.validate()
        assert errors is None

        # Invalid model (modify internal data to make it invalid)
        model._data["currency"] = None
        errors = model.validate()
        assert errors is not None
        assert "currency" in errors

    def test_is_valid_method(self):
        """Test the is_valid method."""
        model = TestModel(amount="10.50", currency="EUR")
        assert model.is_valid() is True

        # Make model invalid
        model._data["currency"] = None
        assert model.is_valid() is False

    def test_model_equality(self):
        """Test model equality comparison."""
        model1 = TestModel(amount="10.50", currency="EUR")
        model2 = TestModel(amount="10.50", currency="EUR")
        model3 = TestModel(amount="20.00", currency="EUR")
        model4 = TestModel(amount="10.50", currency="USD")

        # Same data = equal
        assert model1 == model2

        # Different data = not equal
        assert model1 != model3
        assert model1 != model4

        # Different types = not equal
        assert model1 != "not a model"
        assert model1 != {"amount": "10.50", "currency": "EUR"}

    def test_model_hash(self):
        """Test model hashing."""
        model1 = TestModel(amount="10.50", currency="EUR")
        model2 = TestModel(amount="10.50", currency="EUR")
        model3 = TestModel(amount="20.00", currency="EUR")

        # Same data should have same hash
        assert hash(model1) == hash(model2)

        # Different data should have different hash (usually)
        assert hash(model1) != hash(model3)

    def test_model_repr(self):
        """Test model string representation."""
        model = TestModel(amount="10.50", currency="EUR")
        repr_str = repr(model)

        assert "TestModel" in repr_str
        assert "amount=10.50" in repr_str

    def test_model_repr_with_id_field(self):
        """Test model repr when model has id field."""

        # Create a model with id field
        class ModelWithId(BaseModel):
            def get_constraints(self) -> Dict[str, Any]:
                return {
                    "id": {"type": "string", "required": True},
                    "amount": {"type": "string", "required": True},
                }

            def get_endpoint(self) -> str:
                return "/test"

            def get_method(self) -> str:
                return "POST"

        model = ModelWithId(id="123", amount="10.50")
        repr_str = repr(model)

        assert "ModelWithId" in repr_str
        assert "id=123" in repr_str
        assert "amount=10.50" in repr_str


class TestReadOnlyModelFunctionality:
    """Test the ReadOnlyModel functionality."""

    def test_readonly_model_creation(self):
        """Test creating a read-only model."""
        model = TestReadOnlyModel(id="payment-123", status="completed")

        assert model.get_field("id") == "payment-123"
        assert model.get_field("status") == "completed"
        assert model.get_method() == "GET"  # Should default to GET

    def test_readonly_model_prevents_updates(self):
        """Test that read-only models prevent data updates."""
        model = TestReadOnlyModel(id="payment-123", status="completed")

        with pytest.raises(ValidationError) as exc_info:
            model.update_data(status="failed")

        assert "read-only" in str(exc_info.value)
        assert "cannot be updated" in str(exc_info.value)

    def test_readonly_model_other_methods_work(self):
        """Test that other methods work normally on read-only models."""
        model = TestReadOnlyModel(id="payment-123", status="completed")

        # These should all work normally
        assert model.to_dict() == {"id": "payment-123", "status": "completed"}
        assert model.get_data() == {"id": "payment-123", "status": "completed"}
        assert model.get_field("id") == "payment-123"
        assert model.has_field("status") is True
        assert model.is_valid() is True

    def test_readonly_model_validation_on_creation(self):
        """Test that validation still works on read-only model creation."""
        with pytest.raises(ValidationError):
            TestReadOnlyModel(id="payment-123")  # Missing required status


class TestAbstractMethods:
    """Test that abstract methods must be implemented."""

    def test_cannot_instantiate_base_model_directly(self):
        """Test that BaseModel cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseModel(amount="10.50")

    def test_cannot_instantiate_readonly_model_directly(self):
        """Test that ReadOnlyModel cannot be instantiated directly."""
        with pytest.raises(TypeError):
            ReadOnlyModel(id="123")

    def test_must_implement_get_constraints(self):
        """Test that subclasses must implement get_constraints."""

        class IncompleteModel(BaseModel):
            def get_endpoint(self) -> str:
                return "/test"

            def get_method(self) -> str:
                return "POST"

        with pytest.raises(TypeError):
            IncompleteModel(amount="10.50")

    def test_must_implement_get_endpoint(self):
        """Test that subclasses must implement get_endpoint."""

        class IncompleteModel(BaseModel):
            def get_constraints(self) -> Dict[str, Any]:
                return {"amount": {"type": "string", "required": True}}

            def get_method(self) -> str:
                return "POST"

        with pytest.raises(TypeError):
            IncompleteModel(amount="10.50")

    def test_must_implement_get_method_for_base_model(self):
        """Test that BaseModel subclasses must implement get_method."""

        class IncompleteModel(BaseModel):
            def get_constraints(self) -> Dict[str, Any]:
                return {"amount": {"type": "string", "required": True}}

            def get_endpoint(self) -> str:
                return "/test"

        with pytest.raises(TypeError):
            IncompleteModel(amount="10.50")


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_data_model(self):
        """Test model with no required fields."""

        class EmptyModel(BaseModel):
            def get_constraints(self) -> Dict[str, Any]:
                return {}

            def get_endpoint(self) -> str:
                return "/empty"

            def get_method(self) -> str:
                return "POST"

        model = EmptyModel()
        assert model.to_dict() == {}
        assert model.is_valid() is True

    def test_model_with_complex_validation(self):
        """Test model with complex validation rules."""

        class ComplexModel(BaseModel):
            def get_constraints(self) -> Dict[str, Any]:
                return {
                    "amount": {
                        "type": "string",
                        "required": True,
                        "regex": r"^\d+\.\d{2}$",
                    },
                    "currency": {
                        "type": "string",
                        "required": True,
                        "allowed": ["EUR", "USD", "GBP"],
                    },
                }

            def get_endpoint(self) -> str:
                return "/complex"

            def get_method(self) -> str:
                return "POST"

        # Valid data
        model = ComplexModel(amount="10.50", currency="EUR")
        assert model.is_valid() is True

        # Invalid currency
        with pytest.raises(ValidationError):
            ComplexModel(amount="10.50", currency="JPY")
