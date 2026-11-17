from typing import Literal
from pydantic import BaseModel, model_validator


class AtlasDecision(BaseModel):
    intent: Literal["claims", "member", "general"]
    action: Literal["lookup", "explain"]
    needs_tool: bool
    tool: Literal["claims_tool", "member_tool", "none"]

    @model_validator(mode="after")
    def validate_tool_consistency(self):
        if self.needs_tool and self.tool == "none":
            raise ValueError(
                "A tool must be selected when needs_tool=True"
            )
        if not self.needs_tool and self.tool != "none":
            raise ValueError(
                "Tool must be 'none' when needs_tool=False"
            )
        if self.action == "explain" and self.needs_tool:
            raise ValueError(
                "Explain action should not require a tool"
            )
        if self.action == "lookup" and not self.needs_tool:
            raise ValueError(
                "Lookup action requires a tool"
            )
        if self.intent == "claims" and self.action == "lookup":
            if self.tool != "claims_tool":
                raise ValueError(
                    "Claims intent with lookup action requires claims_tool"
                )
        return self
class AtlasPrediction(BaseModel):
    intent: Literal["claims", "member", "general"]
    action: Literal["lookup", "explain"]

if __name__ == "__main__":
    decision = AtlasDecision(
        intent="claims",
        action="lookup",
        needs_tool=True,
        tool="claims_tool"
    )
    print(decision.model_dump_json(indent=2))