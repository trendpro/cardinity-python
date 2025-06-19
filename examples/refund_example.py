"""
Refund Example

This example demonstrates how to create and manage refunds using the Cardinity Python SDK.
It shows different refund scenarios including full refunds, partial refunds, and refund status checking.
"""

import os
import time

from cardinity import APIError, Cardinity, ValidationError

# Configuration
CONSUMER_KEY = os.getenv(
    "CARDINITY_CONSUMER_KEY", "test_jlol6sogrlvje2zwwsfb6kjajuyy7h"
)
CONSUMER_SECRET = os.getenv(
    "CARDINITY_CONSUMER_SECRET", "1h7j6rvwlpvuwbzrobo6bjbcqv1m3khnlqojpkkwh9wzbrlkmu"
)

# Initialize the Cardinity client
cardinity = Cardinity(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)


def create_test_payment():
    """Create a test payment that can be refunded."""

    print("Creating test payment for refund example...")

    try:
        payment = cardinity.create_payment(
            amount="50.00",
            currency="EUR",
            description="Test payment for refund example",
            country="LT",
            order_id="REFUND-TEST-12345",
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
        print(f"   Amount: {payment['amount']} {payment['currency']}")

        return payment

    except Exception as e:
        print(f"❌ Failed to create test payment: {e}")
        return None


def create_full_refund(payment_id):
    """Create a full refund for a payment."""

    print(f"\nCreating full refund for payment: {payment_id}")

    try:
        # First, get the payment details to know the full amount
        payment = cardinity.get_payment(payment_id)
        full_amount = payment["amount"]

        print(f"   Payment amount: {full_amount} {payment['currency']}")

        # Create full refund with the payment's full amount
        refund = cardinity.create_refund(
            payment_id=payment_id,
            amount=full_amount,
            description="Full refund - Customer not satisfied",
        )

        print("✅ Full refund created successfully!")
        print(f"   Refund ID: {refund['id']}")
        print(f"   Status: {refund['status']}")
        print(f"   Amount: {refund['amount']} {refund['currency']}")
        print(f"   Description: {refund['description']}")

        return refund

    except Exception as e:
        print(f"❌ Failed to create full refund: {e}")
        return None


def create_partial_refund(payment_id, refund_amount, description="Partial refund"):
    """Create a partial refund for a payment."""

    print(f"\nCreating partial refund of {refund_amount} EUR for payment: {payment_id}")

    try:
        refund = cardinity.create_refund(
            payment_id=payment_id, amount=refund_amount, description=description
        )

        print("✅ Partial refund created successfully!")
        print(f"   Refund ID: {refund['id']}")
        print(f"   Status: {refund['status']}")
        print(f"   Amount: {refund['amount']} {refund['currency']}")
        print(f"   Description: {refund['description']}")

        return refund

    except Exception as e:
        print(f"❌ Failed to create partial refund: {e}")
        return None


def get_refund_details(payment_id, refund_id):
    """Retrieve refund details."""

    print(f"\nRetrieving refund details: {refund_id}")

    try:
        refund = cardinity.get_refund(payment_id, refund_id)

        print("✅ Refund details retrieved successfully!")
        print(f"   Refund ID: {refund['id']}")
        print(f"   Status: {refund['status']}")
        print(f"   Amount: {refund['amount']} {refund['currency']}")
        print(f"   Created: {refund['created']}")
        print(f"   Description: {refund['description']}")

        return refund

    except Exception as e:
        print(f"❌ Failed to retrieve refund details: {e}")
        return None


def demonstrate_full_refund_workflow():
    """Demonstrate the complete full refund workflow."""

    print("💰 Full Refund Workflow")
    print("-" * 25)

    # Step 1: Create a payment to refund
    payment = create_test_payment()

    if not payment or payment["status"] != "approved":
        print("❌ Cannot proceed - payment not approved")
        return None

    # Wait a moment (simulate time between payment and refund request)
    time.sleep(1)

    # Step 2: Create full refund
    refund = create_full_refund(payment["id"])

    if refund:
        # Step 3: Check refund status
        time.sleep(1)
        refund_details = get_refund_details(payment["id"], refund["id"])

        if refund_details:
            print("✅ Full refund workflow completed successfully!")
            return {"payment": payment, "refund": refund_details}

    return None


def demonstrate_partial_refund_workflow():
    """Demonstrate partial refund workflow."""

    print("\n💰 Partial Refund Workflow")
    print("-" * 27)

    # Step 1: Create a payment for partial refunds
    payment = create_test_payment()

    if not payment or payment["status"] != "approved":
        print("❌ Cannot proceed - payment not approved")
        return None

    payment_amount = float(payment["amount"])

    # Step 2: Create first partial refund (20% of payment)
    partial_amount_1 = f"{payment_amount * 0.2:.2f}"
    refund_1 = create_partial_refund(
        payment["id"], partial_amount_1, "Partial refund - Shipping charges"
    )

    if refund_1:
        time.sleep(1)

        # Step 3: Create second partial refund (30% of payment)
        partial_amount_2 = f"{payment_amount * 0.3:.2f}"
        refund_2 = create_partial_refund(
            payment["id"], partial_amount_2, "Partial refund - Item return"
        )

        if refund_2:
            print(
                f"✅ Created two partial refunds totaling {float(partial_amount_1) + float(partial_amount_2):.2f} EUR"
            )
            print(
                f"   Remaining amount: {payment_amount - float(partial_amount_1) - float(partial_amount_2):.2f} EUR"
            )

            return {"payment": payment, "refund_1": refund_1, "refund_2": refund_2}

    return None


def demonstrate_refund_scenarios():
    """Demonstrate different refund scenarios."""

    print("🔄 Different Refund Scenarios")
    print("-" * 30)

    # Scenario 1: Customer cancellation (full refund)
    print("\n📋 Scenario 1: Customer Cancellation (Full Refund)")
    full_refund_result = demonstrate_full_refund_workflow()

    # Scenario 2: Partial return (multiple partial refunds)
    print("\n📋 Scenario 2: Partial Return (Multiple Partial Refunds)")
    partial_refund_result = demonstrate_partial_refund_workflow()

    # Scenario 3: Refund error handling
    print("\n📋 Scenario 3: Refund Error Handling")
    demonstrate_refund_error_handling()


def demonstrate_refund_error_handling():
    """Demonstrate proper error handling for refund operations."""

    print("⚠️  Testing refund error scenarios...")

    # Test 1: Try to refund non-existent payment
    try:
        print("\n🔍 Test 1: Refunding non-existent payment")
        fake_refund = cardinity.create_refund(
            payment_id="non-existent-payment-id",
            amount="10.00",
            description="Test refund for non-existent payment",
        )
    except APIError as e:
        print(f"   ✅ Correctly caught API error: {e.status_code}")
    except Exception as e:
        print(f"   ✅ Correctly caught error: {type(e).__name__}")

    # Test 2: Try to refund with invalid amount
    try:
        print("\n🔍 Test 2: Invalid refund amount")
        # Create a valid payment first
        test_payment = create_test_payment()
        if test_payment and test_payment["status"] == "approved":
            invalid_refund = cardinity.create_refund(
                payment_id=test_payment["id"],
                amount="999999.00",  # Amount higher than payment
                description="Invalid amount refund",
            )
    except (ValidationError, APIError) as e:
        print(f"   ✅ Correctly caught validation/API error: {type(e).__name__}")
    except Exception as e:
        print(f"   ✅ Correctly caught error: {type(e).__name__}")


def show_refund_best_practices():
    """Show best practices for refund handling."""

    print("\n💡 Refund Best Practices:")
    print("-" * 25)
    print("✅ Always verify payment exists and is refundable before creating refunds")
    print("✅ Keep detailed records of refund reasons and amounts")
    print("✅ Implement proper error handling for failed refund attempts")
    print("✅ Consider partial refunds for partial returns or adjustments")
    print("✅ Set up webhooks to handle refund status notifications")
    print("✅ Provide clear refund status updates to customers")
    print("✅ Handle concurrent refund attempts gracefully")
    print("✅ Validate refund amounts don't exceed remaining balance")
    print("✅ Implement refund approval workflows for large amounts")
    print("✅ Keep audit trails for all refund operations")


def main():
    """Main function to run the refund example."""

    print("💰 Cardinity Python SDK - Refund Example")
    print("=" * 45)

    try:
        # Demonstrate different refund scenarios
        demonstrate_refund_scenarios()

        # Show best practices
        show_refund_best_practices()

        print("\n" + "=" * 45)
        print("✨ Refund Example completed!")

    except KeyboardInterrupt:
        print("\n\n👋 Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
