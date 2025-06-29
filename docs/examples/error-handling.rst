Error Handling
==============

This section covers comprehensive error handling with the Cardinity Python SDK, including exception types, retry strategies, and robust error management patterns.

Overview
--------

Effective error handling includes:

1. **Exception Types**: Understanding different Cardinity exceptions
2. **Validation Errors**: Handling input validation failures
3. **API Errors**: Managing network and API communication issues
4. **Payment Errors**: Handling payment-specific failures
5. **Retry Strategies**: Implementing intelligent retry logic
6. **Logging**: Proper error logging and monitoring

Exception Types
--------------

The Cardinity SDK provides several exception types:

.. code-block:: python

   """
   Cardinity Exception Types
   
   Understanding and handling different exception types.
   """

   import os
   from cardinity import (
       Cardinity, 
       CardinityError,      # Base exception
       ValidationError,     # Input validation failures
       APIError,           # API communication issues
       AuthenticationError, # Authentication failures
       NotFoundError,      # Resource not found
       RateLimitError      # Rate limiting
   )

   # Initialize client
   cardinity = Cardinity(
       consumer_key=os.getenv("CARDINITY_CONSUMER_KEY", "your_consumer_key_here"),
       consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET", "your_consumer_secret_here")
   )

   def demonstrate_exception_types():
       """Demonstrate different exception types and how to handle them."""
       
       # 1. Validation Error Example
       try:
           payment = cardinity.create_payment(
               amount="invalid_amount",  # Invalid amount format
               currency="EUR",
               description="Test payment",
               country="LT",
               payment_instrument={
                   "pan": "4111111111111111",
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "Test User"
               }
           )
       except ValidationError as e:
           print(f"❌ Validation Error: {e}")
           print("   Check your input data format and required fields")
       
       # 2. Authentication Error Example
       try:
           invalid_client = Cardinity(
               consumer_key="invalid_key",
               consumer_secret="invalid_secret"
           )
           payment = invalid_client.create_payment(
               amount="10.00",
               currency="EUR",
               description="Test",
               country="LT",
               payment_instrument={
                   "pan": "4111111111111111",
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "Test User"
               }
           )
       except AuthenticationError as e:
           print(f"❌ Authentication Error: {e}")
           print("   Check your API credentials")
       
       # 3. Not Found Error Example
       try:
           payment = cardinity.get_payment("non-existent-payment-id")
       except NotFoundError as e:
           print(f"❌ Not Found Error: {e}")
           print("   The requested resource does not exist")
       
       # 4. General API Error Example
       try:
           # This might cause an API error depending on server state
           payment = cardinity.create_payment(
               amount="10.00",
               currency="INVALID_CURRENCY",  # Invalid currency
               description="Test",
               country="LT",
               payment_instrument={
                   "pan": "4111111111111111",
                   "exp_month": 12,
                   "exp_year": 2025,
                   "cvc": "123",
                   "holder": "Test User"
               }
           )
       except APIError as e:
           print(f"❌ API Error: {e}")
           print("   Server-side error or invalid request")
       
       # 5. Rate Limit Error Example (rare in normal usage)
       try:
           # Simulate rapid requests that might trigger rate limiting
           for i in range(100):
               payment = cardinity.create_payment(
                   amount="1.00",
                   currency="EUR",
                   description=f"Rate limit test {i}",
                   country="LT",
                   payment_instrument={
                       "pan": "4111111111111111",
                       "exp_month": 12,
                       "exp_year": 2025,
                       "cvc": "123",
                       "holder": "Test User"
                   }
               )
       except RateLimitError as e:
           print(f"❌ Rate Limit Error: {e}")
           print("   Too many requests - implement backoff strategy")

Comprehensive Error Handling
---------------------------

Robust error handling for payment operations:

