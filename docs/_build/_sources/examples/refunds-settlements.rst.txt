Refunds and Settlements
=======================

This section covers refund processing and settlement management with the Cardinity Python SDK, including full refunds, partial refunds, and settlement operations.

Overview
--------

Refund and settlement operations include:

1. **Full Refunds**: Refund the entire payment amount
2. **Partial Refunds**: Refund a portion of the payment amount
3. **Multiple Refunds**: Process multiple partial refunds for one payment
4. **Settlement Management**: Handle authorization settlements
5. **Void Operations**: Cancel unsettled authorizations

Basic Refund Processing
----------------------

Here's how to process refunds:

.. code-block:: python

   """
   Basic Refund Example
   
   This example demonstrates how to process refunds for payments.
   """

   import os
   from cardinity import Cardinity, CardinityError

   # Initialize client
   cardinity = Cardinity(
       consumer_key=os.getenv("CARDINITY_CONSUMER_KEY", "your_consumer_key_here"),
       consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET", "your_consumer_secret_here")
   )

   def create_test_payment():
       """Create a test payment for refund examples."""
       
       try:
           payment = cardinity.create_payment(
               amount="50.00",
               currency="EUR",
               description="Test payment for refund",
               country="LT",
               payment_instrument={
                   "pan": "4111111111111111",
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "Test Customer"
               }
           )

           print(f"✅ Test payment created: {payment['id']}")
           print(f"   Amount: {payment['amount']} {payment['currency']}")
           print(f"   Status: {payment['status']}")

           return payment

       except CardinityError as e:
           print(f"❌ Test payment failed: {e}")
           return None

   def create_full_refund(payment_id):
       """Create a full refund for a payment."""
       
       try:
           # Get original payment details
           original_payment = cardinity.get_payment(payment_id)
           
           if not original_payment:
               print("❌ Could not retrieve original payment")
               return None
           
           # Create full refund
           refund = cardinity.create_refund(
               payment_id=payment_id,
               amount=original_payment['amount'],  # Full amount
               description="Full refund - Customer not satisfied"
           )

           print(f"✅ Full refund created: {refund['id']}")
           print(f"   Refund Amount: {refund['amount']} {refund['currency']}")
           print(f"   Status: {refund['status']}")
           print(f"   Original Payment: {payment_id}")

           return refund

       except CardinityError as e:
           print(f"❌ Full refund failed: {e}")
           return None

   def create_partial_refund(payment_id, amount, description):
       """Create a partial refund for a payment."""
       
       try:
           refund = cardinity.create_refund(
               payment_id=payment_id,
               amount=amount,
               description=description or f"Partial refund - {amount}"
           )

           print(f"✅ Partial refund created: {refund['id']}")
           print(f"   Refund Amount: {refund['amount']} {refund['currency']}")
           print(f"   Status: {refund['status']}")
           print(f"   Description: {refund['description']}")

           return refund

       except CardinityError as e:
           print(f"❌ Partial refund failed: {e}")
           return None

Multiple Partial Refunds
------------------------

Handle multiple partial refunds for a single payment:

.. code-block:: python

   def process_multiple_refunds():
       """Example of processing multiple partial refunds."""
       
       # Create test payment
       payment = create_test_payment()
       
       if not payment or payment['status'] != 'approved':
           print("❌ Cannot process refunds - payment not approved")
           return
       
       print(f"\n💰 Original payment: {payment['amount']} EUR")
       print("Processing multiple partial refunds...")
       
       # Define refund scenarios
       refund_scenarios = [
           {"amount": "15.00", "reason": "Shipping refund"},
           {"amount": "10.00", "reason": "Product discount"},
           {"amount": "5.00", "reason": "Service fee refund"}
       ]
       
       total_refunded = 0.0
       successful_refunds = []
       
       for scenario in refund_scenarios:
           print(f"\n   🔄 Processing refund: {scenario['amount']} EUR - {scenario['reason']}")
           
           refund = create_partial_refund(
               payment['id'],
               scenario['amount'],
               scenario['reason']
           )
           
           if refund and refund['status'] == 'approved':
               successful_refunds.append(refund)
               total_refunded += float(scenario['amount'])
               print(f"      ✅ Refund successful")
           else:
               print(f"      ❌ Refund failed")
       
       print(f"\n📊 Refund Summary:")
       print(f"   Original Amount: {payment['amount']} EUR")
       print(f"   Total Refunded: {total_refunded:.2f} EUR")
       print(f"   Remaining: {float(payment['amount']) - total_refunded:.2f} EUR")
       print(f"   Successful Refunds: {len(successful_refunds)}")
       
       return successful_refunds

