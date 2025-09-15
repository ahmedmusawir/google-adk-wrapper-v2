# main.py - FastAPI Gateway (Universal Parsing Logic)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import asyncio
from typing import Dict, Optional, List, Any
import logging
import time

# --- Setup and Models (No changes here) ---
app = FastAPI(title="ADK Agent Gateway", version="1.2.0")

class AgentRequest(BaseModel):
    agent_name: str
    message: str
    user_id: str
    session_id: Optional[str] = None

class AgentResponse(BaseModel):
    response: str
    session_id: str
    agent_name: str
    status: str

AGENT_REGISTRY = {
    "greeting_agent": "http://localhost:8000",
    "jarvis_agent": "http://localhost:8000",
    "calc_agent": "http://localhost:8000",
    "product_agent": "http://localhost:8000",
}

logging.basicConfig(level=logging.INFO)

# --- Main Endpoint (No changes here) ---
@app.post("/run_agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """Main gateway endpoint - routes requests to appropriate ADK agents"""
    if request.agent_name not in AGENT_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Agent '{request.agent_name}' not found")
    
    agent_url = AGENT_REGISTRY[request.agent_name]
    
    try:
        session_id = request.session_id or await create_session(agent_url, request.user_id, request.agent_name)
        
        response_text = await run_agent_session(
            agent_url, 
            request.message,
            request.user_id,
            request.agent_name,
            session_id
        )
        
        return AgentResponse(
            response=response_text,
            session_id=session_id,
            agent_name=request.agent_name,
            status="success"
        )
        
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP Error running agent {request.agent_name}: {e.response.status_code} - {e.response.text}")
        raise HTTPException(status_code=e.response.status_code, detail=f"Error from ADK server: {e.response.text}")
    except Exception as e:
        logging.error(f"Error running agent {request.agent_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Helper Functions (create_session has no changes) ---
async def create_session(agent_url: str, user_id: str, app_name: str) -> str:
    """Create a new session with the ADK agent"""
    session_id = f"session-{int(time.time())}"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"{agent_url}/apps/{app_name}/users/{user_id}/sessions/{session_id}",
            headers={"Content-Type": "application/json"},
            json={}
        )
        response.raise_for_status()
        return session_id

# -------------------------------------------------------------------
# vv THIS IS THE ONLY FUNCTION THAT HAS CHANGED vv
# -------------------------------------------------------------------
async def run_agent_session(agent_url: str, message: str, user_id: str, app_name: str, session_id: str) -> str:
    """Run the agent and parse the response universally."""
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{agent_url}/run",
            headers={"Content-Type": "application/json"},
            json={
                "app_name": app_name,
                "user_id": user_id,
                "session_id": session_id,
                "new_message": {
                    "role": "user",
                    "parts": [{"text": message}]
                }
            }
        )
        response.raise_for_status()

        # --- UNIVERSAL PARSING LOGIC ---
        events: List[Dict[str, Any]] = response.json()
        
        final_response = "Agent did not provide a final text response."
        
        # Iterate backwards through events to find the last model response first.
        for event in reversed(events):
            content = event.get("content")
            if content and content.get("role") == "model" and "parts" in content:
                # Once we find the model's turn, search its parts for the text.
                # Iterate backwards through parts to find the final text first.
                for part in reversed(content.get("parts", [])):
                    if isinstance(part, dict) and "text" in part:
                        final_response = part["text"]
                        # Found the final answer, no need to look further.
                        return final_response
                        
    return final_response
# -------------------------------------------------------------------
# ^^ THIS IS THE ONLY FUNCTION THAT HAS CHANGED ^^
# -------------------------------------------------------------------

# --- Utility Endpoints (No changes here) ---
@app.get("/health")
async def health_check():
    return {"status": "healthy", "agents": list(AGENT_REGISTRY.keys())}

@app.get("/agents")
async def list_agents():
    return {"agents": list(AGENT_REGISTRY.keys())}

# --- Main Execution (No changes here) ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)