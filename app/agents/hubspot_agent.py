
import time
import re
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from tools.hubspot_tools import create_real_contact,update_contact


llm = Ollama(model="qwen2.5:14b",keep_alive=300)


def run_test_agent(query: str):
    start = time.time()
    tools = [create_real_contact,update_contact]


#     prompt = PromptTemplate.from_template(
#     """You are a HubSpot CRM specialist. Your ONLY task is creating OR updating contacts using the provided tools.

# {tools}

# Use the following format:

# STRICT RULES:
# 1. Use `create_real_contact` for NEW contact creation.
# 2. Use `update_contact` for UPDATING an existing contact.
# 3. REQUIRED parameters for both tools:
#    - email (valid email format)
#    - first_name (string)
#    - last_name (string)
# 4. NEVER invent or assume contact details.
# 5. If required fields are missing, say so in Final Answer. Do NOT guess.
# 6. if user not specify creat the contact dont creaet it by yourself just retern that contact not found if update contact not exist
# Action: the action to take, should be one of [{tool_names}]
# Execution Format:
# Question: The contact creation or update request
# Thought: Analyze if this is a create or update action, and if all required details are present
# Action: create_real_contact or update_contact
# Action Input: {{"email": "...", "first_name": "...", "last_name": "..."}}
# Observation: Tool response
# Thought: Confirm completion
# Final Answer: Summary of the action taken

# Current Task:
# Question: {input}
# {agent_scratchpad}"""
# )

    prompt = PromptTemplate.from_template(
    """You are a HubSpot agent. ONLY use the tools below for contact tasks.
{tools}
TOOLS:

RULES:
1. Required fields: email, first_name, last_name
2. Don’t guess or create data not provided
3. If details are missing or unclear, just say it
4. If user doesn’t clearly ask to create/update, do nothing

FORMAT:
Question: {input}
Thought: Decide what to do
Action: create_real_contact or update_contact[{tool_names}]
Action Input: {{...}}
Observation: Tool output
Final Answer: Your final summary

{agent_scratchpad}"""
)


    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3,
        return_intermediate_steps=True  # ✅ important
    )

    result = executor.invoke({"input": query})

    print("⏱️ Response time:", round(time.time() - start, 2), "seconds")
    llm_output = result["output"]
    print("jbskbajcb",llm_output)

    # Extract contact info from query
    contact_info = extract_contact_details(query)

    tool_result = ""
    for step in result["intermediate_steps"]:
        if isinstance(step, dict) and "observation" in step:
            tool_result = step["observation"]

    return {
        "output": llm_output,
        "tool_response": tool_result,
        "contact": contact_info
    }

# Helper to extract email, first_name, last_name from query


def extract_contact_details(text: str) -> dict:
    # Extract current email from anywhere
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    email = email_match.group(0) if email_match else ""

    # Try to extract first + last name (capitalized or lowercase)
    name_match = re.search(r"(?:for|name is|of|contact for)?\s*([A-Z]?[a-z]+)\s+([A-Z]?[a-z]+)", text)
    if name_match:
        first_name, last_name = name_match.groups()
    else:
        first_name, last_name = "", ""

    # Extract new email if user says "update email to" or "change email to"
    new_email_match = re.search(r"(?:update|change).*?email.*?to\s([\w\.-]+@[\w\.-]+)", text)
    new_email = new_email_match.group(1) if new_email_match else ""

    return {
       
        "first_name": first_name or "Unknown",
        "last_name": last_name or "User",
        "new_email": new_email  # ✅ useful in update_contact
    }