Refund Status Management
-----------------------

Handle different refund statuses:

.. code-block:: python

   def check_refund_status(refund_id):
       """Check and handle refund status."""
       
       try:
           refund = cardinity.get_refund(refund_id)
           
           status = refund['status']
           
           if status == 'approved':
               print(f"✅ Refund {refund_id} approved")
               print(f"   Amount: {refund['amount']} {refund['currency']}")
               print(f"   Processed: {refund.get('created', 'Unknown')}")
               
           elif status == 'pending':
               print(f"⏳ Refund {refund_id} pending")
               print("   Refund is being processed by the bank")
               
           elif status == 'declined':
               print(f"❌ Refund {refund_id} declined")
               if 'error' in refund:
                   print(f"   Reason: {refund['error']}")
               
           else:
               print(f"⚠️ Unknown refund status: {status}")
           
           return refund
           
       except CardinityError as e:
           print(f"❌ Failed to check refund status: {e}")
           return None

   def monitor_refund_processing(refund_id, max_checks=10, interval=30):
       """Monitor refund processing until completion."""
       
       import time
       
       for attempt in range(max_checks):
           print(f"🔍 Checking refund status (attempt {attempt + 1}/{max_checks})...")
           
           refund = check_refund_status(refund_id)
           
           if not refund:
               break
               
           if refund['status'] in ['approved', 'declined']:
               print(f"✅ Refund processing completed with status: {refund['status']}")
               return refund
               
           print(f"   Still pending... checking again in {interval} seconds")
           time.sleep(interval)
       
       print("⚠️ Refund monitoring timed out")
       return None

E-commerce Refund Scenarios
---------------------------

Real-world e-commerce refund examples:

.. code-block:: python

   class ECommerceRefundManager:
       """Manage e-commerce refunds with business logic."""
       
       def __init__(self, cardinity_client):
           self.cardinity = cardinity_client
           
       def process_order_cancellation(self, payment_id, order_details):
           """Process full refund for order cancellation."""
           
           print(f"🛒 Processing order cancellation for payment {payment_id}")
           
           # Check if order can be cancelled
           if order_details.get('status') == 'shipped':
               print("❌ Cannot cancel shipped order")
               return None
           
           # Create full refund
           refund = self.cardinity.create_refund(
               payment_id=payment_id,
               amount=order_details['total_amount'],
               description=f"Order cancellation - Order #{order_details['order_id']}"
           )
           
           if refund and refund['status'] == 'approved':
               print(f"✅ Order cancellation refund processed: {refund['amount']} EUR")
               return refund
           else:
               print("❌ Order cancellation refund failed")
               return None
       
       def process_return_refund(self, payment_id, returned_items):
           """Process refund for returned items."""
           
           print(f"📦 Processing return refund for payment {payment_id}")
           
           total_refund = 0.0
           refund_description_parts = []
           
           for item in returned_items:
               item_refund = float(item['price']) * int(item['quantity'])
               total_refund += item_refund
               refund_description_parts.append(f"{item['name']} x{item['quantity']}")
           
           description = f"Return refund: {', '.join(refund_description_parts)}"
           
           refund = self.cardinity.create_refund(
               payment_id=payment_id,
               amount=f"{total_refund:.2f}",
               description=description
           )
           
           if refund and refund['status'] == 'approved':
               print(f"✅ Return refund processed: {refund['amount']} EUR")
               return refund
           else:
               print("❌ Return refund failed")
               return None
       
       def process_partial_service_refund(self, payment_id, service_issue):
           """Process partial refund for service issues."""
           
           print(f"🔧 Processing service issue refund for payment {payment_id}")
           
           # Calculate refund based on issue severity
           refund_percentages = {
               'minor': 0.10,    # 10% refund
               'moderate': 0.25, # 25% refund
               'major': 0.50,    # 50% refund
               'critical': 1.0   # Full refund
           }
           
           severity = service_issue.get('severity', 'minor')
           original_amount = float(service_issue['original_amount'])
           refund_percentage = refund_percentages.get(severity, 0.10)
           refund_amount = original_amount * refund_percentage
           
           refund = self.cardinity.create_refund(
               payment_id=payment_id,
               amount=f"{refund_amount:.2f}",
               description=f"Service issue refund ({severity}): {service_issue['description']}"
           )
           
           if refund and refund['status'] == 'approved':
               print(f"✅ Service issue refund processed: {refund['amount']} EUR ({severity})")
               return refund
           else:
               print("❌ Service issue refund failed")
               return None