.. code-block:: python

   import time
   import logging
   from datetime import datetime

   # Configure logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   def create_payment_with_robust_error_handling(payment_data, max_retries=3):
       """Create payment with comprehensive error handling and retry logic."""
       
       for attempt in range(max_retries):
           try:
               logger.info(f"Creating payment - attempt {attempt + 1}/{max_retries}")
               
               payment = cardinity.create_payment(**payment_data)
               
               # Success - log and return
               logger.info(f"✅ Payment created successfully: {payment['id']}")
               return {
                   'success': True,
                   'payment': payment,
                   'attempts': attempt + 1
               }
               
           except ValidationError as e:
               # Validation errors are not retryable
               logger.error(f"❌ Validation error: {str(e)}")
               return {
                   'success': False,
                   'error_type': 'validation',
                   'error_message': str(e),
                   'retryable': False,
                   'attempts': attempt + 1
               }
               
           except AuthenticationError as e:
               # Authentication errors are not retryable
               logger.error(f"❌ Authentication error: {str(e)}")
               return {
                   'success': False,
                   'error_type': 'authentication',
                   'error_message': str(e),
                   'retryable': False,
                   'attempts': attempt + 1
               }
               
           except RateLimitError as e:
               # Rate limit errors are retryable with backoff
               wait_time = 2 ** attempt  # Exponential backoff
               logger.warning(f"⚠️ Rate limit hit - waiting {wait_time}s before retry")
               
               if attempt < max_retries - 1:
                   time.sleep(wait_time)
                   continue
               else:
                   logger.error(f"❌ Rate limit exceeded after {max_retries} attempts")
                   return {
                       'success': False,
                       'error_type': 'rate_limit',
                       'error_message': str(e),
                       'retryable': True,
                       'attempts': attempt + 1
                   }
                   
           except APIError as e:
               # API errors might be retryable
               logger.warning(f"⚠️ API error on attempt {attempt + 1}: {str(e)}")
               
               if attempt < max_retries - 1:
                   wait_time = 1 + attempt  # Linear backoff for API errors
                   logger.info(f"   Retrying in {wait_time} seconds...")
                   time.sleep(wait_time)
                   continue
               else:
                   logger.error(f"❌ API error after {max_retries} attempts")
                   return {
                       'success': False,
                       'error_type': 'api',
                       'error_message': str(e),
                       'retryable': True,
                       'attempts': attempt + 1
                   }
                   
           except CardinityError as e:
               # Generic Cardinity errors
               logger.error(f"❌ Cardinity error: {str(e)}")
               return {
                   'success': False,
                   'error_type': 'cardinity',
                   'error_message': str(e),
                   'retryable': False,
                   'attempts': attempt + 1
               }
               
           except Exception as e:
               # Unexpected errors
               logger.error(f"❌ Unexpected error: {str(e)}")
               return {
                   'success': False,
                   'error_type': 'unexpected',
                   'error_message': str(e),
                   'retryable': False,
                   'attempts': attempt + 1
               }
       
       # Should not reach here, but just in case
       return {
           'success': False,
           'error_type': 'unknown',
           'error_message': 'Unknown error after all retry attempts',
           'retryable': False,
           'attempts': max_retries
       }

Payment-Specific Error Handling
------------------------------

Handle payment-specific error scenarios:

.. code-block:: python

   def handle_payment_errors(payment_result):
       """Handle specific payment error scenarios."""
       
       if payment_result.get('success'):
           payment = payment_result['payment']
           
           if payment['status'] == 'approved':
               return {
                   'outcome': 'success',
                   'message': 'Payment approved successfully',
                   'payment_id': payment['id']
               }
               
           elif payment['status'] == 'declined':
               # Handle declined payments
               decline_reason = payment.get('error', 'Unknown reason')
               
               # Map decline reasons to user-friendly messages
               decline_messages = {
                   'insufficient_funds': 'Insufficient funds in account',
                   'expired_card': 'Card has expired',
                   'invalid_card': 'Invalid card number',
                   'blocked_card': 'Card is blocked',
                   'do_not_honor': 'Transaction declined by bank',
                   'generic_decline': 'Transaction declined'
               }
               
               user_message = decline_messages.get(
                   decline_reason, 
                   f'Payment declined: {decline_reason}'
               )
               
               return {
                   'outcome': 'declined',
                   'message': user_message,
                   'decline_reason': decline_reason,
                   'payment_id': payment['id']
               }
               
           elif payment['status'] == 'pending':
               # Handle pending payments (likely 3DS)
               if 'threeds2_data' in payment:
                   return {
                       'outcome': 'requires_3ds',
                       'message': '3D Secure authentication required',
                       'payment_id': payment['id'],
                       'acs_url': payment['threeds2_data']['acs_url'],
                       'creq': payment['threeds2_data']['creq']
                   }
               else:
                   return {
                       'outcome': 'pending',
                       'message': 'Payment is being processed',
                       'payment_id': payment['id']
                   }
       else:
           # Handle API/system errors
           error_type = payment_result.get('error_type')
           error_message = payment_result.get('error_message')
           
           if error_type == 'validation':
               return {
                   'outcome': 'validation_error',
                   'message': 'Please check your payment information',
                   'details': error_message
               }
               
           elif error_type == 'authentication':
               return {
                   'outcome': 'system_error',
                   'message': 'Payment system temporarily unavailable',
                   'details': 'Authentication failed'
               }
               
           elif error_type == 'rate_limit':
               return {
                   'outcome': 'temporary_error',
                   'message': 'Too many requests. Please try again later.',
                   'retry_after': 60  # seconds
               }
               
           else:
               return {
                   'outcome': 'system_error',
                   'message': 'Payment system temporarily unavailable',
                   'details': error_message
               }

