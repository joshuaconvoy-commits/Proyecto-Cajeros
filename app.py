import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.io as pio
from io import BytesIO
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium


# =========================
# Configuración de la página
# =========================
st.set_page_config(page_title="Dashboard Analítico", layout="wide")


# =========================
# Cargar datos reales
# =========================
df = pd.read_csv("Data\MATRIZ IA CASOS INFORMATICA U DE MEDELLIN TRAIN.csv", encoding='latin-1', sep=';')
df["Fecha Hecho"] = pd.to_datetime(df["Fecha Hecho"], errors="coerce")

df2 = pd.read_csv("data\MATRIZ IA CASOS INFORMATICA U DE MEDELLIN COMPLETO.csv", encoding='latin-1', sep=';')
# =========================
# Título principal
# =========================
st.title("IA CONTRA EL CIBERCRIMEN: ESCANEANDO MEDELLIN CON DATOS")


#------------------ caja 1------------------------
import pandas as pd
import streamlit as st

# Crear columna Año si no existe
df2["Año"] = pd.to_datetime(df2["Fecha Hecho"], errors="coerce").dt.year

# Obtener años únicos ordenados
anios_unicos = sorted(df2["Año"].dropna().unique())

# Seleccionar solo el último año para que esté por defecto
ultimo_anio = anios_unicos[-1] if anios_unicos else None

# Multiselect con solo el último año seleccionado inicialmente
anios_seleccionados = st.multiselect(
    "Selecciona los años:",
    anios_unicos,
    default=[ultimo_anio] if ultimo_anio else []
)

# Filtrar DataFrame según años seleccionados
df_filtrado = df2[df2["Año"].isin(anios_seleccionados)]

# Calcular top articulos con filtro aplicado
top_articulos = (
    df_filtrado["Articulo 2"]
    .value_counts()
    .nlargest(10)
    .reset_index()
)
top_articulos.columns = ["Artículo2", "Cantidad"]

# Gráfico de barras horizontales
import plotly.express as px

fig1 = px.bar(
    top_articulos,
    x="Cantidad",
    y="Artículo2",
    orientation="h",
    text="Cantidad",
    color_discrete_sequence=['#FF6B6B']
)

fig1.update_layout(
    showlegend=False,
    height=400,
    yaxis_title="Artículo",
    xaxis_title="Cantidad"
)

fig1.update_traces(textposition="outside")
st.plotly_chart(fig1, use_container_width=True)



col1, col2 = st.columns(2)
with col1:
    st.subheader("DELITO - Artículo (Top 10)")
    
    top_articulos = (
        df["Artículo2"]
        .value_counts()
        .nlargest(10)
        .reset_index()
    )
    top_articulos.columns = ["Artículo2", "Cantidad"]

    fig1 = px.bar(
        top_articulos,
        x="Cantidad",        # Valores numéricos en el eje X para barras horizontales
        y="Artículo2",       # Categorías en el eje Y
        orientation="h",     # Barra horizontal
        text="Cantidad",
        color_discrete_sequence=['#FF6B6B']
    )

    fig1.update_layout(
        showlegend=False,
        height=400,
        yaxis_title="Artículo",
        xaxis_title="Cantidad"
    )

    fig1.update_traces(textposition="outside")
    st.plotly_chart(fig1, use_container_width=True)


# -------- Variable 2: DESPACHO - UNIDAD --------
with col2:
    st.subheader("DESPACHO - UNIDAD (Top 10)")
    
    df["Despacho_Unidad"] = df["Despacho"].astype(str) + " - " + df["Unidad2"].astype(str)

    top_despacho_unidad = (
        df["Despacho_Unidad"]
        .value_counts()
        .nlargest(10)
        .reset_index()
    )
    top_despacho_unidad.columns = ["Despacho_Unidad", "Cantidad"]

    fig2 = px.bar(
        top_despacho_unidad,
        x="Cantidad",
        y="Despacho_Unidad",
        orientation="h",
        text="Cantidad",
        color_discrete_sequence=["#08539f"]
    )
    fig2.update_layout(
        showlegend=False,
        height=400,
        xaxis_title="Cantidad",
        yaxis_title="Despacho - Unidad"
    )
    fig2.update_traces(textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)


#------------------------------caja 2----------------------------------

st.subheader("Fecha Hecho vs Modalidad")

# Filtros de fecha
min_date = df["Fecha Hecho"].min()
max_date = df["Fecha Hecho"].max()
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Fecha inicial", min_value=min_date, max_value=max_date, value=min_date)
with col2:
    end_date = st.date_input("Fecha final", min_value=min_date, max_value=max_date, value=max_date)

