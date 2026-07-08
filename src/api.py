from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import re

app = FastAPI(
    title="Market Trend AI API",
    description="API Endpoint untuk mengklasifikasi sentimen berita dan memprediksi tren pasar."
)

try:
    model_path = r"D:\Project\market-trend-nlp\market-trend-nlp\models\svm_sentiment_model.pkl"
    vectorizer_path = r"D:\Project\market-trend-nlp\market-trend-nlp\models\tfidf_vectorizer.pkl"
    
    svm_model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("Model AI berhasil dimuat ke dalam server API!")
except Exception as e:
    print(f"Gagal memuat model: {str(e)}")

class NewsPayload(BaseModel):
    text: str
    source: str = "Unknown"

def clean_text(text):
    text = str(text).lower() 
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) 
    text = re.sub(r'\@\w+|\#','', text) 
    text = re.sub(r'[^a-zA-Z\s]', '', text) 
    text = re.sub(r'\s+', ' ', text).strip() 
    return text

def expert_system_trend(sentiment):
    if sentiment == 'positif':
        return "BULLISH - Sentimen pasar positif, potensi kenaikan harga."
    elif sentiment == 'negatif':
        return "BEARISH - Sentimen pasar negatif, waspada tekanan jual."
    else:
        return "STAGNANT - Pasar netral, tunggu katalis informasi lebih lanjut."

@app.post("/api/predict_trend")
async def predict_trend(payload: NewsPayload):
    try:
        if not payload.text.strip():
            raise ValueError("Teks berita tidak boleh kosong.")

        cleaned_input = clean_text(payload.text)
        
        vec_input = vectorizer.transform([cleaned_input])
        prediction = svm_model.predict(vec_input)[0]
        probabilities = svm_model.predict_proba(vec_input)[0]
        confidence = max(probabilities)
        
        market_trend = expert_system_trend(prediction)
        
        return {
            "status": "success",
            "berita_asli": payload.text,
            "hasil_analisis": {
                "sentimen": prediction.upper(),
                "confidence_score": round(confidence * 100, 2),
                "rekomendasi_tren": market_trend
            }
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Bad Request: {str(ve)}")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error: Terjadi kegagalan pada mesin AI saat memproses teks.")