Circuit Breaker Pattern
----------------------

Implement circuit breaker pattern for API resilience:

.. code-block:: python

   class PaymentCircuitBreaker:
       """Circuit breaker for payment operations."""
       
       def __init__(self, failure_threshold=5, timeout=60):
           self.failure_threshold = failure_threshold
           self.timeout = timeout
           self.failure_count = 0
           self.last_failure_time = None
           self.state = 'closed'  # closed, open, half_open
           
       def can_execute(self):
           """Check if operation can be executed."""
           
           if self.state == 'closed':
               return True
               
           elif self.state == 'open':
               # Check if timeout has passed
               if (time.time() - self.last_failure_time) > self.timeout:
                   self.state = 'half_open'
                   return True
               return False
               
           elif self.state == 'half_open':
               return True
               
           return False
           
       def record_success(self):
           """Record successful operation."""
           self.failure_count = 0
           self.state = 'closed'
           
       def record_failure(self):
           """Record failed operation."""
           self.failure_count += 1
           self.last_failure_time = time.time()
           
           if self.failure_count >= self.failure_threshold:
               self.state = 'open'
               
   # Global circuit breaker instance
   payment_circuit_breaker = PaymentCircuitBreaker()

   def create_payment_with_circuit_breaker(payment_data):
       """Create payment with circuit breaker protection."""
       
       if not payment_circuit_breaker.can_execute():
           return {
               'success': False,
               'error_type': 'circuit_breaker',
               'error_message': 'Payment service temporarily unavailable'
           }
       
       try:
           result = create_payment_with_robust_error_handling(payment_data)
           
           if result['success']:
               payment_circuit_breaker.record_success()
           else:
               # Only record failure for certain error types
               if result.get('error_type') in ['api', 'rate_limit']:
                   payment_circuit_breaker.record_failure()
                   
           return result
           
       except Exception as e:
           payment_circuit_breaker.record_failure()
           raise

Error Logging and Monitoring
---------------------------

Implement comprehensive error logging:

.. code-block:: python

   import json
   from datetime import datetime

   class PaymentErrorLogger:
       """Enhanced error logging for payment operations."""
       
       def __init__(self):
           self.logger = logging.getLogger('payment_errors')
           
       def log_payment_error(self, operation, error_details, context=None):
           """Log payment error with context."""
           
           log_entry = {
               'timestamp': datetime.utcnow().isoformat(),
               'operation': operation,
               'error_type': error_details.get('error_type'),
               'error_message': error_details.get('error_message'),
               'attempts': error_details.get('attempts', 1),
               'retryable': error_details.get('retryable', False),
               'context': context or {}
           }
           
           # Add sensitive data filtering
           if 'payment_data' in log_entry['context']:
               log_entry['context']['payment_data'] = self._filter_sensitive_data(
                   log_entry['context']['payment_data']
               )
           
           self.logger.error(json.dumps(log_entry))
           
       def log_payment_success(self, operation, payment_id, attempts=1, context=None):
           """Log successful payment operation."""
           
           log_entry = {
               'timestamp': datetime.utcnow().isoformat(),
               'operation': operation,
               'status': 'success',
               'payment_id': payment_id,
               'attempts': attempts,
               'context': context or {}
           }
           
           self.logger.info(json.dumps(log_entry))
           
       def _filter_sensitive_data(self, data):
           """Remove sensitive data from logs."""
           
           filtered_data = data.copy()
           
           # Remove sensitive payment instrument data
           if 'payment_instrument' in filtered_data:
               instrument = filtered_data['payment_instrument'].copy()
               
               # Mask PAN (keep first 6 and last 4 digits)
               if 'pan' in instrument:
                   pan = instrument['pan']
                   if len(pan) >= 10:
                       instrument['pan'] = pan[:6] + '*' * (len(pan) - 10) + pan[-4:]
               
               # Remove CVC
               if 'cvc' in instrument:
                   instrument['cvc'] = '***'
                   
               filtered_data['payment_instrument'] = instrument
           
           return filtered_data

   # Global error logger
   error_logger = PaymentErrorLogger()

   def create_payment_with_logging(payment_data):
       """Create payment with comprehensive logging."""
       
       context = {
           'amount': payment_data.get('amount'),
           'currency': payment_data.get('currency'),
           'country': payment_data.get('country'),
           'payment_data': payment_data
       }
       
       result = create_payment_with_circuit_breaker(payment_data)
       
       if result['success']:
           error_logger.log_payment_success(
               'create_payment',
               result['payment']['id'],
               result.get('attempts', 1),
               context
           )
       else:
           error_logger.log_payment_error(
               'create_payment',
               result,
               context
           )
       
       return result

