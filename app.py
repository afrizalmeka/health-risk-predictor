"""
app.py - Health Risk Predictor + Dokter Virtual (Sesi 15 - Mini Project).

Prediksi tingkat risiko kesehatan berdasarkan usia, BMI, tekanan darah,
dan gula darah, memakai Decision Tree (Sesi 10), dengan Gemini API
(Sesi 13) sebagai "penerjemah" hasil ke bahasa awam - bukan sebagai
inti logika prediksi.

Jalankan dengan:
    streamlit run app.py
"""
import sqlite3

import joblib
import pandas as pd
import streamlit as st
from google import genai

st.title("Health Risk Predictor + Dokter Virtual")
st.write("Prediksi tingkat risiko kesehatan berdasarkan usia, BMI, tekanan darah, dan gula darah, memakai Decision Tree (Sesi 10) dan Gemini API (Sesi 13) sebagai penjelas bahasa awam.")

# Ganti dengan API key Gemini kamu sendiri (lihat Panduan_Gemini_API_Key_dan_Test.docx
# di folder Sesi13 kalau belum punya).
api_key = "GANTI_DENGAN_API_KEY_ANDA"

bundle = joblib.load("health_risk_model.pkl")
model = bundle["model"]
feature_cols = bundle["feature_cols"]

client = genai.Client(api_key=api_key)

DB_PATH = "riwayat_risiko.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS prediksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usia INTEGER,
            bmi REAL,
            tekanan_darah INTEGER,
            gula_darah INTEGER,
            tingkat_risiko TEXT
        )
        """
    )
    conn.commit()
    conn.close()


init_db()

st.write("### Form Prediksi")
with st.form("form_prediksi"):
    usia = st.number_input("Usia", min_value=1, max_value=100, value=40)
    bmi = st.number_input("BMI (Body Mass Index)", min_value=10.0, max_value=50.0, value=24.0)
    tekanan_darah = st.number_input("Tekanan Darah Sistolik", min_value=70, max_value=220, value=120)
    gula_darah = st.number_input("Gula Darah (mg/dL)", min_value=50, max_value=300, value=100)
    submit = st.form_submit_button("Prediksi Risiko")

if submit:
    row = {"usia": usia, "bmi": bmi, "tekanan_darah": tekanan_darah, "gula_darah": gula_darah}

    X = pd.DataFrame([row])[feature_cols]
    tingkat_risiko = model.predict(X)[0]

    st.write("### Tingkat Risiko:", tingkat_risiko)

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO prediksi (usia, bmi, tekanan_darah, gula_darah, tingkat_risiko) VALUES (?, ?, ?, ?, ?)",
        (usia, bmi, tekanan_darah, gula_darah, tingkat_risiko),
    )
    conn.commit()
    conn.close()

    # Gemini API dipanggil sebagai "penerjemah" ke bahasa awam - WAJIB
    # dibungkus try/except supaya kalau API gagal, aplikasi tetap
    # menampilkan hasil prediksi model tanpa penjelasan LLM.
    st.write("### Penjelasan dari Dokter Virtual")
    try:
        prompt = (
            f"Seorang pasien berusia {usia} tahun dengan BMI {bmi}, "
            f"tekanan darah {tekanan_darah}, dan gula darah {gula_darah} "
            f"diprediksi memiliki tingkat risiko kesehatan '{tingkat_risiko}'. "
            f"Jelaskan dalam 2-3 kalimat bahasa awam apa artinya ini dan "
            f"saran umum apa yang bisa diberikan (bukan diagnosis medis)."
        )
        response = client.models.generate_content(model="gemini-3.5-flash", contents=prompt)
        st.write(response.text)
    except Exception as e:
        st.warning(f"Penjelasan LLM tidak tersedia saat ini ({e}). Hasil prediksi model tetap valid di atas.")

st.write("### Riwayat Prediksi")
conn = sqlite3.connect(DB_PATH)
riwayat_df = pd.read_sql_query("SELECT * FROM prediksi ORDER BY id DESC", conn)
conn.close()
st.dataframe(riwayat_df)
