import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Superinversores | BQuant Finance",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Instrument+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #07070d;
    --bg-card: #0e0e16;
    --bg-elevated: #13131d;
    --bg-hover: #1a1a28;
    --border: rgba(255,255,255,0.06);
    --border-bright: rgba(255,255,255,0.12);
    --text: #eaeaf0;
    --text-2: #9090a8;
    --text-3: #505068;
    --accent: #6366f1;
    --accent-soft: rgba(99,102,241,0.12);
    --green: #22c55e;
    --blue: #3b82f6;
    --red: #ef4444;
    --amber: #f59e0b;
}

.main { background: var(--bg) !important; }
.block-container { padding: 1rem 2rem 2rem !important; max-width: 1800px !important; }
header[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] { display: none !important; }
#MainMenu, footer, div[data-testid="stToolbar"], div[data-testid="stDecoration"] { display: none !important; }

html, body, [class*="css"] {
    font-family: 'Instrument Sans', sans-serif !important;
    color: var(--text) !important;
}

/* ── Animated gradient strip ── */
.gradient-strip {
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--green), var(--blue), var(--amber), var(--red), var(--accent));
    background-size: 300% 100%;
    animation: strip-slide 8s linear infinite;
    border-radius: 0 0 4px 4px;
    margin: -1rem -2rem 1rem -2rem;
}
@keyframes strip-slide {
    0% { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

/* ── Header ── */
.header-row {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.2rem;
}
.header-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    color: var(--text);
    line-height: 1;
}
.header-title .accent-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: var(--accent);
    border-radius: 2px;
    margin-right: 0.5rem;
    box-shadow: 0 0 16px rgba(99,102,241,0.6);
    vertical-align: middle;
}
.header-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.67rem;
    color: var(--text-3);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.35rem;
}
.header-brand {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-3);
    text-align: right;
    line-height: 1.6;
}
.header-brand a {
    color: var(--accent) !important;
    text-decoration: none !important;
    font-weight: 500;
}

/* ── Metric Cards ── */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.6rem;
    margin-bottom: 1.2rem;
}
.m-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease;
}
.m-card:hover {
    border-color: var(--border-bright);
    transform: translateY(-1px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}
.m-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    border-radius: 12px 12px 0 0;
}
.m-card.c-accent::before { background: var(--accent); }
.m-card.c-green::before { background: var(--green); }
.m-card.c-blue::before { background: var(--blue); }
.m-card.c-amber::before { background: var(--amber); }
.m-card.c-red::before { background: var(--red); }
.m-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.58rem;
    color: var(--text-3);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.4rem;
}
.m-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
    letter-spacing: -0.03em;
}
.m-delta {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    margin-top: 0.3rem;
    letter-spacing: 0.03em;
}
.m-delta.green { color: var(--green); }
.m-delta.red { color: var(--red); }
.m-delta.amber { color: var(--amber); }
.m-delta.blue { color: var(--blue); }
.m-delta.accent { color: var(--accent); }

/* ── Controls ── */
.stRadio > div { gap: 0.15rem !important; flex-direction: row !important; }
.stRadio > label { display: none !important; }
div[data-baseweb="radio"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.74rem !important;
    color: var(--text-2) !important;
    padding: 0.3rem 0.65rem !important;
    margin: 0 !important;
    background: transparent !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    transition: all 0.2s ease !important;
}
div[data-baseweb="radio"] label:hover {
    background: var(--bg-hover) !important;
    border-color: var(--border-bright) !important;
}
div[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}
div[data-baseweb="tag"] {
    background: var(--accent-soft) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 6px !important;
}

/* ── Chart container ── */
div[data-testid="stPlotlyChart"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 0.4rem;
    transition: all 0.3s ease;
}
div[data-testid="stPlotlyChart"]:hover {
    border-color: rgba(99,102,241,0.25);
    box-shadow: 0 0 40px rgba(99,102,241,0.06);
}

/* ── Legend bar ── */
.legend-bar {
    display: flex;
    gap: 1.5rem;
    justify-content: center;
    align-items: center;
    padding: 0.6rem 0;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-3);
}
.legend-bar .dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 2px;
    margin-right: 0.3rem;
    vertical-align: middle;
}

/* ── Section headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin: 1.5rem 0 0.8rem;
}
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text);
    white-space: nowrap;
    letter-spacing: -0.01em;
}
.section-line { flex: 1; height: 1px; background: var(--border); }
.section-badge {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    color: var(--text-3);
    background: var(--bg-elevated);
    border: 1px solid var(--border);
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    white-space: nowrap;
}

/* ── Toggle (color mode) ── */
.toggle-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin: 0.4rem 0 0.2rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-3);
}

