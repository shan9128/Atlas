
from fastapi import FastAPI
from pydantic import BaseModel, field_validator

from atlas.agent import run_agent
from atlas.responses.day3_response import format_claim_response
from atlas.responses.day4_response import format_member_response

from fastapi import HTTPException
from ollama import ResponseError
from httpx import ConnectError

app = FastAPI(title="Atlas AI Agent", version="1.0.0")


class AgentRequest(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def validate_question(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Question cannot be empty")

        return value.strip()


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "atlas-ai-agent"
    }


@app.post("/agent")
def ask_agent(request: AgentRequest):
    try:
        result = run_agent(request.question)
    except (ConnectError, ConnectionError, TimeoutError) as exc:
        raise HTTPException(
            status_code=503,
            detail="Atlas AI service is temporarily unavailable"
        ) from exc
    except ResponseError as exc:
        raise HTTPException(
            status_code=502,
            detail="Atlas AI model returned an error"
        ) from exc

    if isinstance(result, dict):
        if "claim_id" in result:
            answer = format_claim_response(result)
        elif "member_id" in result:
            answer = format_member_response(result)
        else:
            answer = result
    else:
        answer = result

    return {
        "question": request.question,
        "answer": answer
    }
