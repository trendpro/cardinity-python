"""
3D Secure Payment Example

This example demonstrates how to handle 3D Secure authentication with the Cardinity Python SDK.
It shows the complete workflow for processing payments that require strong customer authentication.

Note: The current test environment may have limitations with 3DS validation. This example
shows both the intended 3DS workflow and fallback approaches.
"""

import os
import time

from cardinity import Cardinity

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


def create_basic_payment():
    """Create a basic payment that works in the current environment."""
    print("Creating a basic payment...")

    try:
        payment = cardinity.create_payment(
            amount="50.00",
            currency="EUR",
            description="Basic payment example",
            country="LT",
            payment_instrument={
                "pan": "4111111111111111",  # Standard Visa test card
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

        return payment

    except Exception as e:
        print(f"❌ Failed to create payment: {e}")
        return None


def create_3ds_payment_attempt():
    """Attempt to create a 3DS payment (using correct test environment approach)."""
    print("Creating a 3DS payment using test environment approach...")

    try:
        # Create payment with special description to trigger 3DS flow
        payment = cardinity.create_payment(
            amount="15.75",
            currency="EUR",
            description="3ds2-pass",  # Special description for test environment
            payment_instrument={
                "pan": "4111111111111111",
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123",
                "holder": "Test User",
            },
            threeds2_data={
                "notification_url": "https://example.com/notify",
                "browser_info": {
                    "accept_header": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "language": "en-US",
                    "screen_height": 1080,
                    "screen_width": 1920,
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "java_enabled": False,
                    "javascript_enabled": True,
                    "time_zone": -120,
                    "color_depth": 24,
                },
                "challenge_window_size": "02",
            },
            country="LT",
        )

        print("✅ 3DS Payment created successfully!")
        print(f"   Payment ID: {payment['id']}")
        print(f"   Status: {payment['status']}")

        if payment["status"] == "pending":
            print("🔒 Payment is pending - 3DS authentication required")
            if "authorization_information" in payment:
                print("   Authorization information provided for 3DS flow")

        return payment

    except Exception as e:
        print(f"❌ 3DS Payment failed: {e}")
        return None


def create_3ds_payment_success():
    """Create a 3DS payment that will succeed after authentication."""
    print("Creating a 3DS payment (success scenario)...")

    try:
        payment = cardinity.create_payment(
            amount="25.00",
            currency="EUR",
            description="3ds2-pass",  # Triggers successful 3DS flow
            payment_instrument={
                "pan": "4111111111111111",
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123",
                "holder": "Test User",
            },
            threeds2_data={
                "notification_url": "https://example.com/notify",
                "browser_info": {
                    "accept_header": "text/html",
                    "browser_language": "en-US",  # Correct field name
                    "screen_width": 1920,
                    "screen_height": 1040,
                    "challenge_window_size": "500x600",  # Correct format
                    "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0",
                    "color_depth": 24,
                    "time_zone": -60,
                    "ip_address": "216.58.207.35",
                    "javascript_enabled": True,
                    "java_enabled": True,
                },
            },
            country="LT",
        )

        print("✅ 3DS Payment created successfully!")
        print(f"   Payment ID: {payment['id']}")
        print(f"   Status: {payment['status']}")

        return payment

    except Exception as e:
        print(f"❌ 3DS Payment creation failed: {e}")
        return None


def create_3ds_payment_failure():
    """Create a 3DS payment that will fail after authentication."""
    print("Creating a 3DS payment (failure scenario)...")

    try:
        payment = cardinity.create_payment(
            amount="35.00",
            currency="EUR",
            description="3ds2-fail",  # Triggers failed 3DS flow
            payment_instrument={
                "pan": "4111111111111111",
                "exp_month": 12,
                "exp_year": 2025,
                "cvc": "123",
                "holder": "Test User",
            },
            threeds2_data={
                "notification_url": "https://example.com/notify",
                "browser_info": {
                    "accept_header": "text/html",
                    "browser_language": "en-US",
                    "screen_width": 1920,
                    "screen_height": 1040,
                    "challenge_window_size": "500x600",
                    "user_agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20100101 Firefox/21.0",
                    "color_depth": 24,
                    "time_zone": -60,
                    "ip_address": "216.58.207.35",
                    "javascript_enabled": True,
                    "java_enabled": True,
                },
            },
            country="LT",
        )

        print("✅ 3DS Payment created successfully!")
        print(f"   Payment ID: {payment['id']}")
        print(f"   Status: {payment['status']}")

        return payment

    except Exception as e:
        print(f"❌ 3DS Payment creation failed: {e}")
        return None


def handle_3ds_authentication(payment, should_succeed=True):
    """Handle 3DS authentication process."""

    if payment["status"] != "pending":
        print("✅ Payment doesn't require 3DS authentication")
        return payment

    print("\n🔒 3D Secure authentication required")

    # Check if 3DS data is available (threeds2_data contains acs_url and creq)
    if "threeds2_data" not in payment:
        print("❌ No 3DS data available")
        return payment

    threeds_data = payment["threeds2_data"]
    print(f"   3DS data available: {list(threeds_data.keys())}")

    if "acs_url" in threeds_data and "creq" in threeds_data:
        print(f"   ACS URL: {threeds_data['acs_url']}")
        print(f"   Challenge Request: {threeds_data['creq'][:50]}...")

    # In real implementation, you would redirect user to threeds_data['acs_url']
    # For testing, we simulate the 3DS completion
    print("\n⏳ Simulating 3DS authentication...")
    time.sleep(1)

    # Finalize the payment with test cres value
    cres_value = "3ds2-pass" if should_succeed else "3ds2-fail"
    print(f"   Using cres value: {cres_value}")

    try:
        finalized = cardinity.finalize_payment(payment["id"], cres=cres_value)

        print("✅ 3DS authentication completed!")
        print(f"   Final Status: {finalized['status']}")

        if finalized["status"] == "approved":
            print("   🎉 Payment approved after 3DS authentication!")
        elif finalized["status"] == "declined":
            print("   ❌ Payment declined after 3DS authentication")

        return finalized

    except Exception as e:
        print(f"❌ Failed to finalize 3DS payment: {e}")
        return None


def simulate_3ds_workflow():
    """Simulate the complete 3DS workflow."""
    print("Demonstrating complete 3DS workflow...")

    # Create a basic payment first to show the difference
    print("\n1️⃣ Creating basic payment (no 3DS)...")
    basic_payment = create_basic_payment()

    if basic_payment and basic_payment["status"] == "approved":
        print("   → Basic payment approved immediately")


def demonstrate_3ds_concepts():
    """Demonstrate 3DS concepts and best practices."""

    print("🔒 Cardinity Python SDK - 3D Secure Payment Example")
    print("=" * 55)

    # Example 1: Basic payment that works
    print("\n📋 Example 1: Working Basic Payment")
    print("-" * 35)
    basic_payment = create_basic_payment()

    # Example 2: 3DS payment that succeeds
    print("\n📋 Example 2: 3DS Payment (Success Flow)")
    print("-" * 35)
    success_payment = create_3ds_payment_success()
    if success_payment:
        final_success = handle_3ds_authentication(success_payment, should_succeed=True)

    # Example 3: 3DS payment that fails
    print("\n📋 Example 3: 3DS Payment (Failure Flow)")
    print("-" * 35)
    failure_payment = create_3ds_payment_failure()
    if failure_payment:
        final_failure = handle_3ds_authentication(failure_payment, should_succeed=False)

    # 3DS Best Practices and Information
    print("\n💡 3DS Test Environment Guide:")
    print("-" * 32)
    print("✅ Use description='3ds2-pass' for successful 3DS flow")
    print("✅ Use description='3ds2-fail' for failed 3DS flow")
    print("✅ Check for 'pending' status and authorization_information")
    print("✅ Finalize with cres='3ds2-pass' or cres='3ds2-fail'")
    print("✅ Handle both success and failure scenarios")

    print("\n🔧 3DS v2 Browser Info Fields:")
    print("-" * 30)
    print("• accept_header: Browser's Accept header")
    print("• browser_language: Browser language (e.g., 'en-US')")
    print("• screen_height/width: Browser window dimensions")
    print("• user_agent: Full browser user agent string")
    print("• java_enabled: Boolean for Java support")
    print("• javascript_enabled: Boolean for JavaScript support")
    print("• time_zone: Integer offset from UTC in minutes")
    print("• color_depth: Screen color depth (8, 16, 24, 32)")
    print("• challenge_window_size: Window size like '500x600'")
    print("• ip_address: Customer's IP address (optional)")

    print("\n🌐 3DS Test Flow:")
    print("-" * 16)
    print("1. Create payment with description='3ds2-pass' or '3ds2-fail'")
    print("2. Response will be 'pending' with threeds2_data object")
    print("3. threeds2_data contains acs_url and creq for redirection")
    print("4. Redirect customer to acs_url with creq parameter")
    print("5. Finalize with PATCH request using cres='3ds2-pass' or '3ds2-fail'")
    print("6. Final status depends on cres value:")
    print("   - cres='3ds2-pass' → status='approved'")
    print("   - cres='3ds2-fail' → status='declined'")

    print("\n" + "=" * 55)
    print("✨ 3DS Example completed!")

    print("\n📊 Example Summary:")
    if basic_payment:
        print(f"✅ Basic payment: {basic_payment['id']} - {basic_payment['status']}")
    if "success_payment" in locals() and success_payment:
        print(f"✅ 3DS success payment: {success_payment['id']} - created")
    if "failure_payment" in locals() and failure_payment:
        print(f"✅ 3DS failure payment: {failure_payment['id']} - created")


def main():
    """Main function to run the 3DS payment example."""
    try:
        demonstrate_3ds_concepts()
    except KeyboardInterrupt:
        print("\n\n👋 Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
