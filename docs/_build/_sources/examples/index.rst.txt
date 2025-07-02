Examples
========

This section provides comprehensive examples of using the Cardinity Python SDK. Each example includes complete, runnable code with detailed explanations of payment processing workflows.

.. note::
   All examples use placeholder credentials and test card numbers. Replace them with your actual credentials and real data for production use.

Available Examples
------------------

.. toctree::
   :maxdepth: 2
   
   basic-payments
   recurring-payments
   3ds-authentication
   refunds-settlements
   error-handling
   advanced-features

Quick Reference
---------------

Common Test Data
~~~~~~~~~~~~~~~~

Use these test values when running examples:

**Test Credentials (Placeholder):**

.. code-block:: python

   CONSUMER_KEY = "your_consumer_key_here"
   CONSUMER_SECRET = "your_consumer_secret_here"

**Test Card Numbers:**

* **Visa Success**: 4111111111111111
* **MasterCard Success**: 5555555555554444
* **Visa 3DS Success**: 4444333322221111
* **American Express Success**: 378282246310005
* **Failure (any amount >150)**: Any valid card number

**Test Amounts:**

* **Success**: Any amount < 150.00
* **Failure**: Any amount >= 150.00
* **3DS Required**: Use description ``3ds2-pass`` or ``3ds2-fail``

Setting Up Your Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Install the SDK:**

   .. code-block:: bash

      pip install cardinity-python

2. **Set up environment variables (recommended):**

   .. code-block:: bash

      export CARDINITY_CONSUMER_KEY="your_consumer_key_here"
      export CARDINITY_CONSUMER_SECRET="your_consumer_secret_here"

3. **Basic client initialization:**

   .. code-block:: python

      import os
      from cardinity import Cardinity

      cardinity = Cardinity(
          consumer_key=os.getenv("CARDINITY_CONSUMER_KEY"),
          consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET")
      )

Basic Payment Example
----------------------

Here's a simple payment processing example:

.. code-block:: python

   """
   Basic Payment Example
   
   This example demonstrates how to create a simple payment using the Cardinity Python SDK.
   """

   import os
   from cardinity import Cardinity, CardinityError

   # Initialize client with placeholder credentials
   cardinity = Cardinity(
       consumer_key=os.getenv("CARDINITY_CONSUMER_KEY", "your_consumer_key_here"),
       consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET", "your_consumer_secret_here")
   )

   def create_basic_payment():
       """Create a basic payment with a test credit card."""
       
       try:
           payment = cardinity.create_payment(
               amount="10.00",
               currency="EUR",
               description="Basic payment example",
               country="LT",
               payment_instrument={
                   "pan": "4111111111111111",  # Test Visa card
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "John Doe"
               }
           )

           print(f"✅ Payment created: {payment['id']}")
           print(f"   Status: {payment['status']}")
           print(f"   Amount: {payment['amount']} {payment['currency']}")

           return payment

       except CardinityError as e:
           print(f"❌ Payment failed: {e}")
           return None

   # Create the payment
   payment = create_basic_payment()

Recurring Payments Example
---------------------------

Subscription-style recurring payments:

.. code-block:: python

   """
   Recurring Payment Example
   
   This example shows how to set up subscription-style payments.
   """
   
   import time

   def create_initial_payment():
       """Create the initial payment for recurring setup."""
       
       payment = cardinity.create_payment(
           amount="29.99",
           currency="EUR",
           description="Monthly subscription - Initial payment",
           country="LT",
           order_id="SUBSCRIPTION-001-INITIAL",
           payment_instrument={
               "pan": "4111111111111111",
               "exp_month": 12,
               "exp_year": 2025,
               "cvc": "123",
               "holder": "John Doe"
           }
       )
       
       return payment

   def create_recurring_payment(parent_payment_id, amount="29.99"):
       """Create a recurring payment using parent payment."""
       
       recurring_payment = cardinity.create_recurring_payment(
           amount=amount,
           currency="EUR",
           description="Monthly subscription payment",
           country="LT",
           order_id=f"SUBSCRIPTION-{int(time.time())}",  # Optional but recommended
           payment_instrument={
               "payment_id": parent_payment_id  # Reference to initial payment
           }
       )
       
       return recurring_payment

   # Example workflow
   initial_payment = create_initial_payment()
   
   if initial_payment['status'] == 'approved':
       # Create subsequent recurring payments
       recurring_1 = create_recurring_payment(initial_payment['id'])
       recurring_2 = create_recurring_payment(initial_payment['id'])

3D Secure Authentication Example
--------------------------------

Handling 3D Secure v2 authentication:

