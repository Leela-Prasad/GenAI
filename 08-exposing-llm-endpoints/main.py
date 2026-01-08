import os
import httpx
import config
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Union
from pydantic import BaseModel

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str
    

class CompletionRequest(BaseModel):
    messages: List[Message]
    model: str
    max_tokens: int = 1024
    temperature: int = 0.7
    

class EmbeddingRequest(BaseModel):
    input: Union[str, List[str]]
    model: str
    
    
def get_opeani_config():
    return config.OPENAI_BASE_URL, config.OPENAI_API_KEY


@app.post("/v1/chat/completions")
async def chat_completions(request: CompletionRequest):
    base_url, key = get_opeani_config()
    url = f"{base_url}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [msg.dict() for msg in request.messages],
        "model": request.model,
        "max_tokens": request.max_tokens,
        "temperature": request.temperature
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return JSONResponse(content=response.json())
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        

@app.post("/v1/embeddings")
async def embeddings(request: EmbeddingRequest):
    base_url, key = get_opeani_config()
    url = f"{base_url}/embeddings"
    
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    inputs = ([request.input] if isinstance(request.input, str) else request.input)
    
    payload = {
        "input": inputs,
        "model": request.model
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return JSONResponse(content=response.json())
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=e.response.text)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))