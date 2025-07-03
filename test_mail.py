import json
from app.tools.email_tools import send_email_smtp

input_data = {
    "to_email": "zanishbilalsonu@gmail.com",
    "subject": "Test Email from AI Agent 🚀",
    "body": "Hi Zanish, this is a confirmation email sent via your Email Agent using SMTP!"
}

response = send_email_smtp.invoke(json.dumps(input_data))
print(response)
