from langchain.tools import tool
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput
from pydantic import BaseModel
import json

# Load config
with open("app/config/config.json") as f:
    config = json.load(f)

# Initialize HubSpot client
hubspot = HubSpot(access_token=config["hubspot_api_key"])

# Input schema
class CreateContactInput(BaseModel):
    email: str
    first_name: str
    last_name: str

# Tool
@tool("create_hubspot_contact", args_schema=CreateContactInput)
def create_contact_tool(email: str, first_name: str, last_name: str) -> str:
    """
    Creates a contact in HubSpot using email, first name, and last name.
    """
    try:
        properties = {
            "email": email,
            "firstname": first_name,
            "lastname": last_name
        }
        contact_input = SimplePublicObjectInput(properties=properties)

        # ✅ Correct usage with named argument
        contact = hubspot.crm.contacts.basic_api.create(
            simple_public_object_input_for_create=contact_input
        )

        return f"✅ Contact created successfully with ID: {contact.id}"
    except Exception as e:
        return f"❌ Failed to create contact: {e}"
