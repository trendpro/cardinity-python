Recurring Payments
==================

This section covers recurring payment processing with the Cardinity Python SDK, including subscription billing, automatic payments, and recurring payment management.

Overview
--------

Recurring payments enable you to:

1. **Subscription Billing**: Charge customers periodically for services
2. **Automatic Payments**: Process payments without customer intervention
3. **Card Tokenization**: Securely store payment methods for future use
4. **Flexible Billing**: Support various billing cycles and amounts

How Recurring Payments Work
--------------------------

The recurring payment process involves:

1. **Initial Payment**: Customer provides card details for the first payment
2. **Card Tokenization**: Cardinity securely stores the payment method
3. **Recurring Charges**: Use the initial payment ID to create subsequent payments
4. **No 3DS Required**: Recurring payments bypass 3D Secure authentication

Basic Recurring Payment Setup
-----------------------------

Here's how to set up recurring payments:

.. code-block:: python

   """
   Recurring Payment Setup Example
   
   This example shows how to set up and process recurring payments.
   """

   import os
   from cardinity import Cardinity, CardinityError

   # Initialize client
   cardinity = Cardinity(
       consumer_key=os.getenv("CARDINITY_CONSUMER_KEY", "your_consumer_key_here"),
       consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET", "your_consumer_secret_here")
   )

   def create_initial_payment():
       """Create the initial payment that enables recurring billing."""
       
       try:
           # Create initial payment - this will be used for future recurring payments
           payment = cardinity.create_payment(
               amount="29.99",
               currency="EUR",
               description="Monthly subscription - Initial payment",
               country="LT",
               order_id="SUBSCRIPTION-001-INITIAL",
               payment_instrument={
                   "pan": "4111111111111111",  # Test Visa card
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "John Doe"
               }
           )

           print(f"✅ Initial payment created!")
           print(f"   Payment ID: {payment['id']}")
           print(f"   Status: {payment['status']}")
           print(f"   Amount: {payment['amount']} {payment['currency']}")

           return payment

       except CardinityError as e:
           print(f"❌ Initial payment failed: {e}")
           return None

   def create_recurring_payment(parent_payment_id, amount="29.99", description=None):
       """Create a recurring payment using a parent payment ID."""
       
       try:
           if description is None:
               description = f"Monthly subscription payment - ${amount}"
               
           recurring_payment = cardinity.create_recurring_payment(
               amount=amount,
               currency="EUR",
               description=description,
               country="LT",  # Required field
               payment_id=parent_payment_id  # Reference to initial payment
           )

           print(f"✅ Recurring payment created!")
           print(f"   Payment ID: {recurring_payment['id']}")
           print(f"   Status: {recurring_payment['status']}")
           print(f"   Amount: {recurring_payment['amount']} {recurring_payment['currency']}")
           print(f"   Parent Payment: {parent_payment_id}")

           return recurring_payment

       except CardinityError as e:
           print(f"❌ Recurring payment failed: {e}")
           return None

Subscription Workflow Example
----------------------------

Complete subscription billing workflow:

.. code-block:: python

   import time
   from datetime import datetime

   def subscription_billing_workflow():
       """Demonstrate a complete subscription billing workflow."""
       
       print("💳 Starting subscription billing workflow...")
       
       # Step 1: Customer signs up - create initial payment
       print("\n1. Customer signup - Creating initial payment...")
       initial_payment = create_initial_payment()
       
       if not initial_payment or initial_payment['status'] != 'approved':
           print("❌ Initial payment failed. Cannot setup subscription.")
           return None
           
       print("✅ Subscription activated!")
       subscription_data = {
           'customer_id': 'CUST-12345',
           'payment_id': initial_payment['id'],
           'plan': 'monthly',
           'amount': '29.99',
           'created': datetime.now().isoformat()
       }
       
       # Step 2: Process monthly recurring payments
       print("\n2. Processing monthly recurring payments...")
       
       # Month 1
       print("\n   📅 Processing Month 1 payment...")
       month1_payment = create_recurring_payment(
           initial_payment['id'],
           amount="29.99",
           description="Monthly subscription - Month 1"
       )
       
       # Simulate time passing
       time.sleep(1)
       
       # Month 2
       print("\n   📅 Processing Month 2 payment...")
       month2_payment = create_recurring_payment(
           initial_payment['id'],
           amount="29.99",
           description="Monthly subscription - Month 2"
       )
       
       # Step 3: Handle plan upgrade
       print("\n3. Customer upgrades to premium plan...")
       premium_payment = create_recurring_payment(
           initial_payment['id'],
           amount="49.99",
           description="Premium subscription - Upgraded plan"
       )
       
       print("\n✅ Subscription workflow completed!")
       return {
           'initial': initial_payment,
           'month1': month1_payment,
           'month2': month2_payment,
           'premium': premium_payment
       }

