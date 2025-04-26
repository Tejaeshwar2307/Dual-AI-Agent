from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(api_key="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")

# Fetch the list of available models
try:
    models = client.models.list()
    print("Available Models:")
    for model in models.data:
        print(f"- {model.id}")
except Exception as e:
    print("Error fetching models:", e)