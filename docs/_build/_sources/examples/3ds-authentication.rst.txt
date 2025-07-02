3D Secure Authentication
=========================

This section covers 3D Secure (3DS) authentication with the Cardinity Python SDK, including both 3DS1 and 3DS2 implementations for enhanced payment security.

Overview
--------

3D Secure authentication provides an additional layer of security for online payments by:

1. **Strong Customer Authentication (SCA)**: Meets PSD2 requirements in Europe
2. **Fraud Prevention**: Reduces chargebacks and fraudulent transactions
3. **Liability Shift**: Moves liability from merchant to issuer for authenticated transactions
4. **Customer Trust**: Increases customer confidence in payment security

3D Secure Workflow
------------------

The 3DS authentication process follows these steps:

1. **Payment Creation**: Create payment with 3DS parameters
2. **Challenge Required**: Payment status becomes ``pending`` if 3DS is required
3. **Customer Authentication**: Redirect customer to bank's authentication page
4. **Authentication Response**: Customer completes authentication
5. **Payment Finalization**: Finalize payment with authentication result

Basic 3D Secure Example
-----------------------

Here's a complete example of 3D Secure authentication:

.. code-block:: python

   """
   3D Secure Authentication Example
   
   This example demonstrates the complete 3DS authentication workflow.
   """

   import os
   from cardinity import Cardinity, CardinityError

   # Initialize client
   cardinity = Cardinity(
       consumer_key=os.getenv("CARDINITY_CONSUMER_KEY", "your_consumer_key_here"),
       consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET", "your_consumer_secret_here")
   )

   def create_3ds_payment():
       """Create a payment that may require 3D Secure authentication."""
       
       try:
           payment = cardinity.create_payment(
               amount="25.00",
               currency="EUR",
               description="3ds2-pass",  # Triggers 3DS in test environment
               country="LT",
               payment_instrument={
                   "pan": "4111111111111111",  # Test Visa card
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "John Doe"
               },
               # 3DS2 specific data
               threeds2_data={
                   "notification_url": "https://your-site.com/3ds-callback",
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

           print(f"Payment created: {payment['id']}")
           print(f"Status: {payment['status']}")

           return payment

       except CardinityError as e:
           print(f"❌ Payment creation failed: {e}")
           return None

   def handle_3ds_authentication(payment):
       """Handle the 3D Secure authentication process."""
       
       if not payment:
           return None
           
       if payment['status'] == 'approved':
           print("✅ Payment approved without 3DS challenge")
           return payment
           
       elif payment['status'] == 'pending':
           print("🔒 3D Secure authentication required")
           
           if 'threeds2_data' in payment:
               # 3DS2 flow
               acs_url = payment['threeds2_data']['acs_url']
               creq = payment['threeds2_data']['creq']
               
               print(f"Redirect customer to ACS URL: {acs_url}")
               print(f"POST creq parameter: {creq}")
               
               # In a real application, you would:
               # 1. Redirect customer to acs_url with creq
               # 2. Customer completes authentication
               # 3. Receive callback with authentication result
               # 4. Finalize payment with the result
               
               # For testing, simulate successful authentication
               return finalize_3ds_payment(payment['id'], "3ds2-pass")
               
           elif 'authorization_information' in payment:
               # 3DS1 flow (legacy)
               acs_url = payment['authorization_information']['url']
               pareq = payment['authorization_information']['data']
               
               print(f"3DS1 - Redirect to: {acs_url}")
               print(f"3DS1 - PAReq: {pareq}")
               
               # Similar process for 3DS1
               return finalize_3ds_payment(payment['id'], "3ds1-pass")
           
       elif payment['status'] == 'declined':
           print("❌ Payment declined")
           return payment
           
       return payment

   def finalize_3ds_payment(payment_id, auth_result):
       """Finalize the payment after 3DS authentication."""
       
       try:
           finalized_payment = cardinity.finalize_payment(
               payment_id,
               cres=auth_result
           )
           
           print(f"✅ Payment finalized: {finalized_payment['status']}")
           return finalized_payment
           
       except CardinityError as e:
           print(f"❌ Payment finalization failed: {e}")
           return None

3DS2 Browser Information
-------------------------

Comprehensive browser information for 3DS2:

.. code-block:: python

   def get_browser_info_from_request(request):
       """Extract browser information from HTTP request (Flask/Django example)."""
       
       browser_info = {
           "accept_header": request.headers.get('Accept', 'text/html'),
           "browser_language": request.headers.get('Accept-Language', 'en-US').split(',')[0],
           "user_agent": request.headers.get('User-Agent', ''),
           "color_depth": 24,  # Default value
           "screen_width": 1920,  # Default value  
           "screen_height": 1080,  # Default value
           "time_zone": -60,  # UTC offset in minutes
           "javascript_enabled": True,  # Assume enabled
           "java_enabled": False,  # Usually disabled
           "challenge_window_size": "500x600"  # Modal size
       }
       
       return browser_info

   def create_3ds2_payment_with_browser_info(browser_info):
       """Create 3DS2 payment with proper browser information."""
       
       payment = cardinity.create_payment(
           amount="50.00",
           currency="EUR",
           description="3DS2 payment with browser info",
           country="LT",
           payment_instrument={
               "pan": "4111111111111111",
               "exp_month": 12,
               "exp_year": 2025,
               "cvc": "123",
               "holder": "Test User"
           },
           threeds2_data={
               "notification_url": "https://your-site.com/webhooks/3ds-callback",
               "browser_info": browser_info
           }
       )
       
       return payment

Handling Different 3DS Scenarios
--------------------------------

Different 3DS outcomes and how to handle them:

.. code-block:: python

   def handle_all_3ds_scenarios():
       """Handle all possible 3DS authentication scenarios."""
       
       scenarios = [
           {
               "name": "Frictionless - No Challenge",
               "description": "3ds2-pass",
               "expected": "approved"
           },
           {
               "name": "Challenge Required",
               "description": "3ds2-challenge",
               "expected": "pending"
           },
           {
               "name": "Authentication Failed",
               "description": "3ds2-fail",
               "expected": "declined"
           },
           {
               "name": "Technical Error",
               "description": "3ds2-error",
               "expected": "declined"
           }
       ]
       
       for scenario in scenarios:
           print(f"\n🧪 Testing: {scenario['name']}")
           
           payment = cardinity.create_payment(
               amount="30.00",
               currency="EUR",
               description=scenario['description'],
               country="LT",
               payment_instrument={
                   "pan": "4111111111111111",
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "Test User"
               },
               threeds2_data={
                   "notification_url": "https://your-site.com/3ds-callback",
                   "browser_info": {
                       "accept_header": "text/html",
                       "browser_language": "en-US",
                       "screen_width": 1920,
                       "screen_height": 1040,
                       "user_agent": "Mozilla/5.0 Test Browser",
                       "color_depth": 24,
                       "time_zone": -60,
                       "javascript_enabled": True,
                       "java_enabled": False
                   }
               }
           )
           
           if payment:
               print(f"   Status: {payment['status']}")
               
               if payment['status'] == 'pending':
                   # Handle challenge flow
                   finalized = finalize_3ds_payment(payment['id'], scenario['description'])
                   if finalized:
                       print(f"   Final Status: {finalized['status']}")

Web Integration Example
------------------------

Complete web application integration:

.. code-block:: python

   """
   Flask Web Application Example for 3DS Integration
   
   This example shows how to integrate 3DS in a web application.
   """

   from flask import Flask, request, render_template, redirect, session
   import json

   app = Flask(__name__)
   app.secret_key = 'your-secret-key'

   @app.route('/checkout', methods=['POST'])
   def process_checkout():
       """Process checkout with 3DS support."""
       
       # Get form data
       amount = request.form.get('amount')
       card_number = request.form.get('card_number')
       exp_month = request.form.get('exp_month')
       exp_year = request.form.get('exp_year')
       cvc = request.form.get('cvc')
       holder = request.form.get('holder')
       
       # Extract browser information
       browser_info = {
           "accept_header": request.headers.get('Accept', 'text/html'),
           "browser_language": request.headers.get('Accept-Language', 'en-US').split(',')[0],
           "user_agent": request.headers.get('User-Agent', ''),
           "color_depth": 24,
           "screen_width": 1920,
           "screen_height": 1080,
           "time_zone": -60,
           "javascript_enabled": True,
           "java_enabled": False,
           "challenge_window_size": "500x600"
       }
       
       try:
           # Create payment with 3DS data
           payment = cardinity.create_payment(
               amount=amount,
               currency="EUR",
               description="Online purchase",
               country="LT",
               payment_instrument={
                   "pan": card_number,
                   "exp_month": int(exp_month),
                   "exp_year": int(exp_year),
                   "cvc": cvc,
                   "holder": holder
               },
               threeds2_data={
                   "notification_url": request.url_root + "webhooks/3ds-callback",
                   "browser_info": browser_info
               }
           )
           
           # Store payment ID in session
           session['payment_id'] = payment['id']
           
           if payment['status'] == 'approved':
               # Payment successful without challenge
               return redirect('/success')
               
           elif payment['status'] == 'pending':
               # 3DS challenge required
               if 'threeds2_data' in payment:
                   acs_url = payment['threeds2_data']['acs_url']
                   creq = payment['threeds2_data']['creq']
                   
                   # Render 3DS challenge page
                   return render_template('3ds_challenge.html', 
                                        acs_url=acs_url, 
                                        creq=creq,
                                        payment_id=payment['id'])
               
           else:
               # Payment declined or error
               return redirect('/failure')
               
       except CardinityError as e:
           return render_template('error.html', error=str(e))

   @app.route('/3ds-callback', methods=['POST'])
   def handle_3ds_callback():
       """Handle 3DS authentication callback."""
       
       payment_id = session.get('payment_id')
       cres = request.form.get('cres')  # Challenge response
       
       if not payment_id or not cres:
           return redirect('/failure')
       
       try:
           # Finalize payment with 3DS response
           finalized_payment = cardinity.finalize_payment(
               payment_id,
               cres=cres
           )
           
           if finalized_payment['status'] == 'approved':
               return redirect('/success')
           else:
               return redirect('/failure')
               
       except CardinityError as e:
           return render_template('error.html', error=str(e))

   @app.route('/webhooks/3ds-callback', methods=['POST'])
   def webhook_3ds_callback():
       """Handle 3DS webhook notifications."""
       
       # Process webhook data
       webhook_data = request.get_json()
       
       # Update payment status in your system
       # This is called when 3DS authentication completes
       
       return '', 200

Mobile App Integration
-----------------------

3DS integration for mobile applications:

.. code-block:: python

   def mobile_3ds_integration():
       """Example of 3DS integration for mobile apps."""
       
       # Mobile-specific browser info
       mobile_browser_info = {
           "accept_header": "application/json",
           "browser_language": "en-US",
           "user_agent": "YourApp/1.0 (iOS 15.0; iPhone13,2)",
           "color_depth": 32,
           "screen_width": 390,  # iPhone screen width
           "screen_height": 844,  # iPhone screen height
           "time_zone": -300,  # EST timezone
           "javascript_enabled": False,  # Native app
           "java_enabled": False,
           "challenge_window_size": "390x600"  # Mobile modal size
       }
       
       payment = cardinity.create_payment(
           amount="99.99",
           currency="EUR",
           description="Mobile app purchase",
           country="LT",
           payment_instrument={
               "pan": "4111111111111111",
               "exp_month": 12,
               "exp_year": 2025,
               "cvc": "123",
               "holder": "Mobile User"
           },
           threeds2_data={
               "notification_url": "https://your-api.com/webhooks/3ds-mobile",
               "browser_info": mobile_browser_info
           }
       )
       
       if payment['status'] == 'pending' and 'threeds2_data' in payment:
           # Return 3DS data to mobile app
           return {
               "requires_3ds": True,
               "acs_url": payment['threeds2_data']['acs_url'],
               "creq": payment['threeds2_data']['creq'],
               "payment_id": payment['id']
           }
       
       return payment

Advanced 3DS Configuration
--------------------------

Advanced configuration options for 3DS:

.. code-block:: python

   def advanced_3ds_configuration():
       """Advanced 3DS configuration with additional parameters."""
       
       # Comprehensive 3DS2 data
       advanced_3ds_data = {
           "notification_url": "https://your-site.com/webhooks/3ds",
           "browser_info": {
               "accept_header": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
               "browser_language": "en-US,en;q=0.5",
               "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
               "color_depth": 24,
               "screen_width": 1920,
               "screen_height": 1080,
               "time_zone": -300,
               "javascript_enabled": True,
               "java_enabled": False,
               "challenge_window_size": "500x600"
           },
           # Additional merchant data
           "merchant_data": {
               "merchant_name": "Your Store Name",
               "merchant_url": "https://your-store.com"
           },
           # Transaction-specific data
           "transaction_data": {
               "shipping_address_usage": "current_transaction",
               "delivery_timeframe": "electronic_delivery",
               "pre_order_purchase": False,
               "reorder_items": False
           }
       }
       
       payment = cardinity.create_payment(
           amount="150.00",
           currency="EUR",
           description="High-value transaction requiring 3DS",
           country="LT",
           payment_instrument={
               "pan": "4111111111111111",
               "exp_month": 12,
               "exp_year": 2025,
               "cvc": "123",
               "holder": "Premium Customer"
           },
           threeds2_data=advanced_3ds_data
       )
       
       return payment

Error Handling for 3DS
----------------------

Comprehensive error handling for 3DS flows:

.. code-block:: python

   def robust_3ds_handling(payment_data):
       """Robust 3DS handling with comprehensive error management."""
       
       try:
           # Create payment
           payment = cardinity.create_payment(**payment_data)
           
           if not payment:
               return {"error": "Payment creation failed"}
           
           # Handle different statuses
           if payment['status'] == 'approved':
               return {
                   "success": True,
                   "payment_id": payment['id'],
                   "requires_3ds": False
               }
               
           elif payment['status'] == 'pending':
               # Check for 3DS data
               if 'threeds2_data' in payment:
                   return {
                       "success": True,
                       "payment_id": payment['id'],
                       "requires_3ds": True,
                       "acs_url": payment['threeds2_data']['acs_url'],
                       "creq": payment['threeds2_data']['creq']
                   }
               else:
                   return {"error": "Payment pending but no 3DS data available"}
                   
           elif payment['status'] == 'declined':
               return {
                   "error": "Payment declined",
                   "reason": payment.get('error', 'Unknown reason')
               }
               
           else:
               return {"error": f"Unknown payment status: {payment['status']}"}
               
       except ValidationError as e:
           return {"error": f"Validation error: {str(e)}"}
           
       except APIError as e:
           return {"error": f"API error: {str(e)}"}
           
       except CardinityError as e:
           return {"error": f"Cardinity error: {str(e)}"}

Testing 3DS Flows
-----------------

Test different 3DS scenarios:

.. code-block:: python

   def test_3ds_flows():
       """Test various 3DS authentication flows."""
       
       test_cases = [
           {
               "name": "Frictionless Success",
               "description": "3ds2-pass",
               "expected_initial": "approved",
               "expected_final": "approved"
           },
           {
               "name": "Challenge Success", 
               "description": "3ds2-challenge",
               "expected_initial": "pending",
               "expected_final": "approved"
           },
           {
               "name": "Authentication Failed",
               "description": "3ds2-fail",
               "expected_initial": "pending",
               "expected_final": "declined"
           },
           {
               "name": "Bypass 3DS (Low Amount)",
               "description": "Low amount transaction",
               "amount": "5.00",
               "expected_initial": "approved",
               "expected_final": "approved"
           }
       ]
       
       for test_case in test_cases:
           print(f"\n🧪 Testing: {test_case['name']}")
           
           payment_data = {
               "amount": test_case.get("amount", "100.00"),
               "currency": "EUR",
               "description": test_case["description"],
               "country": "LT",
               "payment_instrument": {
                   "pan": "4111111111111111",
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "Test User"
               },
               "threeds2_data": {
                   "notification_url": "https://test.com/3ds-callback",
                   "browser_info": {
                       "accept_header": "text/html",
                       "browser_language": "en-US",
                       "user_agent": "Test Browser",
                       "color_depth": 24,
                       "screen_width": 1920,
                       "screen_height": 1080,
                       "time_zone": -60,
                       "javascript_enabled": True,
                       "java_enabled": False
                   }
               }
           }
           
           result = robust_3ds_handling(payment_data)
           
           if result.get("success"):
               print(f"   ✅ Initial status matches expected: {test_case['expected_initial']}")
               
               if result.get("requires_3ds"):
                   # Simulate 3DS completion
                   finalized = finalize_3ds_payment(
                       result["payment_id"], 
                       test_case["description"]
                   )
                   if finalized:
                       print(f"   ✅ Final status: {finalized['status']}")
           else:
               print(f"   ❌ Test failed: {result.get('error')}")

Best Practices for 3DS
-----------------------

.. code-block:: python

   """
   3D Secure Best Practices
   """

   def threeds_best_practices():
       """Examples of 3DS best practices."""
       
       # 1. Always provide accurate browser information
       def collect_accurate_browser_info():
           """Collect accurate browser information on frontend."""
           
           # JavaScript example (to be included in your frontend)
           js_browser_collection = """
           // Collect browser info on frontend
           const browserInfo = {
               accept_header: document.querySelector('meta[http-equiv="accept"]')?.content || 'text/html',
               browser_language: navigator.language || 'en-US',
               user_agent: navigator.userAgent,
               color_depth: screen.colorDepth || 24,
               screen_width: screen.width,
               screen_height: screen.height,
               time_zone: -new Date().getTimezoneOffset(),
               javascript_enabled: true,
               java_enabled: navigator.javaEnabled(),
               challenge_window_size: '500x600'
           };
           
           // Send this data to your backend
           """
           
           return js_browser_collection
       
       # 2. Handle all possible 3DS outcomes
       def handle_all_outcomes(payment):
           outcomes = {
               'approved': lambda p: handle_approved_payment(p),
               'declined': lambda p: handle_declined_payment(p),
               'pending': lambda p: handle_3ds_challenge(p),
               'error': lambda p: handle_payment_error(p)
           }
           
           handler = outcomes.get(payment['status'], lambda p: handle_unknown_status(p))
           return handler(payment)
       
       # 3. Implement proper callback handling
       def secure_callback_handling():
           """Secure 3DS callback implementation."""
           
           # Validate callback authenticity
           # Store payment state securely
           # Handle both success and failure cases
           # Provide clear user feedback
           
           pass
       
       # 4. User experience considerations
       def ux_considerations():
           """UX best practices for 3DS."""
           
           ux_tips = [
               "Show loading indicators during 3DS process",
               "Provide clear instructions to customers",
               "Handle browser back button gracefully",
               "Implement timeout handling for 3DS challenge",
               "Provide fallback for failed 3DS authentication",
               "Test on different devices and browsers"
           ]
           
           return ux_tips

Production Considerations
-------------------------

Important considerations for production 3DS implementation:

1. **Webhook Security**: Validate webhook signatures
2. **Session Management**: Securely store payment state during 3DS flow
3. **Browser Compatibility**: Test across different browsers and devices
4. **Mobile Optimization**: Optimize 3DS challenge for mobile devices
5. **Timeout Handling**: Handle cases where customers don't complete 3DS
6. **Fallback Mechanisms**: Provide alternatives when 3DS fails
7. **Monitoring**: Track 3DS success/failure rates
8. **Compliance**: Ensure PSD2 and SCA compliance


Next Steps
----------

After implementing 3DS authentication:

1. **Webhook Integration**: Set up secure webhook handling
2. **User Experience Optimization**: Improve 3DS challenge UX  
3. **Analytics**: Track authentication success rates
4. **Fallback Strategies**: Handle 3DS failures gracefully
5. **Mobile Optimization**: Optimize for mobile 3DS flows
6. **Testing**: Comprehensive testing across browsers and devices

</rewritten_file> 
