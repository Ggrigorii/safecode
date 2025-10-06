from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="SafeCode AI — Security Code Analyzer")

# Определяем модель запроса
class CodeRequest(BaseModel):
    code: str
    language: str = "python"

# Импортируем RAG
from rag import get_relevant_context

@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    code = request.code
    language = request.language

    # Получаем контекст из RAG
    context = get_relevant_context(code)

    prompt = f"""
    Ты — эксперт по безопасности кода. Проанализируй следующий код на предмет уязвимостей.
    Если найдёшь уязвимости — выведи:
    1. Тип уязвимости (например, SQL Injection, XSS, Hardcoded Secrets)
    2. Описание риска
    3. Как исправить
    4. Ссылку на OWASP/CWE (если применимо)

    Используй следующую информацию из базы знаний, чтобы сделать анализ точнее:
    ---
    {context}
    ---

    Код ({language}):
    ```{language}
    {code}
    ```

    Ответ должен быть на русском языке, структурированным и полезным для разработчика.
    """

    HF_API_KEY = os.getenv("HF_API_KEY")  # Получаем ключ из переменной окружения

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct",
            headers={"Authorization": f"Bearer {HF_API_KEY}"},
            json={
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 512,
                    "temperature": 0.3,
                    "return_full_text": False
                }
            }
        )
        response.raise_for_status()
        result = response.json()

        # Извлекаем ответ модели
        generated_text = result[0]['generated_text'].strip()

        # Убираем промпт из ответа (если нужно)
        if prompt in generated_text:
            analysis = generated_text.replace(prompt, "").strip()
        else:
            analysis = generated_text

        return {"analysis": analysis}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))