from twilio.rest import Client
from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Model
from uagents.crypto import Identity
from dotenv import load_dotenv
import os
load_dotenv()


class Message(Model):
    message: str
    digest: str
    signature: str


sms_alert=Agent(
    name="sms_agent_alert",
    port=8002,
    seed="sms_agent secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

# Fund the agent if it's low on funds
fund_agent_if_low(sms_alert.wallet.address())


# Your Twilio Account SID and Auth Token
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')

# Create a Twilio client
client = Client(account_sid, auth_token)

# Your Twilio phone number (bought or verified)
from_phone_number = os.getenv('FROM_PHONE_NUMBER')

# Recipient's phone number
to_phone_number = os.getenv("TO_PHONE_NUMBER")  # Replace with the recipient's phone number


@sms_alert.on_message(model=Message)
async def sms_handler(ctx: Context, sender: str, msg: Message):
    # Verify the message's signature
    assert Identity.verify_digest(
        sender, bytes.fromhex(msg.digest), msg.signature
    ),"couldn't verify agent's message"

    # Log that the message has been verified
    ctx.logger.info("\n Agent's message verified!\n")
    ctx.logger.info(f'\nTemperature Alert: {msg.message}\n\n')

    # Message to send
    message_body = f"Temperature notification: {msg.message}"
    try:
        # Send the SMS using twilio
        message = client.messages.create(
            body=message_body,
            from_=from_phone_number,
            to=to_phone_number
        )
        print(f"Message sent with SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

