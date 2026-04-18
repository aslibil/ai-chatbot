from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# hafıza
sohbetler = {}

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Mesaj(BaseModel):
    message: str

@app.post("/chat")
def chat(mesaj: Mesaj):

    try:
        user_id = "default_user"

        # kullanıcı hafızası yoksa oluştur
        if user_id not in sohbetler:
            sohbetler[user_id] = []

        # kullanıcı mesajı ekle
        sohbetler[user_id].append({
            "role": "user",
            "content": mesaj.message
        })

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {
                   "role": "system",
"content": "Sen profesyonel bir haber editörüsün. Kullanıcıya Türkçe olarak haber formatında cevap ver. Cevaplarında mutlaka bir başlık, kısa açıklama ve gerekiyorsa maddeler kullan."
                },
                *sohbetler[user_id]
            ]
        )

        cevap = response.output[0].content[0].text

        # bot cevabı ekle
        sohbetler[user_id].append({
            "role": "assistant",
            "content": cevap
        })

        return {"cevap": cevap}

    except Exception as e:
        return {"hata": str(e)}