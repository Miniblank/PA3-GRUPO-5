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

# ────────────────────────────────────────────────────────────
# ESTILOS CSS AVANZADOS — CLINICAL DARK HEALTH THEME (GRUPO 05)
# ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,600;14..32,700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #070b12 0%, #0c101b 100%);
    color: #e2e8f0;
}

/* Panel Lateral Estilizado */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b0f19 0%, #111625 100%) !important;
    border-right: 1px solid #1f293d;
}

[data-testid="stSidebar"] *, .stExpander {
    color: #cbd5e1 !important;
}

/* Tarjetas KPIs Modificadas (Efecto de Cristal / Glassmorphism) */
.kpi-card {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid #1f293d;
    border-left: 4px solid #06b6d4; /* Color Cian */
    border-radius: 12px;
    padding: 1.25rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    text-align: left;
    margin-bottom: 1rem;
}

.kpi-title {
    color: #94a3b8;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.kpi-value {
    color: #f8fafc;
    font-size: 1.8rem;
    font-weight: 700;
    margin-top: 0.25rem;
}

/* Pestañas (Tabs) con Diseño Profesional Oscuro */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: transparent;
}

.stTabs [data-baseweb="tab"] {
    background-color: #111827 !important;
    border: 1px solid #1f293d !important;
    border-radius: 6px 6px 0px 0px !important;
    padding: 10px 20px !important;
    color: #94a3b8 !important;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background-color: #1e293b !important;
    color: #06b6d4 !important; /* Resaltado Cian */
    border-bottom: 2px solid #06b6d4 !important;
}

/* Tablas e Inputs */
div[data-testid="stDataFrame"] {
    background-color: #0b0f19;
    border: 1px solid #1f293d;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────
# FUNCIONES NATIVAS DE PROCESAMIENTO OPTIMIZADAS
# ────────────────────────────────────────────────────────────
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
                  'artificial', 'intelligence', 'analysis', 'data', 'results', 'based', 'clinical'}
    filtradas = [p for p in palabras if p not in stop_words]
    return pd.DataFrame(Counter(filtradas).most_common(12), columns=['Concepto', 'Frecuencia'])

# ────────────────────────────────────────────────────────────
# CONTROLADORES E INFORMACIÓN EN LA BARRA LATERAL (SIDEBAR)
# ────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align: center; margin-bottom: 1rem;'>
    <h2 style='color: #06b6d4; font-size: 1.5rem; margin-bottom: 0;'>GRUPO 05</h2>
    <small style='color: #64748b;'>Análisis Clínico y Tecnológico</small>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

with st.sidebar.expander("👥 Integrantes del Grupo", expanded=True):
    st.markdown("- 👤 Miembro del Grupo 5 (Líder)")
    st.markdown("- 👤 Colaborador 1")
    st.markdown("- 👤 Colaborador 2")

with st.sidebar.expander("🔬 Metodología de Investigación", expanded=False):
    st.markdown("**Keywords Usadas:**")
    st.caption('"Artificial Intelligence", "Mental Health", "Youth", "Prevention"')
    st.markdown("**Cadena Scopus:**")
    st.code('TITLE-ABS-KEY(("Artificial Intelligence" OR "Machine Learning") AND ("Mental Health") AND ("Youth") AND "Prevention")', language='text')

archivo_defecto = "scopus_export.csv"
uploaded_file = st.sidebar.file_uploader("📂 Importar Dataset Scopus Alternativo", type=["csv"])
ruta_final = uploaded_file if uploaded_file is not None else (archivo_defecto if os.path.exists(archivo_defecto) else None)

