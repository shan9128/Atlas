from atlas.models import AtlasDecision

def build_decision(intent, action):

    if action == "explain":
        needs_tool = False
        tool = "none"

    elif action == "lookup":
        needs_tool = True

        if intent == "claims":
            tool = "claims_tool"

        elif intent == "member":
            tool = "member_tool"

        else:
            raise ValueError(
                "General lookup is not supported"
            )

    else:
        raise ValueError("Unsupported action")

    return AtlasDecision(
        intent=intent,
        action=action,
        needs_tool=needs_tool,
        tool=tool
    )