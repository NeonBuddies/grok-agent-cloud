
import os
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(title="GROK AGENT CLOUD")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://api.freetheai.org/v1/chat/completions"
MODEL = "fta/zai/glm-5.3"

class ChatRequest(BaseModel):
    messages: list

@app.get("/")
def home():
    return {
        "status": "online",
        "agent": "GROK AGENT CLOUD"
    }

@app.post("/chat")
def chat(data: ChatRequest):
    api_key = os.environ.get("FREETHEAI_API_KEY")

    if not api_key:
        return JSONResponse(
            status_code=500,
            content={"error": "FREETHEAI_API_KEY is missing"}
        )

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": data.messages,
                "max_tokens": 1000,
                "temperature": 0.7
            },
            timeout=90
        )

        try:
            result = response.json()
        except ValueError:
            result = {"error": response.text[:1000]}

        return JSONResponse(
            status_code=response.status_code,
            content=result
        )

    except requests.RequestException as error:
        return JSONResponse(
            status_code=502,
            content={"error": str(error)}
        )

