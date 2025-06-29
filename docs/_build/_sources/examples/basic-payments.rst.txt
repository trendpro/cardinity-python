Basic Payment Processing
=======================

This section covers fundamental payment processing with the Cardinity Python SDK, including creating payments, handling responses, and retrieving payment information.

Overview
--------

Basic payment processing involves:

1. **Payment Creation**: Creating a new payment with card details
2. **Status Handling**: Processing different payment statuses (approved, declined, pending)
3. **Payment Retrieval**: Getting payment information after creation
4. **Error Handling**: Managing validation and API errors

Simple Payment Example
---------------------

Here's a complete example of creating a basic payment:

.. code-block:: python

   """
   Basic Payment Example
   
   This example demonstrates the simplest way to create a payment.
   """

   import os
   from cardinity import Cardinity, CardinityError

   # Initialize client
   cardinity = Cardinity(
       consumer_key=os.getenv("CARDINITY_CONSUMER_KEY", "your_consumer_key_here"),
       consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET", "your_consumer_secret_here")
   )

   def create_simple_payment():
       """Create a basic payment."""
       
       try:
           payment = cardinity.create_payment(
               amount="10.00",
               currency="EUR",
               description="Simple payment example",
               country="LT",  # Required: Customer country (ISO 3166-1 alpha-2)
               payment_instrument={
                   "pan": "4111111111111111",  # Test Visa card
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "John Doe"
               }
           )

           print(f"✅ Payment created successfully!")
           print(f"   Payment ID: {payment['id']}")
           print(f"   Status: {payment['status']}")
           print(f"   Amount: {payment['amount']} {payment['currency']}")

           return payment

       except CardinityError as e:
           print(f"❌ Payment failed: {e}")
           return None

   if __name__ == "__main__":
       payment = create_simple_payment()

Payment with Authorization vs Purchase
-------------------------------------

Cardinity supports two types of payments:

**Purchase (Default):** Immediate charge and settlement

.. code-block:: python

   def create_purchase_payment():
       """Create a purchase payment (immediate settlement)."""
       
       payment = cardinity.create_payment(
           amount="25.00",
           currency="EUR",
           description="Purchase payment",
           country="LT",
           settle=True,  # Default: immediate settlement
           payment_instrument={
               "pan": "4111111111111111",
               "exp_month": 12,
               "exp_year": 2025,
               "cvc": "123",
               "holder": "Jane Smith"
           }
       )
       
       return payment

**Authorization:** Reserve funds, settle later

.. code-block:: python

   def create_authorization_payment():
       """Create an authorization (reserve funds, settle later)."""
       
       payment = cardinity.create_payment(
           amount="50.00",
           currency="EUR",
           description="Authorization payment",
           country="LT",
           settle=False,  # Authorization only
           payment_instrument={
               "pan": "4111111111111111",
               "exp_month": 12,
               "exp_year": 2025,
               "cvc": "123",
               "holder": "Bob Johnson"
           }
       )
       
       print(f"Authorization created: {payment['id']}")
       print("Remember to settle within 7 days!")
       
       return payment

Handling Payment Responses
-------------------------

Payments can have different statuses:

.. code-block:: python

   def handle_payment_response(payment):
       """Handle different payment response statuses."""
       
       if not payment:
           print("❌ Payment creation failed")
           return
           
       status = payment['status']
       
       if status == 'approved':
           print("✅ Payment approved immediately")
           print(f"   Transaction ID: {payment['id']}")
           print(f"   Amount charged: {payment['amount']} {payment['currency']}")
           
       elif status == 'declined':
           print("❌ Payment declined")
           if 'error' in payment:
               print(f"   Reason: {payment['error']}")
           if 'merchant_advice_code' in payment:
               print(f"   Advice: {payment['merchant_advice_code']}")
               
       elif status == 'pending':
           print("⏳ Payment pending - may require 3D Secure authentication")
           if 'threeds2_data' in payment:
               print("   3DS authentication required")
               # Handle 3DS flow (see 3DS documentation)
           
       else:
           print(f"⚠️ Unknown payment status: {status}")

Payment Information Retrieval
----------------------------

Retrieve payment details after creation:

.. code-block:: python

   def get_payment_details(payment_id):
       """Retrieve comprehensive payment information."""
       
       try:
           payment = cardinity.get_payment(payment_id)
           
           print(f"Payment Details for {payment_id}:")
           print(f"  Status: {payment['status']}")
           print(f"  Amount: {payment['amount']} {payment['currency']}")
           print(f"  Created: {payment['created']}")
           print(f"  Description: {payment['description']}")
           print(f"  Country: {payment['country']}")
           print(f"  Payment Method: {payment['payment_method']}")
           
           # Card information (masked)
           if 'payment_instrument' in payment:
               card = payment['payment_instrument']
               print(f"  Card: **** **** **** {card['pan']}")
               print(f"  Brand: {card['card_brand']}")
               print(f"  Holder: {card['holder']}")
           
           return payment
           
       except CardinityError as e:
           print(f"❌ Failed to retrieve payment: {e}")
           return None

