import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")
ABAIKAN = {".venv", "venv", ".git", "node_modules"}


def cari_error(node):
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        hasil = cari_error(child)
        if hasil is not None:
            return hasil
    return None


def cek_file(path, ringkasan):
    tree = parser.parse(path.read_bytes())

    # 1. Komentar TODO / FIXME
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        teks = node.text.decode(errors="replace").strip()
        print(f"{path}:{node.start_point[0] + 1}: {teks}")
        ringkasan["todo"] += 1

    # 2. Fungsi lebih dari 30 baris
    for _, cap in QueryCursor(Q_FUNGSI).matches(tree.root_node):
        if "nama" not in cap or "fungsi" not in cap:
            continue
        node_nama = cap["nama"][0]
        node_fungsi = cap["fungsi"][0]
        jumlah_baris = node_fungsi.end_point[0] - node_fungsi.start_point[0] + 1
        if jumlah_baris > 30:
            nama = node_nama.text.decode(errors="replace")
            print(f"{path}:{node_fungsi.start_point[0] + 1}: {nama} ({jumlah_baris} baris)")
            ringkasan["fungsi_panjang"] += 1

    # 3. Deteksi syntax error
    if tree.root_node.has_error:
        node_err = cari_error(tree.root_node)
        baris = node_err.start_point[0] + 1 if node_err else 1
        jenis = "MISSING" if (node_err and node_err.is_missing) else "ERROR"
        print(f"{path}:{baris}: syntax error ({jenis})")
        ringkasan["error"] += 1


def main():
    if len(sys.argv) < 2:
        print("Pemakaian: python cek.py <folder>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Folder tidak ditemukan: {target}")
        sys.exit(1)

    ringkasan = {"file": 0, "todo": 0, "fungsi_panjang": 0, "error": 0}
    for path in sorted(target.rglob("*.py")):
        if any(bagian in ABAIKAN for bagian in path.parts):
            continue
        ringkasan["file"] += 1
        cek_file(path, ringkasan)

    print(
        f"\nRingkasan: {ringkasan['file']} file diperiksa, "
        f"{ringkasan['todo']} TODO/FIXME, "
        f"{ringkasan['fungsi_panjang']} fungsi > 30 baris, "
        f"{ringkasan['error']} file dengan syntax error."
    )


if __name__ == "__main__":
    main()
