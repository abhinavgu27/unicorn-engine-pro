import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import engine # This imports your existing agent logic

app = FastAPI()

# This allows your React app (on port 3000) to talk to this API (on port 8000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

class IndustryRequest(BaseModel):
    industry: str

@app.post("/launch")
async def launch_agents(request: IndustryRequest):
    print(f"Received request to disrupt: {request.industry}")
    
    # We run your Unicorn Engine graph
    initial_state = {
        "messages": [],
        "current_phase": "ideation",
        "product_spec": f"Industry: {request.industry}",
        "codebase_status": "",
        "board_approval": False
    }
    
    # Run the engine and get the final result
    result = engine.app.invoke(initial_state)
    
    return {
        "spec": result["product_spec"],
        "code": result["codebase_status"]
    }

if __name__ == "__main__":
    import uvicorn
    # This allows the cloud server to choose the port
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)