Advanced Payment Options
-----------------------

Using additional payment parameters:

.. code-block:: python

   def create_advanced_payment():
       """Create a payment with additional options."""
       
       payment = cardinity.create_payment(
           amount="75.50",
           currency="EUR",
           description="Advanced payment with options",
           country="LT",
           order_id="ORDER-2023-12345",  # Your internal order ID
           settle=True,
           statement_descriptor_suffix="MYSTORE",  # Appears on card statement
           payment_instrument={
               "pan": "5555555555554444",  # Test MasterCard
               "exp_month": 6,
               "exp_year": 2026,
               "cvc": "456",
               "holder": "Alice Williams"
           }
       )
       
       return payment

Test Card Numbers
----------------

Use these test cards for different scenarios:

.. code-block:: python

   # Test card configurations
   TEST_CARDS = {
       "visa_success": {
           "pan": "4111111111111111",
           "exp_month": 12,
           "exp_year": 2025,
           "cvc": "123",
           "holder": "Visa Success"
       },
       "mastercard_success": {
           "pan": "5555555555554444",
           "exp_month": 12,
           "exp_year": 2025,
           "cvc": "123",
           "holder": "MasterCard Success"
       },
       "amex_success": {
           "pan": "378282246310005",
           "exp_month": 12,
           "exp_year": 2025,
           "cvc": "1234",
           "holder": "AmEx Success"
       },
       "decline_card": {
           "pan": "4111111111111111",
           "exp_month": 12,
           "exp_year": 2025,
           "cvc": "123",
           "holder": "Decline Test"
           # Use amount >= 150.00 to trigger decline
       }
   }

   def test_different_cards():
       """Test payments with different card types."""
       
       for card_type, card_data in TEST_CARDS.items():
           print(f"\nTesting {card_type}...")
           
           # Use higher amount for decline test
           amount = "200.00" if "decline" in card_type else "25.00"
           
           payment = cardinity.create_payment(
               amount=amount,
               currency="EUR",
               description=f"Test payment with {card_type}",
               country="LT",
               payment_instrument=card_data
           )
           
           print(f"Result: {payment['status'] if payment else 'Failed'}")

Complete Workflow Example
------------------------

A complete payment processing workflow:

.. code-block:: python

   def complete_payment_workflow():
       """Demonstrate a complete payment workflow."""
       
       print("🛒 Starting payment workflow...")
       
       # Step 1: Create payment
       print("\n1. Creating payment...")
       payment = create_simple_payment()
       
       if not payment:
           print("❌ Workflow failed at payment creation")
           return
       
       # Step 2: Handle response
       print("\n2. Processing payment response...")
       handle_payment_response(payment)
       
       # Step 3: Retrieve updated payment info
       print("\n3. Retrieving payment details...")
       updated_payment = get_payment_details(payment['id'])
       
       # Step 4: Final status check
       print("\n4. Final status check...")
       if updated_payment and updated_payment['status'] == 'approved':
           print("✅ Payment workflow completed successfully!")
           return updated_payment
       else:
           print("⚠️ Payment workflow completed with issues")
           return None

   if __name__ == "__main__":
       result = complete_payment_workflow()

Common Issues and Solutions
--------------------------

**Invalid Card Number**

.. code-block:: python

   # ❌ Wrong: Invalid card number
   payment = cardinity.create_payment(
       amount="10.00",
       currency="EUR",
       description="Test",
       country="LT",
       payment_instrument={
           "pan": "1234567890123456",  # Invalid number
           "exp_month": 12,
           "exp_year": 2025,
           "cvc": "123",
           "holder": "Test User"
       }
   )

   # ✅ Correct: Valid test card
   payment = cardinity.create_payment(
       amount="10.00",
       currency="EUR",
       description="Test",
       country="LT",
       payment_instrument={
           "pan": "4111111111111111",  # Valid Visa test card
           "exp_month": 12,
           "exp_year": 2025,
           "cvc": "123",
           "holder": "Test User"
       }
   )

**Missing Required Fields**

.. code-block:: python

   # ❌ Wrong: Missing country field
   payment = cardinity.create_payment(
       amount="10.00",
       currency="EUR",
       description="Test",
       # country="LT",  # Required field missing
       payment_instrument={...}
   )

   # ✅ Correct: All required fields included
   payment = cardinity.create_payment(
       amount="10.00",
       currency="EUR",
       description="Test",
       country="LT",  # Required field
       payment_instrument={...}
   )

Next Steps
----------

After mastering basic payments:

1. **Learn 3D Secure**: Handle strong customer authentication
2. **Implement Recurring Payments**: Set up subscription billing
3. **Add Refund Processing**: Handle customer refunds
4. **Error Handling**: Robust error management
5. **Testing Strategies**: Comprehensive testing approaches

Best Practices
--------------

1. **Always validate input data** before creating payments
2. **Use test credentials** during development
3. **Handle all possible payment statuses** in your application
4. **Store payment IDs** for future reference and operations
5. **Implement proper logging** for payment tracking
6. **Use HTTPS** for all payment-related communications
7. **Never log sensitive card data** in your application 
