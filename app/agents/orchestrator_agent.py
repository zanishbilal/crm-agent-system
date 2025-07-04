from langgraph.graph import StateGraph, END
from typing import TypedDict

from app.agents.hubspot_agent import run_test_agent
from app.tools.email_tools import send_email_smtp
import json

# Shared state
class AgentState(TypedDict):
    input: str
    hubspot_response: str
    contact: dict
    email_response: str

# Agent 1 Node
def hubspot_node(state: AgentState) -> AgentState:
    print("🚀 Running HubSpot Agent...")
    result = run_test_agent(state["input"])
    return {
        **state,
        "hubspot_response": result["output"],
        "contact": result["contact"]
    }

# Agent 2 Node
# Agent 2 Node (Email Agent)
def email_node(state: AgentState) -> AgentState:
    print("📧 Running Email Agent...")

    contact = state["contact"]

    email_payload = {
        "to_email": contact["email"],  # ✅ Match tool's expected key
        "subject": "🎉 Welcome to HubSpot!",
        "body": f"Hi {contact['first_name']} {contact['last_name']},\n\nYour contact has been successfully created in our system."
    }

    result = send_email_smtp.run(json.dumps(email_payload))

    return {
        **state,
        "email_response": result
    }

# Graph build
def run_orchestrator(query: str) -> AgentState:
    graph = StateGraph(AgentState)
    graph.add_node("hubspot_node", hubspot_node)
    graph.add_node("email_node", email_node)

    graph.set_entry_point("hubspot_node")
    graph.add_edge("hubspot_node", "email_node")
    graph.add_edge("email_node", END)

    compiled_graph = graph.compile()
    return compiled_graph.invoke({"input": query})
