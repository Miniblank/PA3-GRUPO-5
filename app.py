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
# DISEÑO CSS - INTERFAZ PREMIUM CLÍNICA DARK
# ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0a0e17 0%, #0d1117 100%);
    color: #e2e8f0;
}

/* Barra Lateral Estilizada con Alto Contraste */
[data-testid="stSidebar"] {
    background: #0f111a !important;
    border-right: 1px solid #1f2433;
}

/* Tarjetas KPIs con Efecto Glassmorphic */
.kpi-container {
    background: rgba(22, 27, 34, 0.6);
    border: 1px solid #21262d;
    border-radius: 6px;
    padding: 1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.kpi-label {
    color: #8b949e;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.kpi-val {
    color: #58a6ff;
    font-size: 1.6rem;
    font-weight: 700;
    margin-top: 0.2rem;
}

/* Pestañas de Navegación */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background-color: transparent;
    border-bottom: 1px solid #21262d;
}

.stTabs [data-baseweb="tab"] {
    background-color: #161b22 !important;
    border: 1px solid #21262d !important;
    border-radius: 6px 6px 0px 0px !important;
    padding: 8px 16px !important;
    color: #8b949e !important;
}

.stTabs [aria-selected="true"] {
    background-color: #21262d !important;
    color: #58a6ff !important;
    border-bottom: 2px solid #58a6ff !important;
}
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────
# FUNCIONES DE PROCESAMIENTO DE DATOS
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
                
    df_res = pd.DataFrame(conteo_autores.items(), columns=['Autor', 'Citas'])
    return df_res.sort_values(by='Citas', ascending=False).head(10)

def extraer_conceptos_clave(df):
    texto = " ".join(df['Abstract'].dropna().astype(str).str.lower())
    palabras = re.findall(r'\b[a-z]{5,}\b', texto)
    stop_words = {'with', 'that', 'this', 'from', 'their', 'were', 'also', 'been', 'which', 
                  'study', 'research', 'using', 'used', 'patients', 'health', 'mental', 
                  'artificial', 'intelligence', 'analysis', 'data', 'results', 'based', 'clinical'}
    filtradas = [p for p in palabras if p not in stop_words]
    return pd.DataFrame(Counter(filtradas).most_common(10), columns=['Concepto', 'Frecuencia'])

# ────────────────────────────────────────────────────────────
# CONFIGURACIÓN ESTRUCTURAL DE LA BARRA LATERAL (SEGÚN REQUERIMIENTO)
# ────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="background-color: #161b22; padding: 1rem; border-radius: 6px; border: 1px solid #21262d; margin-bottom: 1rem;">
    <h3 style="color: #58a6ff; font-size: 1.1rem; margin: 0 0 0.5rem 0; font-weight:600;">🧠 GRUPO 05 · BIENESTAR</h3>
    <p style="color: #8b949e; font-size: 0.8rem; margin: 0 0 0.4rem 0;"><strong>Curso:</strong> Fundamentos de ML</p>
    <p style="color: #8b949e; font-size: 0.8rem; margin: 0;"><strong>Área:</strong> Salud Mental Juvenil</p>
</div>

<div style="background-color: #161b22; padding: 1rem; border-radius: 6px; border: 1px solid #21262d; margin-bottom: 1rem;">
    <h4 style="color: #58a6ff; font-size: 0.9rem; margin: 0 0 0.4rem 0; font-weight:600;">🎯 PREGUNTA EJE</h4>
    <p style="color: #c9d1d9; font-size: 0.8rem; line-height: 1.4; margin: 0;">
        ¿Cómo contribuye la investigación académica en inteligencia artificial a la prevención de trastornos de salud mental en jóvenes desde 2019 a la actualidad?
    </p>
