import requests, pandas as pd
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import json

# Load config
with open('config.json') as f:
    config = json.load(f)

FRESHDESK_DOMAIN = config["freshdesk_domain"]
API_KEY = config["freshdesk_api_key"]
EMAIL = config["email"]
EMAIL_PASSWORD = config["email_password"]
SMTP_SERVER = config["smtp_server"]
SMTP_PORT = config.get("smtp_port", 587)
TO_EMAIL = config["to_email"]

# === Step 1: Fetch Freshdesk Tickets ===
url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets"
response = requests.get(url, auth=(API_KEY, 'X'))
tickets = response.json()

data = [{
    'ID': t['id'],
    'Subject': t['subject'],
    'Status': t['status'],
    'Priority': t['priority'],
    'Created': t['created_at'],
    'Updated': t['updated_at']
} for t in tickets]

df = pd.DataFrame(data)
today = datetime.today().strftime('%Y-%m-%d')
file_path = f"freshdesk_tickets_{today}.xlsx"
df.to_excel(file_path, index=False)

# === Step 2: Send Email Report ===
msg = MIMEMultipart()
msg['Subject'] = 'Freshdesk Ticket Report'
msg['From'] = EMAIL
msg['To'] = TO_EMAIL
msg.attach(MIMEText('Attached is the latest Freshdesk ticket report.', 'plain'))

with open(file_path, 'rb') as f:
    part = MIMEApplication(f.read(), Name=file_path)
    part['Content-Disposition'] = f'attachment; filename="{file_path}"'
    msg.attach(part)

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL, EMAIL_PASSWORD)
    server.send_message(msg)

print("✅ Done: Report fetched, saved, and emailed.")

