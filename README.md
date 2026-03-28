# 🎬 Inclusive AI — Расшифровка видео с помощью GigaChat

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green.svg)](https://fastapi.tiangolo.com/)
[![GigaChat](https://img.shields.io/badge/GigaChat-API-orange.svg)](https://developers.sber.ru/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🚀 Сервис для автоматической расшифровки речи из видео с использованием нейросети GigaChat от Сбера. Проект помогает создавать текстовые версии видеоуроков, лекций, интервью и другого контента.

## ✨ Возможности

- 📤 Загрузка видео в форматах MP4, MOV, AVI, MKV
- 🎵 Автоматическое извлечение аудиодорожки
- 🤖 Распознавание речи через GigaChat API
- 📝 Вывод расшифрованного текста с копированием
- 🖥️ Простой веб-интерфейс с индикацией прогресса
- 🔒 Поддержка видео до 200 МБ (аудио до 30 МБ)

## 🛠️ Технологии

| Компонент | Технология | Назначение |
|-----------|------------|------------|
| **Бэкенд** | Python 3.10+, FastAPI | Серверная логика, API |
| **Распознавание** | GigaChat API | Преобразование речи в текст |
| **Аудио** | FFmpeg + MoviePy | Извлечение звука из видео |
| **Фронтенд** | HTML5, CSS3, JavaScript | Интерфейс пользователя |
| **Сервер** | Uvicorn | ASGI-сервер для FastAPI |
