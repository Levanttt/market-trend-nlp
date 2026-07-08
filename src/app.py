import streamlit as st
import requests

st.set_page_config(page_title="Market Trend AI", page_icon="📈", layout="centered")

st.title("Analisis Tren Pasar via Berita Ekonomi")
st.markdown("Masukkan teks berita ekonomi terbaru untuk mengetahui sentimen dan prediksi tren pasar secara otomatis.")

news_text = st.text_area("Teks Berita Ekonomi:", height=150, placeholder="Ketik atau paste teks berita di sini...")

if st.button("Analisis Sentimen & Tren"):
    if not news_text.strip():
        st.warning("Teks berita tidak boleh kosong. Silakan masukkan teks terlebih dahulu.")
    else:
        with st.spinner('Mesin AI sedang mengekstrak insight dari berita...'):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/api/predict_trend",
                    json={"text": news_text, "source": "Streamlit UI"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("Analisis Selesai!")
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Sentimen Analisis (NLP)", result["hasil_analisis"]["sentimen"])
                    col2.metric("Confidence Score", f'{result["hasil_analisis"]["confidence_score"]}%')
                    
                    st.subheader("Rekomendasi Sistem Pakar:")
                    if result["hasil_analisis"]["sentimen"] == "POSITIF":
                        st.info(f"{result['hasil_analisis']['rekomendasi_tren']}")
                    elif result["hasil_analisis"]["sentimen"] == "NEGATIF":
                        st.error(f"{result['hasil_analisis']['rekomendasi_tren']}")
                    else:
                        st.warning(f"{result['hasil_analisis']['rekomendasi_tren']}")
                    
                    with st.expander("Lihat Detail Raw JSON (Response API)"):
                        st.json(result)
                        
                elif response.status_code == 400:
                    st.error(f"Bad Request: {response.json()['detail']}")
                else:
                    st.error("Terjadi kesalahan pada server API.")
                    
            except requests.exceptions.ConnectionError:
                st.error("Gagal terhubung ke server API. Pastikan server FastAPI sudah berjalan di terminal lain.")