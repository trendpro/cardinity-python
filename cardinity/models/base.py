"""
Cardinity Base Model

This module defines the abstract base class for all Cardinity API models.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..exceptions import ValidationError
from ..validation import validate_data


class BaseModel(ABC):
    """Abstract base class for all Cardinity API models.

    This class provides common functionality for data validation, serialization,
    and API endpoint configuration that all model classes inherit.
    """

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the model with data validation.

        Args:
            **kwargs: Model data to validate and store

        Raises:
            ValidationError: If the provided data fails validation
        """
        # Validate the input data against the model's constraints
        validation_errors = validate_data(kwargs, self.get_constraints())
        if validation_errors:
            raise ValidationError(
                f"Validation failed for {self.__class__.__name__}",
                errors=validation_errors,
            )

        # Store the validated data
        self._data = kwargs.copy()

    @abstractmethod
    def get_constraints(self) -> Dict[str, Any]:
        """Get the validation constraints for this model.

        This method must be implemented by each model class to define
        the validation rules for its specific data structure.

        Returns:
            Dict[str, Any]: Cerberus validation schema for this model

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement get_constraints()")

    @abstractmethod
    def get_endpoint(self) -> str:
        """Get the API endpoint for this model's operations.

        This method must be implemented by each model class to define
        which API endpoint should be used for operations.

        Returns:
            str: API endpoint path (e.g., "/payments", "/refunds")

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement get_endpoint()")

    @abstractmethod
    def get_method(self) -> str:
        """Get the HTTP method for this model's primary operation.

        This method must be implemented by each model class to define
        which HTTP method should be used for the primary operation.

        Returns:
            str: HTTP method (e.g., "POST", "GET", "PATCH")

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement get_method()")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary for API serialization.

        This method serializes the model data to a format suitable
        for sending to the Cardinity API.

        Returns:
            Dict[str, Any]: Dictionary representation of the model data
        """
        return self._data.copy()

    def get_data(self) -> Dict[str, Any]:
        """Get the raw model data.

        Returns:
            Dict[str, Any]: Copy of the internal model data
        """
        return self._data.copy()

    def update_data(self, **kwargs: Any) -> None:
        """Update the model data with new values.

        Args:
            **kwargs: New data values to update

        Raises:
            ValidationError: If the updated data fails validation
        """
        # Merge new data with existing data
        updated_data = self._data.copy()
        updated_data.update(kwargs)

        # Validate the updated data
        validation_errors = validate_data(updated_data, self.get_constraints())
        if validation_errors:
            raise ValidationError(
                f"Validation failed for {self.__class__.__name__} update",
                errors=validation_errors,
            )

        # Update the internal data
        self._data = updated_data

    def get_field(self, field_name: str, default: Any = None) -> Any:
        """Get a specific field value from the model data.

        Args:
            field_name: Name of the field to retrieve
            default: Default value if field doesn't exist

        Returns:
            Any: Field value or default
        """
        return self._data.get(field_name, default)

    def has_field(self, field_name: str) -> bool:
        """Check if a field exists in the model data.

        Args:
            field_name: Name of the field to check

        Returns:
            bool: True if field exists, False otherwise
        """
        return field_name in self._data

    def validate(self) -> Optional[Dict[str, Any]]:
        """Validate the current model data against its constraints.

        Returns:
            Optional[Dict[str, Any]]: Validation errors if any, None if valid
        """
        return validate_data(self._data, self.get_constraints())

    def is_valid(self) -> bool:
        """Check if the current model data is valid.

        Returns:
            bool: True if valid, False otherwise
        """
        return self.validate() is None

    def __repr__(self) -> str:
        """Return a string representation of the model.

        Returns:
            str: String representation showing class name and key fields
        """
        key_fields = []

        # Include some common important fields if they exist
        for field in ["id", "amount", "currency", "status", "type"]:
            if self.has_field(field):
                key_fields.append(f"{field}={self.get_field(field)}")

        fields_str = ", ".join(key_fields) if key_fields else "no key fields"
        return f"{self.__class__.__name__}({fields_str})"

    def __eq__(self, other: object) -> bool:
        """Check equality with another model instance.

        Args:
            other: Other object to compare with

        Returns:
            bool: True if equal, False otherwise
        """
        if not isinstance(other, BaseModel):
            return False

        return self.__class__ == other.__class__ and self._data == other._data

    def __hash__(self) -> int:
        """Generate hash for the model instance.

        Returns:
            int: Hash value based on class and data
        """
        # Create a hash based on the class name and a sorted tuple of data items
        data_items = tuple(sorted(self._data.items()))
        return hash((self.__class__.__name__, data_items))


class ReadOnlyModel(BaseModel):
    """Base class for read-only models that don't support data updates.

    This class is used for models that represent data retrieved from the API
    that shouldn't be modified locally (e.g., payment status, transaction history).
    """

    def update_data(self, **kwargs: Any) -> None:
        """Prevent data updates on read-only models.

        Args:
            **kwargs: Ignored

        Raises:
            ValidationError: Always raised for read-only models
        """
        raise ValidationError(
            f"{self.__class__.__name__} is read-only and cannot be updated"
        )

    def get_method(self) -> str:
        """Default HTTP method for read-only models.

        Returns:
            str: Always returns "GET" for read-only models
        """
        return "GET"
