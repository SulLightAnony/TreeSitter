import json
from pathlib import Path
from datetime import datetime


def hitung_diskon(harga, persen):
    if persen < 0 or persen > 100:
        raise ValueError("Persen diskon harus di antara 0 dan 100")
    potongan = harga * (persen / 100)
    return harga - potongan


def format_rupiah(nominal):
    nilai = int(round(nominal))
    return f"Rp{nilai:,}".replace(",", ".")


class Produk:
    def __init__(self, kode, nama, harga, stok):
        self.kode = kode
        self.nama = nama
        self.harga = harga
        self.stok = stok

    def tersedia(self, jumlah):
        return self.stok >= jumlah

    def kurangi_stok(self, jumlah):
        if not self.tersedia(jumlah):
            raise ValueError(f"Stok {self.nama} tidak mencukupi")
        self.stok -= jumlah

    def ringkasan(self):
        return f"{self.kode} - {self.nama} ({format_rupiah(self.harga)}, stok: {self.stok})"


class KeranjangBelanja:
    def __init__(self, pemilik):
        self.pemilik = pemilik
        self.item = []
        self.dibuat_pada = datetime.now().isoformat()

    def tambah_produk(self, produk, jumlah, diskon=0):
        if jumlah <= 0:
            raise ValueError("Jumlah pembelian minimal 1")
        if not produk.tersedia(jumlah):
            return False
        harga_satuan = hitung_diskon(produk.harga, diskon)
        self.item.append(
            {
                "kode": produk.kode,
                "nama": produk.nama,
                "jumlah": jumlah,
                "harga_satuan": harga_satuan,
                "subtotal": harga_satuan * jumlah,
            }
        )
        produk.kurangi_stok(jumlah)
        return True

    def total_belanja(self):
        total = 0
        for baris in self.item:
            total += baris["subtotal"]
        return total

    def cari_item(self, kata_kunci):
        hasil = []
        kunci = kata_kunci.lower()
        for baris in self.item:
            if kunci in baris["nama"].lower():
                hasil.append(baris)
        return hasil

    def cetak_struk(self):
        garis = "=" * 40
        print(garis)
        print(f"Struk Belanja: {self.pemilik}")
        print(f"Waktu: {self.dibuat_pada}")
        print(garis)
        for idx, baris in enumerate(self.item, start=1):
            harga_teks = format_rupiah(baris["subtotal"])
            print(f"{idx}. {baris['nama']} x{baris['jumlah']} = {harga_teks}")
        print(garis)
        print(f"Total: {format_rupiah(self.total_belanja())}")

    def simpan_json(self, tujuan):
        data = {
            "pemilik": self.pemilik,
            "dibuat_pada": self.dibuat_pada,
            "total": self.total_belanja(),
            "item": self.item,
        }
        Path(tujuan).write_text(json.dumps(data, indent=2), encoding="utf-8")


def jalankan_simulasi():
    katalog = [
        Produk("P001", "Buku Algoritma", 85000, 10),
        Produk("P002", "Mouse Wireless", 145000, 5),
        Produk("P003", "Keyboard Mekanikal", 420000, 3),
    ]
    keranjang = KeranjangBelanja("Budi")
    keranjang.tambah_produk(katalog[0], 2, diskon=10)
    keranjang.tambah_produk(katalog[1], 1)

    for produk in katalog:
        if produk.stok < 5:
            print("Stok menipis:", produk.ringkasan())

    keranjang.cetak_struk()
    return keranjang


if __name__ == "__main__":
    jalankan_simulasi()
