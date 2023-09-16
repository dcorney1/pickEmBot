import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

GROUPME_URL = "https://api.groupme.com/v3/bots/post"
GROUPME_BOT_ID = os.getenv("GROUPME_BOT_ID")


def basic_text_msg(msg):
    payload = json.dumps({
      "text": msg,
      "bot_id": GROUPME_BOT_ID
    })
    headers = {
      'Content-Type': 'application/json'
    }
    requests.request("POST", GROUPME_URL, headers=headers, data=payload)
