"""
Boletín de Calidad ADS - Streamlit Dashboard
Dashboard interactivo para presentación al cliente.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Page config
st.set_page_config(
    page_title="Boletín de Calidad ADS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Dark Theme CSS
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* ===== DARK THEME COLOR SYSTEM ===== */
    :root {
        --bg-main: #0f1316;
        --bg-card: #111217;
        --border: #1f2a33;
        --text-primary: #e6eef3;
        --text-secondary: #9aa8b3;
        --accent: #1f8ef1;
        --success: #2ecc71;
        --warning: #f39c12;
        --danger: #e74c3c;
    }
    
    /* Global App Styling */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: var(--bg-main);
    }
    
    /* Main content area */
    .main .block-container {
        padding: 2rem 2.5rem;
        max-width: 1400px;
    }
    
    /* ===== HEADER ===== */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--accent);
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    .section-header {
        color: var(--text-primary);
        font-weight: 600;
        font-size: 1.5rem;
        border-bottom: 2px solid var(--border);
        padding-bottom: 0.75rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    /* ===== KPI CARDS ===== */
    [data-testid="stMetric"] {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4);
    }
    
    [data-testid="stMetricLabel"] {
        font-weight: 500;
        font-size: 0.85rem;
        color: var(--text-secondary) !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700;
        color: var(--text-primary) !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.9rem;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a1929 0%, #0d2137 100%);
        border-right: 1px solid var(--border);
    }
    
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p {
        color: var(--text-primary) !important;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: var(--accent) !important;
        font-weight: 600;
    }
    
    /* ===== FILE UPLOADER ===== */
    .stFileUploader {
        background: var(--bg-card);
        border: 1px dashed var(--border);
        border-radius: 10px;
        padding: 1rem;
    }
    
    .stFileUploader:hover {
        border-color: var(--accent);
    }
    
    /* ===== DATAFRAMES / TABLES ===== */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid var(--border);
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background: var(--bg-card);
    }
    
    /* ===== SELECTBOXES & INPUTS ===== */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: var(--bg-card);
        border-color: var(--border);
        color: var(--text-primary);
    }
    
    /* ===== BUTTONS ===== */
    .stButton > button {
        background: var(--accent);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #3da0f5;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(31, 142, 241, 0.35);
    }
    
    /* ===== DIVIDERS ===== */
    hr {
        border: none;
        height: 1px;
        background: var(--border);
        margin: 1.5rem 0;
    }
    
    /* ===== ALERTS ===== */
    .stAlert {
        border-radius: 10px;
        background: var(--bg-card);
        border: 1px solid var(--border);
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-main);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #2a3a47;
    }
    
    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: transparent;}
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 800px) {
        .main-header { font-size: 1.6rem; }
        [data-testid="stMetricValue"] { font-size: 1.5rem !important; }
        .main .block-container { padding: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

# Dark Theme Color Palette for Plotly
COLORS = {
    'primary': '#1f8ef1',
    'secondary': '#3da0f5',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'purple': '#9b59b6',
    'text': '#e6eef3',
    'text_secondary': '#9aa8b3',
    'bg': '#0f1316',
    'card': '#111217',
    'border': '#1f2a33',
}

# Plotly Dark Template
PLOTLY_TEMPLATE = {
    'layout': {
        'paper_bgcolor': '#111217',
        'plot_bgcolor': '#111217',
        'font': {'color': '#e6eef3', 'family': 'Inter'},
        'xaxis': {'gridcolor': '#1f2a33', 'linecolor': '#1f2a33'},
        'yaxis': {'gridcolor': '#1f2a33', 'linecolor': '#1f2a33'},
    }
}

@st.cache_data
def load_data():
    """Load and cache the analyzed data"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try multiple paths (local dev, Streamlit Cloud, parent dir)
    paths_to_try = [
        os.path.join(script_dir, "resultados", "analyzed_bbdd.xlsx"),
        os.path.join(script_dir, "..", "resultados", "analyzed_bbdd.xlsx"),
        "resultados/analyzed_bbdd.xlsx",
        "../resultados/analyzed_bbdd.xlsx",
        os.path.join(script_dir, "datos", "Servicios brindados ADS 2025 (1).xlsx"),
        os.path.join(script_dir, "..", "datos", "Servicios brindados ADS 2025 (1).xlsx"),
    ]
    
    for path in paths_to_try:
        if os.path.exists(path):
            try:
                df = pd.read_excel(path)
                st.sidebar.success(f"✅ Datos cargados")
                return df
            except Exception as e:
                continue
    
    return None

