from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engine import app as unicorn_graph

app = FastAPI()

# Allow your Vercel frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what the frontend is sending
class LaunchRequest(BaseModel):
    industry: str

@app.post("/launch")
async def launch_engine(request: LaunchRequest):
    # Pass the industry directly into the graph's initial state
    final_state = unicorn_graph.invoke({"industry": request.industry})
    return final_state