"""
Cardinity SDK Exceptions

This module contains all custom exception classes used by the Cardinity SDK.
"""

from typing import Any, Dict, Optional


class CardinityError(Exception):
    """Base exception for all Cardinity SDK errors.

    This is the base exception class that all other Cardinity SDK exceptions
    inherit from. It provides a common interface for error handling.
    """

    def __init__(self, message: str) -> None:
        """Initialize the CardinityError.

        Args:
            message: The error message
        """
        super().__init__(message)
        self.message = message


class ValidationError(CardinityError):
    """Exception raised when input validation fails.

    This exception is raised when data validation fails before making
    an API request. It contains details about which fields failed validation.
    """

    def __init__(self, message: str, errors: Optional[Dict[str, Any]] = None) -> None:
        """Initialize the ValidationError.

        Args:
            message: The error message
            errors: Dictionary containing validation errors for each field
        """
        super().__init__(message)
        self.errors = errors or {}

    def __str__(self) -> str:
        """Return a string representation of the validation error."""
        if self.errors:
            error_details = []
            for field, field_errors in self.errors.items():
                if isinstance(field_errors, list):
                    for error in field_errors:
                        error_details.append(f"{field}: {error}")
                else:
                    error_details.append(f"{field}: {field_errors}")
            return f"{self.message}: {', '.join(error_details)}"
        return self.message


class APIError(CardinityError):
    """Exception raised when the API returns an error response.

    This exception is raised when the Cardinity API returns an error response
    (4xx or 5xx status codes). It contains the HTTP status code and the
    response data from the API.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize the APIError.

        Args:
            message: The error message
            status_code: HTTP status code of the error response
            response_data: Dictionary containing the API response data
        """
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}

    def __str__(self) -> str:
        """Return a string representation of the API error."""
        if self.status_code:
            return f"HTTP {self.status_code}: {self.message}"
        return self.message


class AuthenticationError(APIError):
    """Exception raised when authentication fails.

    This exception is raised when the API returns a 401 Unauthorized response,
    indicating that the OAuth credentials are invalid or expired.
    """

    def __init__(self, message: str = "Authentication failed") -> None:
        """Initialize the AuthenticationError.

        Args:
            message: The error message
        """
        super().__init__(message, status_code=401)


class NotFoundError(APIError):
    """Exception raised when a requested resource is not found.

    This exception is raised when the API returns a 404 Not Found response,
    indicating that the requested resource (payment, refund, etc.) does not exist.
    """

    def __init__(self, message: str = "Resource not found") -> None:
        """Initialize the NotFoundError.

        Args:
            message: The error message
        """
        super().__init__(message, status_code=404)


class RateLimitError(APIError):
    """Exception raised when API rate limits are exceeded.

    This exception is raised when the API returns a 429 Too Many Requests response,
    indicating that the rate limit has been exceeded.
    """

    def __init__(self, message: str = "Rate limit exceeded") -> None:
        """Initialize the RateLimitError.

        Args:
            message: The error message
        """
        super().__init__(message, status_code=429)


class ServerError(APIError):
    """Exception raised when the server encounters an error.

    This exception is raised when the API returns a 5xx Server Error response,
    indicating that there's an issue on the server side.
    """

    def __init__(self, message: str = "Internal server error") -> None:
        """Initialize the ServerError.

        Args:
            message: The error message
        """
        super().__init__(message, status_code=500)
