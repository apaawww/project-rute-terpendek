
def dfs(graf, start, goal):

    # Menyimpan node yang sudah dikunjungi
    dikunjungi = []

    # Menyimpan jalur yang ditemukan
    jalur_ditemukan = []

    # Menyimpan catatan setiap proses pencarian
    events = []

    def pencarian(node, jalur):

        # Menandai node sebagai dikunjungi
        dikunjungi.append(node)

        # Menambahkan node ke jalur
        jalur.append(node)

        # Mencatat node yang sedang diperiksa
        events.append({
            "type": "visit",
            "node": node,
            "path": jalur.copy(),
            "visited": dikunjungi.copy()
        })

        # Memeriksa apakah tujuan ditemukan
        if node == goal:
            jalur_ditemukan.extend(jalur)
            return True

        # Menelusuri tetangga satu per satu
        for tetangga in graf.neighbors(node):

            if tetangga not in dikunjungi:

                # Mencatat sisi yang akan ditelusuri
                events.append({
                    "type": "explore",
                    "node": node,
                    "next_node": tetangga,
                    "path": jalur.copy(),
                    "visited": dikunjungi.copy()
                })

                ditemukan = pencarian(tetangga, jalur)

                if ditemukan:
                    return True

        # Kembali ke node sebelumnya (backtracking)
        node_kembali = jalur.pop()

        events.append({
            "type": "backtrack",
            "node": node_kembali,
            "next_node": jalur[-1] if jalur else None,
            "path": jalur.copy(),
            "visited": dikunjungi.copy()
        })

        return False

    pencarian(start, [])

    # Menghitung total bobot jalur
    total_bobot = 0

    if jalur_ditemukan:
        for i in range(len(jalur_ditemukan) - 1):
            asal = jalur_ditemukan[i]
            tujuan = jalur_ditemukan[i + 1]

            total_bobot += graf[asal][tujuan]["weight"]

    return {
        "path": jalur_ditemukan,
        "visited": dikunjungi,
        "total_bobot": total_bobot,
        "events": events
    }
