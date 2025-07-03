# test_create_contact.py

from app.tools.hubspot_tools import create_contact_tool

# 👇 Test data (change to avoid duplicates in HubSpot)
test_input = {
    "email": "ali.khan2@example.com",
    "first_name": "Ali",
    "last_name": "Khan2"
}

# 🔧 Call the tool
result = create_contact_tool(test_input)

# 🖨️ Print result
print(result)
