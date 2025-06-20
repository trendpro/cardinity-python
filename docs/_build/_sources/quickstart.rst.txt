Quick Start Guide
=================

This guide will help you get started with the Cardinity Python SDK quickly. We'll cover everything from getting your API credentials to making your first payment.

Getting API Credentials
------------------------

Before you can use the SDK, you need to obtain API credentials from Cardinity:

1. **Sign up** for a Cardinity account at `https://cardinity.com/ <https://cardinity.com/>`_
2. **Login** to your Cardinity dashboard
3. **Navigate** to Settings → API keys
4. **Generate** your Consumer Key and Consumer Secret
5. **Save** these credentials securely (you'll need them for authentication)

.. warning::
   Keep your API credentials secure and never commit them to version control. Use environment variables or secure configuration files.

Test vs Live Environment
~~~~~~~~~~~~~~~~~~~~~~~~~

Cardinity provides separate environments:

* **Test Environment**: For development and testing
* **Live Environment**: For production transactions

Test credentials are prefixed with ``test_`` and only work with test card numbers.

Basic Setup
-----------

Import and Initialize
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from cardinity import Cardinity
   
   # Initialize with your credentials
   cardinity = Cardinity(
       consumer_key="your_consumer_key",
       consumer_secret="your_consumer_secret"
   )

Environment Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

For better security, use environment variables:

.. code-block:: bash

   export CARDINITY_CONSUMER_KEY="your_consumer_key"
   export CARDINITY_CONSUMER_SECRET="your_consumer_secret"

.. code-block:: python

   import os
   from cardinity import Cardinity
   
   cardinity = Cardinity(
       consumer_key=os.getenv("CARDINITY_CONSUMER_KEY"),
       consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET")
   )

Your First Payment
------------------

Create a Simple Payment
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from cardinity import Cardinity
   
   cardinity = Cardinity(
       consumer_key="test_jlol6sogrlvje2zwwsfb6kjajuyy7h",
       consumer_secret="1h7j6rvwlpvuwbzrobo6bjbcqv1m3khnlqojpkkwh9wzbrlkmu"
   )
   
   try:
       # Create a payment
       payment = cardinity.create_payment(
           amount="10.00",
           currency="EUR",
           description="Test payment",
           country="LT",
           payment_instrument={
               "pan": "4111111111111111",  # Test Visa card
               "exp_month": 12,
               "exp_year": 2025,
               "cvc": "123",
               "holder": "John Doe"
           }
       )
       
       print(f"Payment created successfully!")
       print(f"Payment ID: {payment['id']}")
       print(f"Status: {payment['status']}")
       print(f"Amount: {payment['amount']} {payment['currency']}")
       
   except Exception as error:
       print(f"Payment failed: {error}")

Test Card Numbers
~~~~~~~~~~~~~~~~~

For testing, use these card numbers:

* **Visa Success**: 4111111111111111
* **MasterCard Success**: 5555555555554444
* **Visa 3DS Success**: 4444333322221111
* **Failure (any amount >150)**: Any valid card number

Handle 3D Secure Authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some payments may require 3D Secure authentication:

.. code-block:: python

   # Create payment that might require 3DS
   payment = cardinity.create_payment(
       amount="50.00",
       currency="EUR",
       description="3DS test payment",
       country="LT",
       payment_instrument={
           "pan": "4444333322221111",  # 3DS test card
           "exp_month": 12,
           "exp_year": 2025,
           "cvc": "123",
           "holder": "John Doe"
       }
   )
   
   if payment['status'] == 'pending':
       # 3DS authentication required
       auth_url = payment['authorization_information']['url']
       print(f"Complete 3DS authentication at: {auth_url}")
       
       # After user completes 3DS, finalize the payment
       # You'll receive the authorization data via callback/redirect
       
       # Example finalization (you'll get this data from your callback)
       finalized_payment = cardinity.finalize_payment(
           payment['id'],
           authorize_data="auth_data_from_3ds_callback"
       )
       
       print(f"Finalized payment status: {finalized_payment['status']}")

Common Operations
-----------------

Retrieve a Payment
~~~~~~~~~~~~~~~~~~

.. code-block:: python

   # Get payment by ID
   payment = cardinity.get_payment("payment_id_here")
   print(f"Payment status: {payment['status']}")

Create a Refund
~~~~~~~~~~~~~~~

.. code-block:: python

   # Refund a payment (partial or full)
   refund = cardinity.create_refund(
       payment_id="payment_id_here",
       amount="5.00",  # Optional: defaults to full amount
       description="Customer requested refund"
   )
   print(f"Refund created: {refund['id']}")

Create a Payment Link
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from datetime import datetime, timedelta
   
   # Create a payment link that expires in 1 hour
   payment_link = cardinity.create_payment_link(
       amount="25.00",
       currency="EUR",
       description="Payment for order #12345",
       country="LT",
       expiration_date=(datetime.now() + timedelta(hours=1)).isoformat()
   )
   
   print(f"Payment link: {payment_link['url']}")

Error Handling
--------------

Always handle errors appropriately:

.. code-block:: python

   from cardinity import Cardinity, CardinityError, ValidationError, APIError
   
   cardinity = Cardinity(
       consumer_key="your_key",
       consumer_secret="your_secret"
   )
   
   try:
       payment = cardinity.create_payment(
           amount="invalid_amount",  # This will cause a validation error
           currency="EUR",
           description="Test payment",
           country="LT",
           payment_instrument={}
       )
   except ValidationError as e:
       print(f"Validation error: {e}")
   except APIError as e:
       print(f"API error: {e}")
       print(f"Status code: {e.status_code}")
   except CardinityError as e:
       print(f"General Cardinity error: {e}")
   except Exception as e:
       print(f"Unexpected error: {e}")

Best Practices
--------------

Security
~~~~~~~~

1. **Never hardcode credentials** in your source code
2. **Use environment variables** or secure configuration management
3. **Validate all inputs** before sending to the API
4. **Log errors** but never log sensitive payment data
5. **Use HTTPS** for all webhook endpoints

Performance
~~~~~~~~~~~

1. **Reuse the client instance** instead of creating new ones
2. **Implement proper retry logic** for network failures
3. **Use connection pooling** for high-volume applications
4. **Cache payment results** when appropriate

Testing
~~~~~~~

1. **Always test with sandbox credentials** first
2. **Use provided test card numbers**
3. **Test all payment scenarios** (success, failure, 3DS)
4. **Implement proper error handling**
5. **Test webhook handling** thoroughly

Next Steps
----------

Now that you've learned the basics:

1. Explore the :doc:`examples/index` for more detailed scenarios
2. Read the :doc:`api` for complete API reference
3. Check out the :doc:`migration` guide if you're coming from Node.js
4. Learn about :doc:`authentication` for advanced configurations

Need Help?
----------

* Visit the GitHub repository for troubleshooting common issues
* Visit our `GitHub Issues <https://github.com/trendpro/cardinity-python/issues>`_
* Contact support at contact@cardinity.com 
