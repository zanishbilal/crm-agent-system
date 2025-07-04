import json
import smtplib
from email.message import EmailMessage
from langchain.tools import tool
import os

with open("app/config/config.json", "r") as f:
    config = json.load(f)

# Extract Gmail App Password
gmail_app_password = config.get("gmail_app_password")

# gmail_password = os.environ.get("GMAIL_APP_PASSWORD")


@tool
def send_email_smtp(action_input: str) -> str:
    """
    Send an email using Gmail SMTP.

    Input (JSON string):
    {
        "to_email": "recipient@example.com",
        "subject": "Email subject",
        "body": "Email body"
    }

    Requires: 2FA enabled on Gmail + 16-character App Password
    """

    try:
        data = json.loads(action_input)
        to_email = data["to_email"]
        subject = data["subject"]
        body = data["body"]

        # ✅ Update with your email and generated App Password
        sender_email = "zanishbilal72@gmail.com"
        app_password = gmail_app_password
        # Create the email
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = to_email
        msg.set_content(body)

        # Send using Gmail's SMTP server
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        return f"✅ Email sent successfully to {to_email}"

    except Exception as e:
        return f"❌ Failed to send email: {str(e)}"