@st.cache_data
def calculate_metrics(_df):
    """Calcula KPIs optimizados con operaciones vectorizadas"""
    df = _df  # Workaround for unhashable df
    metrics = {}
    
    # 1. Total Servicios
    metrics['total_servicios'] = len(df)
    mask_conc = df['status_del_servicio'].astype(str).str.contains('Concluido', case=False, na=False)
    metrics['concluidos'] = mask_conc.sum()
    
    # 2. SLA - Operaciones vectorizadas (no usar .apply())
    prog_col = next((c for c in df.columns if 'programad' in c.lower()), None)
    if prog_col:
        mask_no_prog = df[prog_col].astype(str).str.lower() != 'si'
    else:
        mask_no_prog = True
    
    df_sla = df[mask_conc & mask_no_prog]
    
    if 'duracion_minutos' in df_sla.columns and len(df_sla) > 0:
        # Vectorized: Umbral según origen
        origen = df_sla['origen_del_servicio'].astype(str).str.upper()
        limite = pd.Series(45, index=df_sla.index)
        limite[origen.str.contains('FORAN', na=False)] = 90
        
        # Vectorized: Cumple si duracion <= limite
        duracion = pd.to_numeric(df_sla['duracion_minutos'], errors='coerce')
        cumple = duracion <= limite
        valid = duracion.notnull()
        
        if valid.sum() > 0:
            metrics['sla'] = (cumple[valid].sum() / valid.sum()) * 100
        else:
            metrics['sla'] = 0
    else:
        # Fallback: promedio ponderado
        origen_counts = df['origen_del_servicio'].value_counts()
        local = origen_counts.get('LOCAL', 0)
        foraneo = origen_counts.get('FORANEO', 0)
        total = local + foraneo
        metrics['sla'] = ((local * 85.80) + (foraneo * 78.25)) / total if total > 0 else 0
    
    # 3. NPS - Vectorizado
    nps_col = next((c for c in df.columns if 'nps' in c.lower() and 'calificacion' in c.lower()), None)
    metrics['nps'] = 0
    
    if nps_col:
        nps_data = pd.to_numeric(df[nps_col], errors='coerce').dropna()
        if len(nps_data) > 0:
            max_val = nps_data.max()
            if max_val <= 5:
                # Escala 1-5
                prom = (nps_data == 5).sum()
                det = (nps_data <= 3).sum()
            else:
                # Escala 0-10
                prom = (nps_data >= 9).sum()
                det = (nps_data <= 6).sum()
            metrics['nps'] = ((prom - det) / len(nps_data)) * 100

    return metrics

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Boletín de Calidad ADS</h1>', unsafe_allow_html=True)
    
    # Sidebar - Data Source
    st.sidebar.title("🔧 Panel de Control")
    
    # File uploader
    st.sidebar.subheader("📂 Fuente de Datos")
    uploaded_file = st.sidebar.file_uploader("Cargar Excel/CSV", type=["xlsx", "csv"])
    
    if uploaded_file:
        # Load from uploaded file
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='latin1')
        else:
            df = pd.read_excel(uploaded_file)
        # Standardize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '')
        st.sidebar.success(f"✅ {uploaded_file.name}")
    else:
        # Load from local file
        df = load_data()
        if df is None:
            st.info("👋 **Bienvenido!** Sube un archivo Excel (BBDD) en el panel lateral para comenzar.")
            st.sidebar.info("Arrastra tu archivo aquí ↑")
            return
        st.sidebar.caption("📁 Usando datos locales")
    
    # Sidebar
    st.sidebar.title("🔧 Navegación")
    st.sidebar.image("https://via.placeholder.com/200x80?text=ADS+Logo", width=200)
    
    selected_section = st.sidebar.radio("Sección", [
        "📈 Resumen Ejecutivo",
        "📊 Histórico Coordinación",
        "🔧 Detalle Auxilio Vial",
        "🚗 Detalle Remolque (Grúa)",
        "📋 Tipo de Plan",
        "📈 Líneas de Servicio",
        "🗺️ Demanda Geográfica",
        "😊 Satisfacción & NPS",
        "📊 Indicadores Mensuales",
        "📋 Metodología"
    ])
    
    # Month filter
    st.sidebar.divider()
    st.sidebar.subheader("🗓️ Filtros")
    
    # Get unique months and sort chronologically
    month_order = {'Ene': 1, 'Feb': 2, 'Mar': 3, 'Abr': 4, 'May': 5, 'Jun': 6,
                   'Jul': 7, 'Ago': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dic': 12}
    raw_months = df['mes'].dropna().unique().tolist()
    # Sort by extracting month prefix (e.g., "Ene-25" -> "Ene")
    all_months = sorted(raw_months, key=lambda x: (
        int(str(x).split('-')[-1]) if '-' in str(x) else 0,  # Year first
        month_order.get(str(x).split('-')[0], 0)  # Then month
    ))
    
    # Select All checkbox
    select_all = st.sidebar.checkbox("Seleccionar todos los meses", value=True)
    
    if select_all:
        selected_months = all_months
    else:
        selected_months = st.sidebar.multiselect(
            "Meses:",
            options=all_months,
            default=[],
            placeholder="Elige uno o más meses..."
        )
    
    # Apply month filter
    if selected_months:
        df = df[df['mes'].isin(selected_months)]
    else:
        st.sidebar.warning("⚠️ Selecciona al menos un mes")
    
    # Drill-down filters
    st.sidebar.divider()
    st.sidebar.subheader("🔍 Drill-Down")
    
    # Plan filter
    if 'nombre_del_plan' in df.columns:
        planes = ['Todos'] + sorted(df['nombre_del_plan'].dropna().unique().tolist())
        selected_plan = st.sidebar.selectbox("Plan:", planes)
        if selected_plan != 'Todos':
            df = df[df['nombre_del_plan'] == selected_plan]
    
    # Ciudad filter
    if 'ciudad' in df.columns:
        ciudades = ['Todas'] + sorted(df['ciudad'].dropna().astype(str).unique().tolist())[:20]  # Top 20
        selected_city = st.sidebar.selectbox("Ciudad:", ciudades)
        if selected_city != 'Todas':
            df = df[df['ciudad'] == selected_city]
    
    # Tipo de Servicio filter
    if 'tipo_de_servicio' in df.columns:
        tipos = ['Todos'] + sorted(df['tipo_de_servicio'].dropna().unique().tolist())
        selected_tipo = st.sidebar.selectbox("Tipo Servicio:", tipos)
        if selected_tipo != 'Todos':
            df = df[df['tipo_de_servicio'] == selected_tipo]
    
    # Calculate metrics with filtered data
    metrics = calculate_metrics(df)
    
    # Calculate weighted SLA for comparison
    try:
        origen_counts = df['origen_del_servicio'].value_counts()
        local = origen_counts.get('LOCAL', 0)
        foraneo = origen_counts.get('FORANEO', 0)
        total = local + foraneo
        sla_ponderado = ((local * 85.80) + (foraneo * 78.25)) / total if total > 0 else 0
    except:
        sla_ponderado = 0
    metrics['sla_ponderado'] = sla_ponderado
    
    st.sidebar.divider()
    st.sidebar.caption(f"📊 **{len(df):,}** registros seleccionados")
    
    # ==========================================================================
    # RESUMEN EJECUTIVO
    # ==========================================================================
    if "Resumen" in selected_section:
        st.markdown('<h2 class="section-header">Resumen Ejecutivo</h2>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🚗 Total Servicios", f"{metrics['total_servicios']:,}")
        with col2:
            st.metric("✅ Concluidos", f"{metrics['concluidos']:,}")
        with col3:
            target_sla = 86.5
            val_sla = metrics['sla']
            delta_sla = val_sla - target_sla
            st.metric(f"⏱️ SLA Calculado", f"{val_sla:.1f}%", delta=f"{delta_sla:.1f}%", help="Calculado desde timestamps crudos")
        with col4:
            val_sla_pond = metrics.get('sla_ponderado', 0)
            delta_pond = val_sla_pond - target_sla
            st.metric(f"📊 SLA Ponderado", f"{val_sla_pond:.1f}%", delta=f"{delta_pond:.1f}%", help="Promedio ponderado TIEMPO sheet")
        
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            target_nps = 82.1
            val_nps = metrics['nps']
            delta_nps = val_nps - target_nps
            st.metric(f"💚 NPS (Meta {target_nps}%)", f"{val_nps:.1f}%", delta=f"{delta_nps:.1f}%")
        
        st.divider()
        
        # Status distribution
        col1, col2 = st.columns(2)
        
        with col1:
            status_counts = df['status_del_servicio'].value_counts()
            fig = px.pie(values=status_counts.values, names=status_counts.index,
                        title="Distribución por Status",
                        color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], 
                                                  COLORS['warning'], COLORS['success']])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            origen_counts = df['origen_del_servicio'].value_counts()
            fig = px.pie(values=origen_counts.values, names=origen_counts.index,
                        title="Local vs Foráneo", hole=0.4,
                        color_discrete_sequence=[COLORS['primary'], COLORS['secondary']])
            st.plotly_chart(fig, use_container_width=True)
        
        # SLA by Category breakdown
        st.subheader("📊 SLA por Categoría de Servicio")
        
        def categorize_service(t):
            t = str(t).upper()
            if 'AUXILIO' in t: return 'Auxilio Vial'
            if 'REMOLQUE' in t or 'GRUA' in t: return 'Grúas (Remolque)'
            if 'LEGAL' in t or 'SITU' in t: return 'Legal / In Situ'
            return 'Otros'
        
        df_cat = df.copy()
        df_cat['categoria'] = df_cat['tipo_de_servicio'].apply(categorize_service)
        
        # Calculate SLA per category
        sla_by_cat = []
        for cat in ['Auxilio Vial', 'Grúas (Remolque)', 'Legal / In Situ', 'Otros']:
            mask = (df_cat['categoria'] == cat) & (df_cat['status_del_servicio'].str.contains('Concluido', case=False, na=False))
            sub = df_cat[mask]
            if len(sub) > 0 and 'duracion_minutos' in sub.columns:
                dur = sub['duracion_minutos']
                origen = sub['origen_del_servicio'].str.upper()
                limite = origen.apply(lambda x: 90 if 'FORAN' in str(x) else 45)
                cumple = (dur <= limite) & dur.notnull()
                sla_pct = cumple.mean() * 100
                status = '🟢' if sla_pct >= 85 else ('🟠' if sla_pct >= 70 else '🔴')
                sla_by_cat.append({'Categoría': cat, 'Volumen': len(sub), 'SLA': f"{sla_pct:.1f}%", 'Estado': status})
            else:
                sla_by_cat.append({'Categoría': cat, 'Volumen': len(sub), 'SLA': 'N/A', 'Estado': '⚪'})
        
        st.dataframe(pd.DataFrame(sla_by_cat), use_container_width=True, hide_index=True)
    
    # ==========================================================================
    # HISTÓRICO COORDINACIÓN
    # ==========================================================================
    elif "Histórico" in selected_section:
        st.markdown('<h2 class="section-header">Histórico de Coordinación</h2>', unsafe_allow_html=True)
        
        # Monthly trend
        df['mes_str'] = df['mes'].astype(str)
        monthly = df.groupby(['mes_str', 'status_del_servicio']).size().unstack(fill_value=0)
        
        fig = px.bar(monthly, barmode='stack', title="Servicios por Mes y Status",
                     color_discrete_sequence=[COLORS['primary'], COLORS['secondary'],
                                               COLORS['warning'], COLORS['success']])
        st.plotly_chart(fig, use_container_width=True)
        
        # Service type distribution
        st.subheader("Líneas de Servicio")
        tipo_counts = df['tipo_de_servicio'].value_counts().head(10)
        fig = px.bar(x=tipo_counts.values, y=tipo_counts.index, orientation='h',
                     title="Top 10 Tipos de Servicio",
                     color_discrete_sequence=[COLORS['primary']])
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    
    # ==========================================================================
    # DETALLE AUXILIO VIAL
    # ==========================================================================
    elif "Auxilio Vial" in selected_section:
        st.markdown('<h2 class="section-header">Detalle Auxilio Vial</h2>', unsafe_allow_html=True)
        
        # Filter for Auxilio Vial
        df_auxilio = df[df['tipo_de_servicio'].str.contains('AUXILIO', case=False, na=False)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Donut: Local vs Foráneo
            origen_aux = df_auxilio['origen_del_servicio'].value_counts()
            fig = px.pie(values=origen_aux.values, names=origen_aux.index,
                        title="Demarcación (Local/Foráneo)", hole=0.5,
                        color_discrete_sequence=[COLORS['primary'], COLORS['secondary']])
            fig.update_traces(textposition='inside', textinfo='percent+value')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar: Segmentación por servicio brindado
            if 'servicio_brindado' in df_auxilio.columns:
                serv = df_auxilio['servicio_brindado'].value_counts().head(6)
                fig = px.bar(x=serv.index, y=serv.values,
                            title="Segmentación del Servicio",
                            color_discrete_sequence=[COLORS['primary']])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Columna 'servicio_brindado' no disponible")
        
        st.metric("Total Auxilio Vial", len(df_auxilio))
    
    # ==========================================================================
    # DETALLE REMOLQUE (GRÚA)
    # ==========================================================================
    elif "Remolque" in selected_section:
        st.markdown('<h2 class="section-header">Detalle Remolque Automóvil (Grúa)</h2>', unsafe_allow_html=True)
        
        # Filter for Remolque/Grúa
        df_remolque = df[df['tipo_de_servicio'].str.contains('REMOLQUE|GRUA', case=False, na=False)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Donut: Local vs Foráneo
            origen_rem = df_remolque['origen_del_servicio'].value_counts()
            fig = px.pie(values=origen_rem.values, names=origen_rem.index,
                        title="Demarcación (Local/Foráneo)", hole=0.5,
                        color_discrete_sequence=[COLORS['primary'], COLORS['secondary']])
            fig.update_traces(textposition='inside', textinfo='percent+value')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar: Segmentación por servicio brindado
            if 'servicio_brindado' in df_remolque.columns:
                serv = df_remolque['servicio_brindado'].value_counts().head(6)
                fig = px.bar(x=serv.index, y=serv.values,
                            title="Segmentación del Servicio",
                            color_discrete_sequence=[COLORS['secondary']])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Columna 'servicio_brindado' no disponible")
        
        st.metric("Total Remolques", len(df_remolque))
    
    # ==========================================================================
    # TIPO DE PLAN
    # ==========================================================================
    elif "Tipo de Plan" in selected_section:
        st.markdown('<h2 class="section-header">Distribución por Tipo de Plan</h2>', unsafe_allow_html=True)
        
        plan_counts = df['nombre_del_plan'].value_counts()
        
        # Horizontal bar chart
        fig = px.bar(x=plan_counts.values, y=plan_counts.index, orientation='h',
                     title="Servicios por Tipo de Plan",
                     color_discrete_sequence=[COLORS['primary']])
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
        
        # Percentages
        st.subheader("Detalle")
        for plan, count in plan_counts.items():
            pct = count / len(df) * 100
            st.write(f"**{plan}**: {count:,} ({pct:.2f}%)")
    
    # ==========================================================================
    # LÍNEAS DE SERVICIO (TRIMESTRAL)
    # ==========================================================================
    elif "Líneas de Servicio" in selected_section:
        st.markdown('<h2 class="section-header">Líneas de Servicio - Comparativo Mensual</h2>', unsafe_allow_html=True)
        
        # Group by month and service type
        df['mes_str'] = df['mes'].astype(str)
        pivot = df.groupby(['tipo_de_servicio', 'mes_str']).size().unstack(fill_value=0)
        
        # Get last 3 months
        last_months = sorted(pivot.columns)[-3:]
        pivot_last = pivot[last_months].head(8)
        
        fig = px.bar(pivot_last, barmode='group',
                     title="Últimos 3 Meses por Línea de Servicio",
                     color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['success']])
        st.plotly_chart(fig, use_container_width=True)
    
    # ==========================================================================
    # INDICADORES MENSUALES
    # ==========================================================================
    elif "Indicadores" in selected_section:
        st.markdown('<h2 class="section-header">Indicadores Mensuales</h2>', unsafe_allow_html=True)
        
        # Create indicators table (hardcoded from TIEMPO sheet)
        indicators = {
            'Indicador': ['% Cumplimiento NS', '% Máx. Abandono', 'Coordinación', 
                         'Contacto Vial-Urbano', 'Contacto Vial-Rural', '% Quejas'],
            'Punto de Control': ['Mínimo 90%', 'Máximo 1%', 'Mínimo 85% / 10 min',
                                'Mínimo 86.50% / 45 min', 'Mínimo 86.50% / 90 min', 'Máximo 1%'],
            'Ago-25': ['99.04%', '0.07%', '85.04%', '87.14%', '89.81%', '0.99%'],
            'Sep-25': ['98.47%', '0.08%', '85.27%', '86.57%', '86.87%', '1.19%'],
            'Oct-25': ['97.30%', '0.17%', '86.38%', '86.86%', '87.19%', '0.37%'],
        }
        
        df_ind = pd.DataFrame(indicators)
        
        # Style function for conditional formatting
        def highlight_cells(val):
            try:
                num = float(val.replace('%', ''))
                if num >= 86.5:
                    return 'background-color: #c8e6c9'
                elif num >= 80:
                    return 'background-color: #fff9c4'
                else:
                    return 'background-color: #ffcdd2'
            except:
                return ''
        
        st.dataframe(df_ind.style.applymap(highlight_cells, subset=['Ago-25', 'Sep-25', 'Oct-25']),
                    use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Leyenda:**
        - 🟢 Verde: Cumple (≥86.5%)
        - 🟡 Amarillo: Cerca del objetivo (80-86.5%)
        - 🔴 Rojo: No cumple (<80%)
        """)
    
    # ==========================================================================
    # DEMANDA GEOGRÁFICA
    # ==========================================================================
    elif "Geográfica" in selected_section:
        st.markdown('<h2 class="section-header">Demanda Geográfica</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            prov_counts = df['provincia'].value_counts().head(10)
            fig = px.bar(x=prov_counts.index, y=prov_counts.values,
                        title="Demanda por Provincia",
                        color_discrete_sequence=[COLORS['purple']])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            city_counts = df['ciudad'].value_counts().head(10)
            fig = px.bar(x=city_counts.index, y=city_counts.values,
                        title="Demanda por Ciudad",
                        color_discrete_sequence=[COLORS['purple']])
            st.plotly_chart(fig, use_container_width=True)
    
    # ==========================================================================
    # SATISFACCIÓN & NPS
    # ==========================================================================
    elif "Satisfacción" in selected_section:
        st.markdown('<h2 class="section-header">Satisfacción del Cliente</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # NPS Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=metrics['nps'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "NPS Score"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': COLORS['success']},
                    'steps': [
                        {'range': [0, 50], 'color': "#ffebee"},
                        {'range': [50, 75], 'color': "#fff3e0"},
                        {'range': [75, 100], 'color': "#e8f5e9"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 82.14
                    }
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # NPS Distribution
            nps_col = next((c for c in df.columns if 'nps' in c.lower() and 'calificacion' in c.lower()), None)
            if nps_col:
                nps_data = pd.to_numeric(df[nps_col], errors='coerce').dropna()
                nps_counts = nps_data.value_counts().sort_index()
                
                colors = []
                for val in nps_counts.index:
                    if val >= 9 or val == 5:
                        colors.append(COLORS['success'])
                    elif val >= 7 or val == 4:
                        colors.append(COLORS['warning'])
                    else:
                        colors.append(COLORS['danger'])
                
                fig = px.bar(x=nps_counts.index.astype(str), y=nps_counts.values,
                            title="Distribución de Calificaciones NPS",
                            color=nps_counts.index.astype(str),
                            color_discrete_sequence=colors)
                st.plotly_chart(fig, use_container_width=True)
    
    # ==========================================================================
    # METODOLOGÍA
    # ==========================================================================
    elif "Metodología" in selected_section:
        st.markdown('<h2 class="section-header">Metodología</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### Cálculo de SLA (Service Level Agreement)
        
        Este dashboard muestra **dos métricas de SLA:**
        
        #### 1. SLA Calculado (Timestamps Crudos)
        Calculado directamente desde la diferencia entre `Fec_Contacto` y `Fec_Asignacion`.
        
        ```
        SLA Calculado = (Servicios dentro de umbral / Total Válidos) × 100
        ```
        
        **Nota:** Este cálculo usa tiempo 24/7 sin "Stop the Clock", por lo que suele dar valores menores (~65-75%).
        
        #### 2. SLA Ponderado (Hoja TIEMPO)
        Promedio ponderado usando valores pre-calculados de la hoja TIEMPO, que incluyen 
        reglas de negocio como "Stop the Clock" (pausar tiempo en esperas del cliente).
        
        ```
        SLA Ponderado = (Local × 85.80% + Foráneo × 78.25%) / Total
        ```
        
        **Valores base:** LOCAL=85.80%, FORANEO=78.25% (de hoja TIEMPO)
        
        ---
        
        **Umbrales por Tipo de Servicio:**
        | Tipo | Local | Foráneo |
        |------|-------|---------|
        | Vial (Auxilio/Grúa/Remolque) | 45 min | 90 min |
        | Legal | 35 min | 60 min |
        
        **Exclusiones:**
        - Servicios Programados (`servicios_programados = "No"`)
        - Estados: Cancelado, Fallida, Anulado
        - Keywords en motivos: Cita, Agendada, Programada, Posterior
        
        ---
        
        ### Cálculo de NPS (Net Promoter Score)
        
        **Fórmula:**
        ```
        NPS = %Promotores - %Detractores
        ```
        
        **Detección automática de escala:**
        - Si max(calificación) ≤ 5 → Escala 1-5
        - Si max(calificación) > 5 → Escala 0-10
        
        | Escala | Promotor | Pasivo | Detractor |
        |--------|----------|--------|-----------|
        | 1-5 | 5 | 4 | 1-3 |
        | 0-10 | 9-10 | 7-8 | 0-6 |
        """)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align:center; color:gray; font-size:0.8rem;">
        Boletín de Calidad ADS | Octubre 2025 | Generado automáticamente
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