Settlement Operations
--------------------

Handle authorization settlements:

.. code-block:: python

   def create_authorization_payment():
       """Create an authorization-only payment for settlement examples."""
       
       try:
           payment = cardinity.create_payment(
               amount="100.00",
               currency="EUR",
               description="Authorization for settlement",
               country="LT",
               settle=False,  # Authorization only, no immediate settlement
               payment_instrument={
                   "pan": "4111111111111111",
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "Auth Customer"
               }
           )

           print(f"✅ Authorization created: {payment['id']}")
           print(f"   Amount: {payment['amount']} {payment['currency']}")
           print(f"   Status: {payment['status']}")
           print("   ⚠️ Remember to settle within 7 days!")

           return payment

       except CardinityError as e:
           print(f"❌ Authorization failed: {e}")
           return None

   def settle_authorization(payment_id, amount=None, description=None):
       """Settle an authorization payment."""
       
       try:
           # Get original authorization
           auth_payment = cardinity.get_payment(payment_id)
           
           if not auth_payment:
               print("❌ Could not retrieve authorization")
               return None
           
           # Use original amount if no amount specified
           if amount is None:
               amount = auth_payment['amount']
           
           if description is None:
               description = f"Settlement for authorization {payment_id}"
           
           # Create settlement
           settlement = cardinity.create_settlement(
               payment_id=payment_id,
               amount=amount,
               description=description
           )

           print(f"✅ Settlement created: {settlement['id']}")
           print(f"   Settlement Amount: {settlement['amount']} {settlement['currency']}")
           print(f"   Status: {settlement['status']}")
           print(f"   Authorization: {payment_id}")

           return settlement

       except CardinityError as e:
           print(f"❌ Settlement failed: {e}")
           return None

   def partial_settlement_example():
       """Example of partial settlement workflow."""
       
       # Create authorization
       auth_payment = create_authorization_payment()
       
       if not auth_payment or auth_payment['status'] != 'approved':
           print("❌ Cannot proceed with settlement - authorization failed")
           return
       
       print("\n💰 Processing partial settlements...")
       
       # Partial settlement 1 - 60% of original amount
       settlement1 = settle_authorization(
           auth_payment['id'],
           amount="60.00",
           description="Partial settlement - First shipment"
       )
       
       # Partial settlement 2 - Remaining 40%
       settlement2 = settle_authorization(
           auth_payment['id'],
           amount="40.00",
           description="Partial settlement - Second shipment"
       )
       
       if settlement1 and settlement2:
           print("\n✅ All partial settlements completed")
           print(f"   Settlement 1: {settlement1['amount']} EUR")
           print(f"   Settlement 2: {settlement2['amount']} EUR")
           print(f"   Total Settled: {float(settlement1['amount']) + float(settlement2['amount'])} EUR")

Void Operations
--------------

Cancel unsettled authorizations:

.. code-block:: python

   def void_authorization(payment_id, description=None):
       """Void an unsettled authorization."""
       
       try:
           if description is None:
               description = f"Void authorization {payment_id}"
           
           void = cardinity.create_void(
               payment_id=payment_id,
               description=description
           )

           print(f"✅ Authorization voided: {void['id']}")
           print(f"   Status: {void['status']}")
           print(f"   Voided Payment: {payment_id}")

           return void

       except CardinityError as e:
           print(f"❌ Void failed: {e}")
           return None

   def authorization_lifecycle_example():
       """Complete authorization lifecycle example."""
       
       print("🔄 Authorization Lifecycle Example")
       
       # Step 1: Create authorization
       print("\n1. Creating authorization...")
       auth_payment = create_authorization_payment()
       
       if not auth_payment or auth_payment['status'] != 'approved':
           print("❌ Authorization failed - cannot continue")
           return
       
       # Step 2: Decision point - settle or void
       print("\n2. Decision: Settle or Void?")
       
       # Simulate business logic decision
       should_settle = True  # This would be based on your business logic
       
       if should_settle:
           print("   📋 Decision: Settle authorization")
           
           # Step 3a: Settle authorization
           print("\n3. Settling authorization...")
           settlement = settle_authorization(
               auth_payment['id'],
               description="Final settlement after order confirmation"
           )
           
           if settlement:
               print(f"✅ Authorization lifecycle completed with settlement")
           else:
               print("❌ Settlement failed")
       else:
           print("   📋 Decision: Void authorization")
           
           # Step 3b: Void authorization
           print("\n3. Voiding authorization...")
           void = void_authorization(
               auth_payment['id'],
               description="Order cancelled - voiding authorization"
           )
           
           if void:
               print(f"✅ Authorization lifecycle completed with void")
           else:
               print("❌ Void failed")

