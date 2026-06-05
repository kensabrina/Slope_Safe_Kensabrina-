import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="SlopeSafe",
    layout="wide"
)

# ==========================================
# TITLE
# ==========================================

st.title("SlopeSafe")
st.markdown(
    "Analisis Stabilitas Lereng Berdasarkan Parameter Geoteknik"
)

# ==========================================
# FUNGSI FS
# ==========================================

def hitung_fs(c, phi, gamma, beta):

    if beta <= 0 or gamma <= 0:
        return 0

    beta_rad = np.radians(beta)
    phi_rad = np.radians(phi)

    fs = (
        c / (gamma * np.sin(beta_rad) * np.cos(beta_rad))
    ) + (
        np.tan(phi_rad) / np.tan(beta_rad)
    )

    return round(fs, 3)

def interpretasi_fs(fs):

    if fs >= 1.25:
        return (
            "AMAN",
            "Lereng stabil dan memiliki margin keamanan yang baik."
        )

    elif fs >= 1:
        return (
            "KRITIS",
            "Lereng masih stabil tetapi perlu pemantauan."
        )

    else:
        return (
            "TIDAK AMAN",
            "Potensi longsor tinggi dan perlu mitigasi."
        )

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Parameter Geoteknik")

c = st.sidebar.number_input(
    "Kohesi c (kPa)",
    min_value=0.0,
    value=0.0,
    step=0.1
)

phi = st.sidebar.number_input(
    "Sudut Geser φ (°)",
    min_value=0.0,
    max_value=90.0,
    value=0.0,
    step=0.1
)

gamma = st.sidebar.number_input(
    "Berat Isi γ",
    min_value=0.0,
    value=0.0,
    step=0.1
)

beta = st.sidebar.number_input(
    "Sudut Lereng β",
    min_value=0.0,
    max_value=89.0,
    value=0.0,
    step=0.1
)

# ==========================================
# HITUNG FS
# ==========================================

fs = hitung_fs(
    c,
    phi,
    gamma,
    beta
)

status, ket = interpretasi_fs(fs)

col1, col2 = st.columns(2)

with col1:

    st.subheader("Hasil Analisis")

    st.metric(
        "Factor of Safety",
        fs
    )

    st.metric(
        "Status",
        status
    )

    st.info(ket)

# ==========================================
# VISUALISASI
# ==========================================

with col2:

    st.subheader("Model Lereng")

    tipe = st.selectbox(
        "Tipe Lereng",
        ["Datar", "Terasering"]
    )

    arah = st.selectbox(
        "Arah Lereng",
        ["Kiri → Kanan", "Kanan → Kiri"]
    )

    litologi = st.selectbox(
        "Litologi",
        ["Pasir","Lanau","Lempung","Breksi","Beku","Metamorf"]
    )

    warna_litologi = {
        "Pasir":"gold",
        "Lanau":"green",
        "Lempung":"lightgrey",
        "Breksi":"saddlebrown",
        "Beku":"red",
        "Metamorf":"purple"
    }

    st.markdown("### Input Koordinat Lereng")

    c1, c2 = st.columns(2)

    with c1:

        p1x = st.number_input("P1 X", value=0.0)
        p1y = st.number_input("P1 Y", value=0.0)

        p2x = st.number_input("P2 X", value=0.0)
        p2y = st.number_input("P2 Y", value=0.0)

        p3x = st.number_input("P3 X", value=0.0)
        p3y = st.number_input("P3 Y", value=0.0)

    with c2:

        p4x = st.number_input("P4 X", value=0.0)
        p4y = st.number_input("P4 Y", value=0.0)

        if tipe == "Terasering":

            p5x = st.number_input("P5 X", value=0.0)
            p5y = st.number_input("P5 Y", value=0.0)

            p6x = st.number_input("P6 X", value=0.0)
            p6y = st.number_input("P6 Y", value=0.0)

    if tipe == "Datar":

        X = [p1x, p2x, p3x, p4x]
        Y = [p1y, p2y, p3y, p4y]

    else:

        X = [p1x, p2x, p3x, p4x, p5x, p6x]
        Y = [p1y, p2y, p3y, p4y, p5y, p6y]

    if arah == "Kanan → Kiri":

        max_x = max(X)

        X = [max_x - x for x in X]

    fig, ax = plt.subplots(figsize=(8,5))

    poly = Polygon(
        list(zip(X,Y)),
        closed=True,
        facecolor=warna_litologi[litologi],
        edgecolor="black",
        linewidth=2
    )

    ax.add_patch(poly)

    ax.plot(
        X + [X[0]],
        Y + [Y[0]],
        color="black",
        linewidth=2
    )

    ax.text(
        np.mean(X),
        max(Y)+0.5,
        f"β = {beta:.1f}°"
    )

    ax.set_title("Model Lereng")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.grid(True)

    ax.set_xlim(min(X)-2,max(X)+2)
    ax.set_ylim(min(Y)-2,max(Y)+3)

    st.pyplot(fig)