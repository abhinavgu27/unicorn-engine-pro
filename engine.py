import os
import requests
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langchain_groq import ChatGroq

# ==========================================
# 1. VISUAL AI TOOL (Together AI + Flux)
# ==========================================
def generate_branding_image(industry_idea: str):
    """Calls Together AI and prints the exact raw response for debugging."""
    url = "https://api.together.xyz/v1/images/generations"
    api_key = os.getenv("TOGETHER_API_KEY")
    
    payload = {
        "model": "black-forest-labs/FLUX.1-schnell-Free",
        "prompt": f"Professional high-tech startup logo: {industry_idea}. Minimalist vector, 4k, white background, cinematic lighting.",
        "width": 1024,
        "height": 1024,
        "steps": 4,
        "n": 1,
        "response_format": "b64_json"
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        
        # 🔍 THE MICROSCOPE: Print exactly what Together AI says to the Render Logs
        print(f"\n[DEBUG] Raw Together AI Response: {response_data}\n")
        
        if "data" in response_data:
            base64_image = response_data['data'][0]['b64_json']
            return f"data:image/jpeg;base64,{base64_image}"
        else:
            print("[ERROR] No image data found in the response.")
            return "https://dummyimage.com/1024x1024/1f2937/ffffff&text=API+Denied+Request"
            
    except Exception as e:
        print(f"[ERROR] Python crashed while reading image: {e}")
        return "https://dummyimage.com/1024x1024/1f2937/ffffff&text=Generation+Failed"

# ==========================================
# 2. THE MULTIMODAL STATE
# ==========================================
class UnicornState(TypedDict):
    industry: str
    product_spec: str
    branding_url: str  # Holds the Base64 image
    codebase_status: str
    board_approval: bool

# ==========================================
# 3. THE AI AGENTS
# ==========================================
def visionary_node(state: UnicornState):
    print("\n[CEO] Visionary: Defining Strategy...")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.8)
    prompt = f"You are a startup CEO. Pitch a highly innovative, 2-sentence idea for a new AI-driven company in the {state['industry']} sector. No markdown."
    response = llm.invoke(prompt)
    
    idea = response.content
    print("[DESIGNER] Creative Director: Generating Brand Identity...")
    
    # Trigger Image Generation immediately based on the CEO's idea
    image_url = generate_branding_image(idea)
    
    return {
        "product_spec": idea, 
        "branding_url": image_url
    }

def tech_lead_node(state: UnicornState):
    print("\n[CTO] Tech Lead: Writing Prototype...")
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.8)
    prompt = f"Write a 1-file Python script prototype for: {state['product_spec']}. RAW CODE ONLY."
    response = llm.invoke(prompt)
    raw_code = response.content.replace("```python", "").replace("```", "").strip()
    return {"codebase_status": raw_code}

def board_critic_node(state: UnicornState):
    print("\n[BOARD] Evaluating Assets...")
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