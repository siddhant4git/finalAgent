import os
import hashlib
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import requests
from dotenv import load_dotenv
load_dotenv()

class Message(Model):
    message: str
    digest: str
    signature: str

# Function to encode a message using SHA-256
def encode(message: str) -> bytes:
    hasher = hashlib.sha256()
    hasher.update(message.encode())
    return hasher.digest()


temp_agent = Agent(
    name="temperature_agent",
    port=8000,
    seed="temperature_secret_phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)

fund_agent_if_low(temp_agent.wallet.address())

# Define an SMS address to send temperature notifications
SMS_ADDRESS="agent1qvr4xckegx49c3407ve04q2rdsggfn0lxn4sl9ckx0x36vz9tahe584ww3r"


# Get user input for city and temperature thresholds
location = input("Enter the city name (e.g., Delhi): ")
min_temp = float(input(f"Enter the minimum temperature: "))
max_temp = float(input("Enter the maximum temperature: "))


api_key = os.getenv("API_KEY")
api_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"


# Will notify temperature of given place every 6 hour
@temp_agent.on_interval(period=21600)
async def get_temp_info(ctx: Context):
    try:
        # Fetch temperature data from the OpenWeatherMap API
        response = requests.get(api_url)
        data = response.json()
        temperature_kelvin = data['main']['temp']
        temperature_celsius = temperature_kelvin - 273.15

        # Check if temperature is outside the specified range and send notifications
        if (max_temp <= temperature_celsius):
            msg = f"The temperature in {location} is {temperature_celsius:.2f}°C, which is more than the specified range."
            digest = encode(msg)
            await ctx.send(SMS_ADDRESS,Message(message=msg, digest=digest.hex(), signature=temp_agent.sign_digest(digest)),)
        if (min_temp >= temperature_celsius):
            msg = f"The temperature in {location} is {temperature_celsius:.2f}°C, which is less than the specified range."
            digest = encode(msg)
            await ctx.send(SMS_ADDRESS,Message(message=msg ,digest=digest.hex(), signature=temp_agent.sign_digest(digest)),)
        if (min_temp <= temperature_celsius <= max_temp):
            msg = f"The temperature in {location} is {temperature_celsius:.2f}°C, which is less than the specified range."
            digest = encode(msg)
            await ctx.send(SMS_ADDRESS,Message(message=msg ,digest=digest.hex(), signature=temp_agent.sign_digest(digest)),)
    except Exception as e:
        ctx.send(SMS_ADDRESS,Message(message=f'Error fetching weather data: {e}'))


if __name__ == "__main__":
     temp_agent.run()