Advanced Refund Management
-------------------------

Advanced refund scenarios with business logic:

.. code-block:: python

   class AdvancedRefundManager:
       """Advanced refund management with business rules."""
       
       def __init__(self, cardinity_client):
           self.cardinity = cardinity_client
           self.refund_policies = {
               'full_refund_days': 30,
               'partial_refund_days': 60,
               'no_refund_days': 90,
               'restocking_fee': 0.15  # 15%
           }
       
       def calculate_refund_eligibility(self, payment_date, refund_request_date, order_type):
           """Calculate refund eligibility based on business rules."""
           
           from datetime import datetime, timedelta
           
           # Parse dates
           payment_dt = datetime.fromisoformat(payment_date.replace('Z', '+00:00'))
           request_dt = datetime.fromisoformat(refund_request_date.replace('Z', '+00:00'))
           
           days_elapsed = (request_dt - payment_dt).days
           
           # Determine refund policy
           if days_elapsed <= self.refund_policies['full_refund_days']:
               return {
                   'eligible': True,
                   'refund_type': 'full',
                   'percentage': 1.0,
                   'reason': f"Within {self.refund_policies['full_refund_days']} days"
               }
           elif days_elapsed <= self.refund_policies['partial_refund_days']:
               # Apply partial refund with restocking fee
               percentage = 1.0 - self.refund_policies['restocking_fee']
               return {
                   'eligible': True,
                   'refund_type': 'partial',
                   'percentage': percentage,
                   'reason': f"Restocking fee applied ({self.refund_policies['restocking_fee']*100}%)"
               }
           elif days_elapsed <= self.refund_policies['no_refund_days']:
               return {
                   'eligible': False,
                   'refund_type': 'none',
                   'percentage': 0.0,
                   'reason': f"Beyond {self.refund_policies['partial_refund_days']} day partial refund window"
               }
           else:
               return {
                   'eligible': False,
                   'refund_type': 'none',
                   'percentage': 0.0,
                   'reason': f"Beyond {self.refund_policies['no_refund_days']} day refund window"
               }
       
       def process_policy_based_refund(self, payment_id, refund_request):
           """Process refund based on business policies."""
           
           # Get original payment
           payment = self.cardinity.get_payment(payment_id)
           
           if not payment:
               return {'error': 'Payment not found'}
           
           # Check eligibility
           eligibility = self.calculate_refund_eligibility(
               payment['created'],
               refund_request['request_date'],
               refund_request.get('order_type', 'standard')
           )
           
           if not eligibility['eligible']:
               return {
                   'error': 'Refund not eligible',
                   'reason': eligibility['reason']
               }
           
           # Calculate refund amount
           original_amount = float(payment['amount'])
           refund_amount = original_amount * eligibility['percentage']
           
           # Create refund
           try:
               refund = self.cardinity.create_refund(
                   payment_id=payment_id,
                   amount=f"{refund_amount:.2f}",
                   description=f"Policy-based refund: {eligibility['reason']}"
               )
               
               return {
                   'success': True,
                   'refund': refund,
                   'eligibility': eligibility,
                   'refund_amount': refund_amount,
                   'original_amount': original_amount
               }
           
           except CardinityError as e:
               return {'error': f'Cardinity error: {str(e)}'}

Error Handling for Refunds
--------------------------

Comprehensive error handling for refund operations:

.. code-block:: python

   from cardinity import ValidationError, APIError

   def robust_refund_processing(payment_id, amount, description, max_retries=3):
       """Process refund with robust error handling."""
       
       for attempt in range(max_retries):
           try:
               # Validate refund eligibility first
               payment = cardinity.get_payment(payment_id)
               
               if not payment:
                   return {'error': 'Payment not found'}
               
               if payment['status'] != 'approved':
                   return {'error': f'Cannot refund payment with status: {payment["status"]}'}
               
               # Check refund amount doesn't exceed original
               if float(amount) > float(payment['amount']):
                   return {'error': 'Refund amount exceeds original payment amount'}
               
               # Attempt refund
               refund = cardinity.create_refund(
                   payment_id=payment_id,
                   amount=amount,
                   description=description
               )
               
               if refund['status'] == 'approved':
                   return {
                       'success': True,
                       'refund': refund,
                       'attempt': attempt + 1
                   }
               elif refund['status'] == 'declined':
                   return {
                       'error': 'Refund declined',
                       'reason': refund.get('error', 'Unknown reason')
                   }
               
           except ValidationError as e:
               return {'error': f'Validation error: {str(e)}'}
               
           except APIError as e:
               if attempt < max_retries - 1:
                   print(f"⚠️ API error on attempt {attempt + 1}, retrying...")
                   time.sleep(2 ** attempt)  # Exponential backoff
                   continue
               else:
                   return {'error': f'API error after {max_retries} attempts: {str(e)}'}
                   
           except CardinityError as e:
               return {'error': f'Cardinity error: {str(e)}'}
       
       return {'error': f'Failed after {max_retries} attempts'}

