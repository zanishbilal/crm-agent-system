
import json
from langchain.tools import tool
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput
import os
# Load config
# with open("app/config/config.json") as f:
#     config = json.load(f)

# # Initialize HubSpot client
# hubspot = HubSpot(access_token=config["hubspot_api_key"])

hubspot_api_key = os.environ.get("HUBSPOT_API_KEY")

# Initialize HubSpot client
hubspot = HubSpot(access_token=hubspot_api_key)

@tool
def create_real_contact(action_input: str) -> str:
    """
    Expects a JSON string as input with keys 'email', 'first_name', 'last_name'.
    """
    try:
        data = json.loads(action_input)
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']

        contact_input = SimplePublicObjectInput(properties={
            "email": email,
            "firstname": first_name,
            "lastname": last_name,
        })

        result = hubspot.crm.contacts.basic_api.create(
            simple_public_object_input_for_create=contact_input
        )

        return f"✅ Contact created successfully with ID: {result.id}"
    except Exception as e:
        return f"❌ HubSpot API error: {str(e)}"
