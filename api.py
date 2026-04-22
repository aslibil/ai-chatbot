import feedparser
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

Şu kurallara uy:

- Türkçe yaz
- Gerçekçi yaz
- SEO uyumlu başlık

FORMAT:

TITLE: dikkat çekici başlık

CONTENT:
- 1 kısa giriş
- 2 kısa paragraf

Konu: {mesaj.message}
"""
@app.get("/realnews")
def real_news():

    feed = feedparser.parse("https://rss.app/feeds/turkey-news.xml")

    news_list = []

    for entry in feed.entries[:5]:

        prompt = f"""
Aşağıdaki haberi yeniden yaz:

- Türkçe yaz
- Daha akıcı yap
- Başlık üret

Haber:
{entry.title}

FORMAT:

TITLE:
...

CONTENT:
...
"""

        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )

            text = get_text(response)
        except:
            text = "Haber alınamadı"

        news_list.append(text)

    return {"news": news_list}