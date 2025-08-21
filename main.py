import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Dashboard de Superinversores | BQuantFinance",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 0rem 0rem;
        background: linear-gradient(180deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    /* Card styling */
    .css-1r6slb0 {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
        border: 2px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="metric-container"] label {
        color: rgba(255, 255, 255, 0.9) !important;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        color: white !important;
        font-weight: bold;
        font-size: 1.8rem;
    }
    
    /* Headers styling */
    h1 {
        background: linear-gradient(90deg, #00d2ff 0%, #3a47d5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        padding: 2rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    h2 {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        border-bottom: 3px solid #667eea;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    
    h3 {
        color: #667eea;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #667eea;
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        background: transparent;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 12px 30px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        font-weight: 700;
        color: white !important;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: 2px solid white;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 30px;
        font-weight: bold;
        font-size: 1rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.6);
    }
    
    /* Attribution styling */
    .attribution {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        text-align: center;
        font-weight: bold;
        font-size: 1.1rem;
        margin: 2rem auto;
        max-width: 500px;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    /* Dataframe styling */
    .dataframe {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-radius: 15px;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    /* SelectBox styling */
    div[data-baseweb="select"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    /* Radio button styling */
    div[role="radiogroup"] label {
        background: rgba(255, 255, 255, 0.1);
        padding: 10px 15px;
        border-radius: 10px;
        margin: 5px;
        transition: all 0.3s ease;
    }
    
    div[role="radiogroup"] label:hover {
        background: rgba(102, 126, 234, 0.3);
        transform: translateX(5px);
    }
    </style>
    """, unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    """Cargar y preprocesar los datos"""
    df = pd.read_csv('dataroma_holdings_complete.csv')
    
    # Clean numeric columns
    numeric_cols = ['% of Portfolio', 'Shares']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Clean Value column (remove $ and commas)
    if 'Value' in df.columns:
        df['Value_Clean'] = df['Value'].str.replace(r'[$,]', '', regex=True)
        df['Value_Clean'] = pd.to_numeric(df['Value_Clean'], errors='coerce')
    
    # Extract activity type and percentage
    df['Activity_Type'] = df['RecentActivity'].apply(lambda x: 
        'Mantener' if pd.isna(x) else  # NaN means Hold position
        'Compra' if x == 'Buy' else
        'Añadir' if 'Add' in str(x) else 
        'Reducir' if 'Reduce' in str(x) else 
        'Mantener'  # Default to Hold for any other case
    )
    
    df['Activity_Percentage'] = df['RecentActivity'].apply(lambda x: 
        float(re.findall(r'[\d.]+', str(x))[0]) if pd.notna(x) and re.findall(r'[\d.]+', str(x)) else 0
    )
    
    # Extract stock ticker
    df['Ticker'] = df['Stock'].apply(lambda x: x.split(' - ')[0] if pd.notna(x) and ' - ' in x else x)
    df['Company'] = df['Stock'].apply(lambda x: x.split(' - ')[1] if pd.notna(x) and ' - ' in x else x)
    
    return df

# Load the data
df = load_data()

# Title with gradient and attribution
st.markdown("<h1>🚀 Dashboard de Análisis de Superinversores</h1>", unsafe_allow_html=True)
st.markdown("""
    <div class='attribution'>
        Creado por @Gsnchez - BQuantFinance.com 📈
    </div>
""", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a0aec0; font-size: 1.3rem; margin-bottom: 2rem;'>Analizando las carteras de 81 inversores legendarios con visualizaciones avanzadas</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎨 Controles del Dashboard")
    st.markdown("---")
    
    # View selection with icons
    view_mode = st.radio(
        "Seleccionar Vista de Análisis",
        ["🌟 Universo de Carteras", "🎯 Inteligencia de Portafolio", "🔥 Matriz de Acciones Calientes", 
         "📊 Análisis Avanzado", "🕸️ Análisis de Red", "👤 Análisis Individual", "🎭 Análisis Comparativo"],
        index=0
    )
    
    st.markdown("---")
    
    # Filter controls based on view
    if view_mode == "👤 Análisis Individual":
        selected_investor = st.selectbox(
            "🎯 Seleccionar Inversor",
            sorted(df['Investor'].unique()),
            index=0
        )
    
    if view_mode == "🎭 Análisis Comparativo":
        all_investors_comp = sorted(df['Investor'].unique())
        default_comp = all_investors_comp[:3] if len(all_investors_comp) >= 3 else all_investors_comp
        
        selected_investors = st.multiselect(
            "📊 Seleccionar Inversores para Comparar",
            all_investors_comp,
            default=default_comp
        )
    
    # Activity filter
    st.markdown("### 🔧 Filtros Globales")
    activity_filter = st.multiselect(
        "Filtrar por Tipo de Actividad",
        ["Compra", "Añadir", "Reducir", "Mantener"],
        default=["Compra", "Añadir", "Reducir", "Mantener"]
    )
    
    # Portfolio size filter
    min_portfolio = st.slider(
        "Porcentaje Mínimo de Cartera",
        0.0, 50.0, 0.0, 0.5
    )
    
    # Add info
    st.markdown("---")
    st.info("💡 Consejo: ¡Usa los gráficos 3D para explorar relaciones multidimensionales en los datos!")

# Filter data based on sidebar selections
filtered_df = df[df['Activity_Type'].isin(activity_filter)]
filtered_df = filtered_df[filtered_df['% of Portfolio'] >= min_portfolio]

# Main content area based on view selection
if view_mode == "🌟 Universo de Carteras":
    # Main Portfolio Universe with stunning sunburst as centerpiece
    st.markdown("## 🌟 Universo de Carteras de Superinversores", unsafe_allow_html=True)
    
    # Key metrics with gradient cards - more compact
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Inversores", f"{filtered_df['Investor'].nunique()}", delta="🎯")
    with col2:
        st.metric("Acciones", f"{filtered_df['Stock'].nunique()}", delta="📈")
    with col3:
        total_value = filtered_df['Value_Clean'].sum() / 1e9
        st.metric("AUM Total", f"${total_value:.1f}B", delta="💰")
    with col4:
        num_investors = filtered_df['Investor'].nunique()
        if num_investors > 0:
            avg_holdings = len(filtered_df) / num_investors
        else:
            avg_holdings = 0
        st.metric("Promedio Pos.", f"{avg_holdings:.0f}", delta="📊")
    with col5:
        if not filtered_df.empty:
            # Calculate average Top 5 concentration more safely
            investors_conc = []
            for inv in filtered_df['Investor'].unique():
                inv_df = filtered_df[filtered_df['Investor'] == inv]
                if not inv_df.empty:
                    top5_sum = inv_df.nlargest(5, '% of Portfolio')['% of Portfolio'].sum()
                    investors_conc.append(top5_sum)
            
            if investors_conc:
                concentration = sum(investors_conc) / len(investors_conc)
            else:
                concentration = 0
        else:
            concentration = 0
        st.metric("Top5 Prom.", f"{concentration:.1f}%", delta="🔥")
    with col6:
        if not filtered_df.empty and len(filtered_df) > 0:
            buy_activity = (filtered_df['Activity_Type'].isin(['Compra', 'Añadir'])).sum() / len(filtered_df) * 100
        else:
            buy_activity = 0
        st.metric("Actividad Compra", f"{buy_activity:.1f}%", delta="📈")
    
    st.markdown("---")
    
    # Create two columns for main sunburst and supporting visualizations
    col_main, col_side = st.columns([3, 1])
    
    with col_main:
        st.markdown("### 🎨 Universo Interactivo de Carteras - Haz Clic para Explorar")
        
        # Add investor selection controls
        col_select1, col_select2 = st.columns([3, 1])
        with col_select1:
            all_investors_sunburst = sorted(filtered_df['Investor'].unique())
            default_selection = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(10).index.tolist()
            
            # Add quick selection buttons
            quick_select = st.radio(
                "Selección rápida:",
                ["Top 10 por valor", "Top 5 por valor", "Personalizado"],
                horizontal=True,
                index=0
            )
            
            if quick_select == "Top 10 por valor":
                default_selection = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(10).index.tolist()
            elif quick_select == "Top 5 por valor":
                default_selection = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(5).index.tolist()
            else:
                default_selection = []  # Let user select manually
            
            selected_investors_sunburst = st.multiselect(
                "🎯 Seleccionar inversores para visualizar (máx. 20):",
                all_investors_sunburst,
                default=default_selection if len(all_investors_sunburst) >= len(default_selection) else all_investors_sunburst[:min(10, len(all_investors_sunburst))],
                max_selections=20,
                key="sunburst_investors",
                help="Selecciona específicamente qué inversores quieres ver en el gráfico. Puedes hacer clic en cualquier segmento del gráfico para hacer zoom."
            )
        
        with col_select2:
            # NUEVO: Cambiar de número de acciones a filtro por relevancia
            filter_method = st.radio(
                "Método de filtrado:",
                ["Por % Cartera", "Por % Acumulado", "Todas"],
                index=1,
                help="Elige cómo filtrar las posiciones mostradas"
            )
            
            if filter_method == "Por % Cartera":
                min_position_pct = st.slider(
                    "📊 Mostrar posiciones >",
                    min_value=0.1,
                    max_value=5.0,
                    value=0.5,
                    step=0.1,
                    format="%.1f%%",
                    help="Solo muestra posiciones mayores a este % de la cartera"
                )
            elif filter_method == "Por % Acumulado":
                cumsum_threshold = st.slider(
                    "📊 Mostrar top posiciones hasta",
                    min_value=50,
                    max_value=100,
                    value=90,
                    step=5,
                    format="%d%%",
                    help="Muestra las posiciones más grandes que sumen hasta este % de la cartera"
                )
            else:  # Todas
                st.info("Mostrando todas las posiciones")
        
        # Check if we have data after filtering
        if filtered_df.empty:
            st.warning("⚠️ No hay datos disponibles con los filtros actuales. Por favor ajusta los filtros en la barra lateral.")
            st.info("""
                **Sugerencias:**
                - Verifica los filtros de actividad
                - Ajusta el porcentaje mínimo de portfolio
                - Asegúrate de tener al menos un tipo de actividad seleccionado
            """)
        elif not selected_investors_sunburst:
            st.warning("⚠️ Por favor selecciona al menos un inversor para visualizar.")
            st.info("💡 Usa el selector arriba para elegir qué inversores quieres analizar en detalle.")
        else:
            # Prepare enhanced sunburst data using selected investors
            sunburst_data = filtered_df[filtered_df['Investor'].isin(selected_investors_sunburst)].copy()
            
            if sunburst_data.empty:
                st.warning("No se encontraron datos para los inversores seleccionados.")
            else:
                # Add activity layer
                sunburst_data['Activity_Group'] = sunburst_data['Activity_Type'].apply(
                    lambda x: '🟢 Comprando' if x in ['Compra', 'Añadir'] else '🔴 Vendiendo' if x == 'Reducir' else '⚪ Manteniendo'
                )
                
                # NUEVO: Aplicar filtro por relevancia en lugar de número fijo
                sunburst_filtered = []
                for investor in selected_investors_sunburst:
                    investor_data = sunburst_data[sunburst_data['Investor'] == investor].copy()
                    
                    if not investor_data.empty:
                        # Ordenar por % de Portfolio descendente
                        investor_data = investor_data.sort_values('% of Portfolio', ascending=False)
                        
                        if filter_method == "Por % Cartera":
                            # Filtrar posiciones mayores al umbral
                            investor_data = investor_data[investor_data['% of Portfolio'] >= min_position_pct]
                        
                        elif filter_method == "Por % Acumulado":
                            # Calcular suma acumulada
                            investor_data['cumsum_pct'] = investor_data['% of Portfolio'].cumsum()
                            # Mantener posiciones hasta alcanzar el umbral
                            investor_data = investor_data[investor_data['cumsum_pct'] <= cumsum_threshold + investor_data['% of Portfolio'].iloc[0]]
                            # Limpiar columna temporal
                            investor_data = investor_data.drop('cumsum_pct', axis=1)
                        
                        # Si es "Todas", no filtrar nada
                        
                        if not investor_data.empty:
                            sunburst_filtered.append(investor_data)
                
                if len(sunburst_filtered) == 0:
                    st.warning("No hay datos disponibles para visualización con los filtros actuales.")
                else:
                    sunburst_final = pd.concat(sunburst_filtered)
                    
                    # Calculate proper values for sizing
                    sunburst_final['Display_Value'] = sunburst_final['% of Portfolio']
                    
                    # Create the main sunburst chart with enhanced aesthetics
                    fig_sunburst = px.sunburst(
                        sunburst_final,
                        path=['Investor', 'Activity_Group', 'Stock'],
                        values='Display_Value',
                        color='% of Portfolio',
                        color_continuous_scale=[
                            [0, '#440154'],     # Dark purple
                            [0.2, '#31688e'],   # Blue
                            [0.4, '#35b779'],   # Green
                            [0.6, '#fde725'],   # Yellow
                            [0.8, '#ff6b6b'],   # Red
                            [1, '#c92a2a']      # Dark red
                        ],
                        title='',
                        hover_data={'Value': ':$,.0f', '% of Portfolio': ':.2f%'},
                        custom_data=['Value', 'Shares', 'RecentActivity']
                    )
                    
                    # Update layout for better aesthetics
                    fig_sunburst.update_traces(
                        textinfo='label+percent entry',
                        hovertemplate='<b>%{label}</b><br>' +
                                     'Cartera: %{color:.2f}%<br>' +
                                     'Valor: %{customdata[0]}<br>' +
                                     'Acciones: %{customdata[1]:,.0f}<br>' +
                                     'Actividad: %{customdata[2]}<br>' +
                                     '<extra></extra>',
                        marker=dict(line=dict(color='white', width=2))
                    )
                    
                    fig_sunburst.update_layout(
                        height=850,
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white', size=14),
                        margin=dict(t=30, l=0, r=0, b=0),
                        coloraxis_colorbar=dict(
                            title="% Cartera",
                            thicknessmode="pixels",
                            thickness=15,
                            lenmode="pixels",
                            len=300,
                            yanchor="middle",
                            y=0.5,
                            ticks="outside",
                            tickcolor='white',
                            tickfont=dict(color='white')
                        )
                    )
                    
                    st.plotly_chart(fig_sunburst, use_container_width=True)
                    
                    # Show current visualization stats
                    num_investors_shown = sunburst_final['Investor'].nunique()
                    num_stocks_shown = sunburst_final['Stock'].nunique()
                    
                    # NUEVO: Mostrar estadísticas más detalladas según el filtro
                    if filter_method == "Por % Cartera":
                        avg_positions = sunburst_final.groupby('Investor').size().mean()
                        st.caption(f"📊 Mostrando {num_investors_shown} inversores | {num_stocks_shown} acciones únicas | Promedio {avg_positions:.0f} posiciones por inversor (>{min_position_pct}% de cartera)")
                    elif filter_method == "Por % Acumulado":
                        total_coverage = sunburst_final.groupby('Investor')['% of Portfolio'].sum().mean()
                        st.caption(f"📊 Mostrando {num_investors_shown} inversores | {num_stocks_shown} acciones únicas | Cubriendo ~{total_coverage:.1f}% promedio de cada cartera")
                    else:
                        st.caption(f"📊 Mostrando {num_investors_shown} inversores con {num_stocks_shown} acciones únicas (TODAS las posiciones)")
                    
                    # Instructions
                    st.info("💡 **Características Interactivas:** Haz clic en cualquier segmento para acercar • Clic en el centro para alejar • Pasa el mouse para información detallada • Los colores representan concentración de cartera")
                    
                    # Spanish explanation
                    with st.expander("📚 ¿Cómo funciona este gráfico?"):
                        st.markdown("""
                        ### 🎯 **Gráfico Sunburst - Guía de Uso**
                        
                        **¿Qué es un gráfico Sunburst?**
                        
                        Es una visualización jerárquica circular que muestra las carteras de inversión de los superinversores en múltiples niveles:
                        
                        **Estructura de los Anillos:**
                        1. **Centro (Primer Anillo):** Los inversores seleccionados
                        2. **Segundo Anillo:** Tipo de actividad reciente:
                           - 🟢 **Comprando** = Nuevas posiciones o aumentando
                           - 🔴 **Vendiendo** = Reduciendo posiciones
                           - ⚪ **Manteniendo** = Sin cambios
                        3. **Anillo Exterior:** Las acciones individuales en cada cartera
                        
                        **Métodos de Filtrado:**
                        - **Por % Cartera:** Solo muestra posiciones mayores a X% (elimina ruido de posiciones pequeñas)
                        - **Por % Acumulado:** Muestra las posiciones más grandes hasta sumar X% de la cartera
                        - **Todas:** Muestra todas las posiciones sin filtrar
                        
                        **¿Para qué sirve?**
                        - **Identificar patrones:** Ver rápidamente qué inversores están comprando vs vendiendo
                        - **Descubrir oportunidades:** Encontrar acciones que múltiples inversores están acumulando
                        - **Analizar concentración:** Los colores más intensos (rojo/amarillo) indican mayor concentración en la cartera
                        - **Comparar estrategias:** El tamaño de cada segmento representa el peso en la cartera
                        
                        **Cómo interactuar:**
                        - **Clic en cualquier segmento** para hacer zoom y explorar en detalle
                        - **Clic en el centro** para regresar al nivel anterior
                        - **Pasa el mouse** sobre cualquier segmento para ver información detallada
                        - **Los colores** van de morado (baja concentración) a rojo (alta concentración)
                        
                        **Tip profesional:** Usa "Por % Acumulado" al 90% para ver las posiciones que realmente importan sin ruido.
                        """)
    
    with col_side:
        st.markdown("### 📊 Estadísticas Rápidas")
        
        if not filtered_df.empty:
            # Most active investor
            most_active = filtered_df.groupby('Investor')['Activity_Type'].apply(
                lambda x: (x.isin(['Compra', 'Añadir'])).sum()
            ).nlargest(1)
            
            if not most_active.empty:
                st.markdown(f"**Más Activo:**  \n{most_active.index[0][:25]}")
                st.markdown(f"*{most_active.values[0]} nuevas posiciones*")
            else:
                st.markdown("**Más Activo:**  \n*Sin datos disponibles*")
            
            st.markdown("---")
            
            # Top stock by investor count
            top_stock = filtered_df.groupby('Stock')['Investor'].nunique().nlargest(1)
            
            if not top_stock.empty:
                st.markdown(f"**Acción Más Popular:**  \n{top_stock.index[0].split(' - ')[0]}")
                st.markdown(f"*En {top_stock.values[0]} carteras*")
            else:
                st.markdown("**Acción Más Popular:**  \n*Sin datos disponibles*")
            
            st.markdown("---")
            
            # Activity summary pie
            st.markdown("### 🎯 Resumen de Actividad")
            activity_dist = filtered_df['Activity_Type'].value_counts()
            
            if not activity_dist.empty:
                fig_activity = px.pie(
                    values=activity_dist.values,
                    names=activity_dist.index,
                    color_discrete_map={
                        'Compra': '#10B981',
                        'Añadir': '#60A5FA',
                        'Reducir': '#F87171',
                        'Mantener': '#9CA3AF'
                    },
                    hole=0.6
                )
                
                fig_activity.update_traces(
                    textposition='outside',
                    textinfo='label+percent',
                    marker=dict(line=dict(color='white', width=2))
                )
                
                fig_activity.update_layout(
                    height=300,
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=10),
                    margin=dict(t=0, l=0, r=0, b=0)
                )
                
                st.plotly_chart(fig_activity, use_container_width=True)
            else:
                st.info("Sin datos de actividad con los filtros actuales")
        else:
            st.info("Ajusta los filtros para ver estadísticas")
    
    st.markdown("---")
    
    # Bottom row with supporting visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🏆 Mayores Posiciones en Todas las Carteras")
        with st.expander("ℹ️ ¿Qué muestra esto?"):
            st.markdown("""
            **Propósito:** Identifica las posiciones individuales más grandes entre todos los inversores.
            **Cómo leer:** Cada entrada muestra un ticker, el inversor que lo posee y qué porcentaje representa en su cartera.
            **Por qué importa:** Posiciones grandes (>10%) indican apuestas de alta convicción donde los inversores concentran su capital.
            """)
        
        if not filtered_df.empty:
            top_holdings = filtered_df.nlargest(15, '% of Portfolio')[['Stock', 'Investor', '% of Portfolio']]
            if not top_holdings.empty:
                for _, row in top_holdings.iterrows():
                    stock_ticker = row['Stock'].split(' - ')[0] if ' - ' in row['Stock'] else row['Stock']
                    st.markdown(f"**{stock_ticker}** - {row['Investor'][:20]}  \n*{row['% of Portfolio']:.1f}% de la cartera*")
            else:
                st.info("Sin datos de posiciones disponibles")
        else:
            st.info("Sin datos con los filtros actuales")
    
    with col2:
        st.markdown("### 🔥 Acciones Más Populares (Más Inversores)")
        with st.expander("ℹ️ ¿Qué muestra esto?"):
            st.markdown("""
            **Propósito:** Muestra qué acciones son poseídas por más superinversores.
            **Cómo leer:** Barras más largas = más inversores poseen la acción. La intensidad del color muestra el nivel de consenso.
            **Por qué importa:** Cuando múltiples inversores legendarios poseen la misma acción, sugiere cualidades fundamentales sólidas.
            """)
        
        if not filtered_df.empty:
            hot_stocks = filtered_df.groupby('Stock')['Investor'].nunique().nlargest(15)
            
            if not hot_stocks.empty:
                fig_hot = px.bar(
                    x=hot_stocks.values,
                    y=hot_stocks.index,
                    orientation='h',
                    color=hot_stocks.values,
                    color_continuous_scale='YlOrRd',
                    labels={'x': 'Número de Inversores', 'y': ''}
                )
                
                fig_hot.update_layout(
                    height=450,
                    showlegend=False,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=9),
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=False)
                )
                
                st.plotly_chart(fig_hot, use_container_width=True)
            else:
                st.info("Sin datos de acciones disponibles")
        else:
            st.info("Sin datos con los filtros actuales")

elif view_mode == "🎯 Inteligencia de Portafolio":
    st.markdown("## 🎯 Inteligencia Avanzada de Portafolio", unsafe_allow_html=True)
    
    # Add global investor selection for Portfolio Intelligence
    st.markdown("### 🎯 Selección de Inversores para Análisis de Inteligencia")
    col_intel1, col_intel2 = st.columns([3, 1])
    
    with col_intel1:
        all_investors_intel = sorted(filtered_df['Investor'].unique())
        
        # Quick selection options
        quick_select_intel = st.radio(
            "Selección rápida:",
            ["Top 20 por valor", "Top 10 por valor", "Top 5 por valor", "Personalizado"],
            horizontal=True,
            index=1,  # Default to Top 10
            key="quick_select_intel"
        )
        
        if quick_select_intel == "Top 20 por valor":
            default_intel = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(20).index.tolist()
        elif quick_select_intel == "Top 10 por valor":
            default_intel = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(10).index.tolist()
        elif quick_select_intel == "Top 5 por valor":
            default_intel = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(5).index.tolist()
        else:
            default_intel = []
        
        selected_investors_intel = st.multiselect(
            "🎯 Seleccionar inversores para análisis de inteligencia (máx. 30):",
            all_investors_intel,
            default=default_intel if len(all_investors_intel) >= len(default_intel) else all_investors_intel[:min(10, len(all_investors_intel))],
            max_selections=30,
            key="intel_investors",
            help="Estos inversores se usarán en todos los análisis de inteligencia de portafolio"
        )
    
    with col_intel2:
        st.metric("Inversores seleccionados", len(selected_investors_intel))
        if selected_investors_intel:
            total_positions = filtered_df[filtered_df['Investor'].isin(selected_investors_intel)]['Stock'].nunique()
            st.metric("Acciones únicas", total_positions)
    
    if not selected_investors_intel:
        st.warning("⚠️ Por favor selecciona al menos un inversor para el análisis de inteligencia.")
        st.stop()
    
    # Filter data for selected investors
    intel_df = filtered_df[filtered_df['Investor'].isin(selected_investors_intel)]
    
    st.markdown("---")
    
    # Create sub-tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["📊 Análisis de Concentración", "🎯 Puntuación de Diversidad", "🔮 Reconocimiento de Patrones"])
    
    with tab1:
        st.markdown("### 📊 Análisis Multidimensional de Inversores")
        
        # Refine selection for radar chart from pre-selected investors
        col_radar1, col_radar2 = st.columns([3, 1])
        
        with col_radar1:
            selected_radar = st.multiselect(
                "🎯 Refinar selección para gráfico radar (máx. 8):",
                selected_investors_intel,
                default=selected_investors_intel[:min(6, len(selected_investors_intel))],
                max_selections=8,
                key="radar_investors",
                help="Selecciona hasta 8 inversores del grupo principal para comparación multidimensional"
            )
        
        with col_radar2:
            st.metric("Inversores en radar", len(selected_radar))
            if selected_radar:
                st.caption("✨ Comparación visual de perfiles de inversión")
        
        with st.expander("ℹ️ Cómo leer este gráfico radar"):
            st.markdown("""
            **Propósito:** Comparar múltiples inversores en 5 dimensiones clave simultáneamente.
            
            **Dimensiones explicadas:**
            - **Posiciones:** Número de acciones diferentes (escalado a 100)
            - **Top1:** Posición más grande como % de cartera
            - **Pos. Promedio:** Tamaño promedio de posición (escalado)
            - **Actividad Compra:** % de posiciones siendo compradas/añadidas
            - **Valor:** Valor total de cartera (escalado)
            
            **Cómo interpretar:** Área más grande = enfoque más agresivo/concentrado. Formas balanceadas sugieren estrategias diversificadas.
            
            **Tip:** Selecciona hasta 8 inversores para una comparación clara.
            """)
        
        if selected_radar:
            # Create radar chart for selected investors using intel_df
            radar_data = []
            for investor in selected_radar:
                investor_df = intel_df[intel_df['Investor'] == investor]
                if not investor_df.empty:
                    max_stocks = investor_df['Stock'].nunique()
                    max_portfolio = investor_df['% of Portfolio'].max()
                    mean_portfolio = investor_df['% of Portfolio'].mean()
                    buy_add_count = (investor_df['Activity_Type'].isin(['Compra', 'Añadir'])).sum()
                    total_count = len(investor_df)
                    total_value = investor_df['Value_Clean'].sum()
                    
                    radar_data.append({
                        'Investor': investor,
                        'Posiciones': min((max_stocks / 50) * 100, 100) if max_stocks > 0 else 0,
                        'Top1': max_portfolio if max_portfolio > 0 else 0,
                        'Pos_Promedio': (mean_portfolio * 10) if mean_portfolio > 0 else 0,
                        'Actividad_Compra': (buy_add_count / total_count * 100) if total_count > 0 else 0,
                        'Valor': min(total_value / 1e8, 100) if total_value > 0 else 0
                    })
            
            if radar_data:
                fig_radar = go.Figure()
                
                categories = ['Posiciones', 'Top1', 'Pos_Promedio', 'Actividad_Compra', 'Valor']
                
                for item in radar_data:
                    fig_radar.add_trace(go.Scatterpolar(
                        r=[item.get(cat, 0) for cat in categories],
                        theta=categories,
                        fill='toself',
                        name=item['Investor'][:25]
                    ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )),
                    showlegend=True,
                    title=f"Comparación de Perfiles - {len(selected_radar)} Inversores",
                    height=600,
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig_radar, use_container_width=True)
            else:
                st.info("No hay datos disponibles para los inversores seleccionados")
        else:
            st.warning("Por favor selecciona al menos un inversor para el análisis radar")
    
    with tab2:
        st.markdown("### 🎯 Análisis de Diversidad de Cartera")
        
        # Optionally refine selection for diversity analysis
        selected_investors_div = st.multiselect(
            "Refinar selección para análisis de diversidad (opcional):",
            selected_investors_intel,
            default=selected_investors_intel,
            key="diversity_investors",
            help="Puedes refinar la selección del grupo principal si lo deseas"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("ℹ️ Entendiendo la Puntuación de Diversidad"):
                st.markdown("""
                **¿Qué es la Puntuación de Diversidad?**
                Una métrica compuesta (0-100) que mide qué tan diversificada está la cartera de un inversor.
                
                **Componentes:**
                - 40% - Número de posiciones
                - 30% - Inverso de concentración (HHI)
                - 30% - Inverso de concentración Top 5
                
                **Interpretación:**
                - 80-100: Altamente diversificado
                - 60-80: Moderadamente diversificado
                - 40-60: Concentrado
                - <40: Altamente concentrado
                """)
            
            # Calculate diversity score for selected investors
            if selected_investors_div:
                div_df = intel_df[intel_df['Investor'].isin(selected_investors_div)]
                diversity_scores = div_df.groupby('Investor').apply(
                    lambda x: pd.Series({
                        'Num_Acciones': x['Stock'].nunique(),
                        'HHI': (x['% of Portfolio'] ** 2).sum(),  # Herfindahl index
                        'Concentracion_Top5': x.nlargest(5, '% of Portfolio')['% of Portfolio'].sum()
                    })
                ).reset_index()
                
                if not diversity_scores.empty:
                    max_num = diversity_scores['Num_Acciones'].max()
                    max_num = max_num if max_num > 0 else 1
                    
                    # Calculate diversity score safely
                    diversity_scores['Puntuacion_Diversidad'] = 0  # Initialize
                    if max_num > 0:
                        num_component = (diversity_scores['Num_Acciones'] / max_num) * 40
                        hhi_component = ((1 - diversity_scores['HHI'].clip(upper=10000) / 10000) * 100) * 30
                        top5_component = ((100 - diversity_scores['Concentracion_Top5'].clip(upper=100)) / 100 * 100) * 30
                        
                        diversity_scores['Puntuacion_Diversidad'] = num_component + hhi_component + top5_component
                    
                    fig_diversity = px.scatter(
                        diversity_scores,
                        x='Num_Acciones',
                        y='Puntuacion_Diversidad',
                        size='Concentracion_Top5',
                        color='Puntuacion_Diversidad',
                        hover_data=['Investor'],
                        color_continuous_scale='Turbo',
                        title=f'Panorama de Diversidad - {len(selected_investors_div)} Inversores Seleccionados',
                        labels={'Num_Acciones': 'Número de Posiciones', 'Puntuacion_Diversidad': 'Puntuación de Diversidad (0-100)'}
                    )
                    
                    fig_diversity.update_layout(
                        height=500,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                    )
                    
                    st.plotly_chart(fig_diversity, use_container_width=True)
                else:
                    st.info("No hay datos de diversidad disponibles para los inversores seleccionados")
            else:
                st.warning("Por favor selecciona al menos un inversor para el análisis de diversidad")
        
        with col2:
            st.markdown("### 📊 Distribución de Concentración")
            
            # Use pre-selected investors for box plot
            selected_investors_box = st.multiselect(
                "Refinar selección para distribución (opcional):",
                selected_investors_intel,
                default=selected_investors_intel[:min(10, len(selected_investors_intel))],
                max_selections=15,
                key="box_investors",
                help="Refina la selección para el diagrama de caja"
            )
            
            with st.expander("ℹ️ Cómo leer este gráfico"):
                st.markdown("""
                **Propósito:** Muestra qué tan concentradas están las carteras de diferentes inversores.
                
                **Elementos del diagrama de caja:**
                - Caja: 50% medio de las posiciones
                - Línea en la caja: Tamaño mediano de posición
                - Bigotes: Rango de posiciones
                - Puntos: Posiciones atípicas
                
                **Por qué importa:** Muestra si un inversor tiene pocas apuestas grandes o muchas posiciones iguales.
                """)
            
            # Box plot for selected investors
            if selected_investors_box:
                box_data = intel_df[intel_df['Investor'].isin(selected_investors_box)]
                
                fig_box = px.box(
                    box_data,
                    x='Investor',
                    y='% of Portfolio',
                    color='Investor',
                    title=f'Distribución del Tamaño de Posición - {len(selected_investors_box)} Inversores Seleccionados'
                )
                
                fig_box.update_layout(
                    height=500,
                    showlegend=False,
                    xaxis_tickangle=-45,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=9)
                )
                
                st.plotly_chart(fig_box, use_container_width=True)
            else:
                st.warning("Por favor selecciona al menos un inversor para ver la distribución")
    
    with tab3:
        st.markdown("### 🔮 Reconocimiento de Patrones de Trading")
        
        # Use pre-selected investors for trading patterns
        selected_investors_pattern = st.multiselect(
            "Refinar selección para análisis de patrones (opcional):",
            selected_investors_intel,
            default=selected_investors_intel,
            key="pattern_investors",
            help="Refina la selección para el análisis de patrones de trading"
        )
        
        with st.expander("ℹ️ Entendiendo los Patrones de Trading"):
            st.markdown("""
            **Puntuación de Agresividad:** Porcentaje de posiciones siendo compradas o añadidas (vs vendidas/mantenidas).
            
            **Interpretación:**
            - >70%: Muy alcista, comprando activamente
            - 50-70%: Moderadamente alcista
            - 30-50%: Enfoque balanceado
            - <30%: Defensivo, reduciendo posiciones
            
            **Caso de uso:** Identificar qué inversores tienen más confianza en las condiciones actuales del mercado.
            """)
        
        # Analyze trading patterns for selected investors
        if selected_investors_pattern:
            pattern_df = intel_df[intel_df['Investor'].isin(selected_investors_pattern)]
            if not pattern_df.empty:
                pattern_data = pattern_df.groupby(['Investor', 'Activity_Type']).size().unstack(fill_value=0)
                
                if not pattern_data.empty:
                    # Calculate aggressiveness safely
                    total_sum = pattern_data.sum(axis=1)
                    total_sum = total_sum.replace(0, 1)  # Avoid division by zero
                    pattern_data['Agresividad'] = (pattern_data.get('Compra', 0) + pattern_data.get('Añadir', 0)) / total_sum * 100
                    pattern_data = pattern_data.sort_values('Agresividad', ascending=False)
                    
                    fig_pattern = px.bar(
                        pattern_data.reset_index(),
                        x='Investor',
                        y='Agresividad',
                        color='Agresividad',
                        color_continuous_scale='RdYlGn',
                        title=f'Puntuación de Agresividad en Trading - {len(selected_investors_pattern)} Inversores Seleccionados',
                        labels={'Agresividad': 'Puntuación de Agresividad (%)'}
                    )
                    
                    fig_pattern.update_layout(
                        height=500,
                        xaxis_tickangle=-45,
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white', size=10)
                    )
                    
                    st.plotly_chart(fig_pattern, use_container_width=True)
                else:
                    st.info("No hay datos de patrones disponibles")
            else:
                st.info("No hay datos disponibles para los inversores seleccionados")
        else:
            st.warning("Por favor selecciona al menos un inversor para ver los patrones de trading")

elif view_mode == "🔥 Matriz de Acciones Calientes":
    st.markdown("## 🔥 Matriz Avanzada de Acciones Calientes", unsafe_allow_html=True)
    
    with st.expander("📚 Entendiendo la Puntuación de Calor"):
        st.markdown("""
        **Componentes de la Puntuación de Calor (0-100):**
        - 30% - Número de inversores que poseen la acción
        - 25% - Valor total invertido en todas las carteras
        - 20% - Peso promedio en cartera
        - 15% - Actividad reciente de compra (conteo Compra/Añadir)
        - 10% - Tamaño máximo de posición en cualquier cartera
        
        **Interpretación de la Puntuación:**
        - 80-100: 🔥 Extremadamente caliente - Fuerte consenso entre múltiples inversores
        - 60-80: 🌟 Muy atractiva - Interés significativo de varios inversores
        - 40-60: 📈 Interés moderado - Algunos inversores tomando posiciones
        - <40: 🔍 Selecciones de nicho - Poseída por pocos inversores o en posiciones pequeñas
        """)
    
    # Calculate comprehensive metrics - moved outside of heatmap section
    stock_metrics = filtered_df.groupby('Stock').agg({
        'Investor': 'nunique',
        'Value_Clean': 'sum',
        '% of Portfolio': ['mean', 'max'],
        'Activity_Type': lambda x: (x.isin(['Compra', 'Añadir'])).sum(),
        'Activity_Percentage': 'mean'
    })
    
    stock_metrics.columns = ['Num_Inversores', 'Valor_Total', 'Cartera_Promedio', 'Cartera_Max', 'Conteo_Compra_Añadir', 'Actividad_Promedio']
    
    # Calculate heat score with multiple factors
    if not stock_metrics.empty:
        max_investors = stock_metrics['Num_Inversores'].max() if stock_metrics['Num_Inversores'].max() > 0 else 1
        max_value = stock_metrics['Valor_Total'].max() if stock_metrics['Valor_Total'].max() > 0 else 1
        max_avg = stock_metrics['Cartera_Promedio'].max() if stock_metrics['Cartera_Promedio'].max() > 0 else 1
        max_count = stock_metrics['Conteo_Compra_Añadir'].max() if stock_metrics['Conteo_Compra_Añadir'].max() > 0 else 1
        max_max = stock_metrics['Cartera_Max'].max() if stock_metrics['Cartera_Max'].max() > 0 else 1
        
        stock_metrics['Puntuacion_Calor'] = (
            stock_metrics['Num_Inversores'] / max_investors * 30 +
            stock_metrics['Valor_Total'] / max_value * 25 +
            stock_metrics['Cartera_Promedio'] / max_avg * 20 +
            stock_metrics['Conteo_Compra_Añadir'] / max_count * 15 +
            stock_metrics['Cartera_Max'] / max_max * 10
        ) * 100
    else:
        stock_metrics['Puntuacion_Calor'] = 0
    
    hot_stocks = stock_metrics.sort_values('Puntuacion_Calor', ascending=False).head(30)
    
    # Create 3D bubble chart
    st.markdown("### 🌐 Universo 3D de Acciones Calientes")
    with st.expander("ℹ️ Cómo navegar este gráfico 3D"):
        st.markdown("""
        **Ejes:**
        - Eje X: Número de inversores que poseen la acción
        - Eje Y: Porcentaje promedio en cartera
        - Eje Z: Valor total invertido
        
        **Elementos visuales:**
        - Tamaño de burbuja: Puntuación de calor (más grande = más caliente)
        - Color: Intensidad de puntuación de calor (rojo = más caliente)
        
        **Interacción:**
        - Arrastra para rotar la vista 3D
        - Scroll para acercar/alejar
        - Pasa el mouse sobre las burbujas para detalles
        
        **Qué buscar:**
        - Cuadrante superior derecho: Ampliamente poseída con alta convicción
        - Burbujas rojas grandes: Acciones calientes de consenso
        - Valores atípicos: Apuestas únicas de alta convicción
        """)
    
    if not hot_stocks.empty:
        fig_3d_bubble = px.scatter_3d(
            hot_stocks.reset_index(),
            x='Num_Inversores',
            y='Cartera_Promedio',
            z='Valor_Total',
            size='Puntuacion_Calor',
            color='Puntuacion_Calor',
            hover_data=['Stock', 'Conteo_Compra_Añadir'],
            color_continuous_scale='Hot_r',
            title='Análisis Interactivo 3D de Acciones Calientes'
        )
        
        fig_3d_bubble.update_layout(
            scene=dict(
                xaxis_title='Número de Inversores',
                yaxis_title='% Promedio en Cartera',
                zaxis_title='Valor Total ($)',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.3))
            ),
            height=700,
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_3d_bubble, use_container_width=True)
    else:
        st.info("No hay suficientes datos para mostrar el gráfico 3D de acciones calientes")
    
    # Heatmap of top stocks vs selected investors
    st.markdown("### 🌡️ Matriz de Propiedad Acción-Inversor")
    
    # Add investor selection for heatmap
    col_hm1, col_hm2 = st.columns([3, 1])
    
    with col_hm1:
        all_investors_hm = sorted(filtered_df['Investor'].unique())
        default_hm = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(15).index.tolist()
        
        selected_investors_hm = st.multiselect(
            "🎯 Seleccionar inversores para el mapa de calor:",
            all_investors_hm,
            default=default_hm if len(all_investors_hm) >= 15 else all_investors_hm[:min(15, len(all_investors_hm))],
            max_selections=20,
            key="heatmap_investors",
            help="Selecciona qué inversores quieres ver en el mapa de calor"
        )
    
    with col_hm2:
        num_stocks_hm = st.slider(
            "Top acciones a mostrar",
            min_value=10,
            max_value=30,
            value=20,
            step=5,
            help="Número de acciones calientes a mostrar"
        )
    
    with st.expander("ℹ️ Cómo leer el mapa de calor"):
        st.markdown("""
        **Propósito:** Muestra qué inversores poseen qué acciones calientes y en qué concentración.
        
        **Escala de color:**
        - Azul oscuro/morado: No poseída o posición muy pequeña
        - Verde/amarillo: Posición moderada (2-5%)
        - Naranja/rojo: Posición grande (>5%)
        - Rojo brillante: Posición muy concentrada (>10%)
        
        **Cómo usar:**
        - Encuentra patrones donde múltiples inversores poseen la misma acción
        - Identifica selecciones únicas (celda brillante única en una fila)
        - Compara tamaños de posición entre inversores
        
        **Consejo pro:** Acciones con muchas celdas naranjas/rojas entre diferentes inversores indican fuerte consenso.
        """)
    
    if selected_investors_hm and not hot_stocks.empty:
        top_stocks_hm = hot_stocks.head(num_stocks_hm).index
        
        heatmap_data = filtered_df[
            (filtered_df['Stock'].isin(top_stocks_hm)) & 
            (filtered_df['Investor'].isin(selected_investors_hm))
        ].pivot_table(
            values='% of Portfolio',
            index='Stock',
            columns='Investor',
            fill_value=0
        )
        
        if not heatmap_data.empty:
            fig_heatmap = px.imshow(
                heatmap_data,
                color_continuous_scale='Turbo',
                title=f'Mapa de Calor - Top {num_stocks_hm} Acciones vs {len(selected_investors_hm)} Inversores Seleccionados',
                labels=dict(color="% Cartera"),
                aspect='auto'
            )
            
            fig_heatmap.update_layout(
                height=600,
                xaxis_tickangle=-45,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=9)
            )
            
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Show some statistics
            st.caption(f"💡 Mostrando {len(heatmap_data.columns)} inversores × {len(heatmap_data.index)} acciones = {len(heatmap_data.columns) * len(heatmap_data.index)} posibles posiciones")
        else:
            st.info("No hay datos disponibles para el mapa de calor con los inversores seleccionados")
    else:
        st.warning("Por favor selecciona al menos un inversor para el mapa de calor")

elif view_mode == "📊 Análisis Avanzado":
    st.markdown("## 📊 Análisis Estadístico Avanzado", unsafe_allow_html=True)
    
    # Add investor selection for all advanced analysis
    st.markdown("### 🎯 Selección de Inversores para Análisis")
    col_sel1, col_sel2 = st.columns([3, 1])
    
    with col_sel1:
        all_investors_adv = sorted(filtered_df['Investor'].unique())
        
        # Quick selection options
        quick_select_adv = st.radio(
            "Selección rápida:",
            ["Top 20 por valor", "Top 10 por valor", "Top 5 por valor", "Personalizado"],
            horizontal=True,
            index=0,
            key="quick_select_advanced"
        )
        
        if quick_select_adv == "Top 20 por valor":
            default_adv = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(20).index.tolist()
        elif quick_select_adv == "Top 10 por valor":
            default_adv = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(10).index.tolist()
        elif quick_select_adv == "Top 5 por valor":
            default_adv = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(5).index.tolist()
        else:
            default_adv = []
        
        selected_investors_adv = st.multiselect(
            "🎯 Seleccionar inversores para análisis avanzado (máx. 30):",
            all_investors_adv,
            default=default_adv if len(all_investors_adv) >= len(default_adv) else all_investors_adv[:min(20, len(all_investors_adv))],
            max_selections=30,
            key="advanced_investors",
            help="Estos inversores se usarán en todos los gráficos de análisis avanzado"
        )
    
    with col_sel2:
        st.metric("Inversores seleccionados", len(selected_investors_adv))
        if selected_investors_adv:
            total_value_selected = filtered_df[filtered_df['Investor'].isin(selected_investors_adv)]['Value_Clean'].sum() / 1e9
            st.metric("Valor total", f"${total_value_selected:.1f}B")
    
    if not selected_investors_adv:
        st.warning("⚠️ Por favor selecciona al menos un inversor para el análisis avanzado.")
        st.stop()
    
    # Filter data for selected investors
    analysis_df = filtered_df[filtered_df['Investor'].isin(selected_investors_adv)]
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📈 Análisis de Tendencias", "🔄 Matriz de Correlación", "📊 Patrones de Actividad"])
    
    with tab1:
        st.markdown("### 📈 Análisis de Sentimiento Compra/Venta")
        with st.expander("ℹ️ Entendiendo este gráfico"):
            st.markdown("""
            **Qué muestra:** Relación entre nivel de actividad de trading y sentimiento alcista.
            
            **Ejes:**
            - Eje X: Número total de acciones de trading (compras, añadidos, reducciones)
            - Eje Y: Ratio de compra (% de acciones que son alcistas)
            
            **Interpretación:**
            - Superior derecha: Muy activo y alcista (compra agresiva)
            - Superior izquierda: Selectivo pero alcista (calidad sobre cantidad)
            - Inferior derecha: Activo pero defensivo (reduciendo posiciones)
            - Inferior izquierda: Inactivo o manteniendo
            
            **Tamaño de burbuja:** Representa el número total de acciones
            """)
        
        # Create activity timeline using selected investors
        activity_summary = analysis_df.groupby(['Investor', 'Activity_Type']).size().unstack(fill_value=0)
        
        # Calculate trend metrics
        if not activity_summary.empty:
            trend_data = pd.DataFrame({
                'Inversor': activity_summary.index,
                'Ratio_Compra': ((activity_summary.get('Compra', 0) + activity_summary.get('Añadir', 0)) / 
                                (activity_summary.sum(axis=1).replace(0, 1)) * 100),
                'Acciones_Totales': activity_summary.sum(axis=1)
            })
            
            if not trend_data.empty and len(trend_data) > 0:
                fig_trend = px.scatter(
                    trend_data,
                    x='Acciones_Totales',
                    y='Ratio_Compra',
                    size='Acciones_Totales',
                    color='Ratio_Compra',
                    hover_data=['Inversor'],
                    color_continuous_scale='RdYlGn',
                    title=f'Sentimiento Compra/Añadir vs Nivel de Actividad - {len(selected_investors_adv)} Inversores',
                    labels={'Ratio_Compra': 'Actividad Alcista (%)', 'Acciones_Totales': 'Número de Acciones'}
                )
                
                # Add quadrant lines if we have data
                if len(trend_data['Acciones_Totales']) > 0:
                    fig_trend.add_hline(y=50, line_dash="dash", line_color="gray", opacity=0.5)
                    median_val = trend_data['Acciones_Totales'].median()
                    if pd.notna(median_val):
                        fig_trend.add_vline(x=median_val, line_dash="dash", line_color="gray", opacity=0.5)
                
                fig_trend.update_layout(
                    height=500,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.info("No hay suficientes datos para el análisis de tendencias")
        else:
            st.info("No hay datos disponibles para el análisis de tendencias con los inversores seleccionados")
    
    with tab2:
        st.markdown("### 🔄 Correlación de Carteras de Inversores")
        
        # Use the pre-selected investors but allow further filtering
        col_select1, col_select2 = st.columns([3, 1])
        with col_select1:
            selected_investors_corr = st.multiselect(
                "Refinar selección para matriz de correlación (opcional):",
                selected_investors_adv,
                default=selected_investors_adv[:15] if len(selected_investors_adv) >= 15 else selected_investors_adv,
                key="corr_investors",
                help="Puedes refinar la selección para la matriz de correlación si hay demasiados inversores"
            )
        with col_select2:
            min_common = st.number_input(
                "Mín. acciones comunes",
                min_value=1,
                max_value=50,
                value=5,
                help="Número mínimo de acciones comunes para mostrar correlación"
            )
        
        with st.expander("ℹ️ Cómo interpretar la correlación"):
            st.markdown("""
            **Qué muestra:** Qué tan similares son las carteras de diferentes inversores basándose en posiciones comunes y pesos.
            
            **Escala de color:**
            - Rojo intenso (1.0): Correlación perfecta - carteras idénticas
            - Rojo claro (0.5-1.0): Alta similitud
            - Blanco (0): Sin correlación
            - Azul claro (-0.5-0): Relación inversa
            - Azul intenso (-1.0): Posiciones completamente opuestas
            
            **Casos de uso:**
            - Encontrar inversores con estrategias similares
            - Identificar inversores contrarios
            - Descubrir enfoques de inversión únicos
            
            **Nota:** Alta correlación no significa copiar, podría indicar principios similares de inversión en valor.
            """)
        
        if selected_investors_corr and len(selected_investors_corr) >= 2:
            # Create correlation matrix based on selected investors - using analysis_df
            corr_pivot = analysis_df[analysis_df['Investor'].isin(selected_investors_corr)].pivot_table(
                values='% of Portfolio',
                index='Stock',
                columns='Investor',
                fill_value=0
            )
            
            # Filter for minimum common stocks
            if not corr_pivot.empty:
                stock_counts = (corr_pivot > 0).sum(axis=1)
                stocks_with_min = stock_counts[stock_counts >= min_common].index
                if len(stocks_with_min) > 0:
                    corr_pivot_filtered = corr_pivot.loc[stocks_with_min]
                else:
                    corr_pivot_filtered = corr_pivot
                
                if not corr_pivot_filtered.empty:
                    correlation_matrix = corr_pivot_filtered.corr()
                    
                    fig_corr = px.imshow(
                        correlation_matrix,
                        color_continuous_scale='RdBu',
                        title=f'Matriz de Similitud de Carteras ({len(selected_investors_corr)} inversores seleccionados)',
                        labels=dict(color="Correlación"),
                        zmin=-1,
                        zmax=1
                    )
                    
                    # Add text annotations for values
                    fig_corr.update_traces(text=np.round(correlation_matrix.values, 2), texttemplate='%{text}')
                    
                    fig_corr.update_layout(
                        height=600,
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                    )
                    
                    st.plotly_chart(fig_corr, use_container_width=True)
                    
                    # Show statistics with better error handling
                    col1_stats, col2_stats, col3_stats = st.columns(3)
                    with col1_stats:
                        st.metric("Inversores analizados", len(selected_investors_corr))
                    with col2_stats:
                        if correlation_matrix.size > 0:
                            mask = np.ones(correlation_matrix.shape, dtype=bool)
                            np.fill_diagonal(mask, False)
                            non_diag = correlation_matrix.values[mask]
                            if len(non_diag) > 0:
                                avg_corr = np.nanmean(non_diag)
                                st.metric("Correlación promedio", f"{avg_corr:.3f}")
                            else:
                                st.metric("Correlación promedio", "N/A")
                        else:
                            st.metric("Correlación promedio", "N/A")
                    with col3_stats:
                        if correlation_matrix.size > 0:
                            mask = np.ones(correlation_matrix.shape, dtype=bool)
                            np.fill_diagonal(mask, False)
                            non_diag = correlation_matrix.values[mask]
                            if len(non_diag) > 0:
                                max_corr = np.nanmax(non_diag)
                                st.metric("Correlación máxima", f"{max_corr:.3f}")
                            else:
                                st.metric("Correlación máxima", "N/A")
                        else:
                            st.metric("Correlación máxima", "N/A")
                else:
                    st.info("No hay suficientes datos para calcular correlaciones")
            else:
                st.info("No hay datos disponibles para análisis de correlación")
        else:
            st.warning("Por favor selecciona al menos 2 inversores para el análisis de correlación")
    
    with tab3:
        st.markdown("### 📊 Distribución de Actividad por Tipo de Inversor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🎯 Desglose de Actividad")
            with st.expander("ℹ️ Qué muestra esto"):
                st.markdown("""
                **Propósito:** Comparar cómo están posicionados diferentes inversores.
                
                **Categorías:**
                - **Compradores:** >70% actividad compra/añadir
                - **Balanceados:** 30-70% actividad compra/añadir  
                - **Vendedores:** <30% actividad compra/añadir
                
                **Por qué importa:** Muestra el sentimiento del mercado entre superinversores.
                """)
            
            # Categorize investors using selected data
            if not analysis_df.empty:
                investor_activity = analysis_df.groupby('Investor')['Activity_Type'].apply(
                    lambda x: 'Compradores' if (x.isin(['Compra', 'Añadir'])).mean() > 0.7 
                    else 'Vendedores' if (x.isin(['Compra', 'Añadir'])).mean() < 0.3 
                    else 'Balanceados'
                ).value_counts()
                
                if not investor_activity.empty:
                    fig_activity_pie = px.pie(
                        values=investor_activity.values,
                        names=investor_activity.index,
                        color_discrete_map={
                            'Compradores': '#10B981',
                            'Balanceados': '#60A5FA',
                            'Vendedores': '#F87171'
                        },
                        title='Posicionamiento de Inversores',
                        hole=0.4
                    )
                    
                    fig_activity_pie.update_layout(
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                    )
                    
                    st.plotly_chart(fig_activity_pie, use_container_width=True)
                else:
                    st.info("No hay datos de actividad disponibles")
            else:
                st.info("No hay datos para analizar")
        
        with col2:
            st.markdown("#### 📈 Tendencias de Concentración")
            with st.expander("ℹ️ Entendiendo la concentración"):
                st.markdown("""
                **Qué muestra:** Distribución de niveles de concentración de cartera.
                
                **Categorías:**
                - **Concentrado:** Top 5 posiciones >60%
                - **Moderado:** Top 5 posiciones 40-60%
                - **Diversificado:** Top 5 posiciones <40%
                
                **Perspectiva:** Muestra apetito de riesgo y niveles de convicción.
                """)
            
            # Concentration categories using selected investors
            if not analysis_df.empty:
                concentration_cats = analysis_df.groupby('Investor')['% of Portfolio'].apply(
                    lambda x: 'Concentrado' if x.nlargest(5).sum() > 60
                    else 'Diversificado' if x.nlargest(5).sum() < 40
                    else 'Moderado'
                ).value_counts()
                
                if not concentration_cats.empty:
                    fig_conc_pie = px.pie(
                        values=concentration_cats.values,
                        names=concentration_cats.index,
                        color_discrete_map={
                            'Concentrado': '#F87171',
                            'Moderado': '#60A5FA',
                            'Diversificado': '#10B981'
                        },
                        title='Estilos de Concentración de Cartera',
                        hole=0.4
                    )
                    
                    fig_conc_pie.update_layout(
                        height=400,
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                    )
                    
                    st.plotly_chart(fig_conc_pie, use_container_width=True)
                else:
                    st.info("No hay datos de concentración disponibles")
            else:
                st.info("No hay datos para analizar")

elif view_mode == "🕸️ Análisis de Red":
    st.markdown("## 🕸️ Análisis de Red de Inversores", unsafe_allow_html=True)
    
    # Add investor selection for network analysis
    st.markdown("### 🎯 Selección de Inversores para Análisis de Red")
    col_net1, col_net2 = st.columns([3, 1])
    
    with col_net1:
        all_investors_net = sorted(filtered_df['Investor'].unique())
        
        # Quick selection options
        quick_select_net = st.radio(
            "Selección rápida:",
            ["Top 20 por valor", "Top 15 por valor", "Top 10 por valor", "Personalizado"],
            horizontal=True,
            index=0,
            key="quick_select_network"
        )
        
        if quick_select_net == "Top 20 por valor":
            default_net = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(20).index.tolist()
        elif quick_select_net == "Top 15 por valor":
            default_net = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(15).index.tolist()
        elif quick_select_net == "Top 10 por valor":
            default_net = filtered_df.groupby('Investor')['Value_Clean'].sum().nlargest(10).index.tolist()
        else:
            default_net = []
        
        selected_investors_net = st.multiselect(
            "🎯 Seleccionar inversores para análisis de red (máx. 25):",
            all_investors_net,
            default=default_net if len(all_investors_net) >= len(default_net) else all_investors_net[:min(20, len(all_investors_net))],
            max_selections=25,
            key="network_investors",
            help="Selecciona los inversores para ver sus conexiones basadas en posiciones comunes"
        )
    
    with col_net2:
        st.metric("Inversores seleccionados", len(selected_investors_net))
        min_common_stocks = st.number_input(
            "Mín. acciones comunes",
            min_value=1,
            max_value=10,
            value=2,
            help="Número mínimo de acciones comunes para mostrar conexión"
        )
    
    if not selected_investors_net:
        st.warning("⚠️ Por favor selecciona al menos 2 inversores para el análisis de red.")
        st.stop()
    elif len(selected_investors_net) < 2:
        st.warning("⚠️ Necesitas al menos 2 inversores para ver conexiones de red.")
        st.stop()
    
    # Filter data for selected investors
    network_df = filtered_df[filtered_df['Investor'].isin(selected_investors_net)]
    
    st.markdown("---")
    
    st.markdown("### 🌐 Red de Posiciones Comunes")
    
    with st.expander("📚 Entendiendo el Diagrama de Red"):
        st.markdown("""
        **¿Qué es un Diagrama Sankey?**
        Esta visualización muestra conexiones entre inversores basadas en acciones comunes.
        
        **Cómo leerlo:**
        - **Nodos (rectángulos):** Inversores individuales
        - **Flujos (conexiones):** Número de posiciones comunes entre inversores
        - **Grosor del flujo:** Más acciones comunes = conexión más gruesa
        - **Intensidad del color:** Relaciones más fuertes = flujos más oscuros
        
        **Qué revela:**
        - **Grupos de inversión:** Grupos de inversores con estrategias similares
        - **Enfoques únicos:** Inversores con pocas conexiones tienen carteras distintivas
        - **Selecciones de consenso:** Flujos gruesos indican muchas posiciones compartidas
        
        **Ejemplo de interpretación:**
        Si Buffett y Munger tienen una conexión gruesa, comparten muchas posiciones, sugiriendo principios de valor similares.
        
        **Características interactivas:**
        - Pasa el mouse sobre los flujos para ver el número de posiciones comunes
        - Arrastra los nodos para reorganizar la visualización
        """)
    
    # Find stocks held by multiple investors among selected
    multi_investor_stocks = network_df.groupby('Stock')['Investor'].nunique()
    multi_investor_stocks = multi_investor_stocks[multi_investor_stocks >= 2].index
    
    if len(multi_investor_stocks) == 0:
        st.warning("No se encontraron posiciones comunes entre los inversores seleccionados.")
    else:
        network_data = network_df[network_df['Stock'].isin(multi_investor_stocks)]
        
        # Create chord diagram data with selected investors
        chord_data = []
        investors = selected_investors_net  # Use the selected investors
        
        for i, inv1 in enumerate(investors):
            for j, inv2 in enumerate(investors):
                if i < j:
                    inv1_stocks = set(network_data[network_data['Investor'] == inv1]['Stock'])
                    inv2_stocks = set(network_data[network_data['Investor'] == inv2]['Stock'])
                    common = len(inv1_stocks.intersection(inv2_stocks))
                    if common >= min_common_stocks:  # Use the minimum threshold
                        chord_data.append({'source': inv1, 'target': inv2, 'value': common})
        
        # Create Sankey diagram
        chord_df = pd.DataFrame(chord_data)
        
        if not chord_df.empty:
            st.caption(f"📊 Mostrando {len(chord_df)} conexiones con al menos {min_common_stocks} acciones comunes entre {len(selected_investors_net)} inversores")
            
            # Get unique nodes
            nodes = list(set(chord_df['source'].unique()) | set(chord_df['target'].unique()))
            node_indices = {node: i for i, node in enumerate(nodes)}
            
            fig_sankey = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=nodes,
                    color='rgba(102, 126, 234, 0.8)'
                ),
                link=dict(
                    source=[node_indices[s] for s in chord_df['source']],
                    target=[node_indices[t] for t in chord_df['target']],
                    value=chord_df['value'],
                    color='rgba(102, 126, 234, 0.3)',
                    label=chord_df['value'].astype(str) + ' acciones comunes'
                )
            )])
            
            fig_sankey.update_layout(
                title="Red de Posiciones Comunes entre Inversores",
                height=700,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=10)
            )
            
            st.plotly_chart(fig_sankey, use_container_width=True)
            
            # Show statistics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Conexiones Totales", len(chord_df))
            
            with col2:
                if len(chord_df) > 0:
                    avg_common = chord_df['value'].mean()
                    st.metric("Promedio Posiciones Comunes", f"{avg_common:.1f}")
                else:
                    st.metric("Promedio Posiciones Comunes", "0")
            
            with col3:
                if not chord_df.empty:
                    max_common = chord_df.nlargest(1, 'value')
                    if not max_common.empty:
                        st.metric("Par Más Similar", f"{max_common['value'].values[0]} acciones")
                        st.caption(f"{max_common['source'].values[0][:15]} & {max_common['target'].values[0][:15]}")
                    else:
                        st.metric("Par Más Similar", "N/A")
                else:
                    st.metric("Par Más Similar", "N/A")
        else:
            st.info(f"No se encontraron conexiones entre los inversores seleccionados con al menos {min_common_stocks} acciones comunes.")
            st.info("💡 Intenta reducir el número mínimo de acciones comunes o seleccionar diferentes inversores.")

elif view_mode == "👤 Análisis Individual":
    # Individual investor analysis with advanced visualizations
    investor_df = filtered_df[filtered_df['Investor'] == selected_investor].copy()
    
    st.markdown(f"## 🎭 {selected_investor} - Análisis Completo de Cartera", unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Posiciones", f"{len(investor_df)}")
    with col2:
        if not investor_df.empty:
            total_value = investor_df['Value_Clean'].sum() / 1e6
        else:
            total_value = 0
        st.metric("Valor Cartera", f"${total_value:.1f}M")
    with col3:
        if not investor_df.empty:
            top_holding_df = investor_df.nlargest(1, '% of Portfolio')
            if not top_holding_df.empty:
                top_holding = top_holding_df['% of Portfolio'].values[0]
            else:
                top_holding = 0
        else:
            top_holding = 0
        st.metric("Top Posición", f"{top_holding:.1f}%")
    with col4:
        if not investor_df.empty:
            top5_df = investor_df.nlargest(5, '% of Portfolio')
            if not top5_df.empty:
                concentration = top5_df['% of Portfolio'].sum()
            else:
                concentration = 0
        else:
            concentration = 0
        st.metric("Conc. Top 5", f"{concentration:.1f}%")
    with col5:
        if len(investor_df) > 0:
            buy_ratio = (investor_df['Activity_Type'].isin(['Compra', 'Añadir'])).sum() / len(investor_df) * 100
        else:
            buy_ratio = 0
        st.metric("Ratio Compra/Añadir", f"{buy_ratio:.1f}%")
    
    st.markdown("---")
    
    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["🍩 Vista General de Cartera", "📊 Análisis de Posiciones", "🎯 Vista Treemap", "📈 Tabla de Posiciones"])
    
    with tab1:
        st.markdown("### 🍩 Composición de Cartera")
        with st.expander("ℹ️ Cómo leer este gráfico de dona"):
            st.markdown("""
            **Número central:** Número total de posiciones en la cartera
            
            **Segmentos:** Cada porción representa una posición de acciones
            - **Tamaño:** Porcentaje de cartera
            - **Etiquetas:** Ticker de acción y porcentaje
            
            **Interpretación:**
            - Porciones grandes (>10%): Posiciones de alta convicción
            - Muchas porciones pequeñas: Enfoque diversificado
            - Pocas porciones grandes: Cartera concentrada
            
            **Pasa el mouse:** Ver porcentajes y valores exactos
            """)
        
        if not investor_df.empty:
            # Enhanced donut chart
            fig_donut = px.pie(
                investor_df.nlargest(20, '% of Portfolio'),
                values='% of Portfolio',
                names='Stock',
                title=f'Distribución de Top 20 Posiciones',
                hole=0.6
            )
            
            fig_donut.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Cartera: %{percent}<br>Peso: %{value:.2f}%<extra></extra>'
            )
            
            # Add center text
            fig_donut.add_annotation(
                text=f"{len(investor_df)}<br>Posiciones",
                x=0.5, y=0.5,
                font=dict(size=20, color='white'),
                showarrow=False
            )
            
            fig_donut.update_layout(
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("Sin datos de posiciones disponibles para este inversor")
    
    with tab2:
        st.markdown("### 📊 Análisis de Tamaño de Posición y Actividad")
        
        # Add controls for chart display
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)
        with col_ctrl1:
            show_all_positions = st.checkbox("Mostrar todas las posiciones", value=False, help="Marca para ver todas las posiciones, desmarca para ver solo top 20")
        with col_ctrl2:
            if not show_all_positions:
                top_n_bar = 20
            else:
                top_n_bar = len(investor_df)
        with col_ctrl3:
            sort_by = st.selectbox(
                "Ordenar por:",
                ["% de Cartera", "Actividad Reciente", "Alfabético"],
                index=0
            )
        
        with st.expander("ℹ️ Entendiendo este gráfico"):
            st.markdown("""
            **Qué muestra:** Posiciones con sus pesos en cartera y actividad reciente
            
            **Código de colores:**
            - 🟢 Verde: Posiciones Compra/Añadir
            - 🔴 Rojo: Posiciones Reducir
            - ⚪ Gris: Posiciones Mantener
            
            **Cómo usar:** Identifica en qué posiciones el inversor es más alcista (verde) o bajista (rojo)
            """)
        
        if not investor_df.empty:
            # Sort based on selection
            if sort_by == "% de Cartera":
                sorted_df = investor_df.sort_values('% of Portfolio', ascending=False)
            elif sort_by == "Actividad Reciente":
                sorted_df = investor_df.sort_values(['Activity_Type', '% of Portfolio'], ascending=[True, False])
            else:
                sorted_df = investor_df.sort_values('Stock')
            
            # Select data based on checkbox
            if show_all_positions:
                chart_data = sorted_df
                title_text = f'Todas las {len(sorted_df)} Posiciones con Actividad Reciente'
            else:
                chart_data = sorted_df.head(20)
                title_text = 'Top 20 Posiciones con Actividad Reciente'
            
            # Create color mapping based on activity
            color_map = {
                'Compra': '#10B981',
                'Añadir': '#60A5FA',
                'Reducir': '#F87171',
                'Mantener': '#9CA3AF'
            }
            
            fig_bar = px.bar(
                chart_data,
                x='Stock',
                y='% of Portfolio',
                color='Activity_Type',
                title=title_text,
                color_discrete_map=color_map,
                hover_data=['Value', 'Shares', 'RecentActivity']
            )
            
            # Adjust layout based on number of positions
            fig_height = 500 if len(chart_data) <= 30 else 600
            
            fig_bar.update_layout(
                height=fig_height,
                xaxis_tickangle=-45,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=9 if len(chart_data) > 30 else 10),
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                xaxis=dict(
                    tickmode='linear' if len(chart_data) <= 30 else 'auto'
                )
            )
            
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Show summary statistics
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            with col_stat1:
                buys = len(investor_df[investor_df['Activity_Type'] == 'Compra'])
                st.metric("Compras", buys)
            with col_stat2:
                adds = len(investor_df[investor_df['Activity_Type'] == 'Añadir'])
                st.metric("Añadidos", adds)
            with col_stat3:
                reduces = len(investor_df[investor_df['Activity_Type'] == 'Reducir'])
                st.metric("Reducidos", reduces)
            with col_stat4:
                holds = len(investor_df[investor_df['Activity_Type'] == 'Mantener'])
                st.metric("Mantenidos", holds)
        else:
            st.info("Sin datos de posiciones disponibles")
    
    with tab3:
        st.markdown("### 🎯 Treemap Interactivo de Cartera")
        with st.expander("ℹ️ Cómo navegar el treemap"):
            st.markdown("""
            **Estructura:** Vista jerárquica de cartera organizada por tipo de actividad, luego acciones individuales
            
            **Elementos visuales:**
            - **Tamaño de caja:** Porcentaje de cartera (más grande = posición mayor)
            - **Intensidad de color:** Porcentaje de actividad (más rojo = más venta, más verde = más compra)
            
            **Interacción:**
            - Clic en cualquier caja para acercar
            - Clic en la barra superior para alejar
            
            **Perspectivas:** Identifica rápidamente las posiciones más grandes y sus patrones de actividad reciente
            """)
        
        if not investor_df.empty:
            # Treemap of portfolio
            fig_treemap = px.treemap(
                investor_df,
                path=['Activity_Type', 'Stock'],
                values='% of Portfolio',
                color='Activity_Percentage',
                color_continuous_scale='RdYlGn',
                title='Jerarquía de Cartera por Actividad'
            )
            
            fig_treemap.update_layout(
                height=600,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_treemap, use_container_width=True)
        else:
            st.info("Sin datos de posiciones disponibles")
    
    with tab4:
        st.markdown("### 📋 Tabla Detallada de Posiciones")
        with st.expander("ℹ️ Características de la tabla"):
            st.markdown("""
            **Columnas:**
            - **Stock:** Ticker y nombre de la empresa
            - **% Cartera:** Peso en cartera (con barra de progreso)
            - **Acciones:** Número de acciones poseídas
            - **Valor:** Valor en dólares de la posición
            - **Actividad Reciente:** Última acción de trading
            - **Tipo Actividad:** Actividad categorizada
            
            **Ordenamiento:** Clic en encabezados de columna para ordenar
            **Búsqueda:** Usa búsqueda del navegador (Ctrl+F) para encontrar acciones específicas
            """)
        
        if not investor_df.empty:
            # Enhanced table
            display_cols = ['Stock', '% of Portfolio', 'Shares', 'Value', 'RecentActivity', 'Activity_Type']
            display_df = investor_df[display_cols].sort_values('% of Portfolio', ascending=False)
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=500,
                hide_index=True,
                column_config={
                    "% of Portfolio": st.column_config.ProgressColumn(
                        "% Cartera",
                        format="%.2f%%",
                        min_value=0,
                        max_value=display_df['% of Portfolio'].max(),
                    ),
                    "Shares": st.column_config.NumberColumn(
                        "Acciones",
                        format="%d",
                    ),
                    "Activity_Type": st.column_config.TextColumn(
                        "Actividad",
                        help="Compra/Añadir/Reducir/Mantener"
                    )
                }
            )
        else:
            st.info("Sin datos de posiciones disponibles")

elif view_mode == "🎭 Análisis Comparativo":
    st.markdown("## 🎭 Análisis Comparativo de Carteras", unsafe_allow_html=True)
    
    if selected_investors:
        comparison_df = filtered_df[filtered_df['Investor'].isin(selected_investors)]
        
        if comparison_df.empty:
            st.warning("Sin datos disponibles para los inversores seleccionados con los filtros actuales.")
        else:
            # Comparison metrics
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📊 Comparación de Métricas de Cartera")
                with st.expander("ℹ️ Cómo leer este gráfico"):
                    st.markdown("""
                    **Qué muestra:** Comparación lado a lado de métricas clave de cartera
                    
                    **Métricas:**
                    - **Barras azules:** Número de acciones únicas (diversificación)
                    - **Barras rojas:** Valor total de cartera (escala)
                    
                    **Interpretación:**
                    - Barra azul ancha + barra roja estrecha = Muchas posiciones pequeñas
                    - Barra azul estrecha + barra roja ancha = Pocas posiciones grandes
                    - Anchos similares = Enfoque balanceado
                    """)
                
                # Portfolio size comparison
                portfolio_sizes = comparison_df.groupby('Investor').agg({
                    'Stock': 'nunique',
                    'Value_Clean': lambda x: x.sum() / 1e9  # Convert to billions
                }).reset_index()
                
                portfolio_sizes.columns = ['Inversor', 'Número de Posiciones', 'Valor de Cartera ($B)']
                
                fig_comparison = px.bar(
                    portfolio_sizes.melt(id_vars='Inversor'),
                    x='Inversor',
                    y='value',
                    color='variable',
                    title='Tamaño y Diversificación de Cartera',
                    barmode='group',
                    labels={'value': 'Conteo/Valor', 'variable': 'Métrica'},
                    color_discrete_map={
                        'Número de Posiciones': '#60A5FA',
                        'Valor de Cartera ($B)': '#F87171'
                    }
                )
                
                fig_comparison.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis_tickangle=-45,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )
                
                st.plotly_chart(fig_comparison, use_container_width=True)
            
            with col2:
                st.markdown("### 🔗 Análisis de Posiciones Comunes")
                with st.expander("ℹ️ Entendiendo el análisis de superposición"):
                    st.markdown("""
                    **Propósito:** Identificar ideas de inversión compartidas y selecciones únicas
                    
                    **Métricas explicadas:**
                    - **Posiciones Comunes:** Acciones poseídas por todos los inversores seleccionados
                    - **Posiciones Únicas:** Acciones poseídas por solo un inversor
                    
                    **Por qué importa:**
                    - Alta superposición = Filosofía de inversión similar
                    - Baja superposición = Enfoques diversos
                    - Posiciones comunes = Ideas de alta convicción
                    """)
                
                common_holdings = {}
                for investor in selected_investors:
                    holdings = set(comparison_df[comparison_df['Investor'] == investor]['Stock'])
                    common_holdings[investor] = holdings
                
                # Calculate overlaps
                if len(selected_investors) == 2:
                    overlap = len(common_holdings[selected_investors[0]] & common_holdings[selected_investors[1]])
                    unique_1 = len(common_holdings[selected_investors[0]] - common_holdings[selected_investors[1]])
                    unique_2 = len(common_holdings[selected_investors[1]] - common_holdings[selected_investors[0]])
                    
                    # Create metrics
                    st.metric("🤝 Posiciones Comunes", overlap)
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric(f"📌 Únicas de {selected_investors[0][:15]}", unique_1)
                    with col_b:
                        st.metric(f"📌 Únicas de {selected_investors[1][:15]}", unique_2)
                    
                    # Show Venn diagram representation
                    overlap_data = pd.DataFrame({
                        'Categoría': ['Comunes', f'{selected_investors[0][:15]} Solo', f'{selected_investors[1][:15]} Solo'],
                        'Conteo': [overlap, unique_1, unique_2]
                    })
                    
                    fig_venn = px.pie(
                        overlap_data,
                        values='Conteo',
                        names='Categoría',
                        title='Distribución de Posiciones',
                        hole=0.4,
                        color_discrete_map={
                            'Comunes': '#764ba2',
                            f'{selected_investors[0][:15]} Solo': '#667eea',
                            f'{selected_investors[1][:15]} Solo': '#00d2ff'
                        }
                    )
                    
                    fig_venn.update_layout(
                        height=300,
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                    )
                    
                    st.plotly_chart(fig_venn, use_container_width=True)
                    
                elif len(selected_investors) >= 3:
                    all_common = set.intersection(*common_holdings.values()) if common_holdings else set()
                    st.metric("🤝 Posiciones en Todas las Carteras", len(all_common))
                    
                    unique_counts = []
                    for investor in selected_investors[:5]:  # Limit to 5 for display
                        if investor in common_holdings:
                            unique = len(common_holdings[investor] - set.union(*[h for k, h in common_holdings.items() if k != investor]))
                            unique_counts.append({'Inversor': investor[:20], 'Posiciones Únicas': unique})
                    
                    if unique_counts:
                        unique_df = pd.DataFrame(unique_counts)
                        
                        fig_unique = px.bar(
                            unique_df,
                            x='Inversor',
                            y='Posiciones Únicas',
                            title='Posiciones Únicas por Inversor',
                            color='Posiciones Únicas',
                            color_continuous_scale='Viridis'
                        )
                        
                        fig_unique.update_layout(
                            height=300,
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white'),
                            xaxis_tickangle=-45,
                            showlegend=False
                        )
                        
                        st.plotly_chart(fig_unique, use_container_width=True)
            
            # Common stocks table
            if len(selected_investors) >= 2:
                st.markdown("### 📋 Análisis Detallado de Superposición")
                
                # Find common stocks
                all_holdings = [common_holdings[inv] for inv in selected_investors if inv in common_holdings]
                if all_holdings:
                    common_stocks = set.intersection(*all_holdings)
                    
                    if common_stocks:
                        st.markdown(f"#### Acciones poseídas por los {len(selected_investors)} inversores seleccionados:")
                        
                        common_details = []
                        for stock in common_stocks:
                            stock_data = comparison_df[comparison_df['Stock'] == stock]
                            avg_weight = stock_data['% of Portfolio'].mean()
                            total_value = stock_data['Value_Clean'].sum() / 1e6
                            common_details.append({
                                'Acción': stock,
                                'Peso Promedio': avg_weight,
                                'Valor Total ($M)': total_value,
                                'Inversores': len(stock_data)
                            })
                        
                        common_df = pd.DataFrame(common_details).sort_values('Peso Promedio', ascending=False)
                        
                        st.dataframe(
                            common_df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Peso Promedio": st.column_config.ProgressColumn(
                                    "Peso Promedio %",
                                    format="%.2f%%",
                                    min_value=0,
                                    max_value=common_df['Peso Promedio'].max()
                                ),
                                "Valor Total ($M)": st.column_config.NumberColumn(
                                    "Valor Total ($M)",
                                    format="%.1f"
                                )
                            }
                        )
                    else:
                        st.info("No hay acciones poseídas por todos los inversores seleccionados")
    else:
        st.info("Por favor selecciona al menos un inversor desde la barra lateral para comenzar la comparación")

# Footer with attribution
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin-top: 3rem;'>
        <h3 style='color: white; margin-bottom: 1rem;'>📊 Dashboard de Análisis de Superinversores</h3>
        <p style='color: white; font-size: 1.2rem; font-weight: bold;'>
            Hecho con ❤️ por @Gsnchez - BQuantFinance.com
        </p>
        <p style='color: rgba(255,255,255,0.8); margin-top: 1rem;'>
            Datos de Dataroma.com | Actualizado: Agosto 2025 | Siguiendo 81 Inversores Legendarios
        </p>
        <p style='color: rgba(255,255,255,0.6); font-size: 0.9rem; margin-top: 1rem;'>
            Visualizaciones 3D avanzadas, perspectivas impulsadas por IA y análisis de carteras en tiempo real
        </p>
    </div>
""", unsafe_allow_html=True)
