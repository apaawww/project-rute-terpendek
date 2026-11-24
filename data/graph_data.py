import networkx as nx
# =====================================
# DATA LOKASI / NODE
# =====================================

NODES = {
    1: {"nama": "Gerbang", "h": 9},
    2: {"nama": "Halte", "h": 7},
    3: {"nama": "Kantin", "h": 6},
    4: {"nama": "Pasar", "h": 4},
    5: {"nama": "Mall", "h": 2},
    6: {"nama": "Stasiun", "h": 0},
    7: {"nama": "Kampus", "h": 7},
    8: {"nama": "Perpus", "h": 6},
    9: {"nama": "Asrama", "h": 5},
    10: {"nama": "Lab", "h": 3},
}

# =====================================
# DATA HUBUNGAN ANTAR NODE DAN BOBOT
# =====================================

EDGES = [
    (1, 2, 2),
    (2, 4, 3),
    (4, 5, 2),
    (5, 6, 3),

    (1, 7, 4),
    (1, 3, 3),
    (7, 8, 2),
    (7, 3, 1),

    (3, 9, 4),
    (9, 10, 2),
    (10, 6, 4),
    (8, 10, 3),
    (9, 5, 3),
]

# =====================================
# MEMBUAT GRAF
# =====================================

GRAF = nx.Graph()

# Memasukkan data node
for node, data in NODES.items():
    GRAF.add_node(
        node,
        nama=data["nama"],
        h=data["h"]
    )

# Memasukkan hubungan dan bobot
for asal, tujuan, bobot in EDGES:
    GRAF.add_edge(
        asal,
        tujuan,
        weight=bobot
    )

# =====================================
# TITIK AWAL DAN TUJUAN
# =====================================

START = 1
GOAL = 6

# =====================================
# FUNGSI MENGAMBIL NAMA LOKASI
# =====================================

def nama_node(node):
    return NODES[node]["nama"]

# =====================================
# FUNGSI MENGAMBIL NILAI HEURISTIC
# =====================================

def heuristic(node):
    return NODES[node]["h"]