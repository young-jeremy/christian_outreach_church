from django.conf import settings
from twilio.rest import Client


def process_text_donation(phone_number, amount, donation_type):
    # Set up Twilio client
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Send confirmation message
    message = client.messages.create(
        body=f"Thank you for your {donation_type} donation of ${amount}. Reply YES to confirm.",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    # In a real implementation, you would set up a webhook to handle the reply
    # and process the payment when the user confirms

    return message.sid
