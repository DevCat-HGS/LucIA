from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from ..agents.nlp_agent.nlp_agent import NLPAgent
from ..agents.core.config.nlp_config import NLPConfig

app = FastAPI(title="LucIA API", version="1.0.0")

# Inicializar el agente NLP
nlp_agent = NLPAgent()

class Message(BaseModel):
    text: str
    language: str = "es"

class ChatResponse(BaseModel):
    response: str
    conversation_history: List[Dict[str, str]]

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):
    try:
        response = nlp_agent.process_input(message.text, message.language)
        return ChatResponse(
            response=response,
            conversation_history=nlp_agent.get_conversation_history()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear-history")
async def clear_history():
    nlp_agent.clear_history()
    return {"message": "Historial de conversación limpiado"}

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de LucIA",
        "version": "1.0.0",
        "status": "online"
    }