import requests
import os

HF_API_KEY = os.getenv("HF_API_KEY")  # Заведи переменную окружения

def analyze_code(request: CodeRequest):
    code = request.code
    language = request.language

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

    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/microsoft/Phi-3-mini-4k-instruct",
            headers={"Authorization": f"Bearer {HF_API_KEY}"},
            json={"inputs": prompt, "parameters": {"max_new_tokens": 512}}
        )
        result = response.json()
        return {"analysis": result[0]['generated_text'].replace(prompt, "").strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))