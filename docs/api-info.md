Of course. I have the URL from the successful deployment. Here is the final documentation file, `api-info.md`.

---

### `/docs/api-info.md`

```markdown
# ADK Wrapper API Information

This document provides the necessary information to interact with the deployed ADK Wrapper service.

---

## Service URL

The ADK Wrapper is deployed as a serverless container on Google Cloud Run. The stable production endpoint is:

**Production URL:**
```

[https://adk-wrapper-prod-v2-952978338090.us-east1.run.app](https://adk-wrapper-prod-v2-952978338090.us-east1.run.app)

````

---
## API Endpoints

The wrapper exposes the following endpoints for frontend consumption.

### `POST /run_agent`

This is the primary endpoint for sending a message to a specific agent and receiving a response. It handles session creation and response parsing automatically.

**Request Body:**
```json
{
  "agent_name": "jarvis_agent",
  "message": "What were the key lessons from ADK Hybrid Lab 8?",
  "user_id": "user-tony-stark",
  "session_id": "session-1729354800"
}
````

- `session_id` is optional. If omitted or invalid, the wrapper will create a new session.

**Success Response (200 OK):**

```json
{
  "response": "The key lesson was to adopt a two-phase protocol for cloud development, using a public IP for local testing and a private IP for production deployment.",
  "session_id": "session-1729354800",
  "agent_name": "jarvis_agent",
  "status": "success"
}
```

\<hr\>

### `POST /get_history`

Fetches the formatted conversation history for a given user and session.

**Request Body:**

```json
{
  "agent_name": "jarvis_agent",
  "user_id": "user-tony-stark",
  "session_id": "session-1729354800"
}
```

**Success Response (200 OK):**

```json
{
  "history": [
    {
      "role": "user",
      "content": "What were the key lessons from ADK Hybrid Lab 8?"
    },
    {
      "role": "assistant",
      "content": "The key lesson was to adopt a two-phase protocol for cloud development..."
    }
  ]
}
```

\<hr\>

### `GET /health`

A simple health check endpoint to verify that the service is running.

**Response (200 OK):**

```json
{
  "status": "healthy",
  "agents": [
    "greeting_agent",
    "jarvis_agent",
    "calc_agent",
    "product_agent",
    "ghl_mcp_agent"
  ]
}
```

---

## Example Frontend Usage (Python)

Here is a simple example of how to call the wrapper from a Python application, such as a Streamlit frontend.

```python
import requests
import json

# The stable URL of the deployed wrapper
WRAPPER_URL = "[https://adk-wrapper-prod-v2-952978338090.us-east1.run.app](https://adk-wrapper-prod-v2-952978338090.us-east1.run.app)"

def ask_agent(agent, message, user, session=None):
    """Sends a request to the ADK Wrapper."""

    endpoint = f"{WRAPPER_URL}/run_agent"

    payload = {
        "agent_name": agent,
        "message": message,
        "user_id": user,
        "session_id": session
    }

    print(f"Sending request to {endpoint}...")

    try:
        response = requests.post(endpoint, json=payload, timeout=90)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        response_data = response.json()
        print("--- Agent Response ---")
        print(json.dumps(response_data, indent=2))
        return response_data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# --- Example Call ---
if __name__ == "__main__":
    ask_agent(
        agent="jarvis_agent",
        message="What is the purpose of the ADK Wrapper?",
        user="user-tony-stark"
    )

```
