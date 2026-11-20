import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

# 1. Fungsi sederhana
kode_fungsi = b"""def sapa(nama):
    return "halo " + nama
"""

# 2. Blok if / else
kode_if = b"""if nilai >= 75:
    status = "Lulus"
else:
    status = "Mengulang"
"""

# 3. Kelas dengan satu method
kode_kelas = b"""class Mahasiswa:
    def sapa(self):
        return "halo"
"""

# 4. Kode rusak (tanpa tanda titik dua)
kode_rusak = b"""def sapa(nama)
    return nama
"""

print("=== 1. Fungsi ===")
tree_fungsi = parser.parse(kode_fungsi)
print(f"Pohon: {tree_fungsi.root_node}")
print("Anak langsung function_definition:")
fn_node = tree_fungsi.root_node.children[0]
for c in fn_node.children:
    jenis = "bernama" if c.is_named else "anonim"
    print(f"  - {c.type}: {jenis}")

print("\n=== 2. If / Else ===")
tree_if = parser.parse(kode_if)
print(f"Pohon: {tree_if.root_node}")

print("\n=== 3. Kelas ===")
tree_kelas = parser.parse(kode_kelas)
print(f"Pohon: {tree_kelas.root_node}")

print("\n=== 4. Kode Rusak (tanpa titik dua) ===")
tree_rusak = parser.parse(kode_rusak)
print(f"Pohon: {tree_rusak.root_node}")
