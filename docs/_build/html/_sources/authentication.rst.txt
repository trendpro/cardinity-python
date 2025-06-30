Authentication
==============

The Cardinity Python SDK uses OAuth 1.0 authentication to secure API requests. This guide explains how authentication works and how to configure it properly.

OAuth 1.0 Overview
------------------

Cardinity uses OAuth 1.0 with HMAC-SHA1 signatures to authenticate API requests. This ensures that:

* All requests are authenticated
* Request data integrity is verified
* Sensitive credentials are never sent in plain text
* Replay attacks are prevented using timestamps and nonces

The SDK handles all OAuth 1.0 complexity automatically - you only need to provide your consumer key and secret.

Getting Credentials
-------------------

Test Credentials
~~~~~~~~~~~~~~~~

For development and testing, use test credentials:

1. Sign up for a Cardinity account
2. Access your dashboard
3. Navigate to Settings → API Keys
4. Create test credentials (prefixed with ``test_``)

Test credentials only work with:
* Test card numbers
* Sandbox API endpoints
* No real money transactions

Live Credentials
~~~~~~~~~~~~~~~~

For production use:

1. Complete Cardinity account verification
2. Get approved for live transactions
3. Generate live API credentials
4. Use only with real card data and transactions

.. warning::
   Never use live credentials in development or testing environments.

Configuration Methods
---------------------

Direct Initialization
~~~~~~~~~~~~~~~~~~~~~

The simplest way to configure authentication:

.. code-block:: python

   from cardinity import Cardinity
   
   cardinity = Cardinity(
       consumer_key="your_consumer_key",
       consumer_secret="your_consumer_secret"
   )

