def fungsi_pendek(x):
    return x + 1


def proses_laporan_bulanan(daftar_transaksi):
    total_masuk = 0
    total_keluar = 0
    jumlah_masuk = 0
    jumlah_keluar = 0
    kategori = {}

    for trx in daftar_transaksi:
        jenis = trx.get("jenis", "masuk")
        nominal = trx.get("nominal", 0)
        nama_kat = trx.get("kategori", "umum")

        if nominal <= 0:
            continue

        if nama_kat not in kategori:
            kategori[nama_kat] = 0
        kategori[nama_kat] += nominal

        if jenis == "masuk":
            total_masuk += nominal
            jumlah_masuk += 1
        else:
            total_keluar += nominal
            jumlah_keluar += 1

    saldo = total_masuk - total_keluar
    rata_masuk = total_masuk / jumlah_masuk if jumlah_masuk > 0 else 0
    rata_keluar = total_keluar / jumlah_keluar if jumlah_keluar > 0 else 0

    return {
        "total_masuk": total_masuk,
        "total_keluar": total_keluar,
        "saldo": saldo,
        "rata_masuk": rata_masuk,
        "rata_keluar": rata_keluar,
        "kategori": kategori,
    }
