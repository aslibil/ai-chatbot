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

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=mesaj.message
        )

        # SAFE extraction
        if response.output and len(response.output) > 0:
            cevap = response.output[0].content[0].text
        else:
            cevap = "Boş cevap geldi"

        return {"cevap": cevap}

    except Exception as e:
        return {
            "hata": str(e)
        }