import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

# 環境変数（OPENAI_API_KEY）を読み込む
load_dotenv()

# LLMからの回答を取得する関数
def get_response(role: str, user_input: str) -> str:
    # 選択された専門家に応じてシステムメッセージを切り替え
    role_messages = {
        "法律の専門家": "あなたは経験豊富な法律の専門家です。法律に基づき、一般人にも分かりやすく丁寧に答えてください。",
        "栄養士": "あなたは信頼できる栄養士です。健康と栄養に関する疑問に、的確で親しみやすく答えてください。",
    }

    # LLMのインスタンス生成（APIキーは環境変数に設定済み前提）
    chat = ChatOpenAI(temperature=0.7)

    # システムメッセージとユーザーメッセージを構成
    messages = [
        SystemMessage(content=role_messages.get(role, "あなたは親切なアシスタントです。")),
        HumanMessage(content=user_input)
    ]

    # 応答を取得
    response = chat(messages)
    return response.content

# --- Streamlit アプリ本体 ---
st.title("LLM専門家アシスタント")
st.write("このアプリでは、AIに法律や栄養に関する質問ができます。\n"
         "下記から専門家を選択し、質問を入力して「送信」ボタンを押してください。")

# 専門家の種類を選択（ラジオボタン）
role = st.radio("専門家の種類を選んでください：", ("法律の専門家", "栄養士"))

# ユーザー入力フォーム
user_input = st.text_input("質問を入力してください")

# 回答を表示
if st.button("送信"):
    if user_input:
        answer = get_response(role, user_input)
        st.subheader("AIからの回答")
        st.write(answer)
    else:
        st.warning("質問を入力してください。")
