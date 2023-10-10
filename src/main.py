from uagents import Bureau

from agents.temperature_agent import temp_agent as temperature_agent
from messages.sms_agent import sms_alert as sms_agent_alert


if __name__=="__main__":
    bureau =Bureau(endpoint="http://127.0.0.1:8000/submit", port=8000)
    bureau.add(temperature_agent)
    bureau.add(sms_agent_alert)
    bureau.run()

