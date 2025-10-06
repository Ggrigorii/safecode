#!/bin/bash

# Установка Ollama (если Render позволяет)
curl -fsSL https://ollama.com/install.sh | sh

# Загрузка модели
ollama pull phi3:latest

# Настройка RAG
python -c "from rag import setup_rag; setup_rag()"

# Запуск backend
uvicorn main:app --host 0.0.0.0 --port 8000 &
# Запуск frontend
python frontend.py