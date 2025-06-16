import requests
import sys
import os

ticket_id = sys.argv[1]
api_key = os.environ['FRESHDESK_API_KEY']
domain = os.environ['FRESHDESK_DOMAIN']

url = f"https://{domain}/api/v2/tickets/{ticket_id}"
response = requests.get(url, auth=(api_key, 'X'))

ticket = response.json()
with open(f"ticket_{ticket_id}.json", "w") as f:
    f.write(response.text)

print(f"Fetched ticket #{ticket_id}")

