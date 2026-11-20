<style>
  body { font-size: 9pt; line-height: 1.32; }
  h1 { font-size: 15pt; margin-bottom: 4px; }
  h2 { font-size: 12pt; margin-top: 10px; margin-bottom: 4px; }
  h3 { font-size: 10.5pt; margin-top: 8px; margin-bottom: 2px; }
  p, ul, ol { margin-top: 2px; margin-bottom: 4px; }
  img { max-height: 130px; width: auto; display: block; margin: 4px 0; }
</style>

# File ini dikonversi menjadi PDF menggunakan ekstensi VS Code.

# Laporan Tugas 1-6: Memahami Tree-sitter

**Mata Kuliah:** Programming Pragmatics, Semester 3

## Eksplorasi Struktur Pohon dan Kueri Sintaksis

### Tugas 1 - Membaca Pohon pada `tugas1-3/t1.py`
Memahami cara kerja parser dimulai dengan membedah anatomi kode layaknya mengamati "kerangka bangunan" yang tersusun atas balok utama dan perekat struktural. Pengujian mencakup tiga potongan kode Python sah, yakni fungsi `def sapa`, percabangan `if` dan `else`, serta kelas `class Mahasiswa`, ditambah satu kode rusak berupa definisi `def sapa` tanpa titik dua. Perbandingan antara perkiraan manual dan hasil aktual menunjukkan bahwa parameter tidak diletakkan datar di bawah `function_definition`, melainkan dibungkus dalam node `parameters`, isi blok dikelompokkan dalam `block`, dan cabang alternatif dipisahkan dalam `else_clause`. Pemeriksaan atribut `children` membuktikan bahwa tanda baca dan kata kunci seperti `def`, `:`, `(`, `,`, `)`, `if`, `else`, serta `class` berstatus anonim dengan `is_named` bernilai `False`, sedangkan `identifier`, `parameters`, dan `block` tampil sebagai node bernama. Pada kode tanpa titik dua, pemulihan galat tetap mempertahankan `module` dengan menyisipkan node `ERROR` yang membungkus `identifier` dan `parameters`.

![alt text](image.png)

### Tugas 2 - Penjelajah Node pada `tugas1-3/jelajah.py`
Navigasi pohon sintaksis secara otomatis diwujudkan melalui mekanisme "penelusuran lorong bertingkat" secara rekursif. Skrip `jelajah.py` menelusuri `node.children` menggunakan `enumerate`, menyaring keluar node anonim lewat pemeriksaan `not child.is_named`, serta mengambil label peran lewat `node.field_name_for_child`. Pengujian pada `kecil.py` yang berisi ekspresi `x = 1` maupun berkas `contoh_100_baris.py` sepanjang 116 baris, yang memuat pernyataan impor, fungsi, kelas, perulangan, dan percabangan, menampilkan hierarki lengkap dengan indentasi presisi, label `left:`, `right:`, `name:`, serta koordinat `baris:kolom`.

![alt text](image-1.png)

### Tugas 3 - Query Tree-sitter pada `tugas1-3/q.py` dan Berkas `.scm`
Penelusuran seluruh simpul pohon kemudian dipertajam menjadi "saringan presisi" berbasis pola S-expression melalui skrip `q.py`. Berkas `query_fungsi.scm` dengan metode `matches` menangkap fungsi `halo` dengan 0 parameter, `tambah` dengan 2 parameter, `hitung_total` dengan 3 parameter, serta `ringkas_data` dengan 4 parameter, selaras dengan hitungan manual. Selanjutnya, `query_print.scm` dengan `captures` dan predikat `#eq?` mengidentifikasi empat pemanggilan `print` pada baris 8, 13, 27, dan 34, sedangkan `query_import.scm` menangkap modul `os`, `sys`, `pathlib`, dan `datetime` dari pernyataan `import` maupun `from ... import ...`.

![alt text](image-2.png)

## Perancangan Tata Bahasa Mandiri dan Perkakas Analisis

### Tugas 4 - Grammar DSL Filter pada `tree-sitter-filter/grammar.js`
Perancangan tata bahasa mandiri menuntut pengaturan "hierarki lalu lintas" operator agar ekspresi majemuk terhindar dari ambiguitas. Berkas `grammar.js` mendukung ekspresi `comparison`, `and_expression` dengan prioritas asosiatif kiri `prec.left` bernilai 2, `or_expression` dengan `prec.left` bernilai 1, `not_expression` dengan `prec` bernilai 3, pengelompokan tanda kurung `parenthesized`, `in_expression`, serta `contains_expression`. Pengujian `tree-sitter test` pada `test/corpus/dasar.txt` lulus 7 dari 7 pengujian atau 100 persen, termasuk pembuktian pengelompokan `a = 1 or` dengan sub-pohon `b = 2 and c = 3` serta operator `in` dengan tiga nilai.

