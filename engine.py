import os
import urllib.parse
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

# ==========================================
# 1. VISUAL AI TOOL (Pollinations AI - 100% FREE)
# ==========================================
def generate_branding_image(industry_idea: str):
    """Generates a free image via URL. No API Key required."""
    print("\n[DESIGNER] Requesting free image from Pollinations...")
    try:
        safe_prompt = urllib.parse.quote(f"Professional high-tech startup logo for: {industry_idea}. Minimalist vector, 4k, white background, sleek design.")
        return f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=1024&nologo=true"
    except Exception as e:
        print(f"[ERROR] Free Image Request Failed: {e}")
        return "https://dummyimage.com/1024x1024/1f2937/ffffff&text=Generation+Failed"

# ==========================================
# 2. THE MULTIMODAL STATE
# ==========================================
class UnicornState(TypedDict):
    industry: str
    product_spec: str
    branding_url: str
    codebase_status: str
    board_approval: bool

# ==========================================
# 3. CLOUD AGENT NODES (Running on Groq Free Tier)
# ==========================================
def visionary_node(state: UnicornState):
    print("\n[CEO] Visionary: Defining Strategy via Groq Cloud...")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.8)
    prompt = f"You are a startup CEO. Pitch a highly innovative, 2-sentence idea for a new AI-driven company in the {state['industry']} sector. No markdown."
    response = llm.invoke(prompt)
    
    idea = response.content
    print("[DESIGNER] Creative Director: Generating Brand Identity...")
    image_url = generate_branding_image(idea)
    
    return {"product_spec": idea, "branding_url": image_url}

def tech_lead_node(state: UnicornState):
    print("\n[CTO] Tech Lead: Writing Prototype via Groq Cloud...")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.8)
    prompt = f"Write a 1-file Python script prototype for: {state['product_spec']}. RAW CODE ONLY."
    response = llm.invoke(prompt)
    raw_code = response.content.replace("```python", "").replace("```", "").strip()
    return {"codebase_status": raw_code}

def board_critic_node(state: UnicornState):
    print("\n[BOARD] Evaluating Assets via Groq Cloud...")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.8) 
    prompt = f"Review Spec: {state['product_spec']}. Code: {state['codebase_status']}. Reply APPROVED or REJECTED."
    response = llm.invoke(prompt)
    approval = "APPROVED" in response.content.upper()
    return {"board_approval": approval}

# ==========================================
# 4. CONSTRUCT THE LANGGRAPH WORKFLOW
# ==========================================
workflow = StateGraph(UnicornState)
workflow.add_node("visionary", visionary_node)
workflow.add_node("tech_lead", tech_lead_node)
workflow.add_node("board", board_critic_node)

workflow.set_entry_point("visionary")
workflow.add_edge("visionary", "tech_lead")
workflow.add_edge("tech_lead", "board")

def routing_logic(state: UnicornState):
    return END if state.get("board_approval") else "tech_lead"

workflow.add_conditional_edges("board", routing_logic)
app = workflow.compile()