Testing Refund Operations
-------------------------

Test suite for refund functionality:

.. code-block:: python

   def test_refund_operations():
       """Comprehensive test suite for refund operations."""
       
       print("🧪 Testing Refund Operations")
       
       # Test 1: Full refund
       print("\n1. Testing full refund...")
       test_payment = create_test_payment()
       
       if test_payment and test_payment['status'] == 'approved':
           full_refund = create_full_refund(test_payment['id'])
           assert full_refund['status'] == 'approved', "Full refund should be approved"
           print("   ✅ Full refund test passed")
       
       # Test 2: Partial refund
       print("\n2. Testing partial refund...")
       if test_payment:
           partial_refund = create_partial_refund(
               test_payment['id'],
               "25.00",
               "Partial refund test"
           )
           assert partial_refund['status'] == 'approved', "Partial refund should be approved"
           print("   ✅ Partial refund test passed")
       
       # Test 3: Multiple partial refunds
       print("\n3. Testing multiple partial refunds...")
       test_payment2 = create_test_payment()
       
       if test_payment2 and test_payment2['status'] == 'approved':
           refunds = []
           refund_amounts = ["10.00", "15.00", "20.00"]
           
           for amount in refund_amounts:
               refund = create_partial_refund(
                   test_payment2['id'],
                   amount,
                   f"Multiple refund test - {amount}"
               )
               refunds.append(refund)
           
           successful_refunds = [r for r in refunds if r and r['status'] == 'approved']
           print(f"   ✅ {len(successful_refunds)}/{len(refund_amounts)} refunds successful")
       
       # Test 4: Invalid refund scenarios
       print("\n4. Testing invalid refund scenarios...")
       
       # Test invalid payment ID
       invalid_refund = create_partial_refund(
           "invalid-payment-id",
           "10.00",
           "Invalid test"
       )
       assert invalid_refund is None, "Invalid payment ID should fail"
       print("   ✅ Invalid payment ID handled correctly")

Best Practices
--------------

.. code-block:: python

   """
   Refund and Settlement Best Practices
   """

   def refund_best_practices():
       """Examples of refund best practices."""
       
       practices = [
           {
               "practice": "Validate refund eligibility",
               "example": "Check payment status, amount limits, and business rules"
           },
           {
               "practice": "Use descriptive refund descriptions",
               "example": "Include order ID, reason, and item details"
           },
           {
               "practice": "Track refund status",
               "example": "Monitor refund processing and notify customers"
           },
           {
               "practice": "Handle partial refunds carefully",
               "example": "Ensure total refunds don't exceed original amount"
           },
           {
               "practice": "Implement retry logic",
               "example": "Handle temporary API failures gracefully"
           },
           {
               "practice": "Maintain audit trails",
               "example": "Log all refund operations for compliance"
           },
           {
               "practice": "Set up proper authorization windows",
               "example": "Settle or void authorizations within 7 days"
           }
       ]
       
       for practice in practices:
           print(f"• {practice['practice']}: {practice['example']}")

Production Considerations
-----------------------

Important considerations for production use:

1. **Refund Policies**: Implement clear refund policies and time limits
2. **Amount Validation**: Ensure refunds don't exceed original payment amounts
3. **Status Tracking**: Monitor refund processing status and timing
4. **Customer Communication**: Notify customers of refund status changes
5. **Audit Trails**: Maintain detailed logs of all refund operations
6. **Business Rules**: Implement business-specific refund logic
7. **Settlement Timing**: Manage authorization settlement windows properly
8. **Error Handling**: Handle all possible error scenarios gracefully

Next Steps
----------

After implementing refunds and settlements:

1. **Webhook Integration**: Set up webhooks for refund status updates
2. **Customer Portal**: Allow customers to track refund status
3. **Analytics**: Monitor refund rates and patterns
4. **Automation**: Automate refund processing based on business rules
5. **Compliance**: Ensure refund processes meet regulatory requirements 
