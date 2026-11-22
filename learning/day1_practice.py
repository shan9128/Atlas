# A list of supported AI models
models = ["llama3.2", "qwen2.5"]

# A dictionary containing agent configuration
agent = {
    "name": "Atlas",
    "model": "llama3.2",
    "memory_enabled": True
}

# A function
def describe_agent(config):
    return f"{config['name']} uses {config['model']}"

print(describe_agent(agent))

def choose_model(task):
    if task == "simple":
        return "llama3.2"
    elif task == "complex":
        return "strong_model"
    else:
        return "unknown"
print(choose_model("simple"))
print(choose_model("complex"))
print(choose_model("unknown"))

# A loop
for model in models:
    print("Available model:", model)