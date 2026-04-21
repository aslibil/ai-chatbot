from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
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

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Mesaj(BaseModel):
    message: str

# 🔹 CHAT endpoint (chat bot)
@app.post("/chat")
def chat(mesaj: Mesaj):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=mesaj.message
    )

    return {
        "cevap": response.output[0].content[0].text
    }

# 🔥 NEWS endpoint (haber üretici)
prompt = f"""
Sen profesyonel bir haber editörüsün.

Aşağıdaki kurallara göre haber yaz:

- Başlık: dikkat çekici ve SEO uyumlu olsun
- Giriş: kısa ve çarpıcı
- Detay: 2-3 paragraf
- Tarafsız ve gerçekçi yaz
- Türkçe yaz

Konu: {mesaj.message}

Format:

BAŞLIK:
...

HABER:
...
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return {
        "haber": response.output[0].content[0].text
    }