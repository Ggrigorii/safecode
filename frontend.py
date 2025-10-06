import gradio as gr
import requests

def analyze_code(code, language):
    url = "http://localhost:8000/analyze"
    payload = {"code": code, "language": language}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["analysis"]
    except Exception as e:
        return f"❌ Ошибка: {str(e)}"

demo = gr.Interface(
    fn=analyze_code,
    inputs=[
        gr.Code(language="python", label="Вставьте ваш код"),
        gr.Dropdown(["python", "javascript", "java", "go"], label="Язык кода")
    ],
    outputs=gr.Markdown(label="Результат анализа"),
    title="🔒 SafeCode AI — Анализатор безопасности кода",
    description="""
    Вставьте код — получите предупреждения и советы по исправлению.
    Использует легковесную модель Phi-3 + базу OWASP/CWE для точного анализа.
    """,
    
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)