Graceful Degradation
-------------------

Implement graceful degradation for service failures:

.. code-block:: python

   class PaymentServiceManager:
       """Manage payment service with graceful degradation."""
       
       def __init__(self):
           self.service_health = {
               'payment_creation': True,
               'payment_retrieval': True,
               'refunds': True,
               'settlements': True
           }
           self.maintenance_mode = False
           
       def check_service_health(self):
           """Check health of payment services."""
           
           # In production, this would check actual service health
           # For now, simulate based on recent error rates
           
           if payment_circuit_breaker.state == 'open':
               self.service_health['payment_creation'] = False
           else:
               self.service_health['payment_creation'] = True
               
       def create_payment_with_degradation(self, payment_data):
           """Create payment with graceful degradation."""
           
           self.check_service_health()
           
           if self.maintenance_mode:
               return {
                   'success': False,
                   'error_type': 'maintenance',
                   'error_message': 'Payment system is under maintenance',
                   'retry_after': 1800  # 30 minutes
               }
           
           if not self.service_health['payment_creation']:
               # Offer alternative or queue the payment
               return {
                   'success': False,
                   'error_type': 'service_unavailable',
                   'error_message': 'Payment service temporarily unavailable',
                   'alternatives': [
                       'Try again in a few minutes',
                       'Use alternative payment method',
                       'Contact support for assistance'
                   ]
               }
           
           return create_payment_with_logging(payment_data)

   # Global service manager
   payment_service = PaymentServiceManager()

Webhook Error Handling
---------------------

Handle webhook-related errors:

.. code-block:: python

   def handle_webhook_errors(webhook_data):
       """Handle errors in webhook processing."""
       
       try:
           # Validate webhook signature (implement based on your webhook setup)
           if not validate_webhook_signature(webhook_data):
               logger.error("Invalid webhook signature")
               return {'status': 'error', 'message': 'Invalid signature'}
           
           # Process webhook data
           event_type = webhook_data.get('event_type')
           payment_id = webhook_data.get('payment_id')
           
           if event_type == 'payment.approved':
               handle_payment_approved(payment_id)
           elif event_type == 'payment.declined':
               handle_payment_declined(payment_id)
           elif event_type == 'refund.approved':
               handle_refund_approved(webhook_data.get('refund_id'))
           else:
               logger.warning(f"Unknown webhook event type: {event_type}")
           
           return {'status': 'success'}
           
       except Exception as e:
           logger.error(f"Webhook processing error: {str(e)}")
           
           # Return error response to trigger webhook retry
           return {
               'status': 'error', 
               'message': 'Webhook processing failed',
               'retry': True
           }

   def validate_webhook_signature(webhook_data):
       """Validate webhook signature for security."""
       # Implement signature validation based on your webhook configuration
       return True  # Placeholder

Testing Error Scenarios
-----------------------

Test error handling thoroughly:

.. code-block:: python

   def test_error_handling():
       """Test various error handling scenarios."""
       
       test_cases = [
           {
               'name': 'Invalid Amount Format',
               'payment_data': {
                   'amount': 'invalid',
                   'currency': 'EUR',
                   'description': 'Test',
                   'country': 'LT',
                   'payment_instrument': {
                       'pan': '4111111111111111',
                       'exp_month': 12,
                       'exp_year': 2025,
                       'cvc': '123',
                       'holder': 'Test User'
                   }
               },
               'expected_error': 'validation'
           },
           {
               'name': 'Invalid Currency',
               'payment_data': {
                   'amount': '10.00',
                   'currency': 'INVALID',
                   'description': 'Test',
                   'country': 'LT',
                   'payment_instrument': {
                       'pan': '4111111111111111',
                       'exp_month': 12,
                       'exp_year': 2025,
                       'cvc': '123',
                       'holder': 'Test User'
                   }
               },
               'expected_error': 'api'
           },
           {
               'name': 'Missing Required Field',
               'payment_data': {
                   'amount': '10.00',
                   'currency': 'EUR',
                   'description': 'Test',
                   # Missing country field
                   'payment_instrument': {
                       'pan': '4111111111111111',
                       'exp_month': 12,
                       'exp_year': 2025,
                       'cvc': '123',
                       'holder': 'Test User'
                   }
               },
               'expected_error': 'validation'
           }
       ]
       
       for test_case in test_cases:
           print(f"\n🧪 Testing: {test_case['name']}")
           
           result = create_payment_with_logging(test_case['payment_data'])
           
           if not result['success']:
               if result.get('error_type') == test_case['expected_error']:
                   print(f"   ✅ Expected error type: {test_case['expected_error']}")
               else:
                   print(f"   ❌ Unexpected error type: {result.get('error_type')}")
           else:
               print(f"   ❌ Expected failure but got success")

