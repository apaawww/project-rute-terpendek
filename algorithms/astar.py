
import heapq
from itertools import count


def astar(graf, start, goal):

    # Menghitung estimasi biaya: f(n) = g(n) + h(n)
    nomor = count()

    antrian = [
        (graf.nodes[start]["h"], 0, next(nomor), start)
    ]

    # Menyimpan biaya terbaik dari titik awal
    biaya_terbaik = {start: 0}

    # Menyimpan asal node untuk membentuk jalur
    parent = {start: None}

    # Menyimpan urutan node yang dikunjungi
    dikunjungi = []

    # Menyimpan riwayat proses pencarian
    events = []

    while antrian:

        f, biaya_sekarang, _, node = heapq.heappop(antrian)

        # Mengabaikan data antrian yang sudah tidak terbaru
        if biaya_sekarang != biaya_terbaik.get(node):
            continue

        dikunjungi.append(node)

        heuristic = graf.nodes[node]["h"]

        # Membentuk jalur sementara dari parent
        jalur = []
        posisi = node

        while posisi is not None:
            jalur.append(posisi)
            posisi = parent[posisi]

        jalur.reverse()

        # Memeriksa apakah tujuan ditemukan
        if node == goal:

            events.append({
                "node": node,
                "g": biaya_sekarang,
                "h": heuristic,
                "f": biaya_sekarang + heuristic,
                "path": jalur.copy(),
                "visited": dikunjungi.copy(),
                "checked_edges": []
            })

            return {
                "path": jalur,
                "visited": dikunjungi,
                "total_bobot": biaya_sekarang,
                "events": events
            }

        # Menyimpan garis yang diperiksa
        edges_diperiksa = []

        # Memeriksa seluruh tetangga
        for tetangga in graf.neighbors(node):

            edges_diperiksa.append((node, tetangga))

            bobot = graf[node][tetangga]["weight"]

            biaya_baru = biaya_sekarang + bobot

            # Memperbarui jika ditemukan biaya lebih kecil
            if biaya_baru < biaya_terbaik.get(
                tetangga, float("inf")
            ):

                biaya_terbaik[tetangga] = biaya_baru
                parent[tetangga] = node

                heuristic_tetangga = graf.nodes[tetangga]["h"]

                f_baru = biaya_baru + heuristic_tetangga

                heapq.heappush(
                    antrian,
                    (
                        f_baru,
                        biaya_baru,
                        next(nomor),
                        tetangga
                    )
                )

        # Menyimpan proses pencarian
        events.append({
            "node": node,
            "g": biaya_sekarang,
            "h": heuristic,
            "f": biaya_sekarang + heuristic,
            "path": jalur.copy(),
            "visited": dikunjungi.copy(),
            "checked_edges": edges_diperiksa
        })

    return {
        "path": [],
        "visited": dikunjungi,
        "total_bobot": 0,
        "events": events
    }
