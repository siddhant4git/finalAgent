
# Temperature Alert Agent




### Step 1: Prequisites

Before starting, you'll need the following:

- Python (3.8+ is recommended)
- Poetry (a packaging and dependency management tool for Python)

### Step 2: Set up .env file

To run the demo, you need API keys from:

- OpenWeatherMap 
- Twilio

#### OpenWeatherMap API key

- Sign up for a free OpenWeatherMap account on their website.
- Log in to your OpenWeatherMap account.
- In your account settings, locate the "API Keys" or "API Access" section and generate a new API key.
- You will receive a unique API key that you can use in your applications to access OpenWeatherMap data.

#### Twilio API key

- Sign up for a Twilio account at https://www.twilio.com/.
- Log in to your Twilio account using your newly created credentials.
-  In your dashboard, navigate to the "API Keys" or "API Access" section, and generate a new API key. 
Note that if you’ve run out of Twilio credits, you will not be able to get results for this example.

Once you have all three keys, create a .env file in the temperature-integration/src directory.

```http
  export API_KEY = {GET THE API KEY}
  export ACCOUNT_SID = {GET ACCOUNT SID}
  export AUTH_TOKEN = {GET THE AUTH TOKEN}
  export FROM_PHONE_NUMBER={SET THE TWILIO NUMBER}
  export TO_PHONE_NUMBER={SET THE DESIRED NUMBER}
```

To use the environment variables from .env and install the project:

```http
  cd src
  source .env
  poetry shell
```

### Step 3:Run the main script

To run the project and its agents:

```http
  python main.py
```  

The script will prompt you to enter the following information:

- City name (e.g., Delhi)
- Minimum temperature threshold
- Maximum temperature threshold

Once you hit enter, the agent will run and periodically fetch temperature data from the OpenWeatherMap API.

You will be able to view the results in the console, and notifications will be sent via SMS if the temperature falls outside the specified range.

