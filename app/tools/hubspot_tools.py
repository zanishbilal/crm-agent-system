
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
    Prevents duplicate contacts by checking if the email already exists.
    """
    try:
        data = json.loads(action_input)
        email = data['email']
        first_name = data['first_name']
        last_name = data['last_name']

        # 🔍 Step 1: Check if contact with same email already exists
        search_request = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": email
                }]
            }],
            "limit": 1
        }

        results = hubspot.crm.contacts.search_api.do_search(search_request)

        if results.results:
            contact_id = results.results[0].id
            return f"⚠️ Contact with this email already exists. ID: {contact_id}"

        # ✅ Step 2: Create contact if not exists
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
    Input JSON: {
        "email": "...",             # Required (old email)
        "first_name": "...",        # Optional
        "last_name": "...",         # Optional
        "new_email": "..."          # Optional
    }
    """
    import json
    from hubspot.crm.contacts import SimplePublicObjectInput

    try:
        data = json.loads(action_input)
        old_email = data["email"]

        # Step 1: Search contact by old email
        search_payload = {
            "filterGroups": [{
                "filters": [{
                    "propertyName": "email",
                    "operator": "EQ",
                    "value": old_email
                }]
            }],
            "limit": 1
        }

        results = hubspot.crm.contacts.search_api.do_search(search_payload)
        if not results.results:
            return f"❌ Contact with email {old_email} not found."
    
        contact = results.results[0]
        contact_id = contact.id

        # Step 2: Build update payload with ONLY provided fields
        updated_props = {}
        if "first_name" in data:
            updated_props["firstname"] = data["first_name"]
        if "last_name" in data:
            updated_props["lastname"] = data["last_name"]
        if "new_email" in data:
            updated_props["email"] = data["new_email"]

        if not updated_props:
            return "⚠️ No fields to update. Provide at least one field."

        # Step 3: Send update
        update_input = SimplePublicObjectInput(properties=updated_props)
        hubspot.crm.contacts.basic_api.update(contact_id, update_input)

        return f"✅ Contact updated: {contact_id} | Updated fields: {list(updated_props.keys())}"

    except Exception as e:
        return f"❌ Error updating contact: {e}"

