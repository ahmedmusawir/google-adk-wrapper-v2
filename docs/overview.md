# ADK Wrapper Service Overview

## Core Function

The ADK Wrapper is a lightweight, stateless middleware service designed to act as a smart gateway between any frontend application and the backend ADK Agent Bundle. Its primary purpose is to simplify frontend development by abstracting away the complexities of the ADK's session management and response format.

Think of the wrapper as a **concierge**. The frontend makes a simple request (e.g., "ask this agent a question"), and the wrapper handles all the necessary backend logistics—finding the right agent, ensuring a valid conversation session exists, and returning a clean, simple answer.

---

## Key Responsibilities

The wrapper has several distinct responsibilities:

- **Request Routing**: It maintains a registry of live agent bundle URLs (injected via environment variables) and forwards incoming requests to the correct backend service.
- **Session Management**: It intelligently manages ADK sessions. If a frontend provides an invalid or expired `session_id`, the wrapper automatically creates a new session and retries the request, ensuring a seamless user experience.
- **Response Parsing**: The ADK Agent Bundle returns a detailed array of JSON events for each turn. The wrapper processes this complex array, extracts the final "model" response text, and returns it in a simple, predictable format.
- **History Normalization**: It provides a `/get_history` endpoint that fetches the raw ADK session data and transforms it into a clean, standardized `role`/`content` format suitable for direct rendering in a chat UI.
- **Decoupling**: It serves as a durable interface that decouples the frontend from the backend. The backend ADK Agent Bundle can be updated, moved, or even completely replaced without requiring any changes to the frontend, as long as the wrapper's contract is maintained.

---

## Technology Stack

- **Framework**: Python with **FastAPI** for creating robust, high-performance API endpoints.
- **Web Server**: **Uvicorn** for running the application in a production environment.
- **Deployment**: Deployed as a serverless container on **Google Cloud Run**.
