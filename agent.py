from structured_agent import (
    classify_with_llm,
    Classification,
    route_request
)

from tools import (
    claims_tool,
    member_tool,
    provider_tool,
    rag_search,
    general_llm
)


def run_agent(question: str):

    # 1. Classify
    result = classify_with_llm(question)

    # 2. Validate
    validated = Classification(**result)

    # 3. Route
    route = route_request(validated)

    # 4. Execute
    if route == "claims_tool":
        tool_result = claims_tool(question)

    elif route == "member_tool":
        tool_result = member_tool(question)

    elif route == "provider_tool":
        tool_result = provider_tool(question)

    elif route == "rag_search":
        tool_result = rag_search(question)

    else:
        tool_result = general_llm(question)

    return {
        "question": question,
        "classification": validated.model_dump(),
        "route": route,
        "result": tool_result
    }