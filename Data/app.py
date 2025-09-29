import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# Cargar datos
# =========================
# Asegúrate de tener el archivo en la misma carpeta o cambiar la ruta
df = pd.read_excel("MATRIZ IA CASOS INFORMATICA U DE MEDELLIN (1).ods", engine="odf")

# =========================
# Caja 1
# =========================
st.title("Dashboard de Casos - Caja 1")

# Crear dos columnas
col1, col2 = st.columns(2)

# -------- Columna 1: Artículo (Delito) --------
with col1:
    st.subheader("Top 10 Artículos")
    top_articulos = (
        df["Artículo"]
        .value_counts()
        .nlargest(10)
        .reset_index()
    )
    top_articulos.columns = ["Artículo", "Frecuencia"]

    fig1 = px.bar(
        top_articulos,
        x="Artículo",
        y="Frecuencia",
        text="Frecuencia",
        title="Top 10 Artículos"
    )
    st.plotly_chart(fig1, use_container_width=True)

# -------- Columna 2: Despacho - Unidad --------
with col2:
    st.subheader("Top 10 Despacho - Unidad")
    # Crear columna combinada
    df["Despacho_Unidad"] = df["Despacho"].astype(str) + " - " + df["Unidad"].astype(str)

    top_despacho_unidad = (
        df["Despacho_Unidad"]
        .value_counts()
        .nlargest(10)
        .reset_index()
    )
    top_despacho_unidad.columns = ["Despacho_Unidad", "Frecuencia"]

    fig2 = px.line(
        top_despacho_unidad,
        x="Despacho_Unidad",
        y="Frecuencia",
        markers=True,
        title="Top 10 Despacho - Unidad"
    )
    st.plotly_chart(fig2, use_container_width=True)

