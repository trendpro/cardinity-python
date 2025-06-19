#!/usr/bin/env python3
"""
Basic Payment Example

This example demonstrates how to create a simple payment using the Cardinity Python SDK.
It shows the basic workflow for processing a payment with a credit card.
"""

import os

from cardinity import APIError, Cardinity, CardinityError, ValidationError

# Configuration - use environment variables for production
CONSUMER_KEY = os.getenv(
    "CARDINITY_CONSUMER_KEY", "test_jlol6sogrlvje2zwwsfb6kjajuyy7h"
)
CONSUMER_SECRET = os.getenv(
    "CARDINITY_CONSUMER_SECRET", "1h7j6rvwlpvuwbzrobo6bjbcqv1m3khnlqojpkkwh9wzbrlkmu"
)

# Initialize the Cardinity client
cardinity = Cardinity(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)


def create_basic_payment():
    """Create a basic payment with a test credit card."""

    print("Creating a basic payment...")
    print(f"CONSUMER_KEY = {CONSUMER_KEY}, CONSUMER_SECRET = {CONSUMER_SECRET}")
    print("=" * 50)

    try:
        # Create payment with test data
        payment = cardinity.create_payment(
            amount="10.00",
            currency="EUR",
            description="Basic payment example",
            country="LT",
            payment_instrument={
                "pan": "4111111111111111",  # Test Visa card
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123",
                "holder": "John Doe",
            },
        )

        print("✅ Payment created successfully!")
        print(f"   Payment ID: {payment['id']}")
        print(f"   Status: {payment['status']}")
        print(f"   Amount: {payment['amount']} {payment['currency']}")
        print(f"   Description: {payment['description']}")

        if payment["status"] == "approved":
            print("   🎉 Payment was approved immediately!")
        elif payment["status"] == "pending":
            print("   ⏳ Payment is pending (may require 3DS authentication)")
            if "authorization_information" in payment:
                print(
                    f"   3DS URL: {payment['authorization_information'].get('url', 'N/A')}"
                )

        return payment

    except ValidationError as e:
        print(f"❌ Validation Error: {e}")
        print("   Check your payment data - some fields may be invalid.")
        return None

    except APIError as e:
        print(f"❌ API Error: {e}")
        print("   The API request failed. Check your credentials and try again.")
        return None

    except CardinityError as e:
        print(f"❌ Cardinity Error: {e}")
        print("   A general SDK error occurred.")
        return None


def get_payment_info(payment_id):
    """Retrieve information about a specific payment."""

    print(f"\nRetrieving payment information for ID: {payment_id}")
    print("=" * 50)

    try:
        payment = cardinity.get_payment(payment_id)

        print("✅ Payment retrieved successfully!")
        print(f"   Payment ID: {payment['id']}")
        print(f"   Status: {payment['status']}")
        print(f"   Amount: {payment['amount']} {payment['currency']}")
        print(f"   Created: {payment['created']}")

        return payment

    except APIError as e:
        print(f"❌ API Error: {e}")
        print("   Could not retrieve payment information.")
        return None


def main():
    """Main example function."""

    print("Cardinity Python SDK - Basic Payment Example")
    print("=" * 60)
    print(f"Using Consumer Key: {CONSUMER_KEY[:10]}...")
    print(f"Test Environment: {'Yes' if 'test_' in CONSUMER_KEY else 'No'}")
    print()

    # Create a basic payment
    payment = create_basic_payment()

    if payment:
        # Retrieve the payment information
        get_payment_info(payment["id"])

        print("\n" + "=" * 60)
        print("✅ Basic payment example completed successfully!")
        print("\nNext steps:")
        print("1. Try the 3ds_payment.py example for 3D Secure authentication")
        print("2. Explore recurring_payment.py for subscription payments")
        print("3. Check refund_example.py for processing refunds")
    else:
        print("\n" + "=" * 60)
        print("❌ Basic payment example failed.")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify your API credentials")
        print("3. Ensure you're using test credentials for testing")


if __name__ == "__main__":
    main()