Variable Amount Recurring Payments
---------------------------------

Handle usage-based billing with variable amounts:

.. code-block:: python

   def usage_based_billing_example():
       """Example of usage-based recurring billing with variable amounts."""
       
       print("📊 Usage-based billing example...")
       
       # Create initial payment for usage-based billing
       initial_payment = create_initial_payment()
       
       if not initial_payment or initial_payment['status'] != 'approved':
           return None
           
       # Define different usage scenarios
       usage_scenarios = [
           {"usage": "low", "amount": "15.99", "description": "Low usage month - 100GB"},
           {"usage": "medium", "amount": "25.99", "description": "Medium usage month - 500GB"},
           {"usage": "high", "amount": "45.99", "description": "High usage month - 1TB"},
           {"usage": "enterprise", "amount": "89.99", "description": "Enterprise usage - 5TB"}
       ]
       
       for scenario in usage_scenarios:
           print(f"\n   💰 Processing {scenario['usage']} usage billing...")
           
           payment = create_recurring_payment(
               initial_payment['id'],
               amount=scenario['amount'],
               description=scenario['description']
           )
           
           if payment:
               print(f"      ✅ Charged {scenario['amount']} EUR for {scenario['usage']} usage")

Recurring Payment Error Handling
--------------------------------

Handle common recurring payment issues:

.. code-block:: python

   from cardinity import APIError, ValidationError

   def robust_recurring_payment(parent_payment_id, amount, description, max_retries=3):
       """Create recurring payment with robust error handling."""
       
       for attempt in range(max_retries):
           try:
               payment = cardinity.create_recurring_payment(
                   amount=amount,
                   currency="EUR",
                   description=description,
                   country="LT",
                   payment_id=parent_payment_id
               )
               
               if payment['status'] == 'approved':
                   print(f"✅ Recurring payment successful on attempt {attempt + 1}")
                   return payment
               elif payment['status'] == 'declined':
                   print(f"❌ Payment declined: {payment.get('error', 'Unknown reason')}")
                   # Handle declined payment (notify customer, update subscription, etc.)
                   return None
                   
           except ValidationError as e:
               print(f"❌ Validation error on attempt {attempt + 1}: {e}")
               if attempt == max_retries - 1:
                   print("❌ Max retries reached. Payment failed.")
                   return None
               
           except APIError as e:
               print(f"⚠️ API error on attempt {attempt + 1}: {e}")
               if attempt < max_retries - 1:
                   print(f"   Retrying in 2 seconds...")
                   time.sleep(2)
               else:
                   print("❌ Max retries reached. Payment failed.")
                   return None
                   
           except CardinityError as e:
               print(f"❌ Cardinity error: {e}")
               return None
       
       return None

Subscription Management Class
----------------------------

A complete subscription management implementation:

.. code-block:: python

   class SubscriptionManager:
       """Manage customer subscriptions and recurring payments."""
       
       def __init__(self, cardinity_client):
           self.cardinity = cardinity_client
           self.subscriptions = {}  # In production, use a database
           
       def create_subscription(self, customer_id, plan_amount, plan_name):
           """Create a new subscription for a customer."""
           
           print(f"Creating subscription for customer {customer_id}...")
           
           # Create initial payment
           initial_payment = self.cardinity.create_payment(
               amount=plan_amount,
               currency="EUR",
               description=f"{plan_name} - Initial payment",
               country="LT",
               order_id=f"SUB-{customer_id}-INIT",
               payment_instrument={
                   "pan": "4111111111111111",
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "Subscription Customer"
               }
           )
           
           if initial_payment and initial_payment['status'] == 'approved':
               subscription = {
                   'customer_id': customer_id,
                   'payment_id': initial_payment['id'],
                   'plan_name': plan_name,
                   'plan_amount': plan_amount,
                   'status': 'active',
                   'created': datetime.now().isoformat(),
                   'next_billing': None
               }
               
               self.subscriptions[customer_id] = subscription
               print(f"✅ Subscription created for {customer_id}")
               return subscription
           else:
               print(f"❌ Failed to create subscription for {customer_id}")
               return None
               
       def process_recurring_payment(self, customer_id, amount=None, description=None):
           """Process a recurring payment for a customer."""
           
           if customer_id not in self.subscriptions:
               print(f"❌ No subscription found for customer {customer_id}")
               return None
               
           subscription = self.subscriptions[customer_id]
           
           if subscription['status'] != 'active':
               print(f"❌ Subscription for {customer_id} is not active")
               return None
               
           # Use subscription amount if no amount specified
           if amount is None:
               amount = subscription['plan_amount']
               
           if description is None:
               description = f"{subscription['plan_name']} - Recurring payment"
               
           payment = self.cardinity.create_recurring_payment(
               amount=amount,
               currency="EUR",
               description=description,
               country="LT",
               payment_id=subscription['payment_id']
           )
           
           if payment and payment['status'] == 'approved':
               print(f"✅ Recurring payment processed for {customer_id}")
               return payment
           else:
               print(f"❌ Recurring payment failed for {customer_id}")
               # In production, handle failed payments (retry, suspend, notify)
               return None
               
       def cancel_subscription(self, customer_id):
           """Cancel a customer's subscription."""
           
           if customer_id in self.subscriptions:
               self.subscriptions[customer_id]['status'] = 'cancelled'
               print(f"✅ Subscription cancelled for {customer_id}")
               return True
           else:
               print(f"❌ No subscription found for {customer_id}")
               return False

   # Usage example
   def subscription_manager_example():
       """Demonstrate the subscription manager."""
       
       manager = SubscriptionManager(cardinity)
       
       # Create subscription
       subscription = manager.create_subscription(
           customer_id="CUST-001",
           plan_amount="29.99",
           plan_name="Premium Plan"
       )
       
       if subscription:
           # Process recurring payments
           payment1 = manager.process_recurring_payment("CUST-001")
           payment2 = manager.process_recurring_payment("CUST-001")
           
           # Cancel subscription
           manager.cancel_subscription("CUST-001")

