import os
import streamlit as st
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# .envからOPENAI_API_KEYを読み込む（ローカル用）
load_dotenv()

# OpenAI APIキーを取得（Cloud環境にも対応）
openai_api_key = os.getenv("OPENAI_API_KEY") or st.secrets["OPENAI_API_KEY"]

# LLMへの問い合わせ関数
def get_response(role: str, user_input: str) -> str:
    # 選択された専門家に応じたシステムメッセージ
    role_messages = {
        "法律の専門家": "あなたは経験豊富な法律の専門家です。法的観点から誠実かつ明確にアドバイスを行ってください。",
        "栄養士": "あなたは資格を持つプロの栄養士です。健康的な食生活や栄養バランスについて、優しく丁寧に回答してください。"
    }

    system_msg = role_messages.get(role, "あなたは有能なアシスタントです。")

    chat = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)

    messages = [
        SystemMessage(content=system_msg),
        HumanMessage(content=user_input)
    ]

    response = chat(messages)
    return response.content

# --- Streamlit UI ---
st.set_page_config(page_title="専門家AIアシスタント")
st.title("専門家AIチャット")
st.markdown("""
このアプリでは、あなたの質問に対して、選択した**専門家（法律の専門家 または 栄養士）**としてAIが回答します。  
相談したい内容を入力し、「送信」ボタンを押してください。
""")

# ラジオボタンで専門家選択
role = st.radio("専門家を選んでください：", ("法律の専門家", "栄養士"))

# 入力フォーム
user_input = st.text_area("相談内容を入力してください：", height=150)

# 実行ボタン
if st.button("送信"):
    if not user_input.strip():
        st.warning("相談内容を入力してください。")
    else:
        with st.spinner("AIが考え中..."):
            answer = get_response(role, user_input)
            st.success("AIの回答：")
            st.write(answer)
