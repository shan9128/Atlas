from fastapi import FastAPI
from pydantic import BaseModel
from ollama import chat

from structured_agent import (
    classify_with_llm,
    Classification,
    route_request
)

from agent import run_agent


MODEL = "llama3.2"


app = FastAPI(
    title="Atlas AI Agent",
    version="0.1.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "message": "Atlas AI Agent is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": MODEL
    }


@app.post("/classify")
def classify(request: QuestionRequest):

    result = classify_with_llm(request.question)

    validated = Classification(**result)

    route = route_request(validated)

    return {
        "classification": validated.model_dump(),
        "route": route
    }


@app.post("/chat")
def chat_endpoint(request: QuestionRequest):

    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": request.question
            }
        ]
    )

    return {
        "model": MODEL,
        "question": request.question,
        "answer": response.message.content
    }


@app.post("/agent")
def agent_endpoint(request: QuestionRequest):

    return run_agent(request.question)