</div>
""", unsafe_allow_html=True)

# Filtros y subida de archivos en la barra lateral
archivo_defecto = "scopus_export.csv"
uploaded_file = st.sidebar.file_uploader("📂 Cargar base Scopus alternativo (CSV)", type=["csv"])
ruta_final = uploaded_file if uploaded_file is not None else (archivo_defecto if os.path.exists(archivo_defecto) else None)

if ruta_final is not None:
    try:
        df_base = procesar_datos(ruta_final)
        
        min_year = int(df_base['Year'].min()) if not pd.isna(df_base['Year'].min()) else 2019
        max_year = int(df_base['Year'].max()) if not pd.isna(df_base['Year'].max()) else 2026
        
        st.sidebar.markdown("### 🕒 Filtros Activos")
        rango_anios = st.sidebar.slider("Horizonte Cronológico", min_year, max_year, (2019, max_year))
        
        df_filtrado = df_base[(df_base['Year'] >= rango_anios[0]) & (df_base['Year'] <= rango_anios[1])]
        
        # ────────────────────────────────────────────────────────────
        # MARCO DE TRABAJO PRINCIPAL (DASHBOARD PREMIUM)
        # ────────────────────────────────────────────────────────────
        st.title("🧠 Dashboard Científico: Inteligencia Artificial en Salud Mental")
        st.caption("Plataforma interactiva de analítica bibliométrica basada en metadatos indexados de Scopus")
        st.markdown("---")
        
        # Grid superior de KPIs limpios
        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(f'<div class="kpi-container"><div class="kpi-label">🔬 Volumen de Literatura</div><div class="kpi-value">{len(df_filtrado)} Docs</div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="kpi-container"><div class="kpi-label" style="color:#3fb950;">💬 Citas Acumuladas</div><div class="kpi-value" style="color:#f8fafc;">{int(df_filtrado["Cited by"].sum())} Referencias</div></div>', unsafe_allow_html=True)
        with k3:
            st.markdown(f'<div class="kpi-container"><div class="kpi-label" style="color:#a5d6ff;">🎯 Ratio de Citación</div><div class="kpi-value" style="color:#f8fafc;">{round(df_filtrado["Cited by"].mean(), 2)} c/u</div></div>', unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Pestañas de visualización avanzada
        t_linea, t_autores, t_semantica, t_datos = st.tabs([
            "📈 Tendencias Temporales", 
            "✍️ Impacto de Investigadores", 
            "🔍 Análisis de Resúmenes", 
            "📋 Matriz de Datos"
        ])
        
        with t_linea:
            st.markdown("### 📈 Evolución Cronológica de la Producción Científica")
            prod_anual = df_filtrado['Year'].value_counts().sort_index().reset_index()
            prod_anual.columns = ['Año', 'Cantidad']
            
            if not prod_anual.empty:
                # Réplica exacta del gráfico premium con relleno fluido de área de Plotly
                fig_linea = px.line(
                    prod_anual, x='Año', y='Cantidad',
                    markers=True, text='Cantidad',
                    template="plotly_dark"
                )
                fig_linea.update_traces(
                    line_color="#58a6ff", 
                    line_width=3, 
                    marker_size=8, 
                    marker_color="#f8fafc",
                    fill='tozeroy', 
                    fillcolor='rgba(88, 166, 255, 0.1)',
                    textposition="top center"
                )
                fig_linea.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False, tickmode='linear'),
                    yaxis=dict(showgrid=True, gridcolor='#21262d'),
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_linea, use_container_width=True, config={'displayModeBar': False})
            else:
                st.warning("No hay suficientes registros en este rango.")
                
        with t_autores:
            st.markdown("### ✍️ Top 10 Investigadores con Mayor Nivel de Citación")
            df_autores = obtener_autores_limpios(df_filtrado)
            
            if not df_autores.empty:
                # Gráfico horizontal pulido con gradiente moderno
                fig_barras = px.bar(
                    df_autores, x='Citas', y='Autor',
                    orientation='h', template="plotly_dark",
                    color='Citas',
                    color_continuous_scale=['#161b22', '#58a6ff']
                )
                fig_barras.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    yaxis={'categoryorder': 'total ascending', 'showgrid': False},
                    xaxis={'showgrid': True, 'gridcolor': '#21262d'},
                    coloraxis_showscale=False,
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig_barras, use_container_width=True, config={'displayModeBar': False})
            else:
                st.warning("Sin datos de referencias bibliográficas.")
                
        with t_semantica:
            st.markdown("### 🔍 Palabras Clave más Frecuentes en Resúmenes Académicos")
            df_conceptos = extraer_conceptos_clave(df_filtrado)
            
            if not df_conceptos.empty:
                fig_treemap = px.treemap(
                    df_conceptos, path=['Concepto'], values='Frecuencia',
                    template="plotly_dark",
                    color='Frecuencia',
                    color_continuous_scale=['#161b22', '#3fb950']
                )
                fig_treemap.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    coloraxis_showscale=False,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                st.plotly_chart(fig_treemap, use_container_width=True, config={'displayModeBar': False})
            else:
                st.warning("No se pudieron procesar los resúmenes científicos.")
                
        with t_datos:
            st.markdown("### 📋 Repositorio Integrado de Datos Crudos (df.head)")
            st.dataframe(
                df_filtrado[['Authors', 'Title', 'Year', 'Cited by', 'DOI']].sort_values(by='Cited by', ascending=False).reset_index(drop=True),
                use_container_width=True
            )
            
            # Botón de descarga corporativo
            csv_descarga = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Subconjunto de Datos (CSV)",
                data=csv_descarga,
                file_name="analisis_ia_salud_mental_filtrado.csv",
                mime="text/csv"
            )
            
    except Exception as e:
        st.error(f"Error técnico durante el procesamiento del archivo plano: {e}")
else:
    st.warning("👋 El sistema está listo. Por favor, asegúrese de añadir 'scopus_export.csv' en la raíz de su repositorio o cárguelo desde el panel izquierdo.")
