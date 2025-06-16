from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

JENKINS_URL = os.getenv("JENKINS_URL")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    print("Received webhook from Freshdesk:", data)

    # Trigger Jenkins pipeline
    trigger_jenkins_job(data)
    
    return jsonify({"status": "received"}), 200

def trigger_jenkins_job(payload):
    job_url = f"{JENKINS_URL}/job/freshdesk-pipeline/buildWithParameters"
    response = requests.post(job_url, auth=("admin", JENKINS_TOKEN), params={
        "ticket_subject": payload.get("ticket", {}).get("subject", ""),
        "ticket_id": payload.get("ticket", {}).get("id", "")
    })

    print("Triggered Jenkins:", response.status_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

