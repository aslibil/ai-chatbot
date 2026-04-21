from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# .env yükle
load_dotenv()

app = FastAPI()

# CORS (frontend bağlanabilsin diye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# request modeli
class Mesaj(BaseModel):
    message: str

# güvenli text alma
def get_text(response):
    try:
        return response.output[0].content[0].text
    except:
        return "Haber alınamadı"

# 🔥 NEWS endpoint
@app.post("/news")
def news(mesaj: Mesaj):

    prompt = f"""
Sen profesyonel bir haber editörüsün.

Aşağıdaki kurallara kesinlikle uy:

- Türkçe yaz
- Kısa ve net yaz
- Abartı yapma
- Gerçekçi yaz

FORMAT:

TITLE: kısa ve dikkat çekici başlık

CONTENT: 2-3 cümlelik haber özeti

Konu: {mesaj.message}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        text = get_text(response)
    except Exception as e:
        text = "Şu anda haber alınamıyor"

    return {"haber": text}


# 🔹 CHAT endpoint (opsiyonel)
@app.post("/chat")
def chat(mesaj: Mesaj):

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=mesaj.message
        )
        text = get_text(response)
    except:
        text = "Cevap alınamadı"

    return {"cevap": text}