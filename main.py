import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import re

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Superinversores | BQuant Finance",
    page_icon="◼",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM CSS — Dark luxury terminal aesthetic
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700;800&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

/* ── Root & Global ── */
:root {
    --bg-primary: #0a0a0f;
    --bg-card: #111118;
    --bg-card-hover: #16161f;
    --border: #1e1e2a;
    --border-accent: #2d5bff;
    --text-primary: #e8e8ed;
    --text-secondary: #6b6b7b;
    --text-muted: #3d3d4d;
    --accent: #2d5bff;
    --accent-glow: rgba(45, 91, 255, 0.15);
    --green: #00d084;
    --red: #ff4757;
    --amber: #ffbe0b;
}

.main { background: var(--bg-primary) !important; }
.block-container { padding: 1.5rem 2.5rem 2rem !important; max-width: 1600px !important; }
header[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── Typography ── */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
    color: var(--text-primary) !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    background: none !important;
    -webkit-text-fill-color: unset !important;
    color: var(--text-primary) !important;
}

/* ── Hero Header ── */
.hero-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.5rem 0 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--text-primary);
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.hero-title .dot {
    width: 10px; height: 10px;
    background: var(--accent);
    border-radius: 2px;
    box-shadow: 0 0 12px var(--accent);
    display: inline-block;
}
.hero-subtitle {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.hero-brand {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-secondary);
    text-align: right;
    letter-spacing: 0.04em;
}
.hero-brand a {
    color: var(--accent) !important;
    text-decoration: none;
}

/* ── Metric Cards ── */
.metric-row {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.1rem;
    transition: all 0.2s ease;
}
.metric-card:hover {
    border-color: var(--border-accent);
    background: var(--bg-card-hover);
    box-shadow: 0 0 20px var(--accent-glow);
}
.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.35rem;
}
.metric-value {
    font-family: 'Outfit', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.1;
}
.metric-delta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    margin-top: 0.25rem;
}
.metric-delta.green { color: var(--green); }
.metric-delta.red { color: var(--red); }
.metric-delta.amber { color: var(--amber); }

/* ── Controls Bar ── */
.controls-bar {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.8rem 1.2rem;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    margin-bottom: 1rem;
}
.control-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    white-space: nowrap;
}

/* ── Streamlit overrides ── */
div[data-testid="metric-container"] { display: none; }

div[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border-color: var(--border) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
}

div[data-baseweb="radio"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    color: var(--text-secondary) !important;
    padding: 0.35rem 0.7rem !important;
    margin: 0 !important;
    background: transparent !important;
    border-radius: 6px !important;
    transition: all 0.15s ease !important;
}
div[data-baseweb="radio"] label:hover {
    background: var(--bg-card-hover) !important;
    color: var(--text-primary) !important;
}

.stRadio > div { gap: 0.2rem !important; flex-direction: row !important; }
.stRadio > label { display: none !important; }

div[data-testid="stExpander"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    color: var(--text-secondary) !important;
}

