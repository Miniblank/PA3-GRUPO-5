import streamlit as st
import pandas as pd
import collections
import re
import os

# Configuración profesional de la página de Streamlit
st.set_page_config(
    page_title="Dashboard Bibliométrico | Grupo 05",
    page_icon="🧠",
    layout="wide"
)

# Paleta de colores profesionales para gráficos nativos (Streamlit Theme)
COLOR_TENDENCIA = ["#1f77b4"]
COLOR_AUTORES = ["#42929d"]
COLOR_PALABRAS = ["#2ca02c"]

# Optimización de carga con caché de datos
@st.cache_data
def cargar_y_limpiar_datos(ruta_archivo):
    df = pd.read_csv(ruta_archivo)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Cited by'] = pd.to_numeric(df['Cited by'], errors='coerce').fillna(0)
    df['Abstract'] = df['Abstract'].fillna("No abstract available")
    df['Authors'] = df['Authors'].fillna("Unknown Author")
    return df

# Función optimizada para procesar autores individuales y evitar desbordamientos
def extraer_top_autores(df):
    registro_autores = {}
    
    for _, fila in df.iterrows():
        citas = int(fila['Cited by'])
        cadena_autores = str(fila['Authors'])
        
        # Identificar el separador común en Scopus (; o , o #)
        if ";" in cadena_autores:
            lista_autores = [a.strip() for a in cadena_autores.split(";")]
        elif "," in cadena_autores:
            lista_autores = [a.strip() for a in cadena_autores.split(",")]
        else:
            lista_autores = [cadena_autores.strip()]
            
        # Acumular citas por cada autor individual
        for autor in lista_autores:
            if autor and autor.lower() != "unknown author":
                # Limpieza de caracteres adicionales y recorte estricto para proteger el layout gráfico
                autor_limpio = autor.replace('"', '').replace("'", "")
                if len(autor_limpio) > 22:
                    autor_limpio = autor_limpio[:22] + "..."
                
                registro_autores[autor_limpio] = registro_autores.get(autor_limpio, 0) + citas

    # Convertir a DataFrame ordenado de mayor a menor impacto
    df_autores = pd.DataFrame(registro_autores.items(), columns=['Autor', 'Total Citas'])
    df_autores = df_autores.sort_values(by='Total Citas', ascending=False).header=10 if not df_autores.empty else df_autores
    return df_autores.head(10)

# Función nativa de procesamiento de texto para Abstracts
def analizar_palabras_abstracts(df):
    texto_completo = " ".join(df['Abstract'].dropna().astype(str).str.lower())
    palabras = re.findall(r'\b[a-z]{5,}\b', texto_completo)
    
    # Filtro estricto de stop-words académicas en inglés
    stop_words = {
        'with', 'that', 'this', 'from', 'their', 'were', 'also', 'been', 'which', 
        'study', 'research', 'using', 'used', 'patients', 'health', 'mental', 
        'artificial', 'intelligence', 'analysis', 'data', 'results', 'based', 'clinical'
    }
    palabras_filtradas = [p for p in palabras if p not in stop_words]
    conteo = collections.Counter(palabras_filtradas)
    
    return pd.DataFrame(conteo.most_common(10), columns=['Concepto', 'Frecuencia'])

# --- CONTROLADORES DE LA BARRA LATERAL (SIDEBAR INTERACTIVO) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=70)
st.sidebar.title("Navegación y Filtros")
st.sidebar.markdown("---")

# Cuadro informativo del Grupo y Pregunta de Investigación
st.sidebar.info(
    "**Grupo Académico: 05**\n\n"
    "**Pregunta de Investigación:**\n"
    "¿Cómo contribuye la investigación académica en inteligencia artificial a la prevención de trastornos de salud mental en jóvenes desde 2019 a la actualidad?"
)

archivo_defecto = "scopus_export.csv"
uploaded_file = st.sidebar.file_uploader("📂 Cargar base Scopus alternativo (CSV)", type=["csv"])

ruta_final = None
if uploaded_file is not None:
    ruta_final = uploaded_file
elif os.path.exists(archivo_defecto):
    ruta_final = archivo_defecto

