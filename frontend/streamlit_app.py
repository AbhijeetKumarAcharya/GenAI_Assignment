import streamlit as st
import requests

st.set_page_config(page_title="ZDS GenAI Assignment", layout="centered")

st.title("📄 ZDS GenAI Assignment – Document Q&A")

mode = st.selectbox(
    "Choose Mode",
    ["RAG Mode", "Agent Mode"],
    key="mode_select"
)

query = st.text_input(
    "Enter your question",
    key="query_input"
)

if st.button("Ask", key="ask_button"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        endpoint = "ask" if mode == "RAG Mode" else "agent-ask"
        url = "http://127.0.0.1:8000/" + endpoint

        response = requests.post(
            url,
            json={"query": query}
        )

        if response.status_code == 200:
            data = response.json()

            st.subheader("Answer")
            if mode == "RAG Mode":
                st.write(data.get("answer"))
            else:
                st.write(data.get("final_answer"))

            st.subheader("Retrieved Context")
            st.json(data.get("context", data.get("sources", [])))
        else:
            st.error("Backend error")
