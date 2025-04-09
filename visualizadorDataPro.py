import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

# Configuración visual
sns.set(style="darkgrid")
st.set_page_config(page_title="Visualizador Pro - Christian Duran", layout="wide", page_icon="📊")

# 🎨 Encabezado visual con HTML
st.markdown("""
    <div style="background-color:#4B8BBE;padding:15px;border-radius:10px">
        <h2 style="color:white;text-align:center;">Visualizador de Datos Pro 🔍</h2>
        <p style="color:white;text-align:center;">Desarrollado por <strong>Christian Duran</strong> • Interfaz moderna con filtros dinámicos y visualización avanzada</p>
    </div>
    <br>
""", unsafe_allow_html=True)

# 📥 Carga de archivo
st.sidebar.markdown("## 📂 Carga tu archivo")
archivo = st.sidebar.file_uploader("Sube un archivo CSV, Excel o JSON", type=["csv", "xlsx", "json"])

if archivo is None:
    st.info("👈 Sube un archivo desde el panel lateral para comenzar.")
    st.stop()

# 🧪 Carga el archivo
ext = archivo.name.split('.')[-1]
try:
    if ext == "csv":
        df = pd.read_csv(archivo)
    elif ext == "xlsx":
        df = pd.read_excel(archivo)
    elif ext == "json":
        df = pd.read_json(archivo)
    else:
        st.error("❌ Formato de archivo no soportado.")
        st.stop()
except Exception as e:
    st.error(f"❌ Error al leer el archivo: {e}")
    st.stop()

if df.empty or df.shape[1] == 0:
    st.warning("⚠️ El archivo está vacío o no contiene columnas válidas.")
    st.stop()

st.success("✅ Archivo cargado correctamente.")
st.markdown(f"### 📄 Dataset: `{archivo.name}`  — {df.shape[0]} filas × {df.shape[1]} columnas")

# 🧹 Filtros dinámicos
st.sidebar.markdown("## 🧼 Filtros")

df_filtrado = df.copy()

# Filtro por columnas categóricas
for col in df.select_dtypes(include=['object', 'category']).columns:
    opciones = sorted(df[col].dropna().unique().tolist())
    seleccionados = st.sidebar.multiselect(f"Filtrar por {col}", opciones)
    if seleccionados:
        df_filtrado = df_filtrado[df_filtrado[col].isin(seleccionados)]

# Filtro por columnas numéricas
for col in df.select_dtypes(include=['int64', 'float64']).columns:
    min_val = float(df[col].min())
    max_val = float(df[col].max())
    rango = st.sidebar.slider(f"Rango para {col}", min_val, max_val, (min_val, max_val))
    df_filtrado = df_filtrado[df_filtrado[col].between(rango[0], rango[1])]

# Filtro por columnas de fechas
for col in df.select_dtypes(include=['object', 'datetime64']).columns:
    try:
        df[col] = pd.to_datetime(df[col])
        fecha_min = df[col].min()
        fecha_max = df[col].max()
        rango = st.sidebar.date_input(f"Rango de fechas en {col}", (fecha_min, fecha_max))
        if isinstance(rango, tuple) and len(rango) == 2:
            df_filtrado = df_filtrado[df[col].between(rango[0], rango[1])]
    except:
        continue

# 🧾 Vista del DataFrame filtrado
st.markdown("### 🧾 Vista previa del DataFrame filtrado")
st.dataframe(df_filtrado)

# 📥 Descargar CSV
def descargar_csv(dataframe):
    buffer = BytesIO()
    dataframe.to_csv(buffer, index=False)
    return buffer.getvalue()

csv_data = descargar_csv(df_filtrado)
st.download_button("📥 Descargar CSV", data=csv_data, file_name="datos_filtrados.csv", mime="text/csv")

# 📊 Visualización
st.markdown("### 📈 Visualización de Datos")

if df_filtrado.shape[0] > 0:
    col1, col2 = st.columns([3, 2])

    with col1:
        columna = st.selectbox("📂 Selecciona una columna para graficar", df_filtrado.columns)

    with col2:
        tipo = st.selectbox("📊 Tipo de gráfico", [
            "Histograma", "Gráfico de Línea", "Gráfico de Barras", 
            "Boxplot", "Scatterplot (con otra columna)", 
            "Heatmap de correlación"
        ])

    fig, ax = plt.subplots(figsize=(10, 5))

    try:
        if tipo == "Histograma":
            sns.histplot(df_filtrado[columna].dropna(), kde=True, ax=ax)
            ax.set_title(f"Distribución de {columna}")

        elif tipo == "Gráfico de Línea":
            ax.plot(df_filtrado[columna].dropna())
            ax.set_title(f"Gráfico de Línea - {columna}")

        elif tipo == "Gráfico de Barras":
            df_filtrado[columna].value_counts().plot(kind='bar', ax=ax)
            ax.set_title(f"Frecuencia de valores - {columna}")

        elif tipo == "Boxplot":
            sns.boxplot(y=df_filtrado[columna], ax=ax)
            ax.set_title(f"Boxplot - {columna}")

        elif tipo == "Scatterplot (con otra columna)":
            num_cols = df_filtrado.select_dtypes("number").columns.tolist()
            col2 = st.selectbox("🔁 Otra columna numérica", [c for c in num_cols if c != columna])
            sns.scatterplot(x=df_filtrado[col2], y=df_filtrado[columna], ax=ax)
            ax.set_title(f"Relación entre {col2} y {columna}")

        elif tipo == "Heatmap de correlación":
            corr = df_filtrado.select_dtypes("number").corr()
            fig, ax = plt.subplots(figsize=(12, 8))
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            ax.set_title("Mapa de Calor de Correlación")

        st.pyplot(fig)

        if st.button("💾 Guardar gráfico como PNG"):
            fig.savefig(f"grafico_{columna}_{tipo.replace(' ', '_')}.png")
            st.success("✅ Gráfico guardado.")
    except Exception as e:
        st.error(f"❌ Error al graficar: {e}")
else:
    st.warning("⚠️ No hay datos disponibles para graficar tras aplicar los filtros.")