![alt text](image-3.png)

### Tugas 5 - Syntax Highlighting pada `queries/highlights.scm`
Tata bahasa DSL yang telah teruji dilengkapi lapisan pewarnaan sintaks melalui `queries/highlights.scm` agar setiap kategori token memiliki identitas visual yang jelas. Aturan kueri memetakan kata kunci ke `@keyword`, operator perbandingan ke `@operator`, literal teks ke `@string`, bilangan ke `@number`, nilai boolean ke `@constant.builtin`, serta nama atribut pada `field: identifier` ke `@property`. Eksekusi `tree-sitter highlight contoh.filter` membuktikan seluruh jenis token terwarnai akurat di terminal.

![alt text](image-4.png)

### Tugas 6 - Mini Proyek CLI pada `cek/cek.py`
Seluruh konsep penguraian pohon dirangkai menjadi perkakas baris perintah `cek.py` sebagai "penjaga gerbang" kualitas kode Python yang memindai direktori secara rekursif untuk mendeteksi komentar `TODO` atau `FIXME`, fungsi di atas 30 baris, serta galat sintaksis lewat `has_error`. Pengujian pada `cek/uji/` menemukan 2 komentar `TODO` dan `FIXME`, 1 fungsi sepanjang 38 baris, serta 1 galat sintaksis, sedangkan pemindaian terhadap 5 berkas pada modul standar `Lib/http` mendeteksi 38 fungsi berdurasi lebih dari 30 baris. Pemeriksaan manual pada dua berkas membuktikan keakuratan penuh: pada `http/client.py`, fungsi `_read_status` berada pada baris 278 hingga 309 sepanjang 32 baris sesuai keluaran `client.py:278: _read_status`, dan pada `http/server.py`, fungsi `parse_request` berada pada baris 267 hingga 371 sepanjang 105 baris sesuai keluaran `server.py:267: parse_request`.

![alt text](image-5.png)

## Kendala Teknis dan Penyelesaian
1. **Perubahan Antarmuka `py-tree-sitter` Versi 0.25:** Dokumentasi lama masih memakai metode usang seperti `parser.set_language` dan `query.captures`. Kendala ini diatasi dengan membungkus bahasa ke objek `Parser` dan `Language`, lalu mengeksekusi kueri melalui `QueryCursor`.
2. **Konflik Ambiguitas Operator `and` dan `or`:** Tanpa bobot prioritas, `tree-sitter generate` memunculkan pesan *unresolved conflict*. Masalah diselesaikan dengan menetapkan `prec.left` tingkat 1 untuk `or` dan `prec.left` tingkat 2 untuk `and`.

## Evaluasi Kritis Penggunaan AI
* **Ruang Lingkup Bantuan AI:** Kecerdasan buatan membantu menyusun rancangan awal kueri `import_statement` dan `import_from_statement` pada Tugas 3, aturan `in_expression` dan `contains_expression` di `grammar.js` pada Tugas 4, serta fungsi rekursif pelacak node galat pada Tugas 6.
* **Temuan Kekurangan pada Hasil AI:** Rancangan awal AI pada `query_import.scm` hanya mencocokkan `dotted_name` sehingga impor beralias seperti `import sys as sistem` luput tertangkap karena terbungkus node `aliased_import`. Selain itu, saran perintah `tree-sitter highlight` tanpa opsi jalur `-p .` gagal berjalan karena konfigurasi `parser-directories` belum diarahkan ke folder proyek.
* **Bukti Verifikasi:** Struktur `aliased_import` diverifikasi dengan `jelajah.py` dan diuji ulang memakai `q.py` hingga modul `sys` muncul di `hasil_t3.txt`, aturan tata bahasa divalidasi lewat `tree-sitter test` dengan kelulusan 7 dari 7 kasus uji, serta laporan baris `cek.py` dicocokkan langsung terhadap kode sumber `client.py` dan `server.py`.

## Penutup
Eksplorasi dari pembacaan simpul dasar hingga pembangunan perkakas audit kode membuktikan bahwa analisis berbasis pohon sintaksis memberikan kepastian deterministik yang melampaui pencocokan teks biasa, sehingga pemeriksaan kualitas perangkat lunak dapat dijalankan secara cepat, konsisten, dan akurat.