# Market Trend NLP

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![NLP](https://img.shields.io/badge/AI-NLP-green)
![Model](https://img.shields.io/badge/Model-SVM-orange)
![Status](https://img.shields.io/badge/Status-UAS_Project-lightgrey)

## Deskripsi Proyek

Project ini dibuat untuk UAS mata kuliah Artificial Intelligence dengan topik **Analisis Tren Pasar Berdasarkan Berita Ekonomi**.

Sistem ini bertujuan membantu membaca sentimen dari judul berita ekonomi CNBC Indonesia. Dengan pendekatan NLP, judul berita dapat diklasifikasikan menjadi tiga label:

- `negatif`
- `netral`
- `positif`

Dataset yang digunakan berasal dari Kaggle:
https://www.kaggle.com/datasets/triagungj/cnbc-indonesia-stock-news-sentiment-dataset

## Alur Sistem

```text
Input Judul Berita
        |
        v
Streamlit UI
        |
        v
FastAPI Endpoint
        |
        v
Preprocessing Teks
lowercase, hapus simbol, hapus angka, rapikan spasi
        |
        v
Ekstraksi Fitur TF-IDF
        |
        v
Model SVM
        |
        v
Expert System Tren Pasar
        |
        v
Output Sentimen dan Rekomendasi Tren
negatif / netral / positif + bearish / stagnant / bullish
```

## Teknik AI yang Digunakan

Project ini menggunakan tiga teknik utama:

- **Natural Language Processing (NLP)** untuk membersihkan dan memproses teks berita.
- **Supervised Machine Learning** menggunakan SVM untuk klasifikasi sentimen.
- **Expert System sederhana** untuk mengubah hasil sentimen menjadi rekomendasi tren pasar.

TF-IDF digunakan untuk mengubah teks menjadi angka agar dapat diproses oleh model machine learning.

## Struktur Folder

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
|   |-- api.py
|   `-- app.py
|-- requirements.txt
`-- README.md
```

## Ringkasan Notebook

### 1. EDA

Notebook `notebooks/01_EDA_and_Modeling.ipynb` berisi eksplorasi awal dataset, seperti:

- melihat struktur data,
- mengecek missing value,
- menghapus data duplikat,
- melihat distribusi sentimen,
- menganalisis panjang judul berita,
- membuat word cloud.

Hasil EDA menunjukkan dataset memiliki 9.819 data awal. Setelah 3 data duplikat dihapus, data yang digunakan menjadi 9.816 baris.

### 2. Modeling

Notebook `notebooks/02_Modeling.ipynb` berisi proses:

- preprocessing teks,
- split data training dan testing,
- ekstraksi fitur menggunakan TF-IDF,
- training model SVM,
- evaluasi model,
- export model dan vectorizer,
- sanity check prediksi.

Hasil evaluasi model menunjukkan accuracy dan weighted F1-Score sekitar **82%**.

## Setup Project

Clone repository:

```bash
git clone https://github.com/Levanttt/market-trend-nlp.git
cd market-trend-nlp
```

Install dependency utama:

```bash
pip install -r requirements.txt
```

Jalankan API FastAPI:

```bash
uvicorn src.api:app --reload
```

Jalankan aplikasi Streamlit di terminal lain:

```bash
streamlit run src/app.py
```

## Format Input dan Output API

Sistem menyediakan REST API untuk menerima input berita dan mengembalikan hasil analisis sentimen serta rekomendasi tren.

### Request

Endpoint:

```text
POST /api/predict_trend
```

Payload JSON:

```json
{
  "text": "IHSG anjlok setelah pengumuman kenaikan suku bunga The Fed.",
  "source": "Streamlit UI"
}
```

### Response Berhasil

Status: `200 OK`

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

### Response Gagal

Status: `400 Bad Request`

```json
{
  "detail": "Bad Request: Teks berita tidak boleh kosong."
}
```

## Evaluasi Model

Metrik evaluasi yang digunakan:

- Accuracy
- Precision
- Recall
- F1-Score

Ringkasan hasil:

```text
Accuracy          : 0.82
Weighted Precision: 0.82
Weighted Recall   : 0.82
Weighted F1-Score : 0.82
```

Model sudah cukup baik untuk baseline klasifikasi sentimen berita ekonomi. Namun, model masih dapat dikembangkan lagi, misalnya dengan stemming bahasa Indonesia, tuning parameter SVM, atau menggunakan model berbasis transformer seperti IndoBERT.

## Referensi

- Kaggle: CNBC Indonesia Stock News Sentiment Dataset.
- Scikit-learn Documentation: TF-IDF, SVM, dan classification metrics.
- WordCloud Python Documentation.
- Streamlit Documentation.
