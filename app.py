# -*- coding: utf-8 -*-
from __future__ import annotations

import streamlit as st
import random
import time
import json


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "こんにちは！いい天気ですね！",
            "今日は何をしていますか？",
            "何かお手伝いできることはありますか？",
            "ヤマト運輸の荷物が届きました。",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


# サイドバーでページを選択
st.sidebar.markdown("[new_chat](/)")
st.sidebar.title("Session List")
# ToDo: ここはデータベースから取得する
for session_id in ["session1", "session2"]:
    # ユーザーの最初のメッセージを取得
    with open(f"/app/sessions/{session_id}.json", "r") as f:
        data = json.load(f)
    first_message = data[0]["content"]
    st.sidebar.markdown(
        f"[{first_message}](/?page={session_id})"
    )

# クエリパラメータを取得
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["home"])[0]  # デフォルトは "home"

if page == "home":
    # 会話履歴をリセット
    st.session_state.messages = []
    # チャットアプリ
    st.title("LLM Chat App")

elif page in ["session1", "session2"]:
    # Jsonファイルを読み込む
    # ToDo: ここはデータベースから取得する
    with open(f"/app/sessions/{page}.json", "r") as f:
        data = json.load(f)

    # 会話履歴をセッションに追加
    st.session_state.messages = data

    st.title(f"LLM Chat App: {page}")


# チャット履歴がない場合は初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# チャットメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# チャット入力
if prompt := st.chat_input("What is up?"):
    # ユーザーメッセージを表示
    with st.chat_message("user"):
        st.markdown(prompt)
        time.sleep(0.5)
    # ユーザーメッセージを会話履歴に追加
    st.session_state.messages.append({"role": "user", "content": prompt})

    # アシスタントのレスポンスを表示
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())
    # アシスタントのレスポンスを会話履歴に追加
    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })
