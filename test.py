# from app.agents.hubspot_agent import run_test_agent

# contact_info = {
#     "email": "zanish.user@example.com",
#     "first_name": "zanish",
#     "last_name": "bilal"
# }

# response = run_test_agent(contact_info)
# print("HubSpot Result:", response["output"])



from app.agents.hubspot_agent import run_test_agent

chat_query = "my name is zanish bilal is zanishbilal72@gmail.com ."

response = run_test_agent(chat_query)
print("HubSpot Result:", response["output"])
