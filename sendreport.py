import requests
import os
oid = os.environ['OWNER_ID']
bot_token = os.environ['TELEGRAM_TOKEN']
def send__message(message):
  base_url = ("https://api.telegram.org/bot"+bot_token+"/sendMessage")
  parameters = {
        "chat_id": oid,
        "text" : message
    }
  requests.get(base_url , data = parameters)