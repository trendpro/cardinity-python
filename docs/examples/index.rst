Examples
========

This section provides practical examples of using the Cardinity Python SDK. Each example includes complete, runnable code with explanations.

.. note::
   All examples use test credentials and test card numbers. Replace them with your actual credentials and real data for production use.

Available Examples
------------------

.. note::
   Code examples are available in the ``examples/`` directory of the repository.

Quick Reference
---------------

Common Test Data
~~~~~~~~~~~~~~~~

Use these test values when running examples:

**Test Credentials:**

.. code-block:: python

   CONSUMER_KEY = "test_jlol6sogrlvje2zwwsfb6kjajuyy7h"
   CONSUMER_SECRET = "1h7j6rvwlpvuwbzrobo6bjbcqv1m3khnlqojpkkwh9wzbrlkmu"

**Test Card Numbers:**

* **Visa Success**: 4111111111111111
* **MasterCard Success**: 5555555555554444
* **Visa 3DS Success**: 4444333322221111
* **American Express Success**: 378282246310005
* **Failure (any amount >150)**: Any valid card number

**Test Amounts:**

* **Success**: Any amount < 150.00
* **Failure**: Any amount >= 150.00
* **3DS Required**: Depends on card and amount

Running Examples
----------------

Prerequisites
~~~~~~~~~~~~~

1. Install the SDK:

   .. code-block:: bash

      pip install cardinity-python

2. Set up environment variables (recommended):

   .. code-block:: bash

      export CARDINITY_CONSUMER_KEY="test_jlol6sogrlvje2zwwsfb6kjajuyy7h"
      export CARDINITY_CONSUMER_SECRET="1h7j6rvwlpvuwbzrobo6bjbcqv1m3khnlqojpkkwh9wzbrlkmu"

3. Copy and run any example:

   .. code-block:: bash

      python basic_payment.py

Example Structure
~~~~~~~~~~~~~~~~~

Each example follows this structure:

.. code-block:: python

   """
   Example: Description
   
   This example demonstrates how to...
   """
   
   import os
   from cardinity import Cardinity, CardinityError
   
   # Configuration
   cardinity = Cardinity(
       consumer_key=os.getenv("CARDINITY_CONSUMER_KEY", "test_key"),
       consumer_secret=os.getenv("CARDINITY_CONSUMER_SECRET", "test_secret")
   )
   
   def main():
       try:
           # Example code here
           pass
       except CardinityError as e:
           print(f"Error: {e}")
   
   if __name__ == "__main__":
       main()

Integration Examples
--------------------

For real-world integration scenarios, see:

* **E-commerce Integration**: Complete checkout flow
* **Subscription Billing**: Recurring payment setup
* **Marketplace Payments**: Multi-vendor scenarios
* **Mobile App Integration**: API integration patterns
* **Webhook Handling**: Processing payment notifications

Next Steps
----------

1. Start with ``basic_payment.py`` for simple payment processing
2. Learn about ``3ds_payment.py`` for secure authentication
3. Implement proper error handling for robust applications
4. Explore advanced SDK features for complex scenarios

Need Help?
----------

* Visit our `GitHub Issues <https://github.com/trendpro/cardinity-python/issues>`_
* Contact support at contact@cardinity.com 
