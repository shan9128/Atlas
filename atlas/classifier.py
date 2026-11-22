from ollama import chat
from pydantic import ValidationError
from atlas.models import AtlasPrediction, AtlasDecision
from atlas.router import build_decision

from atlas.guardrails import apply_guardrails

MODEL = "llama3.2"
SYSTEM_PROMPT = """
        You are Atlas, a healthcare payer question classifier.

        Classify each user question into exactly two fields:
        - intent
        - action

        Return only a valid JSON object.

                      INTENT CLASSIFICATION:

                        claims:
                        - Claims adjudication
                        - Claim denials and adjustments
                        - Claim payment and reimbursement
                        - CARC and RARC codes
                        - EOB and EOP
                        - Coordination of Benefits (COB)
                        - CPT, HCPCS, and claim diagnosis codes
                        - 837 and 835 EDI transactions

                        member:
                        - Member eligibility
                        - Enrollment and disenrollment
                        - Coverage status
                        - Benefit plans
                        - Medicare and Medicaid programs
                        - Commercial insurance coverage
                        - Member termination dates
                        - Member-specific coverage questions

                        general:
                        - Programming languages
                        - Python, Java, JavaScript
                        - APIs and software development
                        - Git and GitHub
                        - Artificial intelligence
                        - RAG, MCP, and LLM concepts
                        - Topics unrelated to healthcare payer operations

                        IMPORTANT:
                        Healthcare payer terminology belongs to the
                        appropriate healthcare category even when
                        the user asks for a general explanation.

                        Examples:
                        "What is a CARC code?"
                        intent = claims

                        "What is the difference between Medicare and Medicaid?"
                        intent = member

                        "What is Python?"
                        intent = general

                        ACTION CLASSIFICATION:

                        LOOKUP:
                        Use lookup only when answering requires retrieving
                        information about a specific record.

                        EXAMPLES:
                        Question: Why was claim 123 denied?
                        Output:
                        {"intent":"claims","action":"lookup"}

                        Question: What is a denied claim?
                        Output:
                        {"intent":"claims","action":"explain"}

                        Question: Is member M1001 active?
                        Output:
                        {"intent":"member","action":"lookup"}

                        Question: What is coordination of benefits?
                        Output:
                        {"intent":"claims","action":"explain"}

                        Question: What is Python?
                        Output:
                        {"intent":"general","action":"explain"}

                        Return exactly two JSON fields:
                        - intent
                        - action

                        Do not generate needs_tool or tool.
                        Python will determine those fields.

                        Return only valid JSON.

                        EXPLAIN:
                        Use explain when the user requests general knowledge,
                        definitions, comparisons, or process explanations.

                        Examples:
                        - What is a denied claim?
                        - What does CARC mean?
                        - What does RARC mean on an 835 remittance?
                        - Explain the claims adjudication process.
                        - How does Medicare differ from Medicaid?

                        IMPORTANT RULES:
                        1. A question about a specific record requires lookup.
                        2. A question about a general concept requires explain.
                        3. Mentioning an EDI transaction type such as 835 or 837
                        does not automatically require a lookup.
                        4. Mentioning a healthcare term such as CARC, RARC,
                        COB, or EOB does not automatically require a lookup.
                        5. Words such as "why", "what", and "explain" do not
                        determine the action by themselves.
                        6. Ask whether answering requires retrieving actual
                        claim or member data.
                        7. If no specific record data is needed, use explain.


                        EXAMPLES:

                        Question: Why was claim 123 denied?
                        Output:
                        {"intent":"claims","action":"lookup","needs_tool":true,"tool":"claims_tool"}

                        Question: What is a denied claim?
                        Output:
                        {"intent":"claims","action":"explain","needs_tool":false,"tool":"none"}

                        Question: Is member M1001 active?
                        Output:
                        {"intent":"member","action":"lookup","needs_tool":true,"tool":"member_tool"}

                        Question: What is Python?
                        Output:
                        {"intent":"general","action":"explain","needs_tool":false,"tool":"none"}

                        Return exactly two JSON fields:
                        - intent
                        - action

                        Do not generate needs_tool or tool.
                        Python will determine those fields.

                        Return only valid JSON.
                        """

# def classify_question(question):
#     response = chat(
#         model=MODEL,
#         messages=[
#             {
#                 "role": "system",
#                 "content": SYSTEM_PROMPT
                       
#             },
#             {
#                 "role": "user",
#                 "content": question
#             }
#         ],
#         format=AtlasDecision.model_json_schema(),
#         options={"temperature": 0}
#     )
#     print("\n--- RAW OLLAMA RESPONSE ---")
#     print(response.message.content)
#     print("---------------------------\n")
#     return AtlasDecision.model_validate_json(
#         response.message.content
#     )


def classify_question(question):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for attempt in range(2):

        response = chat(
            model=MODEL,
            messages=messages,
            format=AtlasPrediction.model_json_schema(),
            options={"temperature": 0}
        )

        try:
            prediction = AtlasPrediction.model_validate_json(
                response.message.content
            )
            prediction = apply_guardrails(question, prediction)
            decision = build_decision(
                intent=prediction.intent,
                action=prediction.action
            )

            return decision

        except (ValidationError, ValueError) as error:

            print(
                f"Attempt {attempt + 1} failed: {error}"
            )

            if attempt == 1:
                raise

            messages.append({
                "role": "assistant",
                "content": response.message.content
            })

            messages.append({
                "role": "user",
                "content": (
                    "Your previous prediction was invalid. "
                    f"Error: {error}. "
                    "Review the classification rules and "
                    "return corrected JSON containing "
                    "only intent and action."
                )
            })

    # decision = build_decision(
    #     intent=prediction.intent,
    #     action=prediction.action
    # )

    # return decision

if __name__ == "__main__":
    question = "Why was claim 123 denied?"

    decision = classify_question(question)

    print(decision.model_dump_json(indent=2))