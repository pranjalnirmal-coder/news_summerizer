# ---------- itaexp8f.py ----------
import streamlit as st
import requests

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8000"

st.title("📰 ITA Honors - News Summarizer")
st.write("Summarize and analyze news articles using NLP models.")

# Sidebar
task = st.sidebar.selectbox(
    "Choose Task:",
    ["Extractive Summarization", "Abstractive Summarization", "Sentiment Analysis"]
)

# Text input
text = st.text_area("Enter your news article:", height=200)

# Run button
if st.button("Run Analysis"):
    if not text.strip():
        st.warning("⚠️ Please enter text first.")
    else:
        try:
            if task == "Extractive Summarization":
                res = requests.post(f"{BACKEND_URL}/extractive", data=text)
                st.subheader("🧠 Extractive Summary")
                st.write(res.json().get("summary", "No summary generated."))

            elif task == "Abstractive Summarization":
                res = requests.post(f"{BACKEND_URL}/abstractive", data=text)
                st.subheader("💬 Abstractive Summary")
                st.write(res.json().get("summary", "No summary generated."))

            elif task == "Sentiment Analysis":
                res = requests.post(f"{BACKEND_URL}/sentiment", data=text)
                st.subheader("📊 Sentiment Analysis (VADER)")
                st.json(res.json().get("scores", {}))

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.caption("Developed for ITA Honors Project • NLP • FastAPI + Streamlit")
