import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from dotenv import load_dotenv

# ローカル用：.env を読み込む
load_dotenv()

# Cloud対応：Streamlit Secrets からも読む
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]

# LLMからの回答を返す関数
def get_response(role: str, user_input: str) -> str:
    role_messages = {
        "心理学者": "あなたは熟練の心理学者として、感情面の問題や人間関係について的確にアドバイスを行ってください。",
        "キャリアコンサルタント": "あなたは優秀なキャリアコンサルタントとして、転職・仕事・スキル開発について専門的に助言を行ってください。"
    }

    system_msg = role_messages.get(role, "あなたは有能なアシスタントです。")

    chat = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)

    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=user_input)
    ]

    response = chat(messages)
    return response.content
