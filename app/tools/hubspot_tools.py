
import json
from langchain.tools import tool
from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInput
import os
# Load config
with open("app/config/config.json") as f:
    config = json.load(f)

# Initialize HubSpot client
hubspot = HubSpot(access_token=config["hubspot_api_key"])

# hubspot_api_key = os.environ.get("HUBSPOT_API_KEY")

# Initialize HubSpot client
# hubspot = HubSpot(access_token=hubspot_api_key)

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

@tool
def update_contact(action_input: str) -> str:
    """
    Update an existing contact in HubSpot.
    Input JSON: { "email": "...", "first_name": "...", "last_name": "..." }
    """
    import json
    from hubspot import HubSpot
    from hubspot.crm.contacts import SimplePublicObjectInput

    try:
        data = json.loads(action_input)
        email = data["email"]

        # Search contact by email
        results = hubspot.crm.contacts.search_api.do_search({
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": email
                }]
            }],
            "limit": 1
        })

        if not results.results:
            return f"❌ Contact with email {email} not found."

        contact_id = results.results[0].id
        update_input = SimplePublicObjectInput(properties={
            "firstname": data.get("first_name", ""),
            "lastname": data.get("last_name", "")
        })

        hubspot.crm.contacts.basic_api.update(contact_id, update_input)
        return f"✅ Contact updated: {contact_id}"

    except Exception as e:
        return f"❌ Error updating contact: {e}"
