
# Atlas AI Agent

A Python-based healthcare AI agent prototype built using a local LLM, structured classification, deterministic tool routing, and automated evaluations.

## Features

- Local LLM inference using Ollama and Llama 3.2
- Pydantic-based structured output validation
- Intent classification: claims, member, general
- Action classification: lookup, explain
- Deterministic tool routing
- Claims and member lookup tools
- Guardrails and retry handling
- Automated unit tests and AI evaluations

## Architecture

User Question
    |
    v
Ollama LLM
    |
    v
Structured Classification (Pydantic)
    |
    v
Guardrails + Router
    |
    v
Atlas Agent
    |
    +-- Claims Lookup Tool
    |
    +-- Member Lookup Tool
    |
    v
Formatted Response

## Project Structure

atlas/      Core application and tools
data/       Synthetic healthcare data
evals/      AI evaluation datasets and scripts
tests/      Unit tests
learning/   Earlier learning exercises
Arch/       Previous implementations

## Getting Started

Requirements:
- Python
- Ollama
- Llama 3.2 model

Install and start Ollama, then download the model:

    ollama pull llama3.2

Create a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install Python dependencies:

    pip install ollama pydantic pytest

## Testing

Run unit tests:

    python -m pytest -v

Run classification evaluations:

    python -m evals.day2_evaluate

Run agent evaluations:

    python -m evals.day4_evaluate

## Current Validation Results

- Unit tests: 17 passed
- Classification evaluations: 22/22 passed
- Agent evaluations: 6/6 passed

These results reflect the current development evaluation datasets, not independent production benchmarks.

## Limitations

- Uses synthetic healthcare data
- No production payer-system integration
- No persistent database
- No authentication or authorization layer
- Not intended for processing real PHI
- Requires additional security, observability, and evaluation before production use

## Roadmap

- FastAPI integration
- Persistent data storage
- RAG-based knowledge retrieval
- MCP tool integration
- Logging and observability
- Expanded AI evaluations
- Deployment and CI/CD
