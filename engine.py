import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq # Swapped to Groq for Cloud Speed

# 1. Configuration
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class UnicornState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    current_phase: str
    product_spec: str
    codebase_status: str
    board_approval: bool

# 2. The Agent Nodes (Now running on Groq Llama-3 70B)
def visionary_node(state: UnicornState):
    print("\n[CEO] Visionary: Thinking via Cloud AI...")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.8) 
    prompt = "You are a startup CEO. Pitch a highly innovative, 2-sentence idea for a new AI-driven software company. Do not use markdown."
    response = llm.invoke(prompt)
    return {"current_phase": "development", "product_spec": response.content}

def tech_lead_node(state: UnicornState):
    print("\n[CTO] Tech Lead: Writing code via Cloud AI...")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.8)
    prompt = f"Write a 1-file Python script prototype for: {state.get('product_spec')}. RAW CODE ONLY."
    response = llm.invoke(prompt)
    raw_code = response.content.replace("```python", "").replace("```", "").strip()
    
    # In a Cloud Environment, we don't write to local disk, we return the string
    return {"codebase_status": f"Generated Prototype Code:\n{raw_code}"}

def board_critic_node(state: UnicornState):
    print("\n[BOARD] Evaluating via Cloud AI...")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.8) 
    prompt = f"Board Review: Spec: {state.get('product_spec')}. Code: {state.get('codebase_status')}. Reply APPROVED or REJECTED."
    response = llm.invoke(prompt)
    approval = "APPROVED" in response.content.upper()
    return {"board_approval": approval}

def growth_manager_node(state: UnicornState):
    return {"messages": ["Cloud Launch Complete."]}

# 3. Construct the Graph
workflow = StateGraph(UnicornState)
workflow.add_node("visionary", visionary_node)
workflow.add_node("tech_lead", tech_lead_node)
workflow.add_node("growth_manager", growth_manager_node)
workflow.add_node("board", board_critic_node)

workflow.set_entry_point("visionary")
workflow.add_edge("visionary", "tech_lead")
workflow.add_edge("tech_lead", "board")

def routing_logic(state: UnicornState):
    return "growth_manager" if state.get("board_approval") else "tech_lead"

workflow.add_conditional_edges("board", routing_logic)
workflow.add_edge("growth_manager", END)

app = workflow.compile()