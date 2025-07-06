from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from tools.email_tools import send_email_smtp
import time



llm = Ollama(model="qwen2.5:14b",keep_alive=300)

def run_email_agent(contact_summary: str, contact: dict):
    
    start = time.time()

    tools = [send_email_smtp]

    prompt_template = PromptTemplate.from_template(
        """You are an email generation assistant for a CRM system. Your ONLY job is to send a professional email based on the CRM contact status using the provided tool.

{tools}

STRICT RULES:
1. Use `send_email_smtp` ONLY to send the email.
2. REQUIRED fields:
   - to_email (recipient's email)
   - subject (clear)
   - body (polite and professional)
3. Do NOT assume details — use only what's provided.
4. If contact creation/update failed, inform user politely.
5. If successful, send a confirmation message.

Action: the action to take, should be one of [{tool_names}]
Execution Format:
Question: The CRM summary and context
Thought: Analyze what kind of email needs to be sent
Action: send_email_smtp
Action Input: {{"to_email": "...", "subject": "...", "body": "..."}}
Observation: Tool response
Final Answer: Summary of email action taken

Current Task:
Question: {contact_summary}
{agent_scratchpad}"""
    )

    prompt = prompt_template.partial(
        tools="- send_email_smtp: sends an email to the contact.",
        tool_names="send_email_smtp",
        contact_summary=contact_summary
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
        return_intermediate_steps=True
    )

    result = executor.invoke({})
    print("⏱️ Response time:", round(time.time() - start, 2), "seconds")


    return {
        "output": result["output"],
        "intermediate_steps": result["intermediate_steps"]
    }
