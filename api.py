from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
istek_sayaci = {}
MAKSIMUM_ISTEK = 5

class Mesaj(BaseModel):
    message: str

@app.post("/chat")
def chat(mesaj: Mesaj, x_api_key: str = Header(None)):
    if x_api_key != firma_api_key:
        raise HTTPException(status_code=401, detail="Yetkisiz erişim")

    if x_api_key not in istek_sayaci:
        istek_sayaci[x_api_key] = 0

    if istek_sayaci[x_api_key] >= MAKSIMUM_ISTEK:
        raise HTTPException(status_code=429, detail="Kullanım limitiniz doldu")

    istek_sayaci[x_api_key] += 1

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=mesaj.message
    )

    return {
        "cevap": response.output_text,
        "kalan_hak": MAKSIMUM_ISTEK - istek_sayaci[x_api_key]
    }