Best Practices for Recurring Payments
------------------------------------

.. code-block:: python

   """
   Recurring Payment Best Practices
   """

   def recurring_payment_best_practices():
       """Examples of best practices for recurring payments."""
       
       # 1. Always validate the initial payment before enabling recurring billing
       def setup_subscription_safely(customer_data, plan_data):
           initial_payment = create_initial_payment()
           
           # Only enable recurring if initial payment succeeds
           if initial_payment and initial_payment['status'] == 'approved':
               print("✅ Initial payment approved - subscription activated")
               return initial_payment['id']
           else:
               print("❌ Initial payment failed - subscription not activated")
               return None
       
       # 2. Handle failed recurring payments gracefully
       def handle_failed_recurring_payment(customer_id, payment_failure):
           """Handle failed recurring payment scenarios."""
           
           failure_reason = payment_failure.get('error', 'Unknown error')
           
           if 'insufficient funds' in failure_reason.lower():
               # Retry in a few days
               print(f"⏰ Scheduling retry for {customer_id} due to insufficient funds")
               
           elif 'expired card' in failure_reason.lower():
               # Request card update
               print(f"💳 Requesting card update for {customer_id}")
               
           elif 'card cancelled' in failure_reason.lower():
               # Suspend subscription
               print(f"⏸️ Suspending subscription for {customer_id}")
               
       # 3. Implement subscription lifecycle management
       def subscription_lifecycle_example():
           """Example of complete subscription lifecycle."""
           
           stages = {
               'trial': {'amount': '0.00', 'description': 'Free trial period'},
               'active': {'amount': '29.99', 'description': 'Active subscription'},
               'past_due': {'amount': '29.99', 'description': 'Past due payment'},
               'cancelled': {'amount': '0.00', 'description': 'Cancelled subscription'}
           }
           
           for stage, config in stages.items():
               print(f"📋 {stage.title()} stage: {config['description']}")
       
       # 4. Use meaningful descriptions and order IDs
       def create_descriptive_recurring_payment(parent_payment_id, billing_period):
           """Create recurring payment with descriptive information."""
           
           from datetime import datetime
           
           payment = cardinity.create_recurring_payment(
               amount="29.99",
               currency="EUR",
               description=f"Premium Plan - {billing_period} billing",
               country="LT",
               payment_id=parent_payment_id
           )
           
           return payment

Common Recurring Payment Scenarios
---------------------------------

Different types of recurring billing:

.. code-block:: python

   def recurring_payment_scenarios():
       """Examples of different recurring payment scenarios."""
       
       # Scenario 1: Fixed subscription (SaaS)
       def saas_subscription():
           initial = create_initial_payment()
           
           if initial and initial['status'] == 'approved':
               # Monthly SaaS billing
               monthly_payments = []
               for month in range(1, 13):  # 12 months
                   payment = create_recurring_payment(
                       initial['id'],
                       amount="49.99",
                       description=f"SaaS Premium - Month {month}"
                   )
                   monthly_payments.append(payment)
               
               return monthly_payments
       
       # Scenario 2: Usage-based billing
       def usage_based_billing():
           initial = create_initial_payment()
           
           if initial and initial['status'] == 'approved':
               # Variable usage billing
               usage_bills = [
                   {"amount": "25.99", "usage": "250 API calls"},
                   {"amount": "45.99", "usage": "750 API calls"},
                   {"amount": "89.99", "usage": "2000 API calls"}
               ]
               
               for bill in usage_bills:
                   payment = create_recurring_payment(
                       initial['id'],
                       amount=bill['amount'],
                       description=f"API Usage: {bill['usage']}"
                   )
       
       # Scenario 3: Subscription with add-ons
       def subscription_with_addons():
           initial = create_initial_payment()
           
           if initial and initial['status'] == 'approved':
               # Base subscription + add-ons
               base_payment = create_recurring_payment(
                   initial['id'],
                   amount="29.99",
                   description="Base subscription"
               )
               
               addon_payment = create_recurring_payment(
                   initial['id'],
                   amount="9.99",
                   description="Premium features add-on"
               )
               
               return [base_payment, addon_payment]

