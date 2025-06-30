"""
Cardinity Python SDK

A Python SDK for the Cardinity payment gateway API.
"""

from .auth import CardinityAuth
from .client import CardinityClient
from .exceptions import (
    APIError,
    AuthenticationError,
    CardinityError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .models import BaseModel, ReadOnlyModel
from .sdk import Cardinity
from .validation import (
    CardinityValidator,
    Constraints,
    validate_amount_format,
    validate_card_number,
    validate_country_code,
    validate_currency_code,
    validate_data,
    validate_required_fields,
)

__version__ = "1.0.2"

__all__ = [
    # Main SDK Interface
    "Cardinity",
    # Core functionality
    "CardinityAuth",
    "CardinityClient",
    # Exceptions
    "CardinityError",
    "ValidationError",
    "APIError",
    "AuthenticationError",
    "NotFoundError",
    "RateLimitError",
    "ServerError",
    # Models
    "BaseModel",
    "ReadOnlyModel",
    # Validation
    "Constraints",
    "CardinityValidator",
    "validate_data",
    "validate_required_fields",
    "validate_amount_format",
    "validate_card_number",
    "validate_currency_code",
    "validate_country_code",
    # Version
    "__version__",
]
