# Cardinity Python SDK Examples

This directory contains example scripts demonstrating how to use the Cardinity Python SDK for various payment operations.

## Setup

Before running any examples, you need to configure your Cardinity API credentials. You have two options:

### Option 1: Environment Variables (Recommended)

Set your credentials as environment variables:

```bash
export CARDINITY_CONSUMER_KEY="your_consumer_key_here"
export CARDINITY_CONSUMER_SECRET="your_consumer_secret_here"
```

### Option 2: Edit the Example Files

Open any example file and replace the placeholder values:

```python
CONSUMER_KEY = os.getenv("CARDINITY_CONSUMER_KEY", "your_actual_consumer_key")
CONSUMER_SECRET = os.getenv("CARDINITY_CONSUMER_SECRET", "your_actual_consumer_secret")
```

## Getting API Credentials

1. Sign up at [Cardinity](https://cardinity.com/)
2. Go to the [Developer Dashboard](https://cardinity.com/developers)
3. Create a new application
4. Copy your Consumer Key and Consumer Secret

## Available Examples

### `basic_payment.py`
Demonstrates basic payment processing with a credit card.

```bash
python basic_payment.py
```

### `3ds_payment.py`
Shows how to handle 3D Secure authentication flows.

```bash
python 3ds_payment.py
```

### `recurring_payment.py`
Illustrates subscription-style recurring payments.

```bash
python recurring_payment.py
```

### `refund_example.py`
Demonstrates full and partial refund processing.

```bash
python refund_example.py
```

### `get_payment_example.py`
Shows how to retrieve payment information.

```bash
python get_payment_example.py
```

## Test Environment

All examples use Cardinity's test environment. No real money is processed.

## Common Issues

### "Consumer key cannot be empty"

This means your credentials are not properly configured. Make sure to:

1. Set environment variables correctly
2. Or replace the placeholder values in the example files
3. Ensure your credentials are valid

### Connection Errors

Make sure you have an internet connection and your firewall allows HTTPS connections to api.cardinity.com.

## Support

For questions about the Cardinity API, visit the [Cardinity Developer Documentation](https://cardinity.com/developers). 
