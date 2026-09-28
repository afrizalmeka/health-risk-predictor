# Health Risk Predictor + Dokter Virtual

Mini Project Sesi 15 (Python Programming for AI - Batch 8) - Project 4 dari 5 opsi. Memprediksi tingkat risiko kesehatan (rendah/sedang/tinggi) berdasarkan usia, BMI, tekanan darah, dan gula darah, memakai Decision Tree (Sesi 10) - lalu Gemini API (Sesi 13) menjelaskan hasilnya dalam bahasa awam.

Cocok untuk peserta dengan latar belakang: kesehatan, farmasi, sains, atau yang ingin menyentuh LLM.

**Catatan penting**: Gemini di sini hanya sebagai "penerjemah" hasil model ke bahasa awam - BUKAN inti logika prediksi. Prediksi tetap sepenuhnya dari model Decision Tree.

## Status

Aplikasi ini **sudah 100% jadi** - kode prediksi dan pemanggilan Gemini API sudah lengkap. Yang perlu kamu isi hanya API key kamu sendiri (lihat "Menyiapkan API Key" di bawah). Cocok dipakai sebagai referensi belajar: baca `app.py` untuk lihat bagaimana Decision Tree (Sesi 10) dan Gemini API (Sesi 13) digabung dengan pola `try/except` yang aman.

## Struktur Folder

```
health-risk-predictor/
├── app.py                     # Streamlit - dashboard (lengkap)
├── health_risk_model.pkl      # Model Decision Tree terlatih
├── health_risk_dataset.csv    # Dataset sintetis (usia, BMI, tekanan darah, gula darah)
├── requirements.txt
├── .gitignore
└── README.md
```

## Instalasi

Gunakan virtual environment agar paket project ini tidak bentrok dengan paket Python lain yang sudah terpasang di sistem kamu (mis. error `command not found: streamlit` atau `ImportError` pada scipy/sklearn biasanya disebabkan oleh instalasi global yang tercampur):

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Menyiapkan API Key

Buka `app.py`, ganti baris:

```python
api_key = "GANTI_DENGAN_API_KEY_ANDA"
```

dengan API key Gemini kamu sendiri. Lihat `Panduan_Gemini_API_Key_dan_Test.docx` di folder `Sesi13_AI_Generatif_dan_LLM_API/` kalau belum punya API key.

## Menjalankan

```bash
source .venv/bin/activate      # jika belum aktif
streamlit run app.py
```

## Troubleshooting

- **`zsh: command not found: streamlit`** — venv belum diaktifkan, atau instalasi sebelumnya masuk ke `~/Library/Python/...` yang tidak ada di PATH. Aktifkan venv (`source .venv/bin/activate`) lalu jalankan lagi, atau jalankan sementara dengan `python3 -m streamlit run app.py`.
- **`ImportError` dari `scipy/sparse/linalg/_propack/...`** — biasanya wheel scipy yang ter-install rusak/tidak cocok dengan arsitektur CPU (Apple Silicon vs Intel). Perbaiki dengan menginstal ulang di dalam venv:
  ```bash
  pip uninstall -y scipy numpy
  pip install --no-cache-dir numpy scipy
  ```
- Pastikan `python3 -c "import platform; print(platform.machine())"` dan `uname -m` menunjukkan arsitektur yang sama. Jika berbeda, Python kamu berjalan dalam mode emulasi (Rosetta) — install ulang Python versi native untuk arsitektur mesin kamu.

## Konteks

Bagian dari Sesi 15 - Mini Project: Connecting the Dots, kurikulum Python Programming for AI Batch 8 (rubythalib.ai). Menggabungkan Sesi 6 (SQLite), Sesi 10 (Decision Tree), Sesi 13 (Gemini API), dan Sesi 14 (Streamlit deployment).
