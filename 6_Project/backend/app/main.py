from fastapi import FastAPI
from pydantic import BaseModel, Field
from .generate_answer import generate_answer
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(
    title="Premier League RAG API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://premier-league-rag-api.onrender.com",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    
class ChatResponse(BaseModel):
    answer:  str

@app.get("/api/v1/health")
def health():   
    return {"status": "healthy"}

@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = generate_answer(request.question)
    return ChatResponse(answer=answer)