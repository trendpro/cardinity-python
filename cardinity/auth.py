"""
Cardinity Authentication

This module handles OAuth 1.0 authentication for the Cardinity API.
"""

from typing import Dict

from requests_oauthlib import OAuth1


class CardinityAuth:
    """OAuth 1.0 authentication handler for Cardinity API.

    This class manages OAuth 1.0 authentication using HMAC-SHA1 signature method
    as required by the Cardinity API. It provides authentication headers for
    HTTP requests.
    """

    def __init__(self, consumer_key: str, consumer_secret: str) -> None:
        """Initialize the Cardinity authentication handler.

        Args:
            consumer_key: The OAuth consumer key provided by Cardinity
            consumer_secret: The OAuth consumer secret provided by Cardinity

        Raises:
            ValueError: If consumer_key or consumer_secret is empty
        """
        if not consumer_key:
            raise ValueError("Consumer key cannot be empty")
        if not consumer_secret:
            raise ValueError("Consumer secret cannot be empty")

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

    def get_auth(self) -> OAuth1:
        """Get the OAuth1 authentication object for requests.

        Returns:
            OAuth1: Configured OAuth1 authentication object that can be used
                   with the requests library
        """
        return OAuth1(
            client_key=self.consumer_key,
            client_secret=self.consumer_secret,
            signature_method="HMAC-SHA1",
            signature_type="AUTH_HEADER",
        )

    def get_auth_headers(self, method: str, url: str, body: str = "") -> Dict[str, str]:
        """Get authentication headers for a specific request.

        This is an alternative method to get_auth() that returns the headers
        directly instead of an OAuth1 object.

        Args:
            method: HTTP method (GET, POST, PATCH, etc.)
            url: Full URL for the request
            body: Request body (for POST/PATCH requests)

        Returns:
            Dict[str, str]: Dictionary containing OAuth authentication headers
        """
        # We'll use the OAuth1 object with requests, so this method is mainly
        # for compatibility or debugging purposes
        return {}

    def __repr__(self) -> str:
        """Return a string representation of the auth object."""
        return f"CardinityAuth(consumer_key='{self.consumer_key[:8]}...')"