mask = (df["Fecha Hecho"] >= pd.to_datetime(start_date)) & (df["Fecha Hecho"] <= pd.to_datetime(end_date))
df_filtrado = df.loc[mask].copy()

df_filtrado["Fecha Agrupada"] = df_filtrado["Fecha Hecho"]
conteo = df_filtrado.groupby(["Fecha Agrupada", "Modalidad"]).size().reset_index(name="Cantidad")

fig3 = px.line(
    conteo,
    x="Fecha Agrupada",
    y="Cantidad",
    color="Modalidad",
    markers=True,
)
fig3.update_yaxes(rangemode="tozero")
fig3.update_xaxes(tickangle=45, tickformat="%d %b %Y")
st.plotly_chart(fig3, use_container_width=True)


# Solo botón de descarga, tabla oculta
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Datos')
    return output.getvalue()

excel_data = to_excel(df_filtrado.drop(columns=["Fecha Agrupada"]) if "Fecha Agrupada" in df_filtrado.columns else df_filtrado)
st.download_button(
    label="Descargar tabla en Excel",
    data=excel_data,
    file_name="datos_intervalo.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


#-----------------------------caja 3-----------------------------------

st.subheader("CRUZAMIENTO DE VARIABLES")

col3, col4 = st.columns(2)

# -------- Variable 4: Modo vs Modalidad (Top 10 Modos) --------
with col3:
    st.subheader("Modo vs Modalidad (Top 10)")
    
    top_modos = df["Modo"].value_counts().nlargest(10).index
    df_modo_modalidad = df[df["Modo"].isin(top_modos)]

    modo_modalidad_counts = (
        df_modo_modalidad.groupby(["Modo", "Modalidad"])
        .size()
        .reset_index(name="Cantidad")
    )

    fig4 = px.bar(
        modo_modalidad_counts,
        x="Cantidad",
        y="Modo",
        color="Modalidad",
        orientation="h",
        text="Cantidad",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig4.update_layout(
        height=400,
        xaxis_title="Cantidad",
        yaxis_title="Modo",
        legend_title="Modalidad",
        barmode="stack"
    )
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    st.subheader("Estado Noticia - Distribución porcentual")
    if 'Estado Noticia' in df.columns:
        estado_counts = df['Estado Noticia'].value_counts(dropna=False).reset_index()
        estado_counts.columns = ['Estado Noticia', 'Cantidad']
        fig_estado = px.pie(
            estado_counts,
            names='Estado Noticia',
            values='Cantidad',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_estado.update_traces(textinfo='percent+label')
        fig_estado.update_layout(height=400)
        st.plotly_chart(fig_estado, use_container_width=True)
    else:
        st.info("No se encontró la columna 'Estado Noticia' en los datos.")


# ------------------------- Caja 4-------------------------

st.subheader("🗺️ Mapa de Colombia: Ubicación de Entidades Bancarias")

# Solo una columna para el mapa (no hay filtro al lado)
col_map = st.container()
df["Fecha"] = pd.to_datetime(df["Fecha Hecho"], errors="coerce").dt.date
# Limpiar coordenadas y filtrar DataFrame
def clean_coord(x):
    x = str(x).replace(' ', '').replace('"', '').replace("'", "")
    parts = x.split(',')
    if len(parts) > 1:
        x = parts[0] + '.' + ''.join(parts[1:])
    else:
        x = x.replace(',', '.')
    try:
        return float(x)
    except Exception:
        return None

df['Longitud'] = df['Longitud'].apply(clean_coord)
df['Latitud'] = df['Latitud'].apply(clean_coord)
df_mapa = df[df['Latitud'].notnull() & df['Longitud'].notnull()]

with col_map:
    mapa_colombia = folium.Map(location=[6.2442, -75.5812], zoom_start=10)
    marker_cluster = MarkerCluster().add_to(mapa_colombia)

    for idx, row in df_mapa.iterrows():
        entidad = row['ENTIDAD BANCARIA']
        lat = row['Latitud']
        lon = row['Longitud']
        fecha = row['Fecha']
        popup_text = f"<b>{entidad}</b><br>Lat: {lat:.4f}<br>Lon: {lon:.4f}<br>Fecha: {fecha}"
        folium.Marker(
            location=[lat, lon],
            popup=popup_text,
            tooltip=entidad
        ).add_to(marker_cluster)

    st_folium(mapa_colombia, width=900, height=600)
