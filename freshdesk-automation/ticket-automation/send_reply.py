import requests
import sys
import os

ticket_id = sys.argv[1]
api_key = os.environ['FRESHDESK_API_KEY']
domain = os.environ['FRESHDESK_DOMAIN']

with open(f"reply_{ticket_id}.txt") as f:
    body = f.read()

url = f"https://{domain}/api/v2/tickets/{ticket_id}/reply"
payload = {
    "body": body
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, auth=(api_key, 'X'), headers=headers, json=payload)
print("Reply sent:", response.status_code)

