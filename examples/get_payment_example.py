#!/usr/bin/env python3
"""
Get Payment Example

This example demonstrates how to retrieve payment information using the Cardinity Python SDK.
It shows how to get a single payment by ID and how to list all payments.
"""

import os

from cardinity import APIError, Cardinity, CardinityError, NotFoundError

# Configuration - Replace with your actual Cardinity API credentials
# Get your credentials from: https://cardinity.com/developers
CONSUMER_KEY = os.getenv("CARDINITY_CONSUMER_KEY", "YOUR_CONSUMER_KEY_HERE")
CONSUMER_SECRET = os.getenv("CARDINITY_CONSUMER_SECRET", "YOUR_CONSUMER_SECRET_HERE")

# Check if credentials are properly configured
if (
    CONSUMER_KEY == "YOUR_CONSUMER_KEY_HERE"
    or CONSUMER_SECRET == "YOUR_CONSUMER_SECRET_HERE"
):
    print("❌ Please configure your Cardinity API credentials!")
    print("\nOptions:")
    print("1. Set environment variables:")
    print("   export CARDINITY_CONSUMER_KEY='your_key_here'")
    print("   export CARDINITY_CONSUMER_SECRET='your_secret_here'")
    print("\n2. Or edit this file and replace the placeholder values")
    print("\n3. Get your credentials from: https://cardinity.com/developers")
    exit(1)

# Initialize the Cardinity client
cardinity = Cardinity(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)


def get_single_payment(payment_id: str):
    """Retrieve a single payment by ID."""

    print(f"Retrieving payment with ID: {payment_id}")
    print("=" * 50)

    try:
        payment = cardinity.get_payment(payment_id)

        print("✅ Payment retrieved successfully!")
        print(f"   Payment ID: {payment['id']}")
        print(f"   Status: {payment['status']}")
        print(f"   Amount: {payment['amount']} {payment['currency']}")
        print(f"   Created: {payment['created']}")
        print(f"   Country: {payment.get('country', 'N/A')}")
        print(f"   Description: {payment.get('description', 'N/A')}")

        if payment.get("payment_instrument"):
            instrument = payment["payment_instrument"]
            print(f"   Card Brand: {instrument.get('card_brand', 'N/A')}")
            print(f"   Card Last 4: {instrument.get('pan', 'N/A')}")

        if payment.get("error"):
            print(f"   Error: {payment['error']}")

        return payment

    except NotFoundError:
        print(f"❌ Payment with ID {payment_id} not found")
        return None
    except APIError as e:
        print(f"❌ API Error: {e}")
        return None
    except CardinityError as e:
        print(f"❌ Cardinity Error: {e}")
        return None


def get_all_payments(limit: int = 10):
    """Retrieve all payments with optional limit."""

    print(f"Retrieving up to {limit} payments...")
    print("=" * 50)

    try:
        payments = cardinity.get_payment(limit=limit)

        print(f"✅ Retrieved {len(payments)} payments successfully!")
        print()

        for i, payment in enumerate(payments, 1):
            print(f"   Payment {i}:")
            print(f"     ID: {payment['id']}")
            print(f"     Status: {payment['status']}")
            print(f"     Amount: {payment['amount']} {payment['currency']}")
            print(f"     Created: {payment['created']}")
            print(f"     Description: {payment.get('description', 'N/A')}")
            print()

        return payments

    except APIError as e:
        print(f"❌ API Error: {e}")
        return None
    except CardinityError as e:
        print(f"❌ Cardinity Error: {e}")
        return None


def get_all_payments_unlimited():
    """Retrieve all payments without limit."""

    print("Retrieving all payments (no limit)...")
    print("=" * 50)

    try:
        payments = cardinity.get_payment()

        print(f"✅ Retrieved {len(payments)} payments successfully!")
        print()

        # Show summary statistics
        statuses = {}
        currencies = {}

        for payment in payments:
            status = payment["status"]
            currency = payment["currency"]

            statuses[status] = statuses.get(status, 0) + 1
            currencies[currency] = currencies.get(currency, 0) + 1

        print("   Summary:")
        print(f"     Total payments: {len(payments)}")
        print("     By status:")
        for status, count in statuses.items():
            print(f"       {status}: {count}")
        print("     By currency:")
        for currency, count in currencies.items():
            print(f"       {currency}: {count}")

        return payments

    except APIError as e:
        print(f"❌ API Error: {e}")
        return None
    except CardinityError as e:
        print(f"❌ Cardinity Error: {e}")
        return None


def create_test_payment():
    """Create a test payment to demonstrate get_payment functionality."""

    print("Creating a test payment first...")
    print("=" * 50)

    try:
        payment = cardinity.create_payment(
            amount="5.00",
            currency="EUR",
            description="Test payment for get_payment example",
            country="LT",
            payment_instrument={
                "pan": "4111111111111111",  # Test Visa card
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123",
                "holder": "John Doe",
            },
        )

        print("✅ Test payment created successfully!")
        print(f"   Payment ID: {payment['id']}")
        print(f"   Status: {payment['status']}")

        return payment

    except APIError as e:
        print(f"❌ API Error: {e}")
        return None
    except CardinityError as e:
        print(f"❌ Cardinity Error: {e}")
        return None


def main():
    """Main example function."""

    print("Cardinity Python SDK - Get Payment Example")
    print("=" * 60)
    print(f"Using Consumer Key: {CONSUMER_KEY[:10]}...")
    print(f"Test Environment: {'Yes' if 'test_' in CONSUMER_KEY else 'No'}")
    print()

    # First, create a test payment so we have something to retrieve
    test_payment = create_test_payment()

    if test_payment:
        print("\n")

        # Demonstrate getting a single payment
        get_single_payment(test_payment["id"])

        print("\n")

        # Demonstrate getting all payments with limit
        get_all_payments(limit=5)

        print("\n")

        # Demonstrate getting all payments without limit
        get_all_payments_unlimited()

    print("\n" + "=" * 60)
    print("✅ Get payment example completed!")
    print("\nNext steps:")
    print("1. Try different payment IDs")
    print("2. Experiment with different limit values")
    print("3. Check the API documentation for more details")


if __name__ == "__main__":
    main()
