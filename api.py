from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

# 🔥 CORS EKLENDİ
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=mesaj.message
        )

        # güvenli okuma
        if response.output and len(response.output) > 0:
            cevap = response.output[0].content[0].text
        else:
            cevap = "Boş cevap geldi"

        return {"cevap": cevap}

    except Exception as e:
        return {"hata": str(e)}