# ---------- itaexp8b.py ----------
from fastapi import FastAPI, HTTPException, Body
import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import difflib

# --- Download punkt tokenizer quietly ---
nltk.download('punkt', quiet=True)

# --- Initialize FastAPI app ---
app = FastAPI(title="ITA Honors News Summarizer")

# --- Load models ---
try:
    abstractive_pipeline = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception:
    abstractive_pipeline = pipeline("summarization", model="t5-small")

vader = SentimentIntensityAnalyzer()


# --- Helper: Extractive Summarization (LexRank) ---
def lexrank_summarize(text: str, ratio: float = 0.25) -> str:
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = LexRankSummarizer()
    sentence_count = max(1, int(len(parser.document.sentences) * ratio))
    sentences = summarizer(parser.document, sentence_count)
    return " ".join(str(sentence) for sentence in sentences)


# --- Helper: Check similarity ---
def too_similar(a: str, b: str) -> bool:
    return difflib.SequenceMatcher(None, a.strip(), b.strip()).ratio() > 0.9


# --- Endpoint 1: Extractive Summarization ---
@app.post("/extractive")
async def extractive(text: str = Body(..., media_type="text/plain")):
    try:
        summary = lexrank_summarize(text.strip())
        return {"method": "Extractive (LexRank)", "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Endpoint 2: Abstractive Summarization ---
@app.post("/abstractive")
async def abstractive(text: str = Body(..., media_type="text/plain")):
    try:
        text = text.strip()

        if len(text.split()) < 20:
            return {"method": "Abstractive (short text fallback)", "summary": lexrank_summarize(text, ratio=0.5)}

        result = abstractive_pipeline(
            text,
            max_length=120,
            min_length=30,
            num_beams=6,
            no_repeat_ngram_size=3,
            length_penalty=2.0,
            early_stopping=True
        )
        summary = result[0]["summary_text"].strip()

        if too_similar(text, summary):
            summary = lexrank_summarize(text, ratio=0.25)
            method = "Abstractive (fallback→Extractive)"
        else:
            method = "Abstractive (BART)"

        return {"method": method, "summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --- Endpoint 3: Sentiment Analysis ---
@app.post("/sentiment")
async def sentiment(text: str = Body(..., media_type="text/plain")):
    try:
        score = vader.polarity_scores(text.strip())
        return {"method": "Lexicon-based (VADER)", "scores": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