# --- DESARROLLO DEL CUERPO PRINCIPAL DEL DASHBOARD ---
if ruta_final is not None:
    try:
        df_crudo = cargar_y_limpiar_datos(ruta_final)
        
        # Slider interactivo temporal dinámico en Sidebar
        min_year = int(df_crudo['Year'].min()) if not pd.isna(df_crudo['Year'].min()) else 2019
        max_year = int(df_crudo['Year'].max()) if not pd.isna(df_crudo['Year'].max()) else 2026
        
        st.sidebar.markdown("### Control de Tiempo")
        rango_anios = st.sidebar.slider("Rango Cronológico", min_year, max_year, (2019, max_year))
        
        # Aplicación del filtro dinámico
        df = df_crudo[(df_crudo['Year'] >= rango_anios[0]) & (df_crudo['Year'] <= rango_anios[1])]
        
        # Título y Banner Principal del Dashboard
        st.title("🧠 Inteligencia Artificial y la Prevención de Salud Mental Juvenil")
        st.caption(f"Análisis Bibliométrico de Producción Científica Avanzada e Impacto Global ({rango_anios[0]} - {rango_anios[1]})")
        st.markdown("---")
        
        # Tarjetas de Métricas Clave (KPIs superiores) en Columnas
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.markdown("<div style='background-color:#f0f2f6;padding:15px;border-radius:10px;text-align:center;'>", unsafe_allow_html=True)
            st.metric("🔬 Volumen de Artículos", f"{len(df)} docs")
            st.markdown("</div>", unsafe_allow_html=True)
        with kpi2:
            st.markdown("<div style='background-color:#f0f2f6;padding:15px;border-radius:10px;text-align:center;'>", unsafe_allow_html=True)
            st.metric("💬 Citas Académicas Totales", f"{int(df['Cited by'].sum())} citas")
            st.markdown("</div>", unsafe_allow_html=True)
        with kpi3:
            st.markdown("<div style='background-color:#f0f2f6;padding:15px;border-radius:10px;text-align:center;'>", unsafe_allow_html=True)
            st.metric("📈 Índice de Impacto Promedio", f"{round(df['Cited by'].mean(), 2)} c/u")
            st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # SECCIÓN VISUAL 1: Análisis General de la Producción Científica
        st.subheader("📊 Bloque 1: Evolución Temporal e Investigadores de Mayor Impacto")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Cronología de Publicaciones Científicas**")
            prod_anual = df['Year'].value_counts().sort_index()
            if not prod_anual.empty:
                # Gráfico interactivo de área nativo de Streamlit
                st.area_chart(prod_anual, color="#1f77b4")
            else:
                st.warning("No hay registros en este rango.")
                
        with col2:
            st.markdown("**Top 10 Investigadores con Mayor Nivel de Citación (Filtrado Individual)**")
            df_top_autores = extraer_top_autores(df)
            if not df_top_autores.empty:
                # Gráfico interactivo nativo con nombres corregidos y formateados
                st.bar_chart(df_top_autores.set_index('Autor')['Total Citas'], color="#42929d")
            else:
                st.warning("Sin datos de citación en este segmento.")
                
        st.markdown("---")
        
        # SECCIÓN VISUAL 2: Análisis de Contenido para responder el "CÓMO"
        st.subheader("🔍 Bloque 2: Análisis de Palabras Clave y Tendencias Temáticas en Abstracts")
        col3, col4 = st.columns([1, 1.3])
        
        with col3:
            st.markdown("**Matriz Numérica de Conceptos Frecuentes**")
            df_palabras = analizar_palabras_abstracts(df)
            st.dataframe(df_palabras, use_container_width=True, hide_index=True)
            
        with col4:
            st.markdown("**Frecuencia de Enfoques de IA y Métodos de Prevención**")
            if not df_palabras.empty:
                st.bar_chart(df_palabras.set_index('Concepto')['Frecuencia'], color="#2ca02c")
            else:
                st.warning("No se pudieron procesar los resúmenes.")
                
        st.markdown("---")
        
        # SECCIÓN VISUAL 3: Verificación de Datos Crudos para el Profesor (Requisito df.head)
        st.subheader("📋 Bloque 3: Explorador e Integridad de Datos (Vista Previa df.head)")
        st.success("Carga exitosa: El archivo se ha indexado correctamente en la memoria del aplicativo.")
        st.dataframe(
            df[['Authors', 'Title', 'Year', 'Cited by', 'DOI']].head(10), 
            use_container_width=True
        )
        
    except Exception as e:
        st.error(f"Error técnico durante el parseo del archivo CSV: {e}")
else:
    st.warning("👋 El sistema está en espera del archivo de datos. Por favor, asegúrate de añadir 'scopus_export.csv' en tu repositorio de GitHub o cárgalo usando el botón del panel izquierdo.")
