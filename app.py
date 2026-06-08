import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import re
import numpy as np

# ══════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="🧠 IA y Salud Mental Juvenil | Grupo 05",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════
# CUSTOM CSS — DARK PURPLE / MENTAL HEALTH THEME
# ══════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,300;14..32,400;14..32,600;14..32,700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1117 100%);
    color: #e2e8f0;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f1117 0%, #161b22 100%) !important;
    border-right: 1px solid rgba(124,58,237,0.25);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown { color: #e6edf3 !important; }
[data-testid="stSidebar"] button p,
[data-testid="stSidebar"] a p,
[data-testid="stSidebar"] div[data-baseweb="select"] * {
    color: #a78bfa !important;
    font-weight: 600 !important;
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] caption { color: #8b949e !important; }
[data-testid="stSidebar"] details summary span p {
    color: #a78bfa !important;
    font-weight: 600;
}

/* Hero banner */
.hero-header {
    background: linear-gradient(135deg, rgba(76,29,149,0.92) 0%, rgba(30,27,75,0.95) 45%, rgba(13,17,23,0.98) 100%);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(124,58,237,0.35);
    border-radius: 28px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
}
.hero-header::before {
    content: '🧠';
    position: absolute;
    font-size: 300px;
    opacity: 0.03;
    bottom: -50px;
    right: -50px;
    pointer-events: none;
}
.hero-title {
    font-size: 2.1rem;
    font-weight: 700;
    background: linear-gradient(135deg, #a78bfa 0%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem 0;
    line-height: 1.2;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: #8b949e;
    margin: 0;
}
.hero-question {
    font-size: 0.92rem;
    color: #e6edf3;
    margin-top: 1rem;
    padding: 0.75rem 1rem;
    background: rgba(124,58,237,0.15);
    border-left: 4px solid #7c3aed;
    border-radius: 0 12px 12px 0;
    font-style: italic;
    line-height: 1.6;
}

/* Context box */
.context-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(167,139,250,0.05));
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    color: #e6edf3;
    line-height: 1.7;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #161b22 0%, #1a1f2e 100%);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 20px;
    padding: 1.3rem 1rem;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    transform: translateY(-4px);
    border-color: #a78bfa;
    box-shadow: 0 8px 24px rgba(124,58,237,0.25);
}
.kpi-number {
    font-size: 2.4rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(135deg, #a78bfa 0%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.kpi-label {
    font-size: 0.72rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-top: 0.4rem;
}
.kpi-sub {
    font-size: 0.78rem;
    color: #3fb950;
    margin-top: 0.2rem;
}

/* Section titles */
.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #e6edf3;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid rgba(124,58,237,0.3);
}

/* Highlight text */
.hl { color: #a78bfa; font-weight: 600; }

/* Alert badge */
.alert-badge {
    background: rgba(250,204,21,0.1);
    border-left: 3px solid #fbbf24;
    padding: 0.6rem 1rem;
    border-radius: 8px;
    font-size: 0.85rem;
    margin: 0.5rem 0;
    color: #e6edf3;
}

/* Insight box */
.insight-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 1rem;
}
.insight-item strong { color: #a78bfa; }
.insight-item p { font-size: 0.82rem; margin-top: 0.4rem; color: #8b949e; }

/* Footer */
.footer {
    text-align: center;
    color: #484f58;
    font-size: 0.78rem;
    padding: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# PLOTLY BASE THEME
# ══════════════════════════════════════════════════════════
BASE_LAYOUT = dict(
    paper_bgcolor="rgba(22,27,34,0)",
    plot_bgcolor="rgba(13,17,23,0.6)",
    font=dict(family="Inter", color="#8b949e", size=12),
    margin=dict(l=40, r=20, t=50, b=40),
    hoverlabel=dict(bgcolor="#161b22", font_size=12, font_family="Inter"),
    legend=dict(bgcolor="rgba(22,27,34,0.8)", bordercolor="#30363d", borderwidth=1),
)
PURPLE_SEQ   = ["#a78bfa", "#7c3aed", "#c4b5fd", "#6d28d9", "#ddd6fe", "#8b5cf6", "#ede9fe"]
PURPLE_SCALE = [[0, "#1a0a2e"], [0.5, "#7c3aed"], [1, "#c4b5fd"]]
GREEN_SCALE  = [[0, "#0d2818"], [0.5, "#238636"], [1, "#3fb950"]]

# ══════════════════════════════════════════════════════════
# DATA LOADING & CLEANING
# ══════════════════════════════════════════════════════════
GITHUB_RAW = (
    "https://raw.githubusercontent.com/Miniblank/PA3-GRUPO-5/main/scopus_export.csv"
)

def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Cited by"]    = pd.to_numeric(df.get("Cited by", 0), errors="coerce").fillna(0).astype(int)
    df["Year"]        = pd.to_numeric(df.get("Year"), errors="coerce")
    df               = df.dropna(subset=["Year"])
    df["Year"]        = df["Year"].astype(int)
    df["Authors"]     = df.get("Authors", pd.Series(dtype=str)).fillna("Sin autor")
    df["Abstract"]    = df.get("Abstract", pd.Series(dtype=str)).fillna("")
    df["Title"]       = df.get("Title", pd.Series(dtype=str)).fillna("Sin título")
    df["Document Type"] = df.get("Document Type", pd.Series(dtype=str)).fillna("No especificado")
    df["Source title"]  = df.get("Source title", pd.Series(dtype=str)).fillna("No especificada")
    df["Open Access"]   = df.get("Open Access", pd.Series(dtype=str)).fillna("No disponible")
    df["Authors_list"]  = df["Authors"].apply(
        lambda x: [a.strip() for a in re.split(r"[;,]+", str(x)) if a.strip()]
    )
    df["Is_OA"] = df["Open Access"].apply(
        lambda x: "Open Access" if isinstance(x, str) and "open access" in x.lower()
        else "Acceso Restringido"
    )
    return df

@st.cache_data(ttl=3600)
def load_github() -> pd.DataFrame:
    return clean_df(pd.read_csv(GITHUB_RAW))

# ══════════════════════════════════════════════════════════
# SIDEBAR — INFORMATION PANELS
# ══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🧠 Sobre el Dashboard")
    st.markdown("---")

    with st.expander("🔎 Pregunta de Investigación", expanded=True):
        st.markdown(
            "¿Cómo contribuye la investigación académica en **inteligencia artificial** "
            "a la **prevención de trastornos de salud mental** en **jóvenes** "
            "entre 2019 a la actualidad?"
        )

    with st.expander("📊 Métricas Analizadas", expanded=True):
        st.markdown(
            "- 🔢 **Volumen de publicaciones** por año\n"
            "- 🏆 **Autores más citados** en el campo\n"
            "- 🔑 **Palabras clave** en abstracts\n"
            "- 📈 **Tendencias de investigación** en IA aplicada"
        )

    with st.expander("📋 Fuente y Periodo", expanded=True):
        st.markdown(
            "- **Base de datos:** Scopus\n"
            "- **Rango:** 2019 – 2026\n"
            "- **Keywords:** Artificial Intelligence, Mental Health, Prevention, Youth"
        )
        st.link_button(
            "📁 Repositorio GitHub",
            "https://github.com/Miniblank/PA3-GRUPO-5",
            use_container_width=True,
        )

    st.markdown("---")
    uploaded_file = st.file_uploader("📂 Cargar CSV Scopus alternativo", type=["csv"])
    st.markdown("---")
    st.markdown("### ⚙️ Filtros de Análisis")

# ══════════════════════════════════════════════════════════
# LOAD DATA
# ══════════════════════════════════════════════════════════
if uploaded_file is not None:
    try:
        df_raw = clean_df(pd.read_csv(uploaded_file))
        st.sidebar.success("✅ Archivo CSV cargado correctamente")
    except Exception as e:
        st.sidebar.error(f"Error al parsear: {e}")
        df_raw = load_github()
else:
    try:
        df_raw = load_github()
    except Exception as e:
        st.error(
            f"⚠️ No se pudo cargar el dataset desde GitHub ({e}). "
            "Sube tu archivo CSV usando el panel izquierdo."
        )
        st.stop()

# ══════════════════════════════════════════════════════════
# SIDEBAR — DYNAMIC FILTERS  (after data is loaded)
# ══════════════════════════════════════════════════════════
with st.sidebar:
    all_years = sorted(df_raw["Year"].unique())
    year_range = st.slider(
        "📅 Rango de años",
        min_value=int(min(all_years)),
        max_value=int(max(all_years)),
        value=(int(min(all_years)), int(max(all_years))),
    )

    doc_options = ["Todos"] + sorted(df_raw["Document Type"].unique().tolist())
    selected_doc = st.selectbox("📄 Tipo de documento", doc_options)

    max_cites = max(1, int(df_raw["Cited by"].max()))
    min_cites = st.slider("⭐ Mínimo de citas", 0, max_cites, 0)

    search_kw = st.text_input(
        "🔍 Buscar en títulos / abstracts",
        placeholder="ej: depression, anxiety, nlp…",
    )

    st.markdown("---")
    st.caption("🧠 Scopus · UPCH · Grupo 05 · ML Fundamentos")

# ══════════════════════════════════════════════════════════
# APPLY FILTERS
# ══════════════════════════════════════════════════════════
df = df_raw[
    (df_raw["Year"]     >= year_range[0]) &
    (df_raw["Year"]     <= year_range[1]) &
    (df_raw["Cited by"] >= min_cites)
].copy()

if selected_doc != "Todos":
    df = df[df["Document Type"] == selected_doc]

if search_kw.strip():
    mask = (
        df["Title"].str.contains(search_kw, case=False, na=False) |
        df["Abstract"].str.contains(search_kw, case=False, na=False)
    )
    df = df[mask]

# ══════════════════════════════════════════════════════════
# ── HERO HEADER
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="hero-header">
  <div class="hero-title">🧠 Inteligencia Artificial &amp; Salud Mental Juvenil</div>
  <div class="hero-subtitle">
    🔬 Análisis Bibliométrico Avanzado · Scopus {year_range[0]}–{year_range[1]} · Prevención en Jóvenes · Grupo 05
  </div>
  <div class="hero-question">
    ❝ ¿Cómo contribuye la investigación académica en inteligencia artificial a la prevención
    de trastornos de salud mental en jóvenes entre 2019 a la actualidad? ❞
  </div>
</div>
""", unsafe_allow_html=True)

# ── Contexto
st.markdown("""
<div class="context-box">
    <strong style="color:#a78bfa;">🌐 Contexto de Investigación</strong><br>
    Los trastornos de salud mental afectan a <span class="hl">1 de cada 5 jóvenes</span> a nivel global.
    La inteligencia artificial ha emergido como herramienta clave para la detección temprana e intervención
    personalizada en condiciones como ansiedad, depresión y estrés en poblaciones de
    <span class="hl">hasta 25 años</span>. Este dashboard analiza la evolución y el impacto de esa
    investigación académica a nivel mundial.
    <div style="display:flex;gap:1rem;margin-top:1rem;flex-wrap:wrap;font-size:0.82rem;">
        <span style="background:rgba(124,58,237,0.2);padding:0.25rem 0.8rem;border-radius:20px;">🎯 Prevención temprana</span>
        <span style="background:rgba(63,185,80,0.2);padding:0.25rem 0.8rem;border-radius:20px;">🤖 IA en diagnóstico</span>
        <span style="background:rgba(250,204,21,0.15);padding:0.25rem 0.8rem;border-radius:20px;">👥 Población juvenil</span>
        <span style="background:rgba(167,139,250,0.15);padding:0.25rem 0.8rem;border-radius:20px;">🌎 Investigación global</span>
    </div>
</div>
""", unsafe_allow_html=True)

if len(df) == 0:
    st.warning(
        "⚠️ Ningún artículo coincide con los filtros actuales. "
        "Ajusta el rango de años, tipo de documento o mínimo de citas."
    )
    st.stop()

# ══════════════════════════════════════════════════════════
# ── KPI CARDS
# ══════════════════════════════════════════════════════════
n_art    = len(df)
n_citas  = int(df["Cited by"].sum())
avg_cit  = round(df["Cited by"].mean(), 1)
max_cit  = int(df["Cited by"].max())
n_rev    = df["Source title"].nunique()
n_types  = df["Document Type"].nunique()

cols_kpi = st.columns(6)
for col, num, label, sub in zip(
    cols_kpi,
    [n_art,  n_citas, avg_cit, max_cit,  n_rev,      n_types],
    ["📚 Artículos","📊 Citas Totales","⭐ Citas Prom.","🏆 Máx. Citas","📖 Fuentes","🗂️ Tipos Doc."],
    ["en el período analizado","impacto global","por artículo","artículo más influyente","revistas y conferencias","diversidad documental"],
):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-number">{num}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── SECCIÓN 1 · EVOLUCIÓN TEMPORAL
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📈 Evolución Temporal de la Investigación</div>', unsafe_allow_html=True)

year_agg = (
    df.groupby("Year")
      .agg(Artículos=("Title","count"), Citas=("Cited by","sum"))
      .reset_index()
)

fig_yr = make_subplots(specs=[[{"secondary_y": True}]])
fig_yr.add_trace(
    go.Bar(x=year_agg["Year"], y=year_agg["Artículos"],
           name="📚 Publicaciones", marker_color="#7c3aed", opacity=0.85),
    secondary_y=False,
)
fig_yr.add_trace(
    go.Scatter(x=year_agg["Year"], y=year_agg["Citas"],
               name="📊 Citas totales", mode="lines+markers",
               line=dict(color="#c4b5fd", width=2.5),
               marker=dict(size=9, color="#a78bfa", symbol="diamond")),
    secondary_y=True,
)
fig_yr.update_layout(
    **BASE_LAYOUT,
    title=dict(
        text="🧠 Crecimiento de la Investigación en IA para Salud Mental Juvenil",
        font=dict(color="#e6edf3", size=14),
    ),
    hovermode="x unified",
)
fig_yr.update_xaxes(gridcolor="#21262d", title_text="Año de publicación", dtick=1)
fig_yr.update_yaxes(title_text="📄 Publicaciones", secondary_y=False, gridcolor="#21262d")
fig_yr.update_yaxes(title_text="📊 Citas Totales",  secondary_y=True,  gridcolor="#21262d")
st.plotly_chart(fig_yr, use_container_width=True)

# ══════════════════════════════════════════════════════════
# ── SECCIÓN 2 · TOP ARTÍCULOS + TOP AUTORES
# ══════════════════════════════════════════════════════════
col_2a, col_2b = st.columns(2)

# --- Top artículos ---
with col_2a:
    st.markdown('<div class="section-title">🏆 Artículos Más Citados</div>', unsafe_allow_html=True)
    top_n = st.slider("Mostrar top N artículos", 5, min(20, n_art), 10, key="slider_arts")
    top_arts = (
        df.nlargest(top_n, "Cited by")[["Title","Year","Cited by","Authors"]]
          .copy()
    )
    top_arts["Título corto"] = top_arts["Title"].str[:75] + "…"

    fig_art = px.bar(
        top_arts.sort_values("Cited by"),
        x="Cited by", y="Título corto", orientation="h",
        color="Cited by", color_continuous_scale=PURPLE_SCALE,
        hover_data={"Year": True, "Authors": True},
    )
    fig_art.update_layout(
        **BASE_LAYOUT,
        height=max(350, top_n * 40),
        title=dict(text=f"🏅 Top {top_n} investigaciones más influyentes",
                   font=dict(color="#e6edf3", size=13)),
        coloraxis_showscale=False,
    )
    fig_art.update_xaxes(gridcolor="#21262d", title="Número de citas")
    fig_art.update_yaxes(gridcolor="#21262d", color="#e6edf3", automargin=True, showgrid=False)
    st.plotly_chart(fig_art, use_container_width=True)

# --- Top autores ---
with col_2b:
    st.markdown('<div class="section-title">👩‍🔬 Investigadores Líderes</div>', unsafe_allow_html=True)
    author_cites: dict = {}
    for _, row in df.iterrows():
        for a in row["Authors_list"]:
            author_cites[a] = author_cites.get(a, 0) + int(row["Cited by"])

    top_aut = (
        pd.DataFrame(list(author_cites.items()), columns=["Investigador", "Citas"])
          .sort_values("Citas", ascending=False)
          .head(12)
    )

    fig_aut = px.bar(
        top_aut.sort_values("Citas"),
        x="Citas", y="Investigador", orientation="h",
        color="Citas", color_continuous_scale=GREEN_SCALE,
    )
    fig_aut.update_layout(
        **BASE_LAYOUT,
        height=450,
        title=dict(text="🏅 Top 12 investigadores por citas acumuladas",
                   font=dict(color="#e6edf3", size=13)),
        coloraxis_showscale=False,
    )
    fig_aut.update_xaxes(gridcolor="#21262d", title="Citas acumuladas")
    fig_aut.update_yaxes(gridcolor="#21262d", color="#e6edf3", automargin=True, showgrid=False)
    st.plotly_chart(fig_aut, use_container_width=True)

# ══════════════════════════════════════════════════════════
# ── SECCIÓN 3 · TECNOLOGÍAS DE IA
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🤖 Tecnologías y Enfoques de IA en Salud Mental Juvenil</div>', unsafe_allow_html=True)

AI_GROUPS = {
    "🧠 Deep Learning / Redes Neuronales": ["deep learning","neural network","cnn","lstm","transformer","bert","rnn"],
    "📊 Machine Learning Clásico":          ["machine learning","random forest","svm","xgboost","gradient boosting","naive bayes","logistic"],
    "💬 NLP / Análisis de Texto":           ["natural language","nlp","text analysis","sentiment","chatbot","language model","gpt"],
    "📱 Tecnología Digital / Apps":         ["mobile","smartphone","digital","app","wearable","iot","sensor"],
    "🎯 Detección Temprana / Cribado":      ["early detection","early identification","screening","prediction","risk assessment"],
    "🔬 Intervención y Tratamiento":        ["intervention","treatment","therapy","cognitive behavioral","cbt","support"],
}

kw_counts = {}
for grp, terms in AI_GROUPS.items():
    mask = pd.Series([False] * len(df), index=df.index)
    for t in terms:
        mask |= (df["Abstract"].str.contains(t, case=False, na=False) |
                 df["Title"].str.contains(t, case=False, na=False))
    kw_counts[grp] = int(mask.sum())

kw_df = (
    pd.DataFrame(list(kw_counts.items()), columns=["Tecnología / Enfoque", "N° Artículos"])
      .sort_values("N° Artículos", ascending=False)
)

fig_kw = px.bar(
    kw_df, x="Tecnología / Enfoque", y="N° Artículos",
    color="N° Artículos", color_continuous_scale=PURPLE_SCALE,
    text="N° Artículos",
)
fig_kw.update_layout(
    **BASE_LAYOUT,
    title=dict(text="🤖 Presencia de tecnologías de IA en los artículos del corpus",
               font=dict(color="#e6edf3", size=14)),
    coloraxis_showscale=False,
)
fig_kw.update_xaxes(tickangle=-18, tickfont=dict(size=11), gridcolor="#21262d")
fig_kw.update_yaxes(gridcolor="#21262d")
fig_kw.update_traces(textposition="outside", textfont=dict(color="#a78bfa", size=12))
st.plotly_chart(fig_kw, use_container_width=True)

# ══════════════════════════════════════════════════════════
# ── SECCIÓN 4 · TREEMAP + DONUT TIPO DOCUMENTO
# ══════════════════════════════════════════════════════════
col_4a, col_4b = st.columns([1.6, 1])

STOPWORDS = {
    "the","and","in","a","for","with","using","based","on","an","by","from",
    "to","is","are","at","as","or","into","via","its","their","that","this",
    "be","has","have","were","was","not","they","of","study","among",
}

with col_4a:
    st.markdown('<div class="section-title">🔑 Mapa de Conceptos en Títulos</div>', unsafe_allow_html=True)
    words_all: list = []
    for title in df["Title"].dropna():
        ws = re.findall(r"\b[a-zA-Z]{4,}\b", title.lower())
        words_all.extend([w for w in ws if w not in STOPWORDS])

    wf_df = pd.DataFrame(Counter(words_all).most_common(35), columns=["Término","Frecuencia"])

    fig_tree = px.treemap(
        wf_df, path=["Término"], values="Frecuencia",
        color="Frecuencia", color_continuous_scale=PURPLE_SCALE,
    )
    fig_tree.update_layout(
        paper_bgcolor="rgba(22,27,34,0)",
        font=dict(family="Inter", color="#e6edf3", size=12),
        margin=dict(l=5, r=5, t=45, b=5),
        height=400,
        title=dict(text="🔤 Términos más frecuentes en los títulos",
                   font=dict(color="#e6edf3", size=14)),
    )
    fig_tree.update_traces(textfont=dict(color="white", size=13), textinfo="label+value")
    st.plotly_chart(fig_tree, use_container_width=True)

with col_4b:
    st.markdown('<div class="section-title">📄 Tipos de Documento</div>', unsafe_allow_html=True)
    doc_cnt = df["Document Type"].value_counts().reset_index()
    doc_cnt.columns = ["Tipo","Cantidad"]

    fig_pie = px.pie(
        doc_cnt, names="Tipo", values="Cantidad",
        color_discrete_sequence=PURPLE_SEQ, hole=0.48,
    )
    fig_pie.update_layout(
        paper_bgcolor="rgba(22,27,34,0)",
        font=dict(family="Inter", color="#e6edf3", size=12),
        margin=dict(l=5, r=5, t=45, b=5),
        height=400,
        legend=dict(bgcolor="rgba(22,27,34,0.8)", font=dict(color="#e6edf3", size=11)),
        title=dict(text="📊 Distribución por tipo de documento",
                   font=dict(color="#e6edf3", size=14)),
    )
    fig_pie.update_traces(
        textposition="inside",
        textfont=dict(color="white", size=11),
        pull=[0.04]*len(doc_cnt),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ══════════════════════════════════════════════════════════
# ── SECCIÓN 5 · OPEN ACCESS + EVOLUCIÓN OA POR AÑO
# ══════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🔓 Acceso Abierto en la Investigación</div>', unsafe_allow_html=True)
col_5a, col_5b = st.columns([1, 2])

with col_5a:
    oa_cnt = df["Is_OA"].value_counts().reset_index()
    oa_cnt.columns = ["Tipo","N"]

    fig_oa = px.pie(
        oa_cnt, names="Tipo", values="N",
        color_discrete_sequence=["#a78bfa","#2d333b"], hole=0.52,
    )
    fig_oa.update_layout(
        paper_bgcolor="rgba(22,27,34,0)",
        font=dict(family="Inter", color="#e6edf3", size=12),
        margin=dict(l=5, r=5, t=45, b=5),
        height=320,
        legend=dict(bgcolor="rgba(22,27,34,0.8)", font=dict(color="#e6edf3")),
        title=dict(text="🔓 Open Access vs. Restringido",
                   font=dict(color="#e6edf3", size=14)),
    )
    fig_oa.update_traces(textfont=dict(color="white"))
    st.plotly_chart(fig_oa, use_container_width=True)

with col_5b:
    oa_yr = df.groupby(["Year","Is_OA"]).size().reset_index(name="N")
    fig_oa_yr = px.bar(
        oa_yr, x="Year", y="N", color="Is_OA", barmode="stack",
        color_discrete_map={"Open Access":"#a78bfa","Acceso Restringido":"#2d333b"},
    )
    fig_oa_yr.update_layout(
        **BASE_LAYOUT,
        height=320,
        title=dict(text="📅 Evolución del Acceso Abierto por Año",
                   font=dict(color="#e6edf3", size=14)),
        legend=dict(bgcolor="rgba(22,27,34,0.8)", font=dict(color="#e6edf3")),
    )
    fig_oa_yr.update_xaxes(gridcolor="#21262d", title="Año", dtick=1)
    fig_oa_yr.update_yaxes(gridcolor="#21262d", title="Artículos")
    st.plotly_chart(fig_oa_yr, use_container_width=True)

# ══════════════════════════════════════════════════════════
# ── ALERTA DE SALUD PÚBLICA
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="alert-badge">
    ⚠️ <strong>Dato OMS:</strong> Cerca del 50 % de los trastornos mentales comienzan antes de los 14 años,
    y la mayoría no reciben tratamiento a tiempo. La IA ofrece nuevas vías de detección y prevención
    accesibles y escalables para jóvenes en todo el mundo.
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── SECCIÓN 6 · HALLAZGOS CLAVE
# ══════════════════════════════════════════════════════════
st.markdown("""
<div class="context-box" style="margin-top:1.5rem;">
    <strong style="color:#a78bfa;">💡 Hallazgos Clave del Análisis Bibliométrico</strong>
    <div class="insight-grid" style="margin-top:1rem;">
        <div class="insight-item">
            <strong>📈 Crecimiento acelerado</strong>
            <p>La producción científica en IA aplicada a salud mental juvenil creció de forma sostenida,
            concentrando el mayor volumen entre 2024 y 2026, reflejando el interés académico global creciente.</p>
        </div>
        <div class="insight-item">
            <strong>🤖 Tecnologías dominantes</strong>
            <p>El Deep Learning y el Machine Learning lideran las metodologías empleadas,
            seguidos de herramientas NLP para el análisis del lenguaje como señal de riesgo en jóvenes.</p>
        </div>
        <div class="insight-item">
            <strong>🎯 Enfoque preventivo</strong>
            <p>Las investigaciones se orientan cada vez más a la detección temprana de señales de ansiedad
            y depresión, abriendo vías de intervención preventiva digital y escalable.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# ── TABLA COMPLETA (COLLAPSIBLE)
# ══════════════════════════════════════════════════════════
with st.expander("📋 Ver tabla completa de artículos filtrados", expanded=False):
    display_cols = ["Year","Title","Authors","Source title","Cited by","Document Type"]
    csv_out = (
        df[display_cols]
          .sort_values("Cited by", ascending=False)
          .reset_index(drop=True)
          .to_csv(index=False)
    )
    col_dl, _ = st.columns([1, 4])
    with col_dl:
        st.download_button(
            "📥 Exportar CSV",
            data=csv_out,
            file_name=f"ia_salud_mental_{year_range[0]}_{year_range[1]}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    st.dataframe(
        df[display_cols].sort_values("Cited by", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=420,
        column_config={
            "Year":          st.column_config.NumberColumn("Año",   format="%d"),
            "Cited by":      st.column_config.NumberColumn("Citas", format="%d"),
            "Title":         st.column_config.TextColumn("Título",  width="large"),
            "Authors":       st.column_config.TextColumn("Autores", width="medium"),
            "Source title":  st.column_config.TextColumn("Fuente"),
            "Document Type": st.column_config.TextColumn("Tipo"),
        },
    )

# ══════════════════════════════════════════════════════════
# ── FOOTER
# ══════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div class="footer">
    <strong>🧠 Dashboard Bibliométrico — IA &amp; Salud Mental Juvenil</strong><br>
    Grupo 05 · Fundamentos de Machine Learning · Datos: Scopus (2019–2026)<br>
    <span style="color:#a78bfa;">🎯 Misión:</span>
    Analizar la evidencia académica sobre IA para la prevención de trastornos mentales en jóvenes<br>
    <span style="font-size:0.7rem;">🔬 Stack: Streamlit · Plotly · Pandas · Python</span>
</div>
""", unsafe_allow_html=True)
