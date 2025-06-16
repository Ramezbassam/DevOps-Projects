import json
import sys

ticket_id = sys.argv[1]

with open(f"ticket_{ticket_id}.json") as f:
    ticket = json.load(f)

subject = ticket['subject'].lower()
description = ticket['description'].lower()

# Basic logic
if "password" in subject or "reset" in description:
    reply = "Hi, it seems you need help with a password reset. Please follow this link: ..."
else:
    reply = "Thank you for reaching out. We're reviewing your issue and will get back shortly."

with open(f"reply_{ticket_id}.txt", "w") as f:
    f.write(reply)

print("Generated reply:", reply)

