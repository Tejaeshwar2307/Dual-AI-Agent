import json
import os

DATA_FILE = "data/knowledge_store.json"

def save_to_knowledge_store(data):
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)
    
    with open(DATA_FILE, "r+") as f:
        existing_data = json.load(f)
        existing_data.append(data)
        f.seek(0)
        json.dump(existing_data, f, indent=4)

def load_from_knowledge_store():
    if not os.path.exists(DATA_FILE):
        return []
    
    with open(DATA_FILE, "r") as f:
        return json.load(f)