Best Practices Summary
---------------------

.. code-block:: python

   """
   Error Handling Best Practices Summary
   """

   def error_handling_best_practices():
       """Summary of error handling best practices."""
       
       best_practices = [
           {
               "category": "Exception Handling",
               "practices": [
                   "Catch specific exception types, not generic exceptions",
                   "Handle validation errors differently from API errors",
                   "Implement proper retry logic for transient errors",
                   "Use circuit breaker pattern for service resilience"
               ]
           },
           {
               "category": "User Experience",
               "practices": [
                   "Provide user-friendly error messages",
                   "Map technical errors to business-friendly language",
                   "Offer alternative actions when possible",
                   "Show progress indicators during retry attempts"
               ]
           },
           {
               "category": "Logging and Monitoring",
               "practices": [
                   "Log all errors with context but filter sensitive data",
                   "Use structured logging (JSON) for better parsing",
                   "Monitor error rates and patterns",
                   "Set up alerts for critical error thresholds"
               ]
           },
           {
               "category": "Security",
               "practices": [
                   "Never log sensitive payment data",
                   "Validate all webhook signatures",
                   "Implement rate limiting to prevent abuse",
                   "Use secure error messages that don't leak information"
               ]
           },
           {
               "category": "Resilience",
               "practices": [
                   "Implement exponential backoff for retries",
                   "Use circuit breaker pattern for failing services",
                   "Provide graceful degradation options",
                   "Queue operations when services are unavailable"
               ]
           }
       ]
       
       for category in best_practices:
           print(f"\n{category['category']}:")
           for practice in category['practices']:
               print(f"  • {practice}")

Production Error Monitoring
--------------------------

Set up production error monitoring:

.. code-block:: python

   """
   Production Error Monitoring Setup
   """

   # 1. Error rate monitoring
   def monitor_error_rates():
       """Monitor payment error rates and alert when thresholds exceeded."""
       
       error_thresholds = {
           'validation_errors': 0.05,    # 5% of requests
           'api_errors': 0.01,           # 1% of requests
           'authentication_errors': 0.001 # 0.1% of requests
       }
       
       # Implementation would connect to your monitoring system
       pass

   # 2. Service health checks
   def health_check():
       """Health check endpoint for payment service."""
       
       try:
           # Test basic payment creation
           test_result = create_payment_with_robust_error_handling({
               'amount': '1.00',
               'currency': 'EUR',
               'description': 'Health check',
               'country': 'LT',
               'payment_instrument': {
                   'pan': '4111111111111111',
                   'exp_month': 12,
                   'exp_year': 2025,
                   'cvc': '123',
                   'holder': 'Health Check'
               }
           })
           
           return {
               'status': 'healthy' if test_result['success'] else 'unhealthy',
               'timestamp': datetime.utcnow().isoformat(),
               'details': test_result
           }
           
       except Exception as e:
           return {
               'status': 'unhealthy',
               'timestamp': datetime.utcnow().isoformat(),
               'error': str(e)
           }

   # 3. Error aggregation and reporting
   def generate_error_report(start_date, end_date):
       """Generate error report for analysis."""
       
       # Implementation would query your logging system
       report = {
           'period': {'start': start_date, 'end': end_date},
           'total_requests': 0,
           'total_errors': 0,
           'error_rate': 0.0,
           'error_breakdown': {
               'validation_errors': 0,
               'api_errors': 0,
               'authentication_errors': 0,
               'rate_limit_errors': 0,
               'other_errors': 0
           },
           'top_error_messages': [],
           'recommendations': []
       }
       
       return report

Next Steps
----------

After implementing comprehensive error handling:

1. **Monitoring Setup**: Implement proper error monitoring and alerting
2. **Error Analytics**: Analyze error patterns and trends
3. **User Experience**: Optimize error messages and recovery flows
4. **Service Resilience**: Enhance circuit breaker and retry strategies
5. **Documentation**: Document error codes and troubleshooting guides 
