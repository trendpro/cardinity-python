"""
Recurring Payment Example

This example demonstrates how to create recurring payments using the Cardinity Python SDK.
It shows how to set up subscription-style payments using previously authorized payment methods.
"""

import os
import time

from cardinity import Cardinity

# Configuration
CONSUMER_KEY = os.getenv(
    "CARDINITY_CONSUMER_KEY", "test_jlol6sogrlvje2zwwsfb6kjajuyy7h"
)
CONSUMER_SECRET = os.getenv(
    "CARDINITY_CONSUMER_SECRET", "1h7j6rvwlpvuwbzrobo6bjbcqv1m3khnlqojpkkwh9wzbrlkmu"
)

# Initialize the Cardinity client
cardinity = Cardinity(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET)


def create_initial_payment():
    """Create the initial payment that will be used for recurring payments."""

    print("Creating initial payment for recurring setup...")

    try:
        # Create an initial payment that will be used as a reference for recurring payments
        payment = cardinity.create_payment(
            amount="29.99",
            currency="EUR",
            description="Monthly subscription - Initial payment",
            country="LT",
            order_id="SUBSCRIPTION-001-INITIAL",
            payment_instrument={
                "pan": "4111111111111111",  # Test Visa card
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123",
                "holder": "John Doe",
            },
        )

        print("✅ Initial payment created successfully!")
        print(f"   Payment ID: {payment['id']}")
        print(f"   Status: {payment['status']}")
        print(f"   Amount: {payment['amount']} {payment['currency']}")

        return payment

    except Exception as e:
        print(f"❌ Failed to create initial payment: {e}")
        return None


def create_recurring_payment(
    parent_payment_id, amount="29.99", description="Monthly subscription payment"
):
    """Create a recurring payment based on a previous payment."""

    print(f"\nCreating recurring payment from parent: {parent_payment_id}")

    try:
        # Create recurring payment using the parent payment ID
        # Note: We need to structure the parameters correctly for the RecurringPayment model
        recurring_payment = cardinity.create_recurring_payment(
            amount=amount,
            currency="EUR",
            description=description,
            country="LT",  # Required field that was missing
            order_id=f"SUBSCRIPTION-001-{int(time.time())}",
            payment_instrument={
                "payment_id": parent_payment_id  # Correct structure: payment_id inside payment_instrument
            },
        )

        print("✅ Recurring payment created successfully!")
        print(f"   Payment ID: {recurring_payment['id']}")
        print(f"   Status: {recurring_payment['status']}")
        print(
            f"   Amount: {recurring_payment['amount']} {recurring_payment['currency']}"
        )
        print(f"   Parent Payment: {parent_payment_id}")

        return recurring_payment

    except Exception as e:
        print(f"❌ Failed to create recurring payment: {e}")
        return None


def simulate_subscription_workflow():
    """Simulate a complete subscription workflow with multiple recurring payments."""

    print("💳 Simulating subscription workflow...")
    print("-" * 40)

    # Step 1: Create initial payment (customer signs up)
    initial_payment = create_initial_payment()

    if not initial_payment or initial_payment["status"] != "approved":
        print(
            "❌ Initial payment failed or not approved. Cannot continue with recurring payments."
        )
        return

    # Wait a moment and then create recurring payments
    import time

    # Step 2: Create first recurring payment (month 1)
    print("\n⏰ Processing Month 1 recurring payment...")
    recurring_1 = create_recurring_payment(
        initial_payment["id"],
        amount="29.99",
        description="Monthly subscription - Month 1",
    )

    if recurring_1:
        time.sleep(1)  # Simulate time passing

        # Step 3: Create second recurring payment (month 2)
        print("\n⏰ Processing Month 2 recurring payment...")
        recurring_2 = create_recurring_payment(
            initial_payment["id"],
            amount="29.99",
            description="Monthly subscription - Month 2",
        )

        if recurring_2:
            # Step 4: Create a different amount recurring payment (upgrade)
            print("\n⏰ Processing upgraded subscription payment...")
            recurring_upgrade = create_recurring_payment(
                initial_payment["id"],
                amount="49.99",
                description="Premium subscription - Upgraded plan",
            )

            if recurring_upgrade:
                print("\n✅ Subscription workflow completed successfully!")
                return [initial_payment, recurring_1, recurring_2, recurring_upgrade]

    return None


def demonstrate_recurring_scenarios():
    """Demonstrate different recurring payment scenarios."""

    print("🔄 Different Recurring Payment Scenarios")
    print("-" * 45)

    # Scenario 1: Fixed amount subscription
    print("\n📋 Scenario 1: Fixed Monthly Subscription")
    subscription_payments = simulate_subscription_workflow()

    if subscription_payments:
        print(
            f"   ✅ Created {len(subscription_payments)} payments in subscription flow"
        )

    # Scenario 2: Variable amount recurring payments
    print("\n📋 Scenario 2: Variable Amount Recurring Payments")

    # Create another initial payment for variable amounts
    variable_initial = create_initial_payment()

    if variable_initial and variable_initial["status"] == "approved":
        # Create recurring payments with different amounts
        amounts_and_descriptions = [
            ("15.99", "Usage-based billing - Low usage"),
            ("23.50", "Usage-based billing - Medium usage"),
            ("35.75", "Usage-based billing - High usage"),
        ]

        for amount, description in amounts_and_descriptions:
            recurring = create_recurring_payment(
                variable_initial["id"], amount=amount, description=description
            )
            if recurring:
                print(f"   ✅ Variable payment: {amount} EUR")


def show_recurring_best_practices():
    """Show best practices for recurring payments."""

    print("\n💡 Recurring Payment Best Practices:")
    print("-" * 40)
    print(
        "✅ Always verify initial payment is approved before creating recurring payments"
    )
    print("✅ Use meaningful order IDs to track subscription cycles")
    print("✅ Store parent payment IDs securely for future recurring payments")
    print("✅ Implement proper error handling for failed recurring payments")
    print("✅ Set up webhooks to handle payment notifications automatically")
    print("✅ Consider implementing retry logic for failed recurring payments")
    print("✅ Provide customers with payment history and upcoming charges")
    print("✅ Handle card expiration and update scenarios")
    print("✅ Implement cancellation and pause functionality")
    print("✅ Follow PCI compliance requirements for storing payment references")


def main():
    """Main function to run the recurring payment example."""

    print("🔄 Cardinity Python SDK - Recurring Payment Example")
    print("=" * 55)

    try:
        # Import time for delays

        # Demonstrate recurring payment scenarios
        demonstrate_recurring_scenarios()

        # Show best practices
        show_recurring_best_practices()

        print("\n" + "=" * 55)
        print("✨ Recurring Payment Example completed!")

    except KeyboardInterrupt:
        print("\n\n👋 Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