Testing Recurring Payments
--------------------------

Test your recurring payment implementation:

.. code-block:: python

   def test_recurring_payments():
       """Test suite for recurring payments."""
       
       print("🧪 Testing recurring payments...")
       
       # Test 1: Basic recurring payment
       print("\n1. Testing basic recurring payment...")
       initial = create_initial_payment()
       if initial and initial['status'] == 'approved':
           recurring = create_recurring_payment(initial['id'])
           assert recurring['status'] == 'approved', "Recurring payment should succeed"
           print("   ✅ Basic recurring payment test passed")
       
       # Test 2: Multiple recurring payments
       print("\n2. Testing multiple recurring payments...")
       if initial:
           payments = []
           for i in range(3):
               payment = create_recurring_payment(
                   initial['id'],
                   amount="10.00",
                   description=f"Test payment {i+1}"
               )
               payments.append(payment)
           
           success_count = sum(1 for p in payments if p and p['status'] == 'approved')
           print(f"   ✅ {success_count}/3 recurring payments succeeded")
       
       # Test 3: Invalid parent payment ID
       print("\n3. Testing invalid parent payment ID...")
       try:
           invalid_payment = create_recurring_payment(
               "invalid-payment-id",
               amount="10.00"
           )
           print("   ❌ Should have failed with invalid payment ID")
       except CardinityError:
           print("   ✅ Correctly handled invalid payment ID")

Production Considerations
-----------------------

Important considerations for production use:

.. code-block:: python

   """
   Production Considerations for Recurring Payments
   """

   # 1. Database schema for subscriptions
   SUBSCRIPTION_SCHEMA = {
       'customer_id': 'string',
       'initial_payment_id': 'uuid',
       'status': 'enum(active, cancelled, suspended, past_due)',
       'plan_name': 'string',
       'plan_amount': 'decimal',
       'billing_cycle': 'enum(monthly, quarterly, annually)',
       'next_billing_date': 'datetime',
       'created_at': 'datetime',
       'updated_at': 'datetime',
       'retry_count': 'integer',
       'last_payment_attempt': 'datetime'
   }

   # 2. Webhook handling for payment status updates
   def handle_payment_webhook(webhook_data):
       """Handle payment status updates via webhooks."""
       
       payment_id = webhook_data.get('payment_id')
       status = webhook_data.get('status')
       
       if status == 'declined':
           # Handle failed recurring payment
           handle_failed_payment(payment_id)
       elif status == 'approved':
           # Update subscription as paid
           update_subscription_status(payment_id, 'paid')

   # 3. Retry logic for failed payments
   def retry_failed_payment(subscription_id, max_retries=3):
       """Implement retry logic for failed recurring payments."""
       
       subscription = get_subscription(subscription_id)
       
       if subscription['retry_count'] < max_retries:
           # Attempt payment again
           payment = create_recurring_payment(
               subscription['initial_payment_id'],
               amount=subscription['plan_amount']
           )
           
           if payment['status'] == 'approved':
               # Reset retry count
               update_subscription(subscription_id, {'retry_count': 0})
           else:
               # Increment retry count
               update_subscription(subscription_id, {
                   'retry_count': subscription['retry_count'] + 1
               })
       else:
           # Suspend subscription after max retries
           update_subscription(subscription_id, {'status': 'suspended'})

Next Steps
----------

After implementing recurring payments:

1. **Webhook Integration**: Set up webhooks for real-time payment updates
2. **Customer Portal**: Build a portal for customers to manage subscriptions
3. **Analytics**: Track subscription metrics and churn rates
4. **Dunning Management**: Implement failed payment recovery workflows
5. **Plan Management**: Support plan upgrades, downgrades, and changes

Security Best Practices
-----------------------

1. **Never store raw card data** - use Cardinity's tokenization
2. **Implement PCI compliance** for handling payment data
3. **Use HTTPS** for all payment-related communications
4. **Log payment attempts** for audit trails (without sensitive data)
5. **Implement rate limiting** to prevent abuse
6. **Validate all input data** before processing payments
7. **Use environment variables** for API credentials 
