"""
Cardinity HTTP Client

This module contains the HTTP client for making requests to the Cardinity API.
"""

import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

from requests import Response, Session
from requests.exceptions import ConnectionError, RequestException, Timeout

from .auth import CardinityAuth
from .exceptions import (
    APIError,
    AuthenticationError,
    CardinityError,
    NotFoundError,
    RateLimitError,
    ServerError,
)


class CardinityClient:
    """HTTP client for the Cardinity Payment Gateway API.

    This client handles all HTTP communication with the Cardinity API, including
    OAuth 1.0 authentication, request/response handling, error processing, and
    retry logic for transient failures.
    """

    BASE_URL = "https://api.cardinity.com/v1"
    DEFAULT_TIMEOUT = 30
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds

    def __init__(
        self,
        auth: CardinityAuth,
        base_url: str = BASE_URL,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
    ) -> None:
        """Initialize the Cardinity HTTP client.

        Args:
            auth: CardinityAuth instance for authentication
            base_url: Base URL for the Cardinity API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.auth = auth
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

        # Create a persistent session for connection reuse
        self.session = Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "cardinity-python/1.0.0",
            }
        )

    def _should_retry(
        self, response: Optional[Response], exception: Optional[Exception]
    ) -> bool:
        """Determine if a request should be retried.

        Args:
            response: HTTP response object (if available)
            exception: Exception that occurred (if any)

        Returns:
            bool: True if the request should be retried
        """
        # Retry on connection errors or timeouts
        if isinstance(exception, (ConnectionError, Timeout)):
            return True

        # Retry on server errors (5xx) but not client errors (4xx)
        if response and response.status_code >= 500:
            return True

        # Retry on rate limiting with exponential backoff
        if response and response.status_code == 429:
            return True

        return False

    def _build_url(self, endpoint: str) -> str:
        """Build the full URL for an API endpoint.

        Args:
            endpoint: API endpoint path (e.g., "/payments")

        Returns:
            str: Full URL for the API endpoint
        """
        # Ensure base_url ends with / and endpoint starts with / for proper joining
        base = self.base_url.rstrip("/") + "/"
        endpoint = endpoint.lstrip("/")
        return urljoin(base, endpoint)

    def _parse_response(self, response: Response) -> Dict[str, Any]:
        """Parse and validate API response.

        Args:
            response: HTTP response object

        Returns:
            Dict[str, Any]: Parsed response data

        Raises:
            APIError: If the response indicates an error
        """
        try:
            response_data = response.json()
        except ValueError:
            # Handle non-JSON responses
            response_data = {"error": "Invalid JSON response", "content": response.text}

        # Check for HTTP errors
        if not response.ok:
            error_message = self._extract_error_message(response_data, response)

            if response.status_code == 401:
                raise AuthenticationError(error_message)
            elif response.status_code == 404:
                raise NotFoundError(error_message)
            elif response.status_code == 429:
                raise RateLimitError(error_message)
            elif response.status_code >= 500:
                raise ServerError(error_message)
            else:
                raise APIError(
                    message=error_message,
                    status_code=response.status_code,
                    response_data=response_data,
                )

        return response_data

    def _extract_error_message(
        self, response_data: Dict[str, Any], response: Response
    ) -> str:
        """Extract error message from API response.

        Args:
            response_data: Parsed response data
            response: HTTP response object

        Returns:
            str: Error message
        """
        # Try different common error message fields
        for field in ["message", "error", "detail", "error_description"]:
            if field in response_data and response_data[field]:
                return str(response_data[field])

        # Fall back to generic HTTP status message
        return f"HTTP {response.status_code}: {response.reason}"

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        retry_count: int = 0,
    ) -> Dict[str, Any]:
        """Make an HTTP request to the Cardinity API.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint path
            data: Request payload data (for POST/PATCH requests)
            params: URL query parameters
            retry_count: Current retry attempt number

        Returns:
            Dict[str, Any]: Parsed API response data

        Raises:
            CardinityError: If the request fails after all retries
        """
        url = self._build_url(endpoint)

        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                json=data,
                params=params,
                auth=self.auth.get_auth(),
                timeout=self.timeout,
            )

            return self._parse_response(response)

        except (ConnectionError, Timeout, RequestException) as e:
            if retry_count < self.max_retries and self._should_retry(None, e):
                retry_count += 1
                delay = self.RETRY_DELAY * (
                    2 ** (retry_count - 1)
                )  # Exponential backoff
                time.sleep(delay)
                return self._request(method, endpoint, data, params, retry_count)

            raise CardinityError(f"Request failed: {str(e)}")

        except (RateLimitError, ServerError) as e:
            if retry_count < self.max_retries:
                retry_count += 1
                delay = self.RETRY_DELAY * (
                    2 ** (retry_count - 1)
                )  # Exponential backoff
                time.sleep(delay)
                return self._request(method, endpoint, data, params, retry_count)

            raise e

    def get(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make a GET request to the API.

        Args:
            endpoint: API endpoint path
            params: URL query parameters

        Returns:
            Dict[str, Any]: API response data
        """
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a POST request to the API.

        Args:
            endpoint: API endpoint path
            data: Request payload data

        Returns:
            Dict[str, Any]: API response data
        """
        return self._request("POST", endpoint, data=data)

    def patch(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a PATCH request to the API.

        Args:
            endpoint: API endpoint path
            data: Request payload data

        Returns:
            Dict[str, Any]: API response data
        """
        return self._request("PATCH", endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request to the API.

        Args:
            endpoint: API endpoint path

        Returns:
            Dict[str, Any]: API response data
        """
        return self._request("DELETE", endpoint)

    def execute_request(self, model) -> Dict[str, Any]:
        """Execute a request using a model object.

        Args:
            model: Model object with get_method(), get_endpoint(), and to_dict() methods

        Returns:
            Dict[str, Any]: Parsed API response data

        Raises:
            CardinityError: If the request fails
        """
        method = model.get_method().upper()
        endpoint = model.get_endpoint()

        if method == "GET":
            return self.get(endpoint)
        elif method == "POST":
            return self.post(endpoint, model.to_dict())
        elif method == "PATCH":
            return self.patch(endpoint, model.to_dict())
        elif method == "DELETE":
            return self.delete(endpoint)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

    def close(self) -> None:
        """Close the HTTP session and clean up resources."""
        if self.session:
            self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def __repr__(self) -> str:
        """Return a string representation of the client."""
        return f"CardinityClient(base_url='{self.base_url}')"
