
import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx
import time

from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ucs import ucs
from algorithms.astar import astar
from algorithms.greedy import greedy

from data.graph_data import GRAF, NODES, START, GOAL


# ==========================================
# 1. PENGATURAN HALAMAN
# ==========================================

st.set_page_config(
    page_title="Sistem Pencarian Rute",
    page_icon="🗺️",
    layout="wide"
)


# ==========================================
# 2. DESAIN APLIKASI (CSS)
# ==========================================

st.markdown("""
<style>

.stApp {
    background: #F4F6FB;
    color: #1E293B;
}

.block-container {
    max-width: 1600px;
    padding: 1.2rem 1.6rem 1.5rem;
}

h1, h2, h3, h4 {
    color: #172554 !important;
    letter-spacing: -0.4px;
}

p {
    color: #334155;
}

/* HEADER */

.hero {
    background: linear-gradient(
        120deg,
        #172554 0%,
        #312E81 60%,
        #4F46E5 100%
    );
    padding: 25px 32px;
    border-radius: 17px;
    margin-bottom: 18px;
    box-shadow: 0 8px 22px rgba(30, 41, 90, 0.12);
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: 29px;
    font-weight: 800;
    margin: 0 0 7px 0;
}

.hero p {
    color: #E0E7FF !important;
    font-size: 13px;
    line-height: 1.6;
    margin: 0;
}

/* PANEL */

[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF;
    border-radius: 15px;
    border-color: #E2E8F0;
}

/* Judul panel */

.panel-heading {
    font-size: 18px;
    font-weight: 800;
    color: #172554;
    margin-bottom: 3px;
}

.panel-description {
    font-size: 12px;
    color: #64748B;
    margin-bottom: 13px;
}

/* LOCATION CARDS - LEBIH RINGKAS */

.info-card {
    background: #F8FAFF;
    padding: 10px 13px;
    border-radius: 10px;
    border: 1px solid #E2E8F0;
    border-left: 3px solid #6366F1;
    margin-top: 5px;
    margin-bottom: 10px;
}

.info-card h3 {
    color: #312E81 !important;
    font-size: 14px;
    font-weight: 750;
    margin: 0;
}

/* SELECTBOX */

div[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 9px !important;
    min-height: 42px;
}

div[data-baseweb="select"] span {
    color: #1E293B !important;
    font-weight: 600;
}

[data-testid="stWidgetLabel"] p {
    color: #334155 !important;
    font-weight: 700;
}

/* BUTTON */

.stButton > button[kind="primary"] {
    background: linear-gradient(
        135deg,
        #4F46E5 0%,
        #3730A3 100%
    ) !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    min-height: 43px;
    font-size: 14px !important;
    font-weight: 800 !important;
    box-shadow: 0 5px 14px rgba(79, 70, 229, 0.22);
    transition: all 0.2s ease;
}

.stButton > button[kind="primary"] p,
.stButton > button[kind="primary"] span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 800 !important;
}

.stButton > button[kind="primary"]:hover {
    background: #312E81 !important;
    box-shadow: 0 7px 16px rgba(79, 70, 229, 0.3);
    transform: translateY(-1px);
}

/* METRICS */

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 11px;
    padding: 11px;
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
}

[data-testid="stMetricValue"] {
    color: #312E81 !important;
    font-weight: 800;
}

/* EXPANDER */

[data-testid="stExpander"] {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
}

/* TABLE */

[data-testid="stDataFrame"] {
    border: 1px solid #E2E8F0;
    border-radius: 9px;
}

/* ALERT */

[data-testid="stAlert"] {
    border-radius: 10px;
}

/* DIVIDER */

hr {
    border-color: #E2E8F0;
    margin: 16px 0;
}

/* PANEL SCROLL */

div[data-testid="stVerticalBlockBorderWrapper"] {
    overflow: hidden;
}

/* RESPONSIVE */

@media screen and (max-width: 768px) {
    .block-container {
        padding: 0.8rem;
    }

    .hero {
        padding: 21px 18px;
    }

    .hero h1 {
        font-size: 24px;
    }
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. HEADER APLIKASI
# ==========================================

st.markdown("""
<div class="hero">
    <h1>🗺️ Sistem Pencarian Rute</h1>
    <p>
        Visualisasi proses pencarian jalur menggunakan lima algoritma
        kecerdasan buatan pada graf jaringan lokasi.
    </p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 4. POSISI NODE GRAF
# ==========================================

pos = {
    1: (0, 0),
    2: (1, 2),
    3: (1, -2),
    4: (2.5, 2.5),
    5: (4, 2),
    6: (5.5, 1),
    7: (2, 0),
    8: (3, 0.5),
    9: (3, -2),
    10: (4.5, -0.5)
}


# ==========================================
# 5. FUNGSI MENGGAMBAR GRAF
# ==========================================

def tampilkan_graf(
    path=None,
    visited=None,
    current=None,
    checked_edges=None,
    active_path=None
):

    if path is None:
        path = []

    if visited is None:
        visited = []

    if checked_edges is None:
        checked_edges = []

    if active_path is None:
        active_path = []

    fig, ax = plt.subplots(figsize=(12, 6))

    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    # Menentukan warna node
    warna_node = []

    for node in GRAF.nodes():

        if node == current:
            warna_node.append("#A78BFA")

        elif node == START:
            warna_node.append("#78C091")

        elif node == GOAL:
            warna_node.append("#E88C8C")

        elif node in active_path:
            warna_node.append("#F4D477")

        elif node in path:
            warna_node.append("#F4D477")

        elif node in visited:
            warna_node.append("#60A5FA")

        else:
            warna_node.append("#C7D2FE")

    # Menentukan edge yang diperiksa
    edge_diperiksa = {
        frozenset(edge)
        for edge in checked_edges
    }

    edge_jalur = {
        frozenset((path[i], path[i + 1]))
        for i in range(len(path) - 1)
    }

    edge_aktif = {
        frozenset((active_path[i], active_path[i + 1]))
        for i in range(len(active_path) - 1)
    }

    warna_edge = []
    lebar_edge = []

    for asal, tujuan in GRAF.edges():

        edge = frozenset((asal, tujuan))

        if edge in edge_jalur:
            warna_edge.append("#F97316")
            lebar_edge.append(4)

        elif edge in edge_aktif:
            warna_edge.append("#A78BFA")
            lebar_edge.append(4)

        elif edge in edge_diperiksa:
            warna_edge.append("#38BDF8")
            lebar_edge.append(3)

        else:
            warna_edge.append("#94A3B8")
            lebar_edge.append(2)

    # Menggambar node dan edge
    nx.draw(
        GRAF,
        pos,
        with_labels=False,
        node_size=1900,
        node_color=warna_node,
        edge_color=warna_edge,
        width=lebar_edge,
        edgecolors="#FFFFFF",
        linewidths=2,
        ax=ax
    )

    # Nama lokasi dan heuristic
    labels = {
        node: f"{data['nama']}\nh={data['h']}"
        for node, data in NODES.items()
    }

    nx.draw_networkx_labels(
        GRAF,
        pos,
        labels=labels,
        font_size=8,
        font_weight="bold",
        font_color="#172554",
        ax=ax
    )

    # Bobot setiap garis
    edge_labels = nx.get_edge_attributes(
        GRAF,
        "weight"
    )

    nx.draw_networkx_edge_labels(
        GRAF,
        pos,
        edge_labels=edge_labels,
        font_size=10,
        font_color="#334155",
        font_weight="bold",
        bbox={
            "facecolor": "#FFFFFF",
            "edgecolor": "none",
            "alpha": 0.9,
            "pad": 2
        },
        ax=ax
    )

    ax.set_axis_off()
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# ==========================================
# KETERANGAN NILAI SETIAP ALGORITMA
# ==========================================

def tampilkan_keterangan(algoritma):

    keterangan_nilai = {
        "BFS": [
            ("Level", "Jumlah langkah atau sisi dari titik awal menuju node yang sedang diperiksa."),
            ("Prinsip", "BFS memeriksa node berdasarkan tingkat kedalaman, mulai dari level terdekat.")
        ],

        "DFS": [
            ("Kedalaman", "Jumlah langkah atau sisi dari titik awal menuju posisi terakhir pada jalur aktif."),
            ("Prinsip", "DFS menelusuri satu cabang sedalam mungkin. Jika tidak menemukan tujuan, pencarian kembali ke node sebelumnya (backtracking).")
        ],

        "UCS": [
            ("Cost (g)", "Total bobot jalur dari titik awal sampai node yang sedang diperiksa."),
            ("Prinsip", "UCS memilih node dengan total bobot jalur paling kecil.")
        ],

        "A*": [
            ("g(n) - Biaya Aktual", "Total bobot jalur dari titik awal sampai node saat ini."),
            ("h(n) - Heuristic", "Perkiraan biaya dari node saat ini menuju titik tujuan."),
            ("f(n) - Nilai Evaluasi", "Jumlah biaya aktual dan perkiraan biaya menuju tujuan: f(n) = g(n) + h(n)."),
            ("Prinsip", "A* memilih node dengan nilai f(n) paling kecil.")
        ],

        "Greedy": [
            ("h(n) - Heuristic", "Perkiraan biaya dari node saat ini menuju titik tujuan."),
            ("Prinsip", "Greedy memilih node dengan nilai heuristic paling kecil tanpa memperhitungkan total biaya yang sudah ditempuh.")
        ]
    }

    st.markdown("#### 💡 Keterangan Nilai")

    for judul, penjelasan in keterangan_nilai[algoritma]:

        st.markdown(
            f"""
            <div style="
                background:#F8FAFF;
                border:1px solid #E2E8F0;
                border-radius:9px;
                padding:9px 12px;
                margin-bottom:7px;
            ">
                <div style="
                    color:#312E81;
                    font-size:13px;
                    font-weight:800;
                    margin-bottom:3px;
                ">{judul}</div>
                <div style="
                    color:#475569;
                    font-size:12px;
                    line-height:1.5;
                ">{penjelasan}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
# ==========================================
# 6. SESSION STATE
# ==========================================

if "hasil" not in st.session_state:
    st.session_state["hasil"] = None

if "algoritma" not in st.session_state:
    st.session_state["algoritma"] = None


# ==========================================
# 7. DASHBOARD UTAMA
# ==========================================

kolom_kontrol, kolom_tampilan = st.columns(
    [0.85, 2.15],
    gap="medium"
)


# ==========================================
# 8. PANEL KIRI - KONTROL PENCARIAN
# ==========================================

with kolom_kontrol:

    with st.container(height=760, border=True):

        st.markdown(
            '<div class="panel-heading">⚙️ Kontrol Pencarian</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel-description">'
            'Tentukan algoritma yang ingin digunakan.'
            '</div>',
            unsafe_allow_html=True
        )

        # Titik awal
        st.markdown("**📍 Titik Awal**")

        st.markdown(f"""
        <div class="info-card">
            <h3>{NODES[START]['nama']}</h3>
        </div>
        """, unsafe_allow_html=True)

        # Titik tujuan
        st.markdown("**🏁 Titik Tujuan**")

        st.markdown(f"""
        <div class="info-card">
            <h3>{NODES[GOAL]['nama']}</h3>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Pilihan algoritma
        st.markdown("**Pilih Algoritma**")

        pilihan = st.selectbox(
            "Algoritma Pencarian",
            ["BFS", "DFS", "UCS", "A*", "Greedy"],
            label_visibility="collapsed"
        )

        keterangan = {
            "BFS": "Breadth First Search",
            "DFS": "Depth First Search",
            "UCS": "Uniform Cost Search",
            "A*": "A Star Search",
            "Greedy": "Greedy Best First Search"
        }

        st.caption(
            f"Metode: {keterangan[pilihan]}"
        )

        st.markdown("")

        tombol = st.button(
            "▶ Mulai Simulasi",
            type="primary",
            use_container_width=True
        )

        st.divider()

        st.caption(
            "Sistem Pencarian Rute"
        )

        st.caption(
            "Visualisasi Algoritma Kecerdasan Buatan"
        )


# ==========================================
# 9. PANEL KANAN - SATU AREA SCROLL
# ==========================================

with kolom_tampilan:

    with st.container(height=760, border=True):

        # ======================================
        # VISUALISASI GRAF
        # ======================================

        st.markdown(
            '<div class="panel-heading">'
            '🗺️ Visualisasi Jaringan Lokasi'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel-description">'
            'Graf menunjukkan hubungan antar lokasi. '
            'Angka pada garis adalah bobot jalur, '
            'sedangkan h menunjukkan nilai heuristic.'
            '</div>',
            unsafe_allow_html=True
        )

        tampilkan_graf()

        st.divider()

        # Keterangan graf
        st.markdown("**Keterangan Graf**")

        st.markdown("""
        <div style="
            display:flex;
            flex-wrap:wrap;
            gap:12px;
            font-size:12px;
            font-weight:600;
        ">
            <span style="color:#27834D;">🟢 Titik awal</span>
            <span style="color:#C24141;">🔴 Titik tujuan</span>
            <span style="color:#7C3AED;">🟣 Node aktif</span>
            <span style="color:#2563EB;">🔵 Node dikunjungi</span>
            <span style="color:#B7791F;">🟡 Jalur sementara</span>
            <span style="color:#EA580C;">🟠 Jalur akhir</span>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ======================================
        # PROSES SIMULASI
        # ======================================

        if tombol:

            # Menjalankan algoritma sesuai pilihan
            if pilihan == "BFS":
                hasil = bfs(GRAF, START, GOAL)

            elif pilihan == "DFS":
                hasil = dfs(GRAF, START, GOAL)

            elif pilihan == "UCS":
                hasil = ucs(GRAF, START, GOAL)

            elif pilihan == "A*":
                hasil = astar(GRAF, START, GOAL)

            else:
                hasil = greedy(GRAF, START, GOAL)

            # Menyimpan hasil pencarian
            st.session_state["hasil"] = hasil
            st.session_state["algoritma"] = pilihan

            area_animasi = st.empty()

            # ==================================
            # ANIMASI BFS
            # ==================================

            if pilihan == "BFS" and hasil.get("events"):

                edges_terperiksa = []
                node_dikunjungi = []

                for langkah, event in enumerate(
                    hasil["events"],
                    start=1
                ):

                    node_sekarang = event["node"]

                    node_dikunjungi.append(node_sekarang)

                    edges_terperiksa.extend(
                        event["checked_edges"]
                    )

                    with area_animasi.container():

                        st.markdown("### 🔍 Proses Pencarian BFS")

                        kolom1, kolom2 = st.columns(2)

                        with kolom1:
                            st.metric(
                                "Langkah Pencarian",
                                langkah
                            )

                        with kolom2:
                            st.metric(
                                "Level Node",
                                event["level"]
                            )
                        
                        tampilkan_keterangan("BFS")

                        st.info(
                            f"Sedang memeriksa: "
                            f"**{NODES[node_sekarang]['nama']}**"
                        )

                        tampilkan_graf(
                            visited=node_dikunjungi,
                            current=node_sekarang,
                            checked_edges=edges_terperiksa
                        )

                        nama_dikunjungi = [
                            NODES[n]["nama"]
                            for n in node_dikunjungi
                        ]

                        st.markdown("#### Urutan Kunjungan")
                        st.write(" → ".join(nama_dikunjungi))

                    time.sleep(0.8)

                with area_animasi.container():

                    st.success("Pencarian BFS selesai!")

                    tampilkan_graf(
                        path=hasil["path"],
                        visited=hasil["visited"],
                        checked_edges=edges_terperiksa
                    )

            # ==================================
            # ANIMASI DFS
            # ==================================

            elif pilihan == "DFS" and hasil.get("events"):

                edges_terperiksa = []

                for langkah, event in enumerate(
                    hasil["events"],
                    start=1
                ):

                    jenis = event["type"]
                    node_sekarang = event["node"]
                    jalur_aktif = event["path"]

                    if jenis == "explore":

                        edges_terperiksa.append(
                            (event["node"], event["next_node"])
                        )

                    with area_animasi.container():

                        st.markdown("### 🔍 Proses Pencarian DFS")

                        kolom1, kolom2 = st.columns(2)

                        with kolom1:
                            st.metric(
                                "Langkah Pencarian",
                                langkah
                            )

                        with kolom2:
                            st.metric(
                                "Kedalaman Cabang",
                                len(jalur_aktif) - 1
                            )
                        tampilkan_keterangan("DFS")

                        if jenis == "visit":

                            st.info(
                                f"🔎 Mengunjungi: "
                                f"**{NODES[node_sekarang]['nama']}**"
                            )

                        elif jenis == "explore":

                            st.info(
                                f"➡️ Menelusuri cabang: "
                                f"**{NODES[node_sekarang]['nama']}** "
                                f"menuju "
                                f"**{NODES[event['next_node']]['nama']}**"
                            )

                        elif jenis == "backtrack":

                            if event["next_node"] is not None:

                                st.warning(
                                    f"↩️ Backtracking dari "
                                    f"**{NODES[node_sekarang]['nama']}** "
                                    f"kembali ke "
                                    f"**{NODES[event['next_node']]['nama']}**"
                                )

                            else:

                                st.warning(
                                    "Pencarian kembali ke titik awal."
                                )

                        if jenis == "backtrack":
                            node_aktif = event["next_node"]

                        elif jenis == "explore":
                            node_aktif = event["next_node"]

                        else:
                            node_aktif = node_sekarang

                        tampilkan_graf(
                            visited=event["visited"],
                            current=node_aktif,
                            checked_edges=edges_terperiksa,
                            active_path=jalur_aktif
                        )

                        nama_jalur_aktif = [
                            NODES[n]["nama"]
                            for n in jalur_aktif
                        ]

                        st.markdown(
                            "#### Jalur yang Sedang Ditelusuri"
                        )

                        if nama_jalur_aktif:
                            st.write(" → ".join(nama_jalur_aktif))
                        else:
                            st.write("Belum ada jalur aktif.")

                    time.sleep(0.8)

                with area_animasi.container():

                    st.success("Pencarian DFS selesai!")

                    tampilkan_graf(
                        path=hasil["path"],
                        visited=hasil["visited"],
                        checked_edges=edges_terperiksa
                    )

            # ==================================
            # ANIMASI UCS
            # ==================================

            elif pilihan == "UCS" and hasil.get("events"):

                edges_terperiksa = []

                for langkah, event in enumerate(
                    hasil["events"],
                    start=1
                ):

                    node_sekarang = event["node"]

                    edges_terperiksa.extend(
                        event["checked_edges"]
                    )

                    with area_animasi.container():

                        st.markdown("### 🔍 Proses Pencarian UCS")

                        kolom1, kolom2 = st.columns(2)

                        with kolom1:
                            st.metric(
                                "Langkah Pencarian",
                                langkah
                            )

                        with kolom2:
                            st.metric(
                                "Total Bobot Sementara (g)",
                                event["cost"]
                            )
                        tampilkan_keterangan("UCS")

                        st.info(
                            f"🎯 UCS memilih node "
                            f"**{NODES[node_sekarang]['nama']}** "
                            f"dengan total bobot "
                            f"**{event['cost']}**"
                        )

                        st.caption(
                            "UCS memprioritaskan jalur dengan "
                            "total bobot paling kecil."
                        )

                        tampilkan_graf(
                            visited=event["visited"],
                            current=node_sekarang,
                            checked_edges=edges_terperiksa,
                            active_path=event["path"]
                        )

                        nama_dikunjungi = [
                            NODES[n]["nama"]
                            for n in event["visited"]
                        ]

                        st.markdown("#### Urutan Kunjungan")
                        st.write(" → ".join(nama_dikunjungi))

                        nama_jalur = [
                            NODES[n]["nama"]
                            for n in event["path"]
                        ]

                        st.markdown("#### Jalur Sementara")
                        st.write(" → ".join(nama_jalur))

                    time.sleep(0.8)

                with area_animasi.container():

                    st.success("Pencarian UCS selesai!")

                    tampilkan_graf(
                        path=hasil["path"],
                        visited=hasil["visited"],
                        checked_edges=edges_terperiksa
                    )

            # ==================================
            # ANIMASI A*
            # ==================================

            elif pilihan == "A*" and hasil.get("events"):

                edges_terperiksa = []

                for langkah, event in enumerate(
                    hasil["events"],
                    start=1
                ):

                    node_sekarang = event["node"]

                    edges_terperiksa.extend(
                        event["checked_edges"]
                    )

                    with area_animasi.container():

                        st.markdown("### 🔍 Proses Pencarian A*")

                        kolom1, kolom2, kolom3 = st.columns(3)

                        with kolom1:
                            st.metric(
                                "Biaya Aktual (g)",
                                event["g"]
                            )

                        with kolom2:
                            st.metric(
                                "Heuristic (h)",
                                event["h"]
                            )

                        with kolom3:
                            st.metric(
                                "Nilai Evaluasi (f)",
                                event["f"]
                            )
                        tampilkan_keterangan("A*")

                        st.info(
                            f"🎯 A* memilih node "
                            f"**{NODES[node_sekarang]['nama']}** "
                            f"dengan nilai f = "
                            f"**{event['f']}**"
                        )

                        st.caption(
                            "A* memilih node berdasarkan nilai "
                            "f(n) = g(n) + h(n) terkecil."
                        )

                        tampilkan_graf(
                            visited=event["visited"],
                            current=node_sekarang,
                            checked_edges=edges_terperiksa,
                            active_path=event["path"]
                        )

                        nama_dikunjungi = [
                            NODES[n]["nama"]
                            for n in event["visited"]
                        ]

                        st.markdown("#### Urutan Kunjungan")
                        st.write(" → ".join(nama_dikunjungi))

                        nama_jalur = [
                            NODES[n]["nama"]
                            for n in event["path"]
                        ]

                        st.markdown("#### Jalur Sementara")
                        st.write(" → ".join(nama_jalur))

                    time.sleep(0.8)

                with area_animasi.container():

                    st.success("Pencarian A* selesai!")

                    tampilkan_graf(
                        path=hasil["path"],
                        visited=hasil["visited"],
                        checked_edges=edges_terperiksa
                    )

            # ==================================
            # ANIMASI GREEDY
            # ==================================

            elif pilihan == "Greedy" and hasil.get("events"):

                edges_terperiksa = []

                for langkah, event in enumerate(
                    hasil["events"],
                    start=1
                ):

                    node_sekarang = event["node"]

                    edges_terperiksa.extend(
                        event["checked_edges"]
                    )

                    with area_animasi.container():

                        st.markdown("### 🔍 Proses Pencarian Greedy")

                        kolom1, kolom2 = st.columns(2)

                        with kolom1:
                            st.metric(
                                "Langkah Pencarian",
                                langkah
                            )

                        with kolom2:
                            st.metric(
                                "Nilai Heuristic (h)",
                                event["heuristic"]
                            )
                        tampilkan_keterangan("Greedy")

                        st.info(
                            f"🎯 Greedy memilih node "
                            f"**{NODES[node_sekarang]['nama']}** "
                            f"dengan nilai heuristic "
                            f"**h = {event['heuristic']}**"
                        )

                        st.caption(
                            "Greedy memprioritaskan node dengan "
                            "nilai heuristic paling kecil."
                        )

                        tampilkan_graf(
                            visited=event["visited"],
                            current=node_sekarang,
                            checked_edges=edges_terperiksa,
                            active_path=event["path"]
                        )

                        nama_dikunjungi = [
                            NODES[n]["nama"]
                            for n in event["visited"]
                        ]

                        st.markdown("#### Urutan Kunjungan")
                        st.write(" → ".join(nama_dikunjungi))

                        nama_jalur = [
                            NODES[n]["nama"]
                            for n in event["path"]
                        ]

                        st.markdown("#### Jalur Sementara")
                        st.write(" → ".join(nama_jalur))

                    time.sleep(0.8)

                with area_animasi.container():

                    st.success("Pencarian Greedy selesai!")

                    tampilkan_graf(
                        path=hasil["path"],
                        visited=hasil["visited"],
                        checked_edges=edges_terperiksa
                    )

            else:

                st.warning(
                    "Data animasi belum tersedia. "
                    "Periksa kembali file algoritma yang dipilih."
                )

        # ======================================
        # HASIL PENCARIAN
        # ======================================

        if st.session_state["hasil"] is not None:

            hasil = st.session_state["hasil"]
            algoritma_terpilih = st.session_state["algoritma"]

            st.divider()

            st.markdown(
                f"### 📊 Hasil Pencarian {algoritma_terpilih}"
            )

            if hasil["path"]:

                nama_jalur = [
                    NODES[node]["nama"]
                    for node in hasil["path"]
                ]

                nama_dikunjungi = [
                    NODES[node]["nama"]
                    for node in hasil["visited"]
                ]

                st.success(
                    " → ".join(nama_jalur)
                )

                kolom1, kolom2 = st.columns(2)

                with kolom1:
                    st.metric(
                        "Total Bobot Jalur",
                        hasil["total_bobot"]
                    )

                with kolom2:
                    st.metric(
                        "Jumlah Lokasi Dikunjungi",
                        len(hasil["visited"])
                    )

                st.markdown("#### 🔎 Urutan Lokasi Dikunjungi")

                st.write(" → ".join(nama_dikunjungi))

                st.markdown("#### 🗺️ Graf Jalur Hasil Pencarian")

                tampilkan_graf(
                    path=hasil["path"],
                    visited=hasil["visited"]
                )

                st.markdown("#### 💡 Kesimpulan Pencarian")

                kesimpulan = {
                    "BFS": (
                        "BFS melakukan pencarian secara melebar berdasarkan level. "
                        "Algoritma ini menemukan jalur berdasarkan jumlah sisi "
                        "paling sedikit, bukan total bobot terkecil."
                    ),

                    "DFS": (
                        "DFS melakukan pencarian sedalam mungkin pada satu cabang "
                        "sebelum melakukan backtracking untuk mencoba cabang lain. "
                        "Hasil jalurnya bergantung pada urutan tetangga."
                    ),

                    "UCS": (
                        "UCS memilih node berdasarkan total bobot perjalanan "
                        "terkecil dari titik awal. Algoritma ini dapat menemukan "
                        "jalur dengan total biaya minimum."
                    ),

                    "A*": (
                        "A* memilih node berdasarkan gabungan biaya aktual "
                        "dan perkiraan biaya menuju tujuan menggunakan rumus "
                        "f(n) = g(n) + h(n)."
                    ),

                    "Greedy": (
                        "Greedy memilih node berdasarkan nilai heuristic terkecil "
                        "tanpa memperhitungkan total biaya yang sudah dikeluarkan. "
                        "Karena itu, hasilnya belum tentu merupakan jalur dengan "
                        "total bobot minimum."
                    )
                }

                st.info(kesimpulan[algoritma_terpilih])


            else:

                st.error("Tidak ditemukan jalur menuju tujuan.")

        # ======================================
        # TABEL DATA LOKASI - LEBAR PANEL KANAN
        # ======================================

        st.divider()

        with st.expander("📋 Data Seluruh Lokasi", expanded=False):

            data_lokasi = [
                {
                    "Nomor Node": node,
                    "Nama Lokasi": data["nama"],
                    "Heuristic": data["h"]
                }
                for node, data in NODES.items()
            ]

            st.dataframe(
                data_lokasi,
                use_container_width=True,
                hide_index=True,
                height=300
            )


# ==========================================
# 10. FOOTER
# ==========================================

st.markdown("""
<div style="
    text-align:center;
    color:#64748B;
    padding:10px;
    font-size:12px;
">
    <b>Sistem Pencarian Rute</b> |
    UTS Kecerdasan Buatan by Kelompok2-E
</div>
""", unsafe_allow_html=True)
