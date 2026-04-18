from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Mesaj(BaseModel):
    message: str

@app.post("/chat")
def chat(mesaj: Mesaj):

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=mesaj.message
    )

    # 🔥 SAFE PARSE (HATA ÖNLEYİCİ)
    cevap = response.output[0].content[0].text if response.output else "Boş cevap"

    return {"cevap": cevap}