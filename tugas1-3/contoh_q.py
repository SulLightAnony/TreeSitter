import os
import sys as sistem
from pathlib import Path
from datetime import datetime


def halo():
    print("Halo dari program uji")


def tambah(a, b):
    hasil = a + b
    print("Hasil penjumlahan:", hasil)
    return hasil


def hitung_total(harga, jumlah, diskon=0):
    subtotal = harga * jumlah
    potongan = subtotal * (diskon / 100)
    total = subtotal - potongan
    return total


def ringkas_data(nama, umur, kota, aktif):
    info = f"{nama} ({umur}) - {kota}"
    if aktif:
        print(info)
    return info


if __name__ == "__main__":
    halo()
    tambah(3, 5)
    print("Folder saat ini:", Path.cwd())