Environment Variables (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For better security, use environment variables:

.. code-block:: bash

   # In your shell or .env file
   export CARDINITY_CONSUMER_KEY="test_jlol6sogrlvje2zwwsfb6kjajuyy7h"
   export CARDINITY_CONSUMER_SECRET="1h7j6rvwlpvuwbzrobo6bjbcqv1m3khnlqojpkkwh9wzbrlkmu"

.. code-block:: python

   import os
   from cardinity import Cardinity
   
   cardinity = Cardinity(
       consumer_key=os.getenv("CARDINITY_CONSUMER_KEY"),
       consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET")
   )

Configuration Files
~~~~~~~~~~~~~~~~~~~

For applications with multiple environments:

.. code-block:: python

   import json
   from cardinity import Cardinity
   
   # Load from JSON config
   with open('config.json') as f:
       config = json.load(f)
   
   cardinity = Cardinity(
       consumer_key=config['cardinity']['key'],
       consumer_secret=config['cardinity']['secret']
   )

.. code-block:: json

   {
     "cardinity": {
       "key": "test_jlol6sogrlvje2zwwsfb6kjajuyy7h",
       "secret": "1h7j6rvwlpvuwbzrobo6bjbcqv1m3khnlqojpkkwh9wzbrlkmu"
     }
   }

Advanced Authentication
-----------------------

Custom HTTP Client
~~~~~~~~~~~~~~~~~~

For advanced use cases, you can customize the HTTP client:

.. code-block:: python

   from cardinity import CardinityClient
   from cardinity.auth import CardinityAuth
   
   # Create custom auth
   auth = CardinityAuth(
       consumer_key="your_key",
       consumer_secret="your_secret"
   )
   
   # Create custom client
   client = CardinityClient(auth=auth)
   
   # Use client directly
   response = client._request('GET', '/payments')

Connection Pooling
~~~~~~~~~~~~~~~~~~

For high-volume applications, configure connection pooling:

.. code-block:: python

   import requests
   from requests.adapters import HTTPAdapter
   from urllib3.util.retry import Retry
   from cardinity import CardinityClient
   
   # Create session with connection pooling
   session = requests.Session()
   
   # Configure retry strategy
   retry_strategy = Retry(
       total=3,
       backoff_factor=1,
       status_forcelist=[429, 500, 502, 503, 504],
   )
   
   adapter = HTTPAdapter(
       pool_connections=10,
       pool_maxsize=20,
       max_retries=retry_strategy
   )
   
   session.mount("http://", adapter)
   session.mount("https://", adapter)
   
   # Use custom session (not directly supported yet, but planned)
   # client = CardinityClient(session=session)

Security Best Practices
------------------------

Credential Storage
~~~~~~~~~~~~~~~~~~

**DO:**

* Store credentials in environment variables
* Use secure configuration management (HashiCorp Vault, AWS Secrets Manager)
* Rotate credentials regularly
* Use different credentials for different environments

**DON'T:**

* Hardcode credentials in source code
* Commit credentials to version control
* Share credentials via email or chat
* Use production credentials in development

Network Security
~~~~~~~~~~~~~~~~

* Always use HTTPS endpoints (enforced by the SDK)
* Validate SSL certificates (default behavior)
* Use secure network connections
* Monitor for suspicious API usage

Logging and Monitoring
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import logging
   from cardinity import Cardinity, APIError
   
   # Configure logging (be careful not to log credentials)
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   cardinity = Cardinity(
       consumer_key=os.getenv("CARDINITY_CONSUMER_KEY"),
       consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET")
   )
   
   try:
       payment = cardinity.create_payment(...)
       logger.info(f"Payment created successfully: {payment['id']}")
   except APIError as e:
       # Safe to log error details (no sensitive data)
       logger.error(f"Payment failed: {e.status_code} - {e}")

Error Handling
--------------

Authentication Errors
~~~~~~~~~~~~~~~~~~~~~

Common authentication errors and solutions:

.. code-block:: python

   from cardinity import Cardinity, APIError
   
   try:
       cardinity = Cardinity(
           consumer_key="invalid_key",
           consumer_secret="invalid_secret"
       )
       payment = cardinity.create_payment(...)
   except APIError as e:
       if e.status_code == 401:
           print("Authentication failed - check your credentials")
       elif e.status_code == 403:
           print("Access forbidden - check your account permissions")
       else:
           print(f"API error: {e}")

Testing Authentication
----------------------

Verify Credentials
~~~~~~~~~~~~~~~~~~

Test your credentials before making transactions:

.. code-block:: python

   from cardinity import Cardinity, APIError
   
   def verify_credentials(consumer_key, consumer_secret):
       try:
           cardinity = Cardinity(
               consumer_key=consumer_key,
               consumer_secret=consumer_secret
           )
           
           # Try to list payments (minimal API call)
           payments = cardinity.get_payment(limit=1)
           return True
       except APIError as e:
           if e.status_code in [401, 403]:
               return False
           raise  # Re-raise other errors
   
   # Test credentials
   if verify_credentials("your_key", "your_secret"):
       print("Credentials are valid")
   else:
       print("Invalid credentials")

OAuth Signature Debugging
~~~~~~~~~~~~~~~~~~~~~~~~~~

For debugging OAuth signature issues:

.. code-block:: python

   import os
   from cardinity.auth import CardinityAuth
   
   # Enable OAuth debugging (for development only)
   os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # Only for localhost testing
   
   auth = CardinityAuth(
       consumer_key="your_key",
       consumer_secret="your_secret"
   )
   
   # The auth object handles OAuth signature generation
   oauth_client = auth.get_auth()
   
   # You can inspect the OAuth client if needed
   print(f"OAuth client: {oauth_client}")

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**401 Unauthorized**
   - Check consumer key and secret
   - Verify credentials are for the correct environment (test vs live)
   - Ensure no extra whitespace in credentials

**403 Forbidden**
   - Account may not be approved for the requested operation
   - Check account status in dashboard
   - Contact Cardinity support

**Signature Errors**
   - Usually caused by incorrect credentials
   - Check for special characters in credentials
   - Verify system clock is accurate (OAuth uses timestamps)

**SSL Certificate Errors**
   - Update system SSL certificates
   - Check firewall settings
   - Verify internet connectivity

Environment-Specific Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Development**
   - Use test credentials only
   - Test with provided test card numbers
   - Check for proxy or firewall restrictions

**Production**
   - Use live credentials
   - Ensure account is verified and approved
   - Monitor for rate limiting
   - Implement proper error handling and logging

Next Steps
----------

* Learn about :doc:`examples/index` for practical authentication scenarios
* Check the API reference for advanced client configuration
* Visit the GitHub repository for troubleshooting authentication issues 
