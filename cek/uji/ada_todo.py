def hitung_pajak(total):
    # TODO: ambil tarif pajak dari konfigurasi database
    tarif = 0.11
    return total * tarif


def kirim_notifikasi(email):
    # FIXME: tambahkan retry jika koneksi SMTP gagal
    print(f"Mengirim ke {email}")
