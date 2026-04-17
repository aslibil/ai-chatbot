from openai import OpenAI

import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Hafızalı AI chatbot başlatıldı. Çıkmak için 'q' yaz.\n")

previous_response_id = None

while True:
    kullanici_sorusu = input("Sen: ")

    if kullanici_sorusu.lower() == "q":
        print("Chatbot kapatıldı.")
        break

    if previous_response_id is None:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=kullanici_sorusu
        )
    else:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=kullanici_sorusu,
            previous_response_id=previous_response_id
        )

    print("\nAI:", response.output_text)
    print("-" * 40)

    previous_response_id = response.id