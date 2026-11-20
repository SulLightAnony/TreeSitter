import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

file_kode = sys.argv[1]
file_query = sys.argv[2]

with open(file_kode, "rb") as f:
    kode = f.read()
with open(file_query, encoding="utf-8") as f:
    pola = f.read()

tree = parser.parse(kode)
cursor = QueryCursor(Query(PY, pola))

if "@params" in pola:
    for _, cap in cursor.matches(tree.root_node):
        nama = cap["nama"][0].text.decode()
        jumlah = cap["params"][0].named_child_count
        print(f"{nama}: {jumlah} parameter")
elif "@call" in pola or "@fn" in pola:
    for _, cap in cursor.matches(tree.root_node):
        node = cap.get("call", cap.get("fn"))[0]
        baris = node.start_point[0] + 1
        teks = node.text.decode().splitlines()[0]
        print(f"baris {baris}: {teks}")
elif "@modul" in pola:
    nodes = cursor.captures(tree.root_node).get("modul", [])
    for node in sorted(nodes, key=lambda n: n.start_byte):
        baris = node.start_point[0] + 1
        print(f"baris {baris}: {node.text.decode()}")
else:
    for nama, nodes in cursor.captures(tree.root_node).items():
        for n in nodes:
            print(f"@{nama} baris {n.start_point[0] + 1}: {n.text.decode()}")
