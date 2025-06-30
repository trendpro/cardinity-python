Migration from Node.js SDK
==========================

This guide helps you migrate from the Cardinity Node.js SDK to the Python SDK. We'll cover the key differences, provide side-by-side examples, and explain the migration process step by step.

Overview of Changes
-------------------

The Python SDK maintains functional parity with the Node.js SDK while following Python conventions and best practices. Here are the main differences:

**Language Conventions**
* Python uses ``snake_case`` for variables and functions vs JavaScript's ``camelCase``
* Python classes use ``PascalCase`` (same as JavaScript)
* Dictionary access uses brackets ``payment['id']`` vs dot notation ``payment.id``
* Error handling uses ``try/except`` vs ``try/catch``

**Package Structure**
* Import: ``from cardinity import Cardinity`` vs ``const Cardinity = require('cardinity')``
* Configuration uses keyword arguments vs object properties
* Return values are Python dictionaries vs JavaScript objects

**Authentication**
* Same OAuth 1.0 approach, but configured differently
* Environment variable patterns follow Python conventions

Side-by-Side Comparison
-----------------------

Basic Setup
~~~~~~~~~~~

**Node.js SDK:**

.. code-block:: javascript

   const Cardinity = require('cardinity');
   
   const client = Cardinity({
     consumerKey: 'your_consumer_key',
     consumerSecret: 'your_consumer_secret'
   });

**Python SDK:**

.. code-block:: python

   from cardinity import Cardinity
   
   client = Cardinity(
       consumer_key='your_consumer_key',
       consumer_secret='your_consumer_secret'
   )

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

**Node.js SDK:**

.. code-block:: javascript

   const client = Cardinity({
     consumerKey: process.env.CARDINITY_CONSUMER_KEY,
     consumerSecret: process.env.CARDINITY_CONSUMER_SECRET
   });

**Python SDK:**

.. code-block:: python

   import os
   
   client = Cardinity(
       consumer_key=os.getenv('CARDINITY_CONSUMER_KEY'),
       consumer_secret=os.getenv('CARDINITY_CONSUMER_SECRET')
   )

Creating a Payment
~~~~~~~~~~~~~~~~~~

**Node.js SDK:**

.. code-block:: javascript

   client.payments.create({
     amount: '10.00',
     currency: 'EUR',
     description: 'Test payment',
     country: 'LT',
     paymentInstrument: {
       pan: '4111111111111111',
       expMonth: 12,
       expYear: 2025,
       cvc: '123',
       holder: 'John Doe'
     }
   }).then(payment => {
     console.log('Payment created:', payment.id);
   }).catch(error => {
     console.error('Payment failed:', error);
   });

**Python SDK:**

.. code-block:: python

   try:
       payment = client.create_payment(
           amount='10.00',
           currency='EUR',
           description='Test payment',
           country='LT',
           payment_instrument={
               'pan': '4111111111111111',
               'exp_month': 12,
               'exp_year': 2025,
               'cvc': '123',
               'holder': 'John Doe'
           }
       )
       print(f"Payment created: {payment['id']}")
   except Exception as error:
       print(f"Payment failed: {error}")

Retrieving a Payment
~~~~~~~~~~~~~~~~~~~~

**Node.js SDK:**

.. code-block:: javascript

   client.payments.get(paymentId)
     .then(payment => {
       console.log('Payment status:', payment.status);
     })
     .catch(error => {
       console.error('Error:', error);
     });

**Python SDK:**

.. code-block:: python

   try:
       payment = client.get_payment(payment_id)
       print(f"Payment status: {payment['status']}")
   except Exception as error:
       print(f"Error: {error}")

3D Secure Finalization
~~~~~~~~~~~~~~~~~~~~~~~

**Node.js SDK:**

.. code-block:: javascript

   client.payments.finalize(paymentId, {
     authorizeData: 'auth_data_from_3ds'
   }).then(payment => {
     console.log('Payment finalized:', payment.status);
   });

**Python SDK:**

.. code-block:: python

   payment = client.finalize_payment(
       payment_id,
       authorize_data='auth_data_from_3ds'
   )
   print(f"Payment finalized: {payment['status']}")

Migration Steps
---------------

Step 1: Environment Setup
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Install Python SDK:**

   .. code-block:: bash

      pip install cardinity-python

2. **Update environment variables** (optional but recommended):

   .. code-block:: bash

      # Keep existing names or use new Python conventions
      export CARDINITY_CONSUMER_KEY="your_key"
      export CARDINITY_CONSUMER_SECRET="your_secret"

Step 2: Update Imports and Initialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Replace your Node.js imports:

.. code-block:: python

   # Replace: const Cardinity = require('cardinity');
   from cardinity import Cardinity
   
   # Replace: const client = Cardinity({...});
   client = Cardinity(
       consumer_key='your_key',
       consumer_secret='your_secret'
   )

Step 3: Convert API Calls
~~~~~~~~~~~~~~~~~~~~~~~~~

Use this mapping to convert your API calls:

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - Node.js SDK
     - Python SDK
   * - ``client.payments.create()``
     - ``client.create_payment()``
   * - ``client.payments.get()``
     - ``client.get_payment()``
   * - ``client.payments.finalize()``
     - ``client.finalize_payment()``
   * - ``client.recurringPayments.create()``
     - ``client.create_recurring_payment()``
   * - ``client.refunds.create()``
     - ``client.create_refund()``
   * - ``client.refunds.get()``
     - ``client.get_refund()``
   * - ``client.settlements.create()``
     - ``client.create_settlement()``
   * - ``client.voids.create()``
     - ``client.create_void()``
   * - ``client.paymentLinks.create()``
     - ``client.create_payment_link()``

Step 4: Test Your Migration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Test basic operations** first
2. **Verify error handling** works correctly
3. **Test 3DS flows** if applicable
4. **Check webhook handling** (structure remains the same)
5. **Validate all payment scenarios** you currently use

Common Migration Pitfalls
--------------------------

Dictionary vs Object Access
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**❌ Don't do this:**

.. code-block:: python

   # This won't work - Python doesn't support dot notation on dicts
   payment.id  # AttributeError

**✅ Do this instead:**

.. code-block:: python

   # Use bracket notation for dictionary access
   payment['id']

Parameter Naming
~~~~~~~~~~~~~~~~

**❌ Don't do this:**

.. code-block:: python

   # Wrong parameter names (Node.js style)
   client.create_payment(paymentInstrument={...})

**✅ Do this instead:**

.. code-block:: python

   # Correct Python parameter names
   client.create_payment(payment_instrument={...}) 
