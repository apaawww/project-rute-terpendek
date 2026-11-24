
from collections import deque


def bfs(graf, start, goal):

    # Membuat antrian pencarian
    antrian = deque([[start]])

    # Menyimpan node yang sudah dikunjungi
    dikunjungi = []

    # Menyimpan catatan proses pencarian untuk animasi
    events = []

    while antrian:

        # Mengambil jalur paling depan
        jalur = antrian.popleft()

        # Mengambil node terakhir dari jalur
        node = jalur[-1]

        # Melewati node jika sudah dikunjungi
        if node in dikunjungi:
            continue

        # Menandai node sebagai dikunjungi
        dikunjungi.append(node)

        # Menentukan level atau kedalaman node
        level = len(jalur) - 1

        # Menyimpan sisi yang diperiksa dari node ini
        edges_diperiksa = []

        # Memeriksa apakah tujuan ditemukan
        if node == goal:
            events.append({
                "node": node,
                "level": level,
                "path": jalur.copy(),
                "checked_edges": []
            })

            return {
                "path": jalur,
                "visited": dikunjungi,
                "total_bobot": sum(
                    graf[jalur[i]][jalur[i + 1]]["weight"]
                    for i in range(len(jalur) - 1)
                ),
                "events": events
            }

        # Memeriksa semua tetangga node
        for tetangga in graf.neighbors(node):

            edges_diperiksa.append((node, tetangga))

            if tetangga not in dikunjungi:
                jalur_baru = jalur + [tetangga]
                antrian.append(jalur_baru)

        # Mencatat proses pencarian node
        events.append({
            "node": node,
            "level": level,
            "path": jalur.copy(),
            "checked_edges": edges_diperiksa
        })

    return {
        "path": [],
        "visited": dikunjungi,
        "total_bobot": 0,
        "events": events
    }
