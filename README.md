gpt-oss-120b Streamlit Chatbot
A simple chatbot UI for interacting with OpenAI’s open-source gpt-oss-120b LLM via an OpenAI-compatible API (e.g., Hugging Face Inference Endpoints, vLLM, or Ollama) using Streamlit.
Features
	•	Live Chat UI: Streamlit-based, browser-accessible interface
	•	Model Switching: Easily configure for any OpenAI-compatible endpoint
	•	Streaming Responses: Supports real-time, token-by-token responses
	•	Reasoning Effort: Selectable logic depth (if supported)
	•	Session Management: Maintains chat history per session
Installation
pip install streamlit openai

Get a Hugging Face API token:
	•	Sign up/log in at huggingface.co
	•	Go to your profile > Settings > Access Tokens
	•	Create a token (default “read” scope)
	•	Copy and store it securely
Usage
Run the app from the project root:
streamlit run app.py
