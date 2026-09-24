import requests
from dotenv import load_dotenv
import os

load_dotenv()

SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(ticket: dict, classification: dict):
    """Post a formatted alert to Slack for a ticket."""
    text = (
        f"*New {classification['urgency'].upper()} priority ticket* "
        f"({classification['category']})\n"
        f"*From:* {ticket['sender']}\n"
        f"*Subject:* {ticket['subject']}\n"
        f"*Summary:* {classification['summary']}"
    )

    response = requests.post(SLACK_WEBHOOK_URL, json={"text": text})
    response.raise_for_status()
    return response.status_code == 200