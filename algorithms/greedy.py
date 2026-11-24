
import heapq
from itertools import count


def greedy(graf, start, goal):

    nomor = count()

    # Antrian berdasarkan nilai heuristic terkecil
    antrian = [
        (graf.nodes[start]["h"], next(nomor), start, [start])
    ]

    # Menyimpan node yang sudah dikunjungi
    dikunjungi = []

    # Menyimpan riwayat proses pencarian
    events = []

    while antrian:

        heuristic, _, node, jalur = heapq.heappop(antrian)

        # Melewati node yang sudah dikunjungi
        if node in dikunjungi:
            continue

        dikunjungi.append(node)

        # Memeriksa apakah tujuan ditemukan
        if node == goal:

            events.append({
                "type": "visit",
                "node": node,
                "heuristic": heuristic,
                "path": jalur.copy(),
                "visited": dikunjungi.copy(),
                "checked_edges": []
            })

            total_bobot = sum(
                graf[jalur[i]][jalur[i + 1]]["weight"]
                for i in range(len(jalur) - 1)
            )

            return {
                "path": jalur,
                "visited": dikunjungi,
                "total_bobot": total_bobot,
                "events": events
            }

        # Menyimpan sisi yang diperiksa
        edges_diperiksa = []

        # Memeriksa semua tetangga
        for tetangga in graf.neighbors(node):

            edges_diperiksa.append((node, tetangga))

            if tetangga not in dikunjungi:

                nilai_heuristic = graf.nodes[tetangga]["h"]

                jalur_baru = jalur + [tetangga]

                heapq.heappush(
                    antrian,
                    (
                        nilai_heuristic,
                        next(nomor),
                        tetangga,
                        jalur_baru
                    )
                )

        events.append({
            "type": "visit",
            "node": node,
            "heuristic": heuristic,
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
