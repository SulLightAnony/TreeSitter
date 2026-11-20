# Cek Kode Python dengan Tree-sitter

CLI sederhana untuk memeriksa komentar `TODO`/`FIXME`, fungsi yang terlalu panjang (> 30 baris), dan error sintaks pada berkas Python di dalam suatu folder.

## Instalasi

Pastikan Python 3.10+ sudah terpasang, lalu pasang dependensi berikut:

```bash
pip install tree-sitter tree-sitter-python
```

## Cara Menjalankan

Jalankan skrip `cek.py` dengan argumen path folder target:

```bash
python cek.py uji/
```

Catatan perilaku:
- Folder `.venv`, `venv`, `.git`, dan `node_modules` otomatis dilewati.
- Semua `function_definition` ikut dihitung, termasuk method di dalam kelas dan fungsi bersarang.

## Contoh Output

### 1. Uji pada folder `uji/`

```text
$ python cek.py uji/
uji\ada_todo.py:2: # TODO: ambil tarif pajak dari konfigurasi database
uji\ada_todo.py:8: # FIXME: tambahkan retry jika koneksi SMTP gagal
uji\fungsi_panjang.py:5: proses_laporan_bulanan (38 baris)
uji\sintaks_rusak.py:1: syntax error (ERROR)

Ringkasan: 3 file diperiksa, 2 TODO/FIXME, 1 fungsi > 30 baris, 1 file dengan syntax error.
```

### 2. Uji pada modul standar Python (`Lib/http`)

```text
$ python cek.py "C:\Users\frans\AppData\Local\Programs\Python\Python310\Lib\http"
...\http\client.py:278: _read_status (32 baris)
...\http\client.py:311: begin (71 baris)
...
...\http\server.py:267: parse_request (105 baris)
...\http\server.py:1041: run_cgi (185 baris)

Ringkasan: 5 file diperiksa, 0 TODO/FIXME, 38 fungsi > 30 baris, 0 file dengan syntax error.
```