/* ── Data table ── */
div[data-testid="stDataFrame"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* ── Footer ── */
.footer-bar {
    text-align: center;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid var(--border);
    margin-top: 1.5rem;
}
.footer-text {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-3);
    letter-spacing: 0.05em;
}
.footer-text a { color: var(--accent) !important; text-decoration: none; }

@media (max-width: 900px) {
    .metrics-grid { grid-template-columns: repeat(3, 1fr); }
    .header-title { font-size: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# DATA — real schema
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv('dataroma_holdings_complete.csv')

    # % of Portfolio already float64, Shares already int64 — just ensure clean
    df['% of Portfolio'] = pd.to_numeric(df['% of Portfolio'], errors='coerce')
    df['Shares'] = pd.to_numeric(df['Shares'], errors='coerce')

    # Parse Value (string like "$1,234,567")
    if 'Value' in df.columns:
        df['Value_Clean'] = df['Value'].astype(str).str.replace(r'[$,]', '', regex=True)
        df['Value_Clean'] = pd.to_numeric(df['Value_Clean'], errors='coerce')

    # Parse +/-Reported Price (string like "-17.94%")
    if '+/-Reported Price' in df.columns:
        df['Performance'] = df['+/-Reported Price'].astype(str).str.replace(r'[%,]', '', regex=True)
        df['Performance'] = pd.to_numeric(df['Performance'], errors='coerce')
    else:
        df['Performance'] = 0.0

    # Parse 52-week range
    for col in ['52Week Low', '52Week High', 'Current Price']:
        if col in df.columns:
            df[col + '_Num'] = df[col].astype(str).str.replace(r'[$,]', '', regex=True)
            df[col + '_Num'] = pd.to_numeric(df[col + '_Num'], errors='coerce')

    # Activity classification
    df['Activity_Type'] = df['RecentActivity'].apply(lambda x:
        'Mantener' if pd.isna(x) or str(x).strip() == 'NaN' else
        'Compra' if str(x).strip() == 'Buy' else
        'Añadir' if 'Add' in str(x) else
        'Reducir' if 'Reduce' in str(x) else 'Mantener')

    # Extract ticker and company name
    df['Ticker'] = df['Stock'].apply(lambda x: x.split(' - ')[0].strip() if pd.notna(x) and ' - ' in str(x) else str(x).strip())
    df['Company'] = df['Stock'].apply(lambda x: x.split(' - ')[1].strip() if pd.notna(x) and ' - ' in str(x) else str(x).strip())

    return df

df = load_data()


# ═══════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="gradient-strip"></div>', unsafe_allow_html=True)

n_inv = df['Investor'].nunique()
n_stk = df['Ticker'].nunique()

st.markdown(f"""
<div class="header-row">
    <div>
        <div class="header-title"><span class="accent-dot"></span>Superinversores</div>
        <div class="header-sub">{n_inv} inversores legendarios · {n_stk:,} acciones · Análisis visual</div>
    </div>
    <div class="header-brand">
        por <a href="https://x.com/Gsnchez" target="_blank">@Gsnchez</a><br>
        <a href="https://bquantfinance.com" target="_blank">BQuant Finance</a>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# METRICS
# ═══════════════════════════════════════════════════════════════
aum = df['Value_Clean'].sum() / 1e9
avg_pos = len(df) / n_inv if n_inv else 0

concs = []
for inv in df['Investor'].unique():
    inv_df = df[df['Investor'] == inv]
    concs.append(inv_df.nlargest(5, '% of Portfolio')['% of Portfolio'].sum())
avg_conc = np.mean(concs) if concs else 0

buy_pct = (df['Activity_Type'].isin(['Compra', 'Añadir'])).sum() / len(df) * 100 if len(df) else 0
buy_color = 'green' if buy_pct > 50 else 'red'
buy_label = 'Alcista' if buy_pct > 50 else 'Bajista'

# Average performance across all holdings
avg_perf = df['Performance'].dropna().mean()
perf_color = 'green' if avg_perf > 0 else 'red'
perf_sign = '+' if avg_perf > 0 else ''

st.markdown(f"""
<div class="metrics-grid">
    <div class="m-card c-accent">
        <div class="m-label">Inversores</div>
        <div class="m-value">{n_inv}</div>
        <div class="m-delta accent">Legendarios</div>
    </div>
    <div class="m-card c-blue">
        <div class="m-label">Acciones Únicas</div>
        <div class="m-value">{n_stk:,}</div>
        <div class="m-delta blue">Universo completo</div>
    </div>
    <div class="m-card c-green">
        <div class="m-label">AUM Total</div>
        <div class="m-value">${aum:,.0f}B</div>
        <div class="m-delta green">Valor agregado</div>
    </div>
    <div class="m-card c-amber">
        <div class="m-label">Conc. Top 5</div>
        <div class="m-value">{avg_conc:.1f}%</div>
        <div class="m-delta amber">Promedio</div>
    </div>
    <div class="m-card c-{buy_color}">
        <div class="m-label">Ratio Compra</div>
        <div class="m-value">{buy_pct:.0f}%</div>
        <div class="m-delta {buy_color}">{buy_label}</div>
    </div>
    <div class="m-card c-{perf_color}">
        <div class="m-label">Rendimiento Medio</div>
        <div class="m-value">{perf_sign}{avg_perf:.1f}%</div>
        <div class="m-delta {perf_color}">vs Precio Reportado</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# CONTROLS
# ═══════════════════════════════════════════════════════════════
c1, c2, c3 = st.columns([1.2, 2.8, 1.0])

with c1:
    scope = st.radio("s", ["Top 5", "Top 10", "Top 20", "Todos"], index=1, horizontal=True, label_visibility="collapsed")

with c2:
    ranked = df.groupby('Investor')['Value_Clean'].sum().sort_values(ascending=False)
    if scope == "Top 5":
        defaults = ranked.head(5).index.tolist()
    elif scope == "Top 10":
        defaults = ranked.head(10).index.tolist()
    elif scope == "Top 20":
        defaults = ranked.head(20).index.tolist()
    else:
        defaults = sorted(df['Investor'].unique())
    selected = st.multiselect("i", sorted(df['Investor'].unique()), default=defaults, label_visibility="collapsed")

with c3:
    threshold = st.radio("t", ["Top 80%", "Top 90%", "Todas"], index=1, horizontal=True, label_visibility="collapsed")

if not selected:
    st.warning("Selecciona al menos un inversor.")
    st.stop()

# Color mode toggle
c_mode_1, c_mode_2 = st.columns([1, 3])
with c_mode_1:
    color_mode = st.radio("Color del mapa", ["Actividad reciente", "Rendimiento vs precio reportado"], index=0, horizontal=True, label_visibility="collapsed")


# ═══════════════════════════════════════════════════════════════
# DATA PREP
# ═══════════════════════════════════════════════════════════════
viz_df = df[df['Investor'].isin(selected)].copy()

chunks = []
for inv in selected:
    d = viz_df[viz_df['Investor'] == inv].sort_values('% of Portfolio', ascending=False).copy()
    if d.empty:
        continue
    if threshold in ("Top 80%", "Top 90%"):
        limit = 80 if threshold == "Top 80%" else 90
        d['_cs'] = d['% of Portfolio'].cumsum()
        d = d[d['_cs'] <= limit + d['% of Portfolio'].iloc[0]].drop('_cs', axis=1)
    chunks.append(d)

if not chunks:
    st.warning("Sin datos con los filtros actuales.")
    st.stop()

treemap_df = pd.concat(chunks)

# Activity score
act_map = {'Compra': 1.0, 'Añadir': 0.5, 'Mantener': 0.0, 'Reducir': -1.0}
treemap_df['Act_Score'] = treemap_df['Activity_Type'].map(act_map)
treemap_df['Label'] = treemap_df['Ticker']

# Performance clamped for color scale
treemap_df['Perf_Clamped'] = treemap_df['Performance'].clip(-50, 50).fillna(0)

# Format performance for hover
treemap_df['Perf_Str'] = treemap_df['Performance'].apply(
    lambda x: f"+{x:.1f}%" if pd.notna(x) and x > 0 else f"{x:.1f}%" if pd.notna(x) else "N/A"
)

# 52-week position (where current price sits in range)
if 'Current Price_Num' in treemap_df.columns:
    low = treemap_df['52Week Low_Num']
    high = treemap_df['52Week High_Num']
    curr = treemap_df['Current Price_Num']
    range_width = (high - low).replace(0, np.nan)
    treemap_df['Range_Pct'] = ((curr - low) / range_width * 100).round(0).fillna(50)
    treemap_df['Range_Str'] = treemap_df['Range_Pct'].apply(lambda x: f"{x:.0f}%" if pd.notna(x) else "N/A")
else:
    treemap_df['Range_Pct'] = 50
    treemap_df['Range_Str'] = "N/A"


# ═══════════════════════════════════════════════════════════════
# HERO TREEMAP
# ═══════════════════════════════════════════════════════════════
use_performance = color_mode == "Rendimiento vs precio reportado"

if use_performance:
    color_col = 'Perf_Clamped'
    cscale = [
        [0.0,  '#dc2626'],   # -50% deep red
        [0.35, '#7f1d1d'],   # -15% dark red
        [0.5,  '#13131d'],   # 0% neutral dark
        [0.65, '#14532d'],   # +15% dark green
        [1.0,  '#22c55e'],   # +50% vivid green
    ]
    crange = [-50, 50]
    bar_tickvals = [-50, -25, 0, 25, 50]
    bar_ticktext = ['-50%', '-25%', '0%', '+25%', '+50%']
    bar_title = 'RENDIMIENTO'
else:
    color_col = 'Act_Score'
    cscale = [
        [0.0,  '#dc2626'],
        [0.35, '#1c1c2e'],
        [0.65, '#3b82f6'],
        [1.0,  '#22c55e'],
    ]
    crange = [-1, 1]
    bar_tickvals = [-1, 0, 0.5, 1]
    bar_ticktext = ['Reducir', 'Mantener', 'Añadir', 'Compra']
    bar_title = 'ACTIVIDAD'

fig = px.treemap(
    treemap_df,
    path=['Investor', 'Label'],
    values='% of Portfolio',
    color=color_col,
    color_continuous_scale=cscale,
    range_color=crange,
    custom_data=['Company', 'Investor', '% of Portfolio', 'Value', 'Activity_Type', 'Ticker', 'Perf_Str', 'Range_Str'],
)

fig.update_traces(
    hovertemplate=(
        '<b style="font-size:14px">%{customdata[5]}</b>  %{customdata[0]}<br>'
        '<span style="color:#9090a8">Inversor:</span> %{customdata[1]}<br>'
        '<span style="color:#9090a8">Peso:</span> %{customdata[2]:.2f}%%<br>'
        '<span style="color:#9090a8">Valor:</span> %{customdata[3]}<br>'
        '<span style="color:#9090a8">Actividad:</span> %{customdata[4]}<br>'
        '<span style="color:#9090a8">Rendimiento:</span> %{customdata[6]}<br>'
        '<span style="color:#9090a8">Posición 52sem:</span> %{customdata[7]} del rango'
        '<extra></extra>'
    ),
    textinfo='label+percent entry',
    textfont=dict(family='DM Mono, monospace', size=11, color='#eaeaf0'),
    marker=dict(
        line=dict(color='#07070d', width=1.5),
        cornerradius=5,
    ),
    tiling=dict(packing='squarify', pad=3),
)

fig.update_layout(
    height=720,
    margin=dict(t=0, l=0, r=0, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Instrument Sans, sans-serif', color='#eaeaf0'),
    coloraxis_colorbar=dict(
        title=dict(text=bar_title, font=dict(size=9, family='DM Mono, monospace', color='#505068')),
        thicknessmode='pixels', thickness=6,
        lenmode='fraction', len=0.3,
        yanchor='middle', y=0.5,
        xanchor='right', x=1.005,
        tickvals=bar_tickvals,
        ticktext=bar_ticktext,
        tickfont=dict(size=8, family='DM Mono, monospace', color='#505068'),
        outlinewidth=0,
        bgcolor='rgba(0,0,0,0)',
    ),
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Legend
if use_performance:
    st.markdown("""
    <div class="legend-bar">
        <span><span class="dot" style="background:#dc2626"></span>Pérdida fuerte</span>
        <span><span class="dot" style="background:#7f1d1d"></span>Pérdida leve</span>
        <span><span class="dot" style="background:#13131d; border:1px solid #505068"></span>Sin cambio</span>
        <span><span class="dot" style="background:#14532d"></span>Ganancia leve</span>
        <span><span class="dot" style="background:#22c55e"></span>Ganancia fuerte</span>
        <span style="color:#505068; border-left:1px solid #1e1e2a; padding-left:1rem;">Color = rendimiento vs precio reportado</span>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="legend-bar">
        <span><span class="dot" style="background:#22c55e"></span>Compra nueva</span>
        <span><span class="dot" style="background:#3b82f6"></span>Añadir posición</span>
        <span><span class="dot" style="background:#1c1c2e; border:1px solid #505068"></span>Mantener</span>
        <span><span class="dot" style="background:#dc2626"></span>Reducir</span>
        <span style="color:#505068; border-left:1px solid #1e1e2a; padding-left:1rem;">Clic en inversor → zoom · Clic en cabecera → volver</span>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# CONSENSUS PICKS
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="section-header">
    <div class="section-title">Selecciones de Consenso</div>
    <div class="section-line"></div>
    <div class="section-badge">Acciones en 2+ carteras</div>
</div>
""", unsafe_allow_html=True)

sel_df = df[df['Investor'].isin(selected)]

consensus = sel_df.groupby('Ticker').agg(
    Inversores=('Investor', 'nunique'),
    Peso_Promedio=('% of Portfolio', 'mean'),
    Peso_Max=('% of Portfolio', 'max'),
    Valor_Total=('Value_Clean', 'sum'),
    Empresa=('Company', 'first'),
    Rendimiento=('Performance', 'mean'),
    Comprando=('Activity_Type', lambda x: (x.isin(['Compra', 'Añadir'])).sum()),
    Total=('Activity_Type', 'count'),
).reset_index()

consensus = consensus[consensus['Inversores'] >= 2].sort_values('Inversores', ascending=False).head(30)
consensus['Valor_M'] = (consensus['Valor_Total'] / 1e6).round(1)
consensus['Rendimiento'] = consensus['Rendimiento'].round(1)
consensus['Sentimiento'] = consensus.apply(
    lambda r: '🟢 Alcista' if r['Comprando'] > r['Total'] * 0.5
    else '🔴 Bajista' if r['Comprando'] == 0
    else '⚪ Mixto', axis=1
)
consensus['Rend_Str'] = consensus['Rendimiento'].apply(
    lambda x: f"+{x:.1f}%" if x > 0 else f"{x:.1f}%"
)

col_chart, col_table = st.columns([1, 1.4])

with col_chart:
    top15 = consensus.head(15).sort_values('Inversores', ascending=True)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        y=top15['Ticker'] + '  ' + top15['Empresa'].str[:16],
        x=top15['Inversores'],
        orientation='h',
        marker=dict(
            color=top15['Inversores'],
            colorscale=[[0, '#13131d'], [0.5, '#3b82f6'], [1.0, '#6366f1']],
            line=dict(width=0),
            cornerradius=4,
        ),
        text=top15.apply(lambda r: f"{r['Inversores']}  ({r['Rend_Str']})", axis=1),
        textposition='inside',
        textfont=dict(family='DM Mono, monospace', size=10, color='#eaeaf0'),
        hovertemplate=(
            '<b>%{y}</b><br>'
            'Inversores: %{x}<br>'
            '<extra></extra>'
        ),
    ))

    fig_bar.update_layout(
        height=480,
        margin=dict(t=8, l=0, r=16, b=8),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='DM Mono, monospace', color='#9090a8', size=9),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.04)', zeroline=False, title=None),
        yaxis=dict(showgrid=False, zeroline=False, title=None),
        bargap=0.2,
    )

    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

with col_table:
    tbl = consensus[['Ticker', 'Empresa', 'Inversores', 'Peso_Promedio', 'Peso_Max', 'Valor_M', 'Rend_Str', 'Sentimiento']].copy()
    tbl.columns = ['Ticker', 'Empresa', 'Nº Inv.', 'Peso Medio %', 'Peso Máx %', 'Valor $M', 'Rendimiento', 'Sentimiento']

    max_inv = int(tbl['Nº Inv.'].max()) if len(tbl) > 0 else 10

    st.dataframe(
        tbl,
        use_container_width=True,
        height=480,
        hide_index=True,
        column_config={
            'Ticker': st.column_config.TextColumn(width='small'),
            'Empresa': st.column_config.TextColumn(width='medium'),
            'Nº Inv.': st.column_config.ProgressColumn(min_value=0, max_value=max_inv, format='%d', width='small'),
            'Peso Medio %': st.column_config.NumberColumn(format='%.2f', width='small'),
            'Peso Máx %': st.column_config.NumberColumn(format='%.2f', width='small'),
            'Valor $M': st.column_config.NumberColumn(format='$%,.1f', width='small'),
            'Rendimiento': st.column_config.TextColumn(width='small'),
            'Sentimiento': st.column_config.TextColumn(width='small'),
        }
    )


# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="footer-bar">
    <div class="footer-text">
        <a href="https://bquantfinance.com" target="_blank">@Gsnchez</a> · BQuant Finance ·
        Datos: Dataroma · {n_inv} inversores · {n_stk:,} acciones
    </div>
</div>
""", unsafe_allow_html=True)
