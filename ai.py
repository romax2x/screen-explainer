import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def explain_text(text, lang="RU"):

    if lang == "RU":
        system_prompt = (
            "Ты объясняешь текст со скриншота. "
            "Отвечай ТОЛЬКО на русском языке. "
            "Если текст искажен — исправь его и объясни смысл."
        )
    else:
        system_prompt = (
            "You explain text from a screenshot. "
            "Answer ONLY in English. "
            "If the text is distorted, fix it and explain the meaning."
        )

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3.2:1b",
            "prompt": system_prompt + "\n\n" + text,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]