import requests

MODEL = "llama3"

def call_llm(prompt):
    res = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )
    return res.json()["response"]