/* ── Consensus Table ── */
.consensus-header {
    font-family: 'Outfit', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 1.5rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.consensus-header .line {
    flex: 1;
    height: 1px;
    background: var(--border);
}

div[data-testid="stDataFrame"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
}
.footer-brand {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 0.06em;
}
.footer-brand a { color: var(--accent); text-decoration: none; }

/* ── Plotly chart container ── */
div[data-testid="stPlotlyChart"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.5rem;
    transition: border-color 0.2s ease;
}
div[data-testid="stPlotlyChart"]:hover {
    border-color: var(--border-accent);
}

/* ── Hide default streamlit elements ── */
#MainMenu { display: none; }
footer { display: none !important; }
div[data-testid="stToolbar"] { display: none; }
div[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv('dataroma_holdings_complete.csv')

    for col in ['% of Portfolio', 'Shares']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    if 'Value' in df.columns:
        df['Value_Clean'] = df['Value'].str.replace(r'[$,]', '', regex=True)
        df['Value_Clean'] = pd.to_numeric(df['Value_Clean'], errors='coerce')

    df['Activity_Type'] = df['RecentActivity'].apply(lambda x:
        'Mantener' if pd.isna(x) else
        'Compra' if x == 'Buy' else
        'Añadir' if 'Add' in str(x) else
        'Reducir' if 'Reduce' in str(x) else
        'Mantener'
    )

    df['Ticker'] = df['Stock'].apply(lambda x: x.split(' - ')[0] if pd.notna(x) and ' - ' in x else x)
    df['Company'] = df['Stock'].apply(lambda x: x.split(' - ')[1] if pd.notna(x) and ' - ' in x else x)

    return df

df = load_data()


# ─────────────────────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div>
        <div class="hero-title"><span class="dot"></span>Superinversores</div>
        <div class="hero-subtitle">Carteras de los mejores inversores del mundo · Análisis visual</div>
    </div>
    <div class="hero-brand">
        por <a href="https://bquantfinance.com" target="_blank">@Gsnchez</a><br>
        BQuant Finance
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# METRICS ROW
# ─────────────────────────────────────────────────────────────
n_investors = df['Investor'].nunique()
n_stocks = df['Stock'].nunique()
total_aum = df['Value_Clean'].sum() / 1e9
avg_positions = len(df) / n_investors if n_investors > 0 else 0

# Top 5 concentration
conc_list = []
for inv in df['Investor'].unique():
    inv_df = df[df['Investor'] == inv]
    conc_list.append(inv_df.nlargest(5, '% of Portfolio')['% of Portfolio'].sum())
avg_conc = np.mean(conc_list) if conc_list else 0

buy_pct = (df['Activity_Type'].isin(['Compra', 'Añadir'])).sum() / len(df) * 100 if len(df) > 0 else 0

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-label">Inversores</div>
        <div class="metric-value">{n_investors}</div>
        <div class="metric-delta amber">Legendarios</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Acciones Únicas</div>
        <div class="metric-value">{n_stocks}</div>
        <div class="metric-delta green">Universo completo</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">AUM Total</div>
        <div class="metric-value">${total_aum:.0f}B</div>
        <div class="metric-delta green">Billones USD</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Pos. Promedio</div>
        <div class="metric-value">{avg_positions:.0f}</div>
        <div class="metric-delta amber">Por inversor</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Conc. Top 5</div>
        <div class="metric-value">{avg_conc:.1f}%</div>
        <div class="metric-delta red">Promedio</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">Ratio Compra</div>
        <div class="metric-value">{buy_pct:.0f}%</div>
        <div class="metric-delta {'green' if buy_pct > 50 else 'red'}">{'Alcista' if buy_pct > 50 else 'Bajista'}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CONTROLS — Minimal, inline
# ─────────────────────────────────────────────────────────────
c1, c2, c3 = st.columns([1.2, 2.5, 1.3])

with c1:
    scope = st.radio(
        "Alcance",
        ["Top 5", "Top 10", "Top 20", "Todos"],
        index=1,
        horizontal=True,
        key="scope"
    )

with c2:
    if scope == "Top 5":
        default_inv = df.groupby('Investor')['Value_Clean'].sum().nlargest(5).index.tolist()
    elif scope == "Top 10":
        default_inv = df.groupby('Investor')['Value_Clean'].sum().nlargest(10).index.tolist()
    elif scope == "Top 20":
        default_inv = df.groupby('Investor')['Value_Clean'].sum().nlargest(20).index.tolist()
    else:
        default_inv = sorted(df['Investor'].unique())

    selected = st.multiselect(
        "Inversores",
        sorted(df['Investor'].unique()),
        default=default_inv,
        label_visibility="collapsed",
        key="investors"
    )

with c3:
    threshold = st.radio(
        "Posiciones",
        ["Top 80%", "Top 90%", "Todas"],
        index=1,
        horizontal=True,
        key="threshold"
    )

if not selected:
    st.warning("Selecciona al menos un inversor.")
    st.stop()


# ─────────────────────────────────────────────────────────────
# DATA PREP — Filter & prepare treemap data
# ─────────────────────────────────────────────────────────────
viz_df = df[df['Investor'].isin(selected)].copy()

# Apply cumulative threshold per investor
filtered_chunks = []
for inv in selected:
    inv_data = viz_df[viz_df['Investor'] == inv].sort_values('% of Portfolio', ascending=False).copy()
    if inv_data.empty:
        continue

    if threshold == "Top 80%":
        inv_data['_cumsum'] = inv_data['% of Portfolio'].cumsum()
        cutoff = 80 + inv_data['% of Portfolio'].iloc[0]
        inv_data = inv_data[inv_data['_cumsum'] <= cutoff].drop('_cumsum', axis=1)
    elif threshold == "Top 90%":
        inv_data['_cumsum'] = inv_data['% of Portfolio'].cumsum()
        cutoff = 90 + inv_data['% of Portfolio'].iloc[0]
        inv_data = inv_data[inv_data['_cumsum'] <= cutoff].drop('_cumsum', axis=1)

    filtered_chunks.append(inv_data)

if not filtered_chunks:
    st.warning("Sin datos con los filtros actuales.")
    st.stop()

treemap_df = pd.concat(filtered_chunks)

# Activity color mapping
activity_colors = {
    'Compra': '#00d084',
    'Añadir': '#2d5bff',
    'Reducir': '#ff4757',
    'Mantener': '#3d3d4d'
}
treemap_df['Activity_Color'] = treemap_df['Activity_Type'].map(activity_colors)

# Create display label
treemap_df['Label'] = treemap_df['Ticker']
treemap_df['Hover_Text'] = (
    '<b>' + treemap_df['Ticker'] + '</b> — ' + treemap_df['Company'] +
    '<br>Inversor: ' + treemap_df['Investor'] +
    '<br>Peso: ' + treemap_df['% of Portfolio'].round(2).astype(str) + '%' +
    '<br>Valor: ' + treemap_df['Value'].fillna('N/A') +
    '<br>Actividad: ' + treemap_df['Activity_Type']
)

# Map activity to numeric for color scale
activity_num = {'Compra': 1.0, 'Añadir': 0.6, 'Mantener': 0.0, 'Reducir': -1.0}
treemap_df['Activity_Score'] = treemap_df['Activity_Type'].map(activity_num)


# ─────────────────────────────────────────────────────────────
# HERO TREEMAP
# ─────────────────────────────────────────────────────────────
fig = px.treemap(
    treemap_df,
    path=['Investor', 'Label'],
    values='% of Portfolio',
    color='Activity_Score',
    color_continuous_scale=[
        [0.0, '#ff4757'],   # Reduce = red
        [0.45, '#1a1a2a'],  # Hold = dark
        [0.75, '#2d5bff'],  # Add = blue
        [1.0, '#00d084'],   # Buy = green
    ],
    range_color=[-1, 1],
    custom_data=['Company', 'Investor', '% of Portfolio', 'Value', 'Activity_Type', 'Ticker'],
)

fig.update_traces(
    hovertemplate=(
        '<b>%{customdata[5]}</b> — %{customdata[0]}<br>'
        'Inversor: %{customdata[1]}<br>'
        'Peso: %{customdata[2]:.2f}%<br>'
        'Valor: %{customdata[3]}<br>'
        'Actividad: %{customdata[4]}'
        '<extra></extra>'
    ),
    textinfo='label+percent entry',
    textfont=dict(
        family='JetBrains Mono, monospace',
        size=12,
        color='#e8e8ed'
    ),
    marker=dict(
        line=dict(color='#0a0a0f', width=1.5),
        cornerradius=4,
    ),
    tiling=dict(packing='squarify', pad=3),
)

fig.update_layout(
    height=700,
    margin=dict(t=0, l=0, r=0, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Outfit, sans-serif', color='#e8e8ed'),
    coloraxis_colorbar=dict(
        title=dict(text='ACTIVIDAD', font=dict(size=10, family='JetBrains Mono')),
        thicknessmode='pixels', thickness=8,
        lenmode='fraction', len=0.35,
        yanchor='middle', y=0.5,
        xanchor='right', x=1.01,
        tickvals=[-1, 0, 0.6, 1],
        ticktext=['Reducir', 'Mantener', 'Añadir', 'Compra'],
        tickfont=dict(size=9, family='JetBrains Mono', color='#6b6b7b'),
        outlinewidth=0,
        bgcolor='rgba(0,0,0,0)',
    ),
    treemapcolorway=None,
)

st.plotly_chart(fig, use_container_width=True, config={
    'displayModeBar': False,
    'scrollZoom': False,
})

# Legend hint
st.markdown("""
<div style="display:flex; gap:1.5rem; justify-content:center; padding:0.3rem 0 0.5rem; font-family:'JetBrains Mono',monospace; font-size:0.68rem;">
    <span style="color:#00d084">● Compra nueva</span>
    <span style="color:#2d5bff">● Añadir posición</span>
    <span style="color:#3d3d4d">● Mantener</span>
    <span style="color:#ff4757">● Reducir</span>
    <span style="color:#6b6b7b; margin-left:1rem;">Clic en inversor para hacer zoom · Clic header para volver</span>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# CONSENSUS PICKS — Bottom table
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="consensus-header">
    Selecciones de Consenso
    <div class="line"></div>
</div>
""", unsafe_allow_html=True)

consensus = df[df['Investor'].isin(selected)].groupby('Ticker').agg(
    Inversores=('Investor', 'nunique'),
    Peso_Promedio=('% of Portfolio', 'mean'),
    Peso_Max=('% of Portfolio', 'max'),
    Valor_Total=('Value_Clean', 'sum'),
    Empresa=('Company', 'first'),
    Comprando=('Activity_Type', lambda x: (x.isin(['Compra', 'Añadir'])).sum()),
).reset_index()

consensus = consensus[consensus['Inversores'] >= 2].sort_values('Inversores', ascending=False).head(25)
consensus['Valor_Total'] = (consensus['Valor_Total'] / 1e6).round(1)
consensus['Sentimiento'] = consensus.apply(
    lambda r: '🟢 Alcista' if r['Comprando'] > r['Inversores'] * 0.5
    else '🔴 Bajista' if r['Comprando'] == 0
    else '⚪ Mixto', axis=1
)

display_consensus = consensus[['Ticker', 'Empresa', 'Inversores', 'Peso_Promedio', 'Peso_Max', 'Valor_Total', 'Sentimiento']].copy()
display_consensus.columns = ['Ticker', 'Empresa', 'Nº Inversores', 'Peso Medio %', 'Peso Máx %', 'Valor Total $M', 'Sentimiento']

st.dataframe(
    display_consensus,
    use_container_width=True,
    height=400,
    hide_index=True,
    column_config={
        'Peso Medio %': st.column_config.NumberColumn(format='%.2f'),
        'Peso Máx %': st.column_config.NumberColumn(format='%.2f'),
        'Valor Total $M': st.column_config.NumberColumn(format='$%.1f'),
        'Nº Inversores': st.column_config.ProgressColumn(
            min_value=0,
            max_value=display_consensus['Nº Inversores'].max(),
            format='%d',
        ),
    }
)


# ─────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div class="footer-brand">
        Hecho por <a href="https://bquantfinance.com" target="_blank">@Gsnchez</a> · BQuant Finance ·
        Datos: Dataroma · {n_inv} inversores · {n_stk} acciones
    </div>
</div>
""".format(n_inv=n_investors, n_stk=n_stocks), unsafe_allow_html=True)
