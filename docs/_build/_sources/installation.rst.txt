Installation
============

Requirements
------------

The Cardinity Python SDK requires:

* Python 3.8 or higher
* Internet connection for API requests
* Cardinity account with API credentials

Supported Python Versions
~~~~~~~~~~~~~~~~~~~~~~~~~~

The SDK is tested and officially supports:

* Python 3.8
* Python 3.9
* Python 3.10
* Python 3.11
* Python 3.12

Installation Methods
--------------------

pip (Recommended)
~~~~~~~~~~~~~~~~~

Install the latest stable version from PyPI:

.. code-block:: bash

   pip install cardinity-python

To install a specific version:

.. code-block:: bash

   pip install cardinity-python==1.0.0

uv (Fast Alternative)
~~~~~~~~~~~~~~~~~~~~~

If you're using the `uv <https://github.com/astral-sh/uv>`_ package manager:

.. code-block:: bash

   uv add cardinity-python

Development Installation
~~~~~~~~~~~~~~~~~~~~~~~~

To install from source for development:

.. code-block:: bash

   git clone https://github.com/trendpro/cardinity-python.git
   cd cardinity-python
   uv install --dev

Or with pip:

.. code-block:: bash

   git clone https://github.com/trendpro/cardinity-python.git
   cd cardinity-python
   pip install -e ".[dev]"

Dependencies
------------

The SDK has minimal required dependencies:

Core Dependencies
~~~~~~~~~~~~~~~~~

* **requests** (>=2.25.0): HTTP library for API communication
* **requests-oauthlib** (>=1.3.0): OAuth 1.0 authentication
* **cerberus** (>=1.3.0): Data validation
* **python-dateutil** (>=2.8.0): Date/time parsing

Development Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~

* **pytest** (>=6.0): Testing framework
* **pytest-cov**: Test coverage reporting
* **ruff**: Code formatting and linting
* **mypy**: Static type checking
* **sphinx**: Documentation generation
* **sphinx-rtd-theme**: Documentation theme

Verification
------------

After installation, verify that the SDK is working correctly:

.. code-block:: python

   import cardinity
   
   # Check version
   print(f"Cardinity SDK version: {cardinity.__version__}")
   
   # Test import
   from cardinity import Cardinity
   print("Installation successful!")

Virtual Environment (Recommended)
----------------------------------

It's highly recommended to use a virtual environment:

Using venv
~~~~~~~~~~

.. code-block:: bash

   python -m venv cardinity-env
   source cardinity-env/bin/activate  # On Windows: cardinity-env\Scripts\activate
   pip install cardinity-python

Using conda
~~~~~~~~~~~

.. code-block:: bash

   conda create -n cardinity python=3.11
   conda activate cardinity
   pip install cardinity-python

Using uv
~~~~~~~~

.. code-block:: bash

   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv add cardinity-python

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**ImportError: No module named 'cardinity'**
   Make sure you've activated your virtual environment and installed the package correctly.

**SSL Certificate Errors**
   Ensure your system has up-to-date SSL certificates. On macOS, you might need to run:
   
   .. code-block:: bash
   
      /Applications/Python\ 3.x/Install\ Certificates.command

**Permission Errors**
   Use ``--user`` flag with pip if you encounter permission issues:
   
   .. code-block:: bash
   
      pip install --user cardinity-python

Platform-Specific Notes
~~~~~~~~~~~~~~~~~~~~~~~~

**Windows**
   - Use PowerShell or Command Prompt
   - Consider using Windows Subsystem for Linux (WSL) for better compatibility

**macOS**
   - Xcode Command Line Tools may be required for some dependencies
   - Install with: ``xcode-select --install``

**Linux**
   - Most distributions work out of the box
   - Ensure ``python3-dev`` is installed for compiling dependencies

Next Steps
----------

Once installed, proceed to the :doc:`quickstart` guide to learn how to configure your API credentials and make your first API call. 
