# Aplikasi Analisis Tweet

Aplikasi web untuk menganalisis dan menampilkan data tweet. Aplikasi ini terdiri dari beberapa komponen utama yang menghandle pengambilan data, pembersihan, analisis, dan visualisasi.

## Fitur

- Scraping tweet otomatis dari Twitter menggunakan Selenium
- Pembersihan dan preprocessing data tweet
- Analisis data termasuk:
  - Statistik dasar (total tweet, user unik, rata-rata panjang)
  - Analisis waktu posting
  - Analisis user paling aktif
  - Word cloud dari konten tweet
- Visualisasi data interaktif menggunakan Chart.js
- REST API untuk mengakses data
- Interface web responsif dengan Tailwind CSS
- Tabel interaktif dengan fitur pencarian dan pengurutan

## Struktur Proyek

```
├── main.py             # Script untuk scraping data Twitter
├── data.py            # Kelas untuk analisis dan pembersihan data
├── api.py             # REST API menggunakan Flask
├── index.html         # Antarmuka web
├── requirements.txt   # Dependensi Python
├── tweets.csv         # Data mentah hasil scraping
└── tweets_clean.csv   # Data yang sudah dibersihkan
```

## Teknologi yang Digunakan

- **Backend**:
  - Python 3.8+
  - Flask (REST API)
  - Pandas (Analisis Data)
  - Selenium (Web Scraping)
- **Frontend**:
  - HTML5
  - Tailwind CSS
  - Chart.js
  - DataTables
  - jQuery

## Cara Penggunaan

1. Install dependensi Python:

```bash
pip install -r requirements.txt
```

2. Scraping data Twitter:

```bash
python main.py
```

3. Bersihkan dan analisis data:

```bash
python data.py
```

4. Jalankan server API:

```bash
python api.py
```

5. Buka `index.html` di browser

## Format Data

Data tweet disimpan dalam format CSV dengan kolom-kolom berikut:

- `username`: Nama pengguna Twitter
- `waktu`: Waktu posting (format: DD-MM-YYYY HH:MM)
- `konten`: Isi tweet
- `tweet_length`: Panjang tweet dalam karakter

## API Endpoints

### GET /api/tweets

Mengambil semua data tweet yang sudah dibersihkan.

Response:

```json
{
    "status": "success",
    "data": [
        {
            "username": "string",
            "waktu": "YYYY-MM-DD HH:MM",
            "konten": "string"
        }
    ],
    "total": integer
}
```

## Pembersihan Data

Proses pembersihan data meliputi:

- Penghapusan pengulangan username
- Pembersihan URL dan teks tambahan
- Penghapusan pengulangan angka
- Standardisasi format waktu
- Penghapusan tweet kosong

## Kontribusi

Silakan buat pull request untuk kontribusi. Untuk perubahan besar, harap buka issue terlebih dahulu untuk mendiskusikan perubahan yang diinginkan.

## Lisensi

[MIT License](https://opensource.org/licenses/MIT)
