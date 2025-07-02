.. Cardinity Python SDK documentation master file, created by
   sphinx-quickstart on Wed Jun 18 22:01:50 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Cardinity Python SDK Documentation
====================================

.. image:: https://img.shields.io/pypi/v/cardinity-python.svg
   :target: https://pypi.org/project/cardinity-python/
   :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/cardinity-python.svg
   :target: https://pypi.org/project/cardinity-python/
   :alt: Python versions

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/trendpro/cardinity-python/blob/main/LICENSE
   :alt: License

Welcome to the official Python SDK for the Cardinity Payment Gateway. This library provides a simple and intuitive way to integrate Cardinity's payment processing capabilities into your Python applications.

Key Features
------------

* **Complete API Coverage**: Full support for all Cardinity API operations
* **3D Secure v2**: Built-in support for strong customer authentication
* **Type Safety**: Full type hints for better development experience
* **Async Support**: Built on modern Python async/await patterns
* **Comprehensive Testing**: Extensive test suite with 92% coverage
* **Production Ready**: Built for scalability and reliability

Quick Start
-----------

Installation
~~~~~~~~~~~~

Install the Cardinity Python SDK using pip:

.. code-block:: bash

   pip install cardinity-python

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from cardinity import Cardinity

   # Initialize the client
   cardinity = Cardinity(
       consumer_key="your_consumer_key",
       consumer_secret="your_consumer_secret"
   )

   # Create a payment
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

   print(f"Payment created: {payment['id']}")

Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   installation
   quickstart
   authentication
   examples/index

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api

Support
-------

* **Documentation**: You're reading it!
* **Issues**: `GitHub Issues <https://github.com/trendpro/cardinity-python/issues>`_
* **Support**: kyalo@trendpro.co.ke
* **API Docs**: `Cardinity API Documentation <https://developers.cardinity.com/api/v1/#introduction>`_

License
-------

This project is licensed under the MIT License - see the `LICENSE <https://github.com/trendpro/cardinity-python/blob/main/LICENSE>`_ file for details.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

