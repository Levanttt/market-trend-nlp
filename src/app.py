import streamlit as st
import joblib
import re
import os

st.set_page_config(page_title="Market Trend AI", page_icon="📈", layout="centered")

@st.cache_resource
def load_models():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    model_path = os.path.join(base_dir, "models", "svm_sentiment_model.pkl")
    vectorizer_path = os.path.join(base_dir, "models", "tfidf_vectorizer.pkl")
    
    svm_model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return svm_model, vectorizer

def clean_text(text):
    text = str(text).lower() 
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) 
    text = re.sub(r'\@\w+|\#','', text) 
    text = re.sub(r'[^a-zA-Z\s]', '', text) 
    text = re.sub(r'\s+', ' ', text).strip() 
    return text

try:
    svm_model, vectorizer = load_models()
except Exception as e:
    st.error(f"Gagal memuat model. Pastikan file .pkl ada di folder models/. Error: {e}")
    st.stop()

st.title("Analisis Tren Pasar via Berita Ekonomi")
st.markdown("Masukkan teks berita ekonomi terbaru untuk mengetahui sentimen dan prediksi tren pasar secara otomatis.")

news_text = st.text_area("Teks Berita Ekonomi:", height=150, placeholder="Ketik atau paste teks berita di sini...")

if st.button("Analisis Sentimen & Tren"):
    if not news_text.strip():
        st.warning("Teks berita tidak boleh kosong. Silakan masukkan teks terlebih dahulu.")
    else:
        with st.spinner('Mesin AI sedang mengekstrak insight dari berita...'):
            cleaned_input = clean_text(news_text)
            input_vectorized = vectorizer.transform([cleaned_input])
            
            prediction = svm_model.predict(input_vectorized)[0]
            probabilities = svm_model.predict_proba(input_vectorized)[0]
            confidence = max(probabilities) * 100
            
            label_map = {"negatif": "NEGATIF", "netral": "NETRAL", "positif": "POSITIF"}
            sentimen_hasil = label_map.get(prediction.lower(), "UNKNOWN")
            
            if sentimen_hasil == "POSITIF":
                rekomendasi = "BULLISH - Sentimen pasar positif, potensi kenaikan harga aset."
            elif sentimen_hasil == "NEGATIF":
                rekomendasi = "BEARISH - Sentimen pasar negatif, waspada tekanan jual."
            else:
                rekomendasi = "STAGNANT/HOLD - Sentimen pasar netral, pertahankan portofolio."

            st.success("Analisis Selesai!")
            col1, col2 = st.columns(2)
            col1.metric("Sentimen Analisis (NLP)", sentimen_hasil)
            col2.metric("Confidence Score", f'{confidence:.2f}%')
            
            st.subheader("Rekomendasi Sistem Pakar:")
            if sentimen_hasil == "POSITIF":
                st.info(f"{rekomendasi}")
            elif sentimen_hasil == "NEGATIF":
                st.error(f"{rekomendasi}")
            else:
                st.warning(f"{rekomendasi}")