import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import collections
import re
import os

# Configuración de la página del Dashboard
st.set_page_config(
    page_title="Dashboard Bibliométrico: IA en Salud Mental",
    page_icon="🧠",
    layout="wide"
)

# Optimización de carga usando la caché recomendada para Data Science
@st.cache_data
def cargar_datos(ruta_archivo):
    df = pd.read_csv(ruta_archivo)
    # Limpieza básica de columnas clave
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Cited by'] = pd.to_numeric(df['Cited by'], errors='coerce').fillna(0)
    df['Abstract'] = df['Abstract'].fillna("No abstract available")
    df['Authors'] = df['Authors'].fillna("Unknown Author")
    return df

# Función nativa para analizar las palabras más frecuentes en los Abstracts (Evita librerías pesadas)
def analizar_palabras_abstracts(df):
    texto_completo = " ".join(df['Abstract'].dropna().astype(str).str.lower())
    # Extraer palabras de más de 4 letras para evitar conectores
    palabras = re.findall(r'\b[a-z]{5,}\b', texto_completo)
    
    # Lista de stop-words comunes en inglés científico para limpiar el gráfico
    stop_words = {
        'with', 'that', 'this', 'from', 'their', 'were', 'also', 'been', 'which', 
        'study', 'research', 'using', 'used', 'patients', 'health', 'mental', 
        'artificial', 'intelligence', 'analysis', 'data', 'results', 'based', 'clinical'
    }
    palabras_filtradas = [p for p in palabras if p not in stop_words]
    conteo = collections.Counter(palabras_filtradas)
    
    df_palabras = pd.DataFrame(conteo.most_common(10), columns=['Palabra', 'Frecuencia'])
    return df_palabras

# --- INTERFAZ DE USUARIO (SIDEBAR) ---
st.sidebar.title("Configuración del Dashboard")
st.sidebar.markdown("### PA3 - Grupo 05")
st.sidebar.markdown("**Pregunta:** ¿Cómo contribuye la IA a la prevención de trastornos de salud mental en jóvenes (2019-actualidad)?")

# Comprobación de archivo automático o subida manual
archivo_defecto = "scopus_export.csv"
uploaded_file = st.sidebar.file_uploader("Subir un archivo Scopus CSV alternativo", type=["csv"])

ruta_final = None
if uploaded_file is not None:
    ruta_final = uploaded_file
elif os.path.exists(archivo_defecto):
    ruta_final = archivo_defecto

# --- CUERPO PRINCIPAL ---
st.title("🧠 Dashboard Bibliométrico de Inteligencia Artificial en Salud Mental Juvenil")
st.markdown("Análisis interactivo de la literatura científica indexada en Scopus (Periodo 2019 - 2026).")

if ruta_final is not None:
    try:
        df = cargar_datos(ruta_final)
        
        # Filtro temporal dinámico en el Sidebar
        min_year = int(df['Year'].min()) if not pd.isna(df['Year'].min()) else 2019
        max_year = int(df['Year'].max()) if not pd.isna(df['Year'].max()) else 2026
        
        rango_anios = st.sidebar.slider("Filtrar por Rango de Años", min_year, max_year, (2019, max_year))
        df_filtrado = df[(df['Year'] >= rango_anios[0]) & (df['Year'] <= rango_anios[1])]
        
        # Métricas de alto nivel en columnas layout
        metrica1, metrica2, metrica3 = st.columns(3)
        with metrica1:
            st.metric("Total de Artículos Analizados", len(df_filtrado))
        with metrica2:
            st.metric("Total de Citas Acumuladas", int(df_filtrado['Cited by'].sum()))
        with metrica3:
            st.metric("Promedio de Citas por Artículo", round(df_filtrado['Cited by'].mean(), 2))
            
        st.markdown("---")
        
        # FILA 1: Gráficos de Tendencia y Autores (Estructura en columnas)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Distribución de Publicaciones por Año")
            prod_anual = df_filtrado['Year'].value_counts().sort_index()
            if not prod_anual.empty:
                st.bar_chart(prod_anual)
            else:
                st.warning("No hay suficientes datos para el rango seleccionado.")
                
        with col2:
            st.subheader("✍️ Top 10 Autores Más Citados")
            autores_citados = df_filtrado.groupby('Authors')['Cited by'].sum().nlargest(10).reset_index()
            if not autores_citados.empty:
                fig, ax = plt.subplots()
                ax.barh(autores_citados['Authors'], autores_citados['Cited by'], color='#42929D')
                ax.invert_yaxis()  # El autor con más citas arriba
                ax.set_xlabel('Total de Citas')
                st.pyplot(fig)
            else:
                st.warning("No hay datos de citación disponibles.")
                
        st.markdown("---")
        
        # FILA 2: Análisis de Contenido de los Abstracts
        col3, col4 = st.columns([1, 1.5])
        
        with col3:
            st.subheader("🔍 Palabras Clave más Frecuentes en Abstracts")
            st.markdown("Muestra los términos científicos recurrentes más allá de las palabras de búsqueda estándar.")
            df_palabras = analizar_palabras_abstracts(df_filtrado)
            st.dataframe(df_palabras, use_container_width=True)
            
        with col4:
            st.subheader("📊 Frecuencia de Conceptos Clave")
            fig2, ax2 = plt.subplots()
            ax2.bar(df_palabras['Palabra'], df_palabras['Frecuencia'], color='#1F77B4')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig2)
            
        st.markdown("---")
        
        # Explorador de datos crudos interactivo
        st.subheader("📋 Vista Previa del Dataset Integrado (df.head)")
        st.dataframe(df_filtrado[['Authors', 'Title', 'Year', 'Cited by']].head(10), use_container_width=True)
        
    except Exception as e:
        st.error(f"Error al procesar el archivo CSV: {e}")
else:
    st.info("👋 Por favor, asegúrate de que el archivo 'scopus_export.csv' esté en la carpeta del repositorio o súbelo manualmente desde la barra lateral.")
