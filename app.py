import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re
import os

st.set_page_config(
    page_title="Dashboard IA y Salud Mental | Grupo 05",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def procesar_datos(ruta):
    df = pd.read_csv(ruta)
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Cited by'] = pd.to_numeric(df['Cited by'], errors='coerce').fillna(0)
    df['Abstract'] = df['Abstract'].fillna("No abstract available")
    df['Authors'] = df['Authors'].fillna("Unknown Author")
    df['Title'] = df['Title'].fillna("Untitled")
    return df

def obtener_autores_limpios(df):
    conteo_autores = {}
    for _, fila in df.iterrows():
        citas = int(fila['Cited by'])
        autores_crudos = str(fila['Authors'])
        
        if ";" in autores_crudos:
            lista = [a.strip() for a in autores_crudos.split(";")]
        elif "," in autores_crudos:
            lista = [a.strip() for a in autores_crudos.split(",")]
        else:
            lista = [autores_crudos.strip()]
            
        for autor in lista:
            if autor and autor.lower() != "unknown author":
                autor_formateado = autor.replace('"', '').replace("'", "")
                if len(autor_formateado) > 20:
                    autor_formateado = autor_formateado[:18] + "..."
                conteo_autores[autor_formateado] = conteo_autores.get(autor_formateado, 0) + citas
                
    df_res = pd.DataFrame(conteo_autores.items(), columns=['Autor', 'Citas Acumuladas'])
    return df_res.sort_values(by='Citas Acumuladas', ascending=False).head(10)

def extraer_conceptos_clave(df):
    texto = " ".join(df['Abstract'].dropna().astype(str).str.lower())
    palabras = re.findall(r'\b[a-z]{5,}\b', texto)
    stop_words = {'with', 'that', 'this', 'from', 'their', 'were', 'also', 'been', 'which', 
                  'study', 'research', 'using', 'used', 'patients', 'health', 'mental', 
                  'artificial', 'intelligence', 'analysis', 'data', 'results', 'based', 'clinical',
                  'intervention', 'system', 'learning', 'models', 'applications', 'potential'}
    filtradas = [p for p in palabras if p not in stop_words]
    return pd.DataFrame(Counter(filtradas).most_common(12), columns=['Concepto', 'Frecuencia'])

st.sidebar.markdown("# 🛠️ Panel de Control")
st.sidebar.markdown("---")

with st.sidebar.expander("📝 Detalles del Proyecto", expanded=True):
    st.markdown("**Curso:** Fundamentos de Machine Learning")
    st.markdown("**Grupo:** 05")
    st.markdown("**Docente:** Mentor de Curso")
    st.markdown("---")
    st.markdown("**Pregunta de Investigación:**")
    st.caption("¿Cómo contribuye la investigación académica en inteligencia artificial a la prevención de trastornos de salud mental en jóvenes desde 2019 a la actualidad?")

archivo_defecto = "scopus_export.csv"
uploaded_file = st.sidebar.file_uploader("📂 Importar Dataset Scopus (CSV)", type=["csv"])
ruta_final = uploaded_file if uploaded_file is not None else (archivo_defecto if os.path.exists(archivo_defecto) else None)

if ruta_final is not None:
    try:
        df_base = procesar_datos(ruta_final)
        
        min_year = int(df_base['Year'].min()) if not pd.isna(df_base['Year'].min()) else 2019
        max_year = int(df_base['Year'].max()) if not pd.isna(df_base['Year'].max()) else 2026
        
        st.sidebar.markdown("### 🕒 Filtro Temporal")
        rango_anios = st.sidebar.slider("Rango de Años", min_year, max_year, (2019, max_year))
        
        df_filtrado = df_base[(df_base['Year'] >= rango_anios[0]) & (df_base['Year'] <= rango_anios[1])]
        
        st.title("📊 Análisis Bibliométrico de Inteligencia Artificial en la Salud Mental Juvenil")
        st.markdown("Exploración interactiva avanzada de datos científicos indexados.")
        st.markdown("---")
        
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric(label="📚 Artículos Indexados", value=f"{len(df_filtrado)} documentos")
        with kpi2:
            st.metric(label="💬 Impacto Total (Citas)", value=f"{int(df_filtrado['Cited by'].sum())} referencias")
        with kpi3:
            st.metric(label="🎯 Ratio de Citación Medio", value=f"{round(df_filtrado['Cited by'].mean(), 2)} por documento")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        tab_lineas, tab_autores, tab_contenido, tab_explorador = st.tabs([
            "📈 Tendencias Temporales", 
            "✍️ Análisis de Investigadores", 
            "🔍 Mapeo Lingüístico de Abstracts", 
            "📋 Repositorio Integrado"
        ])
        
        with tab_lineas:
            st.subheader("Evolución Cronológica de la Producción Científica")
            prod_anual = df_filtrado['Year'].value_counts().sort_index().reset_index()
            prod_anual.columns = ['Año', 'Cantidad de Publicaciones']
            
            if not prod_anual.empty:
                fig_linea = px.line(
                    prod_anual, x='Año', y='Cantidad de Publicaciones',
                    markers=True, text='Cantidad de Publicaciones',
                    template="plotly_white",
                    labels={'Cantidad de Publicaciones': 'Documentos'}
                )
                fig_linea.update_traces(line_width=3, marker_size=10, textposition="top center")
                st.plotly_chart(fig_linea, use_container_width=True)
            else:
                st.warning("No hay suficientes datos temporales para el rango seleccionado.")
                
        with tab_autores:
            st.subheader("Top 10 Investigadores con Mayor Impacto Académico")
            df_autores = obtener_autores_limpios(df_filtrado)
            
            if not df_autores.empty:
                fig_barras_autores = px.bar(
                    df_autores, x='Citas Acumuladas', y='Autor',
                    orientation='h', template="plotly_white",
                    color='Citas Acumuladas',
                    color_continuous_scale=px.colors.sequential.Teal
                )
                fig_barras_autores.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
                st.plotly_chart(fig_barras_autores, use_container_width=True)
            else:
                st.warning("Sin datos de referencias bibliográficas disponibles.")
                
        with tab_contenido:
            st.subheader("Desglose de Enfoques Metodológicos y de Prevención")
            st.markdown("Frecuencia de términos técnicos y médicos más utilizados dentro de los resúmenes académicos.")
            df_conceptos = extraer_conceptos_clave(df_filtrado)
            
            if not df_conceptos.empty:
                fig_conceptos = px.treemap(
                    df_conceptos, path=['Concepto'], values='Frecuencia',
                    template="plotly_white",
                    color='Frecuencia',
                    color_continuous_scale=px.colors.sequential.Mint
                )
                fig_conceptos.update_layout(coloraxis_showscale=False)
                st.plotly_chart(fig_conceptos, use_container_width=True)
            else:
                st.warning("No se pudo procesar el campo de resúmenes científicos.")
                
        with tab_explorador:
            st.subheader("Exploración Completa de la Literatura Indexada")
            st.info("Utiliza las herramientas internas de la tabla para ordenar, buscar o aislar columnas específicas.")
            
            columnas_visualizacion = ['Authors', 'Title', 'Year', 'Cited by', 'DOI']
            st.dataframe(
                df_filtrado[columnas_visualizacion].sort_values(by='Cited by', ascending=False).reset_index(drop=True),
                use_container_width=True
            )
            
            csv_descarga = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Subconjunto de Datos Filtrados (CSV)",
                data=csv_descarga,
                file_name=f"analisis_ia_salud_mental_{rango_anios[0]}_{rango_anios[1]}.csv",
                mime="text/csv"
            )
            
    except Exception as e:
        st.error(f"Error durante el procesamiento del archivo plano: {e}")
else:
    st.warning("👋 Cargue el archivo 'scopus_export.csv' en la raíz de su repositorio o utilícelo mediante el cargador manual de la barra lateral.")
