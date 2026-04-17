import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

st.title("Hafızalı Yapay Zeka Chatbot")
st.write("Mesaj yaz, ben de geçmişi hatırlayarak cevap vereyim.")

if st.button("Sohbeti Temizle"):
    st.session_state.mesajlar = []
    st.rerun()

if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["role"]):
        st.write(mesaj["content"])

kullanici_mesaji = st.chat_input("Mesajını yaz...")

if kullanici_mesaji:
    st.session_state.mesajlar.append({
        "role": "user",
        "content": kullanici_mesaji
    })

    with st.chat_message("user"):
        st.write(kullanici_mesaji)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=st.session_state.mesajlar
    )

    cevap = response.output_text

    st.session_state.mesajlar.append({
        "role": "assistant",
        "content": cevap
    })

    with st.chat_message("assistant"):
        st.write(cevap)