.. code-block:: python

   """
   3D Secure Payment Example
   
   This example demonstrates 3D Secure v2 authentication workflow.
   """

   def create_3ds_payment():
       """Create a payment with 3D Secure authentication."""
       
       payment = cardinity.create_payment(
           amount="25.00",
           currency="EUR",
           description="3ds2-pass",  # Triggers 3DS flow in test environment
           country="LT",
           payment_instrument={
               "pan": "4111111111111111",
               "exp_month": 12,
               "exp_year": 2025,
               "cvc": "123",
               "holder": "Test User"
           },
           threeds2_data={
               "notification_url": "https://yoursite.com/3ds-callback",
               "browser_info": {
                   "accept_header": "text/html",
                   "browser_language": "en-US",
                   "screen_width": 1920,
                   "screen_height": 1040,
                   "challenge_window_size": "500x600",
                   "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0)",
                   "color_depth": 24,
                   "time_zone": -60,
                   "javascript_enabled": True,
                   "java_enabled": False
               }
           }
       )
       
       return payment

   def handle_3ds_flow(payment):
       """Handle 3D Secure authentication flow."""
       
       if payment['status'] == 'pending':
           print("🔒 3DS authentication required")
           
           if 'threeds2_data' in payment:
               acs_url = payment['threeds2_data']['acs_url']
               creq = payment['threeds2_data']['creq']
               
               print(f"Redirect customer to: {acs_url}")
               print("After authentication, finalize the payment...")
               
               # Simulate successful authentication response
               finalized_payment = cardinity.finalize_payment(
                   payment['id'],
                   cres="3ds2-pass"  # Test environment response for 3DS v2
               )
               
               return finalized_payment
       
       return payment

   # Example workflow
   payment = create_3ds_payment()
   final_payment = handle_3ds_flow(payment)

Refund Processing Example
--------------------------

Processing full and partial refunds:

.. code-block:: python

   """
   Refund Example
   
   This example demonstrates refund processing workflows.
   """

   def create_full_refund(payment_id):
       """Create a full refund for a payment."""
       
       # Get payment details first
       payment = cardinity.get_payment(payment_id)
       
       refund = cardinity.create_refund(
           payment_id=payment_id,
           amount=payment['amount'],  # Full amount
           description="Full refund - Customer not satisfied"
       )
       
       return refund

   def create_partial_refund(payment_id, amount, description):
       """Create a partial refund."""
       
       refund = cardinity.create_refund(
           payment_id=payment_id,
           amount=amount,
           description=description
       )
       
       return refund

   # Example: Process multiple partial refunds
   payment = create_basic_payment()
   
   if payment['status'] == 'approved':
       # Partial refund for shipping
       shipping_refund = create_partial_refund(
           payment['id'], 
           "5.00", 
           "Shipping refund"
       )
       
       # Partial refund for product
       product_refund = create_partial_refund(
           payment['id'], 
           "3.00", 
           "Product return"
       )

Error Handling Example
-----------------------

Comprehensive error handling:

.. code-block:: python

   """
   Error Handling Example
   
   This example shows proper error handling techniques.
   """

   from cardinity import Cardinity, CardinityError, ValidationError, APIError

   def create_payment_with_error_handling():
       """Create payment with comprehensive error handling."""
       
       try:
           payment = cardinity.create_payment(
               amount="10.00",
               currency="EUR",
               description="Test payment",
               country="LT",
               payment_instrument={
                   "pan": "4111111111111111",
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "John Doe"
               }
           )
           
           return payment
           
       except ValidationError as e:
           print(f"❌ Validation Error: {e}")
           print("Check your payment data - some fields may be invalid.")
           
       except APIError as e:
           print(f"❌ API Error: {e}")
           print("The API request failed. Check your credentials.")
           
       except CardinityError as e:
           print(f"❌ Cardinity Error: {e}")
           print("A general SDK error occurred.")
           
       return None

Running Examples
----------------

Each example follows this structure:

.. code-block:: python

   """
   Example: Description
   
   This example demonstrates how to...
   """
   
   import os
   from cardinity import Cardinity, CardinityError
   
   # Configuration with placeholder credentials
   cardinity = Cardinity(
       consumer_key=os.getenv("CARDINITY_CONSUMER_KEY", "your_consumer_key_here"),
       consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET", "your_consumer_secret_here")
   )
   
   def main():
       try:
           # Example code here
           pass
       except CardinityError as e:
           print(f"Error: {e}")
   
   if __name__ == "__main__":
       main()

Integration Patterns
--------------------

For real-world integration scenarios:

* **E-commerce Integration**: Complete checkout flow with cart processing
* **Subscription Billing**: Automated recurring payment management
* **Marketplace Payments**: Multi-vendor payment scenarios
* **Mobile App Integration**: API integration patterns for mobile apps
* **Webhook Handling**: Processing payment notifications and status updates

Best Practices
--------------

1. **Environment Variables**: Always use environment variables for credentials
2. **Error Handling**: Implement comprehensive error handling for all operations
3. **Testing**: Use test credentials and test cards during development
4. **Security**: Never log or expose sensitive payment data
5. **Idempotency**: Use unique order IDs to prevent duplicate payments
6. **Monitoring**: Implement proper logging and monitoring for production

Next Steps
----------

1. Start with ``basic_payment.py`` for simple payment processing
2. Learn about 3D Secure with ``3ds_payment.py`` 
3. Implement subscriptions using ``recurring_payment.py``
4. Handle refunds with ``refund_example.py``
5. Explore advanced features for complex scenarios

Need Help?
----------

* Visit our `GitHub Issues <https://github.com/trendpro/cardinity-python/issues>`_
* Check the `API Documentation <https://developers.cardinity.com/api/v1/#introduction>`_
* Contact support at kyalo@trendpro.co.ke 
