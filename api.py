from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

# 🔥 CORS EKLENDİ
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

sohbet_gecmisi = []

# 🔥 CORS AYARI (BUNU EKLEMEZSEN FRONTEND ÇALIŞMAZ)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tüm sitelere izin
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
        # kullanıcı mesajını ekle
        sohbet_gecmisi.append({"role": "user", "content": mesaj.message})

        response = client.responses.create(
    model="gpt-4.1-mini",
    input=[
        {
            "role": "system",
            "content": "Sen Türkçe konuşan, kısa ve net cevap veren bir yardımcı asistansın. Gereksiz uzatma yapma."
        },
        *sohbet_gecmisi
    ]
)

        cevap = response.output[0].content[0].text

        # bot cevabını da ekle
        sohbet_gecmisi.append({"role": "assistant", "content": cevap})

        return {"cevap": cevap}

    except Exception as e:
        return {"hata": str(e)}