if ruta_final is not None:
    try:
        df_base = procesar_datos(ruta_final)
        
        min_year = int(df_base['Year'].min()) if not pd.isna(df_base['Year'].min()) else 2019
        max_year = int(df_base['Year'].max()) if not pd.isna(df_base['Year'].max()) else 2026
        
        st.sidebar.markdown("### 🕒 Configuración de Filtros")
        rango_anios = st.sidebar.slider("Horizonte Temporal", min_year, max_year, (2019, max_year))
        
        df_filtrado = df_base[(df_base['Year'] >= rango_anios[0]) & (df_base['Year'] <= rango_anios[1])]
        
        # BARRA LATERAL EN BASE A LA CAPTURA DEL COMPAÑERO
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📋 Resumen del Segmento")
        st.sidebar.caption(f"Filtro activo para documentos publicados entre **{rango_anios[0]}** y **{rango_anios[1]}**.")
        
        # ────────────────────────────────────────────────────────────
        # CONTENIDO PRINCIPAL DEL DASHBOARD (DISEÑO PREMIUM)
        # ────────────────────────────────────────────────────────────
        st.title("🧠 Inteligencia Artificial Aplicada a la Prevención en Salud Mental Juvenil")
        st.caption(f"Plataforma Interactiva Bibliométrica de Análisis de Producción Científica Global")
        st.markdown("---")
        
        # Renderizado de KPIs con diseño HTML integrado al CSS
        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-title">🔬 Volumen de Literatura</div>
                <div class="kpi-value">{len(df_filtrado)} Documentos</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi2:
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #10b981;">
                <div class="kpi-title">💬 Citas Totales Acumuladas</div>
                <div class="kpi-value">{int(df_filtrado['Cited by'].sum())} Referencias</div>
            </div>
            """, unsafe_allow_html=True)
        with kpi3:
            st.markdown(f"""
            <div class="kpi-card" style="border-left-color: #a855f7;">
                <div class="kpi-title">🎯 Tasa de Impacto Promedio</div>
                <div class="kpi-value">{round(df_filtrado['Cited by'].mean(), 2)} Citas/Doc</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        tab_lineas, tab_autores, tab_contenido, tab_explorador = st.tabs([
            "📈 Tendencias Temporales", 
            "✍️ Impacto de Investigadores", 
            "🔍 Análisis de Abstracts", 
            "📋 Explorador de Datos"
        ])
        
        with tab_lineas:
            st.markdown("### 📈 Evolución Cronológica de Publicaciones Científicas")
            prod_anual = df_filtrado['Year'].value_counts().sort_index().reset_index()
            prod_anual.columns = ['Año', 'Publicaciones']
            
            if not prod_anual.empty:
                fig_linea = px.line(
                    prod_anual, x='Año', y='Publicaciones',
                    markers=True, text='Publicaciones',
                    template="plotly_dark"
                )
                fig_linea.update_traces(line_color="#06b6d4", line_width=4, marker_size=10, textposition="top center")
                fig_linea.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#1f293d')
                )
                st.plotly_chart(fig_linea, use_container_width=True)
            else:
                st.warning("Rango temporal sin suficientes registros.")
                
        with tab_autores:
            st.markdown("### ✍️ Top 10 Investigadores con Mayor Índice de Citación")
            df_autores = obtener_autores_limpios(df_filtrado)
            
            if not df_autores.empty:
                fig_barras = px.bar(
                    df_autores, x='Citas Acumuladas', y='Autor',
                    orientation='h', template="plotly_dark",
                    color='Citas Acumuladas',
                    color_continuous_scale=['#1e293b', '#06b6d4']
                )
                fig_barras.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    yaxis={'categoryorder': 'total ascending', 'showgrid': False},
                    xaxis={'showgrid': True, 'gridcolor': '#1f293d'},
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig_barras, use_container_width=True)
            else:
                st.warning("Sin datos bibliográficos de citación.")
                
        with tab_contenido:
            st.markdown("### 🔍 Mapeo Semántico de Enfoques Preventivos en Abstracts")
            df_conceptos = extraer_conceptos_clave(df_filtrado)
            
            if not df_conceptos.empty:
                fig_treemap = px.treemap(
                    df_conceptos, path=['Concepto'], values='Frecuencia',
                    template="plotly_dark",
                    color='Frecuencia',
                    color_continuous_scale=['#0f172a', '#10b981']
                )
                fig_treemap.update_layout(paper_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
                st.plotly_chart(fig_treemap, use_container_width=True)
            else:
                st.warning("No se pudieron procesar los resúmenes académicos.")
                
        with tab_explorador:
            st.markdown("### 📋 Repositorio Integrado de Datos Crudos (df.head)")
            st.dataframe(
                df_filtrado[['Authors', 'Title', 'Year', 'Cited by', 'DOI']].sort_values(by='Cited by', ascending=False).reset_index(drop=True),
                use_container_width=True
            )
            
            csv_descarga = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Exportar subconjunto filtrado a CSV",
                data=csv_descarga,
                file_name=f"subconjunto_ia_salud_mental.csv",
                mime="text/csv"
            )
            
    except Exception as e:
        st.error(f"Error en la lectura del archivo estructurado: {e}")
else:
    st.warning("👋 Cargue el archivo 'scopus_export.csv' en la raíz de su repositorio para habilitar la interfaz.")
