# 📰 ITA Honors – News Summarizer

## 🧠 Overview
This project is part of the **ITA Honors (Natural Language Processing)** coursework at  
**K. J. Somaiya School of Engineering, Mumbai**.  
It is a **web-based NLP application** that summarizes news articles and performs **sentiment analysis** using **FastAPI (backend)** and **Streamlit (frontend)**.
---

## ✨ Features

| Feature | Description |
|----------|--------------|
| 🧠 **Extractive Summarization** | Selects the most important sentences using **LexRank (Sumy)** |
| 💬 **Abstractive Summarization** | Generates a rephrased summary using **BART** or **T5 transformer** |
| 📊 **Sentiment Analysis** | Uses **VADER** to detect positive, negative, or neutral sentiment |
| ⚡ **Fast & Interactive** | FastAPI handles backend logic, Streamlit gives a clean UI |

---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend Framework** | FastAPI |
| **Frontend Framework** | Streamlit |
| **Summarization Models** | BART / T5 / LexRank |
| **Sentiment Model** | VADER |
| **Programming Language** | Python |
| **Libraries Used** | `transformers`, `sumy`, `nltk`, `vaderSentiment`, `requests`, `fastapi`, `uvicorn`, `streamlit` |

---

## ⚙️ Installation & Setup

### 1️⃣ Clone this Repository
```bash
git clone https://github.com/pranjalnirmal-coder/news_summerizer.git
cd news_summerizer
