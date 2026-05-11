import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from engine import app as unicorn_graph

app = FastAPI()

# Allow your Vercel frontend to talk to this backend safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define what the Next.js frontend is sending us
class LaunchRequest(BaseModel):
    industry: str

# The main endpoint
@app.post("/launch")
async def launch_engine(request: LaunchRequest):
    # Pass the industry directly into the graph's initial state
    final_state = unicorn_graph.invoke({"industry": request.industry})
    return final_state

# Keeps the Render server alive and listening
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)