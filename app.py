import os
import streamlit as st
from openai import OpenAI

# --------------- Configure ---------------
# Option A: Hosted (Hugging Face Inference Providers)
# Set these via `streamlit secrets` or environment variables:
# st.secrets["OPENAI_API_KEY"] = "<HF_TOKEN>"
# st.secrets["OPENAI_API_BASE"] = "https://router.huggingface.co/v1"
# st.secrets["MODEL_NAME"] = "openai/gpt-oss-120b:cerebras"

API_KEY = st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
API_BASE = st.secrets.get("OPENAI_API_BASE", os.getenv("OPENAI_API_BASE", "https://router.huggingface.co/v1"))
MODEL_NAME = st.secrets.get("MODEL_NAME", os.getenv("MODEL_NAME", "openai/gpt-oss-120b:cerebras"))

client = OpenAI(api_key=API_KEY, base_url=API_BASE)

st.set_page_config(page_title="gpt-oss-120b Chatbot", page_icon="🤖")
st.title("gpt-oss-120b Chatbot")

# --------------- Session State ---------------
if "messages" not in st.session_state:
    # gpt-oss models expect the "harmony" chat format—use standard role/content messages
    st.session_state.messages = [{"role":"system","content":"You are a helpful assistant."}]

# Sidebar controls
with st.sidebar:
    st.subheader("Settings")
    effort = st.selectbox("Reasoning effort", ["low","medium","high"], index=1)
    if st.button("Clear chat"):
        st.session_state.messages = [{"role":"system","content":"You are a helpful assistant."}]
        st.experimental_rerun()

# --------------- Chat history render ---------------
for m in st.session_state.messages:
    if m["role"] in ("user","assistant"):
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# --------------- Input & Streaming ---------------
prompt = st.chat_input("Ask anything...")
if prompt:
    # Append user message
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream assistant response
    with st.chat_message("assistant"):
        # Use Chat Completions streaming
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages if m["role"]!="system" or m["content"]],
            # Many OpenAI-compatible providers accept extra kwargs—check provider docs.
            # gpt-oss models expose configurable "reasoning effort"; names vary per router/provider.
            stream=True,
            extra_body={"reasoning": {"effort": effort}},  # Supported on many GPT-OSS integrations
        )
        response_text = st.write_stream(stream)

    # Save assistant message
    st.session_state.messages.append({"role":"assistant","content":response_text})
