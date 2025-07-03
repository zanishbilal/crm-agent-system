# from langchain.agents import AgentExecutor, create_react_agent
# from langchain_community.llms import Ollama
# from langchain_core.prompts import PromptTemplate
# from app.tools.hubspot_tools import create_real_contact

# def run_test_agent(contact_info: dict):
#     llm = Ollama(model="qwen2.5:14b")
#     tools = [create_real_contact]

#     # Required ReAct-style prompt
#     prompt = PromptTemplate.from_template(
#         """You are a HubSpot CRM specialist. Your ONLY task is creating contacts using the provided tool.

# {tools}

# Use the following format:

# STRICT RULES:
# 1. MUST use create_real_contact tool for all contact creation
# 2. REQUIRED parameters:
#    - email (valid email format)
#    - first_name (string)
#    - last_name (string)
# 3. NEVER invent or modify contact details

# Action: the action to take, should be one of [{tool_names}]
# Execution Format:
# Question: The contact creation request
# Thought: Analyze if all required details are present
# Action: create_real_contact
# Action Input: {{"email": "...", "first_name": "...", "last_name": "..."}}
# Observation: Tool response
# Thought: Confirm completion
# Final Answer: Summary of the action taken

# Current Task:
# Question: {input}
# {agent_scratchpad}"""
#     )

#     agent = create_react_agent(
#         llm=llm,
#         tools=tools,
#         prompt=prompt
#     )

#     executor = AgentExecutor.from_agent_and_tools(
#         agent=agent,
#         tools=tools,
#         verbose=True,
#         handle_parsing_errors=True,
#         max_iterations=3
#     )

#   # Let the LLM interpret this instruction and generate structured input
#     return executor.invoke({
#         "input": f"Please create a HubSpot contact with email {contact_info['email']}, first name {contact_info['first_name']}, and last name {contact_info['last_name']}."
#     })

from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from app.tools.hubspot_tools import create_real_contact

def run_test_agent(query: str):
    llm = Ollama(model="qwen2.5:14b")
    tools = [create_real_contact]

    prompt = PromptTemplate.from_template(
        """You are a HubSpot CRM specialist. Your ONLY task is creating contacts using the provided tool.

{tools}

Use the following format:

STRICT RULES:
1. MUST use create_real_contact tool for all contact creation
2. REQUIRED parameters:
   - email (valid email format)
   - first_name (string)
   - last_name (string)
3. NEVER invent or modify contact details

Action: the action to take, should be one of [{tool_names}]
Execution Format:
Question: The contact creation request
Thought: Analyze if all required details are present
Action: create_real_contact
Action Input: {{"email": "...", "first_name": "...", "last_name": "..."}}
Observation: Tool response
Thought: Confirm completion
Final Answer: Summary of the action taken

Current Task:
Question: {input}
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
        max_iterations=3
    )

    return executor.invoke({"input": query})
