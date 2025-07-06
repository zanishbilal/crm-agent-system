# from langgraph.graph import StateGraph, END
# from typing import TypedDict

# from agents.hubspot_agent import run_test_agent
# from tools.email_tools import send_email_smtp
# import json

# # Shared state
# class AgentState(TypedDict):
#     input: str
#     hubspot_response: str
#     contact: dict
#     email_response: str

# # Agent 1 Node
# def hubspot_node(state: AgentState) -> AgentState:
#     print("🚀 Running HubSpot Agent...")
#     result = run_test_agent(state["input"])
#     return {
#         **state,
#         "hubspot_response": result["output"],
#         "contact": result["contact"]
#     }

# # Agent 2 Node
# # Agent 2 Node (Email Agent)
# def email_node(state: AgentState) -> AgentState:
#     print("📧 Running Email Agent...")

#     contact = state["contact"]

#     email_payload = {
#         "to_email": contact["email"],  # ✅ Match tool's expected key
#         "subject": "🎉 Welcome to HubSpot!",
#         "body": f"Hi {contact['first_name']} {contact['last_name']},\n\nYour contact has been successfully created in our system."
#     }

#     result = send_email_smtp.run(json.dumps(email_payload))

#     return {
#         **state,
#         "email_response": result
#     }

# # Graph build
# def run_orchestrator(query: str) -> AgentState:
#     graph = StateGraph(AgentState)
#     graph.add_node("hubspot_node", hubspot_node)
#     graph.add_node("email_node", email_node)

#     graph.set_entry_point("hubspot_node")
#     graph.add_edge("hubspot_node", "email_node")
#     graph.add_edge("email_node", END)

#     compiled_graph = graph.compile()
#     return compiled_graph.invoke({"input": query})



from langgraph.graph import StateGraph, END
from typing import TypedDict

from agents.hubspot_agent import run_test_agent
from agents.email_agent import run_email_agent           # Agent 2: Email agent using LLM
import json

# ------------------- SHARED STATE -------------------
class AgentState(TypedDict):
    input: str
    hubspot_response: str
    tool_response: str
    contact: dict
    email_response: str

# ------------------- AGENT 1 NODE -------------------
async def hubspot_node(state: AgentState) -> AgentState:
    print("🚀 Running HubSpot Agent...")
    
    result = run_test_agent(state["input"])

    return {
        **state,
        "hubspot_response": result["output"],         # Final LLM output
        "tool_response": result["tool_response"],     # Actual result from HubSpot tool
        "contact": result["contact"]                  # Extracted contact info
    }

# ------------------- AGENT 2 NODE -------------------
# ------------------- AGENT 2 NODE -------------------
async def email_node(state: AgentState) -> AgentState:
    print("📧 Running Email Agent...")

    # ✅ No manual check — email agent will handle both success & failure professionally
    contact_summary = state["hubspot_response"]
    contact = state["contact"]

    # ✅ Agent 2 will generate the appropriate email and send it
    result = run_email_agent(contact_summary, contact)

    return {
        **state,
        "email_response": result["output"]
    }


# ------------------- GRAPH FLOW -------------------
async def run_orchestrator(query: str) -> AgentState:
    graph = StateGraph(AgentState)

    graph.add_node("hubspot_node", hubspot_node)
    graph.add_node("email_node", email_node)

    graph.set_entry_point("hubspot_node")
    graph.add_edge("hubspot_node", "email_node")
    graph.add_edge("email_node", END)

    compiled_graph = graph.compile()

    return await compiled_graph.ainvoke({"input": query})

