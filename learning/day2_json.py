import json

decision = {
    "intent": "claims",
    "action": "explain",
    "needs_tool": False,
    "tool": "none"
}

# Convert Python dictionary to JSON
json_output = json.dumps(decision, indent=2)

print("JSON:")
print(json_output)

# Convert JSON back into a Python dictionary
parsed = json.loads(json_output)

print("Intent:", parsed["intent"])
print("Action:", parsed["action"])
print("Tool Required:", parsed["needs_tool"])
print("Selected Tool:", parsed["tool"])