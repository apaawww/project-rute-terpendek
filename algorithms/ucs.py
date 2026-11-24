
import heapq


def ucs(graf, start, goal):

    # Antrian prioritas: (total_bobot, jalur)
    antrian = [(0, [start])]

    # Mencatat node yang sudah dikunjungi
    dikunjungi = []

    # Menyimpan biaya terbaik setiap node
    biaya_terbaik = {start: 0}

    # Menyimpan riwayat proses pencarian
    events = []

    while antrian:

        # Mengambil jalur dengan bobot terkecil
        total_bobot, jalur = heapq.heappop(antrian)

        # Mengambil node terakhir
        node = jalur[-1]

        # Mengabaikan jalur yang lebih mahal
        if total_bobot > biaya_terbaik.get(
            node, float("inf")
        ):
            continue

        # Menghindari pemeriksaan ulang
        if node in dikunjungi:
            continue

        # Menandai node sebagai dikunjungi
        dikunjungi.append(node)

        # Memeriksa apakah tujuan ditemukan
        if node == goal:

            events.append({
                "node": node,
                "cost": total_bobot,
                "path": jalur.copy(),
                "visited": dikunjungi.copy(),
                "checked_edges": []
            })

            return {
                "path": jalur,
                "visited": dikunjungi,
                "total_bobot": total_bobot,
                "events": events
            }

        # Menyimpan garis yang diperiksa
        edges_diperiksa = []

        # Memeriksa semua tetangga
        for tetangga in graf.neighbors(node):

            edges_diperiksa.append((node, tetangga))

            if tetangga not in dikunjungi:

                bobot = graf[node][tetangga]["weight"]

                biaya_baru = total_bobot + bobot

                # Memperbarui jika ditemukan biaya lebih kecil
                if biaya_baru < biaya_terbaik.get(
                    tetangga, float("inf")
                ):

                    biaya_terbaik[tetangga] = biaya_baru

                    jalur_baru = jalur + [tetangga]

                    heapq.heappush(
                        antrian,
                        (biaya_baru, jalur_baru)
                    )

        events.append({
            "node": node,
            "cost": total_bobot,
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
