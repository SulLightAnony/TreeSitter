<style>
  body { font-size: 8.8pt; line-height: 1.28; }
  h1 { font-size: 14pt; margin-top: 0; margin-bottom: 6px; }
  p, ul, ol { margin-top: 2px; margin-bottom: 4px; }
  pre { font-size: 8pt; line-height: 1.2; padding: 5px 8px; margin: 3px 0; }
</style>

# File ini dikonversi menjadi PDF menggunakan ekstensi VS Code.

# Draf Proposal Proyek Tree-sitter

**1. Judul:** Pendeteksi Potensi SQL Injection pada Aplikasi Web Node.js dan Express Berbasis Tree-sitter

**2. Masalah:** Dalam pengembangan sistem backend web berskala enterprise, kerentanan keamanan kerap muncul layaknya "pintu belakang" yang tidak disengaja ketika pengembang menyusun kueri SQL secara dinamis melalui penggabungan string dengan operator `+` maupun interpolasi *template literal*. Peninjau keamanan dan pengembang sering kecolongan terhadap pola ini karena pemindaian berbasis regex pada teks mentah sangat rapuh terhadap penulisan kode lintas baris, variasi spasi, serta ketidakmampuan memahami struktur pemanggilan fungsi database.

**3. Kenapa Tidak Cukup dengan AI Saja:** Agen pemrograman berbasis kecerdasan buatan bekerja secara probabilistik dan membutuhkan biaya token untuk setiap berkas yang dianalisis, sehingga lambat serta mahal apabila dijalankan pada ratusan berkas di setiap *commit* alur CI/CD. Sebaliknya, perkakas berbasis Tree-sitter beroperasi secara deterministik dengan hasil yang selalu konsisten, hampir tanpa biaya komputasi per eksekusi, serta mampu memindai ribuan berkas dalam hitungan detik sebagai "penjaga gerbang" kualitas otomatis di dalam pipeline.

**4. Bahasa dan Framework Target:** Ekosistem JavaScript dan Node.js menggunakan framework Express dengan driver database `mysql2` atau `pg`, yang dianalisis melalui pustaka tata bahasa `tree-sitter-javascript` dari PyPI.

**5. Contoh Kode:**
* Pola rentan berupa penggabungan string dinamis yang harus terdeteksi:
  ```javascript
  db.query("SELECT * FROM users WHERE id = " + req.params.id);
  ```
* Pola aman menggunakan *parameterized query* yang tidak boleh terdeteksi:
  ```javascript
  db.query("SELECT * FROM users WHERE id = ?", [req.params.id]);
  ```

**6. Rancangan Query:**
```scheme
(call_expression
  function: (member_expression property: (property_identifier) @method)
  arguments: (arguments
    [(binary_expression left: (string) @sql operator: "+")
     (template_string (template_substitution)) @sql])
  (#match? @method "^(query|execute)$")
  (#match? @sql "(?i)(SELECT|INSERT|UPDATE|DELETE)"))
```

**7. Bentuk Output:** Peringatan langsung pada terminal dengan format `file:baris:kolom: potensi SQL injection` serta keluaran terstruktur berupa berkas `report.json` untuk integrasi otomatis pada pipeline CI/CD.

**8. Cara Evaluasi:** Pengujian dijalankan pada satu repositori sumber terbuka berbasis Express, kemudian diikuti audit manual terhadap 20 temuan acak untuk mengukur tingkat presisi serta memverifikasi ketiadaan *false positive*.

**9. Rencana Kerja dan Risiko:**
* **Minggu 1 hingga Minggu 2:** Eksplorasi struktur AST pada `tree-sitter-javascript` dan implementasi kueri deteksi operator `+` serta *template literal*.
* **Minggu 3:** Pengembangan format laporan terminal, ekspor berkas JSON, serta dukungan variasi metode eksekusi seperti `query` dan `execute`.
* **Minggu 4 hingga Minggu 5:** Pengujian pada repositori sumber terbuka, audit manual terhadap 20 temuan, penyempurnaan aturan untuk menekan *false positive*, dan penyusunan laporan akhir.
* **Risiko Teknis:** Kueri SQL yang ditampung terlebih dahulu di dalam variabel terpisah sebelum diteruskan ke fungsi `db.query` memerlukan pelacakan variabel lokal sederhana agar tidak menjadi "titik buta" pemindaian.