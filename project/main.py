import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from moviepy.video.io.VideoFileClip import VideoFileClip

app = FastAPI(title="Video to Text via GigaChat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⬇️ ВАША АВТОРИЗАЦИОННАЯ СТРОКА
AUTH_DATA = "MDE5YjMxZWUtYTUzZS03ZDc4LThkZmItM2MzNjNmYTVhZDIzOjY4OWE1NjNjLTQ4ZDYtNDViMC1hMmI4LWI3NGViZDlmMzUxMw=="

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/transcribe")
async def transcribe_video(file: UploadFile = File(...)):
    video_path = None
    audio_path = None
    try:
        print(f"Получен файл: {file.filename}")
        
        video_bytes = await file.read()
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
            tmp.write(video_bytes)
            video_path = tmp.name
        print(f"Видео сохранено: {video_path}")

        audio_path = video_path.replace(".mp4", ".mp3")
        clip = VideoFileClip(video_path)
        clip.audio.write_audiofile(audio_path, codec='mp3', bitrate='128k')
        clip.close()
        print(f"Аудио извлечено: {audio_path}")

        size_mb = os.path.getsize(audio_path) / (1024 * 1024)
        print(f"Размер аудио: {size_mb:.2f} МБ")
        if size_mb > 30:
            raise HTTPException(status_code=413, detail="Аудио превышает 30 МБ")

        with GigaChat(
            credentials=AUTH_DATA,
            verify_ssl_certs=False,
            user="",
            password=""
        ) as giga:
            with open(audio_path, "rb") as f:
                uploaded_file = giga.upload_file(f)
            print(f"Файл загружен в GigaChat, ID: {uploaded_file.id_}")

            # Используем модель GigaChat:latest (поддерживает аудио)
            payload = Chat(
                messages=[
                    Messages(
                        role=MessagesRole.USER,
                        content="Расшифруй речь из этого аудио. Выдай только текст, без комментариев.",
                        attachments=[uploaded_file.id_]
                    )
                ],
                model="GigaChat-Pro"
            )
            
            response = giga.chat(payload)
            text = response.choices[0].message.content
            print("Расшифровка получена")
            return JSONResponse(content={"text": text})

    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if video_path and os.path.exists(video_path):
            os.unlink(video_path)
        if audio_path and os.path.exists(audio_path):
            os.unlink(audio_path)

@app.get("/")
async def root():
    from fastapi.responses import FileResponse
    return FileResponse("static/index.html")
