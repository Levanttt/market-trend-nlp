# Market Trend NLP

![Python](https://img.shields.io/badge/Python-3.11-blue)
![NLP](https://img.shields.io/badge/AI-NLP-green)
![Model](https://img.shields.io/badge/Model-SVM-orange)
![Status](https://img.shields.io/badge/Status-UAS_Project-lightgrey)

## Deskripsi Proyek

Repositori ini memuat implementasi *end-to-end pipeline* Artificial Intelligence untuk menganalisis sentimen berita ekonomi dari CNBC Indonesia. Sistem mengorkestrasikan ekstraksi fitur teks, model machine learning klasifikasi, dan sistem pakar berbasis heuristik untuk memberikan rekomendasi tren pasar saham secara otomatis.

Masalah utama yang diselesaikan adalah *information overload* bagi pelaku pasar saham. Melalui pendekatan pemrosesan bahasa alami, sistem ini membaca dan mengkategorikan tendensi judul berita menjadi tiga label objektif: **Negatif**, **Netral**, dan **Positif**.

Dataset bersumber dari Kaggle: [CNBC Indonesia Stock News Sentiment Dataset](https://www.kaggle.com/datasets/triagungj/cnbc-indonesia-stock-news-sentiment-dataset).

---

## Arsitektur & Alur Sistem

Untuk mengakomodasi penilaian akademis dan aksesibilitas publik, sistem ini dirancang dengan dua pendekatan arsitektur:

### 1. Mode Lokal / Development (Microservices)

Menggunakan REST API berstandar industri dengan pemisahan *backend* dan *frontend*.

```text
[Streamlit UI] ---> (HTTP POST) ---> [FastAPI Endpoint] ---> [NLP & SVM Pipeline]
```

### 2. Mode Live Demo (Monolitik)

Dioptimalkan untuk cloud deployment publik (Streamlit Community Cloud) tanpa limitasi server gratis, di mana pipeline NLP diintegrasikan langsung ke dalam frontend.

```text
[Input Berita] -> [Streamlit App] -> [Local NLP Preprocessing] -> [SVM Model] -> [Expert System] -> [Output]
```

---

## Teknik AI & Justifikasi Arsitektur

Proyek ini mengintegrasikan tiga pilar teknologi utama:

1. **Natural Language Processing (NLP) & TF-IDF:** Digunakan untuk *noise reduction* dan mengubah struktur teks menjadi matriks probabilitas numerik.
2. **Support Vector Machine (SVM):** Dipilih sebagai model klasifikasi utama karena algoritma *linear kernel*-nya terbukti empiris sangat stabil dan efisien dalam mencari *hyperplane* pemisah pada ruang dimensi tinggi yang dihasilkan oleh matriks *sparse* TF-IDF.
3. **Sistem Pakar (Expert System):** Bertugas sebagai *decision-support layer* yang menerjemahkan hasil klasifikasi model NLP menjadi rekomendasi tren pasar saham yang *actionable* bagi pengguna.

---

## Struktur Repositori

```text
market-trend-nlp/
|-- data/
|   `-- Dataset-CNBCI-Sentimented.csv
|-- models/
|   |-- svm_sentiment_model.pkl
|   `-- tfidf_vectorizer.pkl
|-- notebooks/
|   |-- 01_EDA_and_Modeling.ipynb
|   `-- 02_Modeling.ipynb
|-- src/
|   |-- api.py (REST API Backend)
|   `-- app.py (Streamlit Frontend)
|-- requirements.txt
`-- README.md
```

---

## Metrik & Evaluasi Model

Data dipisahkan secara ketat (*train-test split*) sebelum proses ekstraksi TF-IDF untuk mencegah kebocoran data (*data leakage*). Evaluasi akhir menunjukkan performa yang solid untuk *baseline* model klasifikasi teks bahasa Indonesia:

* **Accuracy** : 0.82
* **Weighted Precision**: 0.82
* **Weighted Recall** : 0.82
* **Weighted F1-Score** : 0.82

---

## Setup & Panduan Instalasi

### Live Demo Publik

Aplikasi dapat langsung diakses dan diuji coba melalui Streamlit Community Cloud pada tautan berikut: [https://market-trend-nlp.streamlit.app/](#)

### Instalasi Lokal (API Mode)

Jika ingin menjalankan sistem secara lokal beserta dokumentasi API-nya:

**1. Clone Repository & Install Dependencies**

```bash
git clone https://github.com/Levanttt/market-trend-nlp.git
cd market-trend-nlp
pip install -r requirements.txt
```

**2. Menjalankan Backend API (FastAPI)**

```bash
uvicorn src.api:app --reload
```

Dokumentasi Swagger UI otomatis dapat diakses di: `http://127.0.0.1:8000/docs`

**3. Menjalankan Frontend (Streamlit)**
Buka terminal baru dan eksekusi:

```bash
streamlit run src/app.py
```

---

## Spesifikasi REST API (Untuk Mode Lokal)

Sistem backend diorkestrasikan menggunakan metode HTTP POST dengan format payload standar industri.

**Endpoint:** `POST /api/predict_trend`

**Request Payload:**

```json
{
  "text": "IHSG anjlok setelah pengumuman kenaikan suku bunga The Fed.",
  "source": "Local Testing"
}
```

**Response (200 OK):**

```json
{
  "status": "success",
  "berita_asli": "IHSG anjlok setelah pengumuman kenaikan suku bunga The Fed.",
  "hasil_analisis": {
    "sentimen": "NEGATIF",
    "confidence_score": 93.73,
    "rekomendasi_tren": "BEARISH - Sentimen pasar negatif, waspada tekanan jual."
  }
}
```

---

## Referensi

* Kaggle: CNBC Indonesia Stock News Sentiment Dataset.
* Scikit-learn Documentation: TF-IDF, SVM, dan metrik klasifikasi.
* FastAPI & Streamlit Official Documentation.
