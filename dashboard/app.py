"""
Boletín de Calidad ADS - Streamlit Dashboard
Dashboard interactivo para presentación al cliente.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import os

# Set global Plotly dark theme
pio.templates.default = "plotly_dark"

try:
    from modules import metrics as metrics_module
except ImportError:
    # Fallback if running from a different directory context
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
    import metrics as metrics_module

# Page config
st.set_page_config(
    page_title="Boletín de Calidad ADS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional Dark Theme CSS
def load_css():
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
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: var(--accent);
    }
    
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
        font-weight: 700;
        font-size: 1.8rem !important;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 0.9rem !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* ===== SECTION HEADERS ===== */
    .section-header {
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border);
        color: var(--accent) !important;
    }
    
    /* ===== SIDEBAR ===== */
    [data-testid="stSidebar"] {
        background-color: #0b0d10;
        border-right: 1px solid var(--border);
    }
    
    .css-1d391kg {  /* Sidebar sections */
        padding-top: 2rem;
    }

    /* ===== DATAFRAMES & TABLES ===== */
    .stDataFrame {
        border: 1px solid var(--border);
        border-radius: 8px;
        overflow: hidden;
    }
    

    /* ===== CUSTOM FILE UPLOADER ===== */
    [data-testid="stFileUploader"] {
        border: 1px dashed var(--border);
        border-radius: 10px;
        padding: 1rem;
        background: rgba(255,255,255,0.02);
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent);
        background: rgba(31, 142, 241, 0.05);
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
    'secondary': '#6c757d',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'purple': '#9b59b6',
    'dark_bg': '#0f1316',
    'dark_paper': '#111217'
}

def style_dark_chart(fig):
    """Apply dark theme styling to any Plotly figure."""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent to match Streamlit background
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='#e6eef3',
        title_font_color='#1f8ef1',
        legend_bgcolor='rgba(0,0,0,0)',
        legend_font_color='#e6eef3'
    )
    return fig

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
def calculate_metrics(df_in):
    """Calcula KPIs optimizados con operaciones vectorizadas"""
    df = df_in
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

@st.cache_data
def preprocess_data(df):
    """Ensure critical columns exist for analysis"""
    # Standardize column names
    df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(' ', '_').str.replace('.', '')
    
    # 1. Calculate 'duracion_minutos' if missing but timestamps exist
    # Candidates for Start/End
    start_cols = [c for c in df.columns if 'contacto' in c and 'fec' in c] # fec_contacto
    end_cols = [c for c in df.columns if 'asignacion' in c and 'fec' in c] # fec_asignacion
    
    if 'duracion_minutos' not in df.columns and start_cols and end_cols:
        try:
            start = pd.to_datetime(df[start_cols[0]], errors='coerce')
            end = pd.to_datetime(df[end_cols[0]], errors='coerce')
            df['duracion_minutos'] = (end - start).dt.total_seconds() / 60
        except:
            pass
            
    # 2. Extract 'mes' (e.g., 'Oct-25') if missing but date exists
    if 'mes' not in df.columns and start_cols:
        try:
            # Create Spanish month names
            months_es = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun',
                         7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
            dates = pd.to_datetime(df[start_cols[0]], errors='coerce')
            df['mes'] = dates.apply(lambda x: f"{months_es.get(x.month, '')}-{str(x.year)[-2:]}" if pd.notnull(x) else 'N/A')
        except:
            pass
            
    return df

def main():
    st.set_page_config(page_title="Boletín de Calidad ADS", layout="wide", page_icon="📊")
    load_css()
    
    # Sidebar Logo
    st.sidebar.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #1f8ef1;">ADS Dashboard</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # File Uploader
    uploaded_file = st.sidebar.file_uploader(
        "📂 Cargar BBDD (Excel)",
        type=["xlsx"],
        help="Carga un archivo Excel. Se calcularán automáticamente SLA y Fechas si faltan."
    )
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            df = preprocess_data(df) # Auto-fix columns
            st.sidebar.success(f"✅ Cargado: {uploaded_file.name}")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")
            return
    else:
        # Load from local file
        df = load_data()
        if df is None:
            st.info("👋 **Bienvenido!** Sube un archivo Excel (BBDD) en el panel lateral para comenzar.")
            st.sidebar.info("Arrastra tu archivo aquí ↑")
            return
        df = preprocess_data(df) # Ensure consistency for local file too
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
    
    # --- APPLY CONTEXT FILTERS FIRST (Affects both Current View and History) ---
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
    
    # Exclude 'Otros' toggle (Granular Control)
    st.sidebar.divider()
    
    # 1. Identify all types and default 'others'
    all_service_types = sorted(df['tipo_de_servicio'].astype(str).unique().tolist())
    
    def is_definitely_otros(t):
        t = str(t).upper()
        # Core keywords to KEEP
        if 'AUXILIO' in t or 'REMOLQUE' in t or 'GRUA' in t or 'LEGAL' in t or 'SITU' in t:
            return False
        return True # Default exclude
        
    default_excluded = [t for t in all_service_types if is_definitely_otros(t)]
    
    # 2. Multiselect Widget
    with st.sidebar.expander("🚫 Gestión de Exclusiones", expanded=False):
        st.caption("Selecciona los servicios que NO deseas incluir en el análisis (SLA, NPS, etc).")
        types_to_exclude = st.multiselect(
            "Servicios Excluidos:",
            options=all_service_types,
            default=default_excluded,
            placeholder="Selecciona servicios a excluir..."
        )
        
    # 3. Apply Exclusion Filter
    if types_to_exclude:
        mask_exclude = df['tipo_de_servicio'].isin(types_to_exclude)
        count_excluded = mask_exclude.sum()
        df = df[~mask_exclude]
        
        if count_excluded > 0:
            st.sidebar.warning(f"⚠️ Se han excluido {count_excluded} servicios del análisis.")
    else:
        st.sidebar.success("✅ Se están mostrando TODOS los servicios.")
    
    # 4. Exclusiones SLA (Global - Aplica a todas las secciones)
    with st.sidebar.expander("📋 Exclusiones SLA", expanded=False):
        st.caption("Controla qué registros se excluyen del cálculo de SLA.")
        
        st.markdown("**📌 Por Estado/Tipo:**")
        exc_programados = st.checkbox("Servicios Programados", value=False, key="exc_prog_sidebar", help="Excluir servicios_programados = 'Sí'")
        exc_cancelados = st.checkbox("Estados Cancelados/Fallidos", value=False, key="exc_cancel_sidebar", help="Excluir Cancelado, Fallida, Anulado")
        
        st.markdown("**🔤 Por Keywords en Motivo:**")
        exc_cita = st.checkbox("'Cita'", value=False, key="exc_cita_sidebar")
        exc_agendada = st.checkbox("'Agendada'", value=False, key="exc_agendada_sidebar")
        exc_programada = st.checkbox("'Programada'", value=False, key="exc_programada_sidebar")
        exc_posterior = st.checkbox("'Posterior'", value=False, key="exc_posterior_sidebar")
        
        # Resumen
        active_exc = []
        if exc_programados: active_exc.append("Prog")
        if exc_cancelados: active_exc.append("Cancel")
        if exc_cita: active_exc.append("Cita")
        if exc_agendada: active_exc.append("Agend")
        if exc_programada: active_exc.append("Progr")
        if exc_posterior: active_exc.append("Post")
        
        if active_exc:
            st.success(f"✅ Activas: {', '.join(active_exc)}")
        else:
            st.info("SLA sin exclusiones (real)")

    # --- CAPTURE HISTORY (Context filtered, but ALL months) ---
    df_unfiltered = df.copy()

    # --- APPLY TIME FILTER (Only selected months) ---
    if selected_months:
        df = df[df['mes'].isin(selected_months)]
    else:
        st.sidebar.warning("⚠️ Selecciona al menos un mes")
            
    # Disclaimer about Stop the Clock
    st.sidebar.info("ℹ️ **Nota:** El cálculo de SLA es estricto (tiempo total) ya que la base de datos no contiene registros de 'tiempos muertos' imputables al cliente.")
    
    # Calculate metrics with filtered data
    metrics = calculate_metrics(df)
    
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
            st.metric(f"⏱️ SLA (Meta {target_sla}%)", f"{val_sla:.1f}%", delta=f"{delta_sla:.1f}%", help="Calculado desde BBDD")
        with col4:
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
            style_dark_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            origen_counts = df['origen_del_servicio'].value_counts()
            fig = px.pie(values=origen_counts.values, names=origen_counts.index,
                        title="Local vs Foráneo", hole=0.4,
                        color_discrete_sequence=[COLORS['primary'], COLORS['secondary']])
            style_dark_chart(fig)
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
        
        # Aplicar exclusiones SLA según checkboxes del sidebar
        mask_base = df_cat['status_del_servicio'].str.contains('Concluido', case=False, na=False)
        
        # Exclusión: Servicios programados
        if exc_programados:
            prog_col = next((c for c in df_cat.columns if 'programad' in c.lower()), None)
            if prog_col:
                mask_base = mask_base & (df_cat[prog_col].astype(str).str.lower() != 'si')
        
        # Exclusión: Keywords en motivo
        motivo_col = next((c for c in df_cat.columns if 'motivo' in c.lower()), None)
        if motivo_col:
            motivo_vals = df_cat[motivo_col].astype(str).str.lower()
            if exc_cita:
                mask_base = mask_base & ~motivo_vals.str.contains('cita', case=False, na=False)
            if exc_agendada:
                mask_base = mask_base & ~motivo_vals.str.contains('agendada', case=False, na=False)
            if exc_programada:
                mask_base = mask_base & ~motivo_vals.str.contains('programada', case=False, na=False)
            if exc_posterior:
                mask_base = mask_base & ~motivo_vals.str.contains('posterior', case=False, na=False)
        
        # Calculate SLA per category
        sla_by_cat = []
        for cat in ['Auxilio Vial', 'Grúas (Remolque)', 'Legal / In Situ', 'Otros']:
            mask = (df_cat['categoria'] == cat) & mask_base
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
        style_dark_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
        
        # Service type distribution
        st.subheader("Líneas de Servicio")
        tipo_counts = df['tipo_de_servicio'].value_counts().head(10)
        fig = px.bar(x=tipo_counts.values, y=tipo_counts.index, orientation='h',
                     title="Top 10 Tipos de Servicio",
                     color_discrete_sequence=[COLORS['primary']])
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        style_dark_chart(fig)
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
            style_dark_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar: Segmentación por servicio brindado
            if 'servicio_brindado' in df_auxilio.columns:
                serv = df_auxilio['servicio_brindado'].value_counts().head(6)
                fig = px.bar(x=serv.index, y=serv.values,
                            title="Segmentación del Servicio",
                            color_discrete_sequence=[COLORS['primary']])
                style_dark_chart(fig)
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
            style_dark_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Bar: Segmentación por servicio brindado
            if 'servicio_brindado' in df_remolque.columns:
                serv = df_remolque['servicio_brindado'].value_counts().head(6)
                fig = px.bar(x=serv.index, y=serv.values,
                            title="Segmentación del Servicio",
                            color_discrete_sequence=[COLORS['secondary']])
                style_dark_chart(fig)
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
        style_dark_chart(fig)
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
        style_dark_chart(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    # ==========================================================================
    # INDICADORES MENSUALES
    # ==========================================================================
    elif "Indicadores" in selected_section:
        st.markdown('<h2 class="section-header">Indicadores Mensuales</h2>', unsafe_allow_html=True)
        
        # Nota sobre las exclusiones (referencia al sidebar)
        st.info("💡 **Tip:** Usa el control **📋 Exclusiones SLA** en el panel lateral para ajustar qué registros se excluyen del cálculo.")
        
        try:
            # 1. Prepare Columns Structure (Months + Quarterly Avgs + Total)
            columns_struct = [
                'INDICADOR', 'PUNTO DE CONTROL',
                'Ene-25', 'Feb-25', 'Mar-25', 'PROMEDIO 1er. TRIMESTRE',
                'Abr-25', 'May-25', 'Jun-25', 'PROMEDIO 2do. TRIMESTRE',
                'Jul-25', 'Ago-25', 'Sep-25', 'PROMEDIO 3er. TRIMESTRE',
                'Oct-25', 'PROMEDIO TOTAL'
            ]
            
            # --- CALCULO DE INDICADORES MENSUALES (Desde metrics.py) ---
            # Se usa df_unfiltered para tener historial completo
            monthly_data = metrics_module.calculate_monthly_kpis(df_unfiltered)
            
            # Helper to get monthly data or '-'
            def get_metric(metric_key, month, df_u, is_percent=True):
                
                # 1. Buscar en resultados pre-calculados (metrics.py)
                val = None
                m_data = monthly_data.get(month, {})
                
                if metric_key == 'NS': val = m_data.get('ns')
                elif metric_key == 'Abandono': val = m_data.get('abandono')
                elif metric_key == 'Coord': val = m_data.get('coordinacion')
                elif metric_key == 'Quejas': val = m_data.get('quejas')
                elif metric_key == 'Recobros': val = m_data.get('recobros')
                
                if val is not None:
                    if metric_key == 'Recobros': return f"${val:,.0f}"
                    return f"{val:.2f}%"

                # 2. Dynamic SLA Calc (Detallado por tipo/zona) - Fallback logic
                # Se mantiene esta lógica local para SLAs específicos no cubiertos por coordinacion general
                df_m = df_u[df_u['mes'] == month]
                if len(df_m) == 0: return "-"
                
                # Common filters - Servicios concluidos
                mask_conc = df_m['status_del_servicio'].astype(str).str.contains('Concluido', case=False, na=False)
                
                # Iniciar con máscara base
                mask_final = mask_conc.copy()
                
                # Aplicar exclusiones granulares según checkboxes seleccionados
                # 1. Excluir servicios programados
                if exc_programados:
                    prog_col = next((c for c in df_m.columns if 'programad' in c.lower()), None)
                    if prog_col:
                        mask_final = mask_final & (df_m[prog_col].astype(str).str.lower() != 'si')
                
                # 2. Excluir estados cancelados/fallidos (nota: ya filtrados por Concluido, pero por seguridad)
                if exc_cancelados:
                    mask_final = mask_final & ~df_m['status_del_servicio'].astype(str).str.contains('Cancelado|Fallid|Anulado', case=False, na=False)
                
                # 3. Excluir por keywords en motivo (granular)
                motivo_col = next((c for c in df_m.columns if 'motivo' in c.lower()), None)
                if motivo_col:
                    motivo_vals = df_m[motivo_col].astype(str).str.lower()
                    if exc_cita:
                        mask_final = mask_final & ~motivo_vals.str.contains('cita', case=False, na=False)
                    if exc_agendada:
                        mask_final = mask_final & ~motivo_vals.str.contains('agendada', case=False, na=False)
                    if exc_programada:
                        mask_final = mask_final & ~motivo_vals.str.contains('programada', case=False, na=False)
                    if exc_posterior:
                        mask_final = mask_final & ~motivo_vals.str.contains('posterior', case=False, na=False)
                
                df_sla = df_m[mask_final]
                
                def calc_sla(sub_df, limit_min):
                     dur = pd.to_numeric(sub_df['duracion_minutos'], errors='coerce')
                     valid = dur.notnull()
                     if valid.sum() == 0: return "-"
                     val = (dur[valid] <= limit_min).sum() / valid.sum() * 100
                     return f"{val:.2f}%"

                if metric_key == 'SLA_Vial_Local':
                     mask = df_sla['origen_del_servicio'].astype(str).str.upper() == 'LOCAL'
                     return calc_sla(df_sla[mask], 45)
                     
                if metric_key == 'SLA_Situ_Local':
                     mask = df_sla['origen_del_servicio'].astype(str).str.upper() == 'LOCAL'
                     return calc_sla(df_sla[mask], 35)

                if metric_key == 'SLA_Vial_Foraneo':
                     mask = df_sla['origen_del_servicio'].astype(str).str.upper().str.contains('FORAN')
                     return calc_sla(df_sla[mask], 90)

                if metric_key == 'SLA_Situ_Foraneo':
                     mask = df_sla['origen_del_servicio'].astype(str).str.upper().str.contains('FORAN')
                     return calc_sla(df_sla[mask], 60)
                     
                return "-"


            rows_definitions = [
                {'name': '% Cumplimiento del NS', 'control': 'Mínimo 90%', 'key': 'NS'},
                {'name': '% Máximo de Abandono', 'control': 'Máximo 1%', 'key': 'Abandono'},
                {'name': 'Coordinación Local y Foráneo', 'control': '10 minutos Mínimo el 85%', 'key': 'Coord'},
                {'name': 'Contacto Vial-Local', 'control': 'Mínimo 86.50% Antes de 45 minutos', 'key': 'SLA_Vial_Local'},
                {'name': 'Contacto In situ - Local', 'control': 'Mínimo 80% Antes de 35 minutos', 'key': 'SLA_Situ_Local'},
                {'name': 'Contacto Vial - Foráneo', 'control': 'Mínimo 86.50% Antes de 90 minutos', 'key': 'SLA_Vial_Foraneo'},
                {'name': 'Contacto In situ - Foráneo', 'control': 'Mínimo 90% Antes de 60 minutos', 'key': 'SLA_Situ_Foraneo'}
            ]
            
            month_keys = ['Ene-25', 'Feb-25', 'Mar-25', 'Abr-25', 'May-25', 'Jun-25', 'Jul-25', 'Ago-25', 'Sep-25', 'Oct-25']
            
            table_data = []
            for row_def in rows_definitions:
                row = {'INDICADOR': row_def['name'], 'PUNTO DE CONTROL': row_def['control']}
                values_for_avg = {1: [], 2: [], 3: []} # Trimestres
                
                for m in month_keys:
                    val = get_metric(row_def['key'], m, df_unfiltered)
                    row[m] = val
                    
                    # Logic for averages (cleaning % and $)
                    if val != "-" and '%' in val:
                         try:
                            num = float(val.replace('%', ''))
                            if m in ['Ene-25', 'Feb-25', 'Mar-25']: values_for_avg[1].append(num)
                            if m in ['Abr-25', 'May-25', 'Jun-25']: values_for_avg[2].append(num)
                            if m in ['Jul-25', 'Ago-25', 'Sep-25']: values_for_avg[3].append(num)
                         except: pass
                
                # Compute Averages
                all_values = []  # Para promedio total
                for t in [1, 2, 3]:
                    if values_for_avg[t]:
                        avg = sum(values_for_avg[t]) / len(values_for_avg[t])
                        row[f'PROMEDIO {t}er. TRIMESTRE' if t!=2 else f'PROMEDIO {t}do. TRIMESTRE'] = f"{avg:.2f}%"
                        all_values.extend(values_for_avg[t])
                    else:
                        row[f'PROMEDIO {t}er. TRIMESTRE' if t!=2 else f'PROMEDIO {t}do. TRIMESTRE'] = "-"
                
                # Compute Total Average (all months)
                if all_values:
                    total_avg = sum(all_values) / len(all_values)
                    row['PROMEDIO TOTAL'] = f"{total_avg:.2f}%"
                else:
                    row['PROMEDIO TOTAL'] = "-"
                        
                table_data.append(row)
                
            df_table = pd.DataFrame(table_data, columns=columns_struct)
            
            st.success(f"✅ Tabla generada con éxito. Filas: {len(df_table)}")

            # Style
            def style_table(val):
                # Basic styling logic
                if isinstance(val, str):
                    if '-' in val and len(val) == 1: return ''
                    if '%' in val:
                        try:
                            num = float(val.replace('%', ''))
                            # Heuristic: >80 is usually green/yellow, <5 is green (for abandonment/quejas)
                            if num < 5: 
                                # Abandono/Quejas: Low is Good
                                if num <= 1.5: return 'background-color: #c8e6c9; color: black' # Green
                                else: return 'background-color: #ffcdd2; color: black' # Red
                            else:
                                # SLAs/NS: High is Good
                                if num >= 86.5: return 'background-color: #c8e6c9; color: black' # Green
                                elif num >= 80: return 'background-color: #fff9c4; color: black' # Yellow
                                else: return 'background-color: #ffcdd2; color: black' # Red
                        except: pass
                    if '$' in val:
                         return 'color: black' # Ensure readable if styled row
                return ''

            # CSS for sticky columns
            sticky_css = """
            <style>
            /* Make first two columns sticky */
            [data-testid="stDataFrame"] table {
                display: block;
                overflow-x: auto;
            }
            [data-testid="stDataFrame"] th:nth-child(1),
            [data-testid="stDataFrame"] td:nth-child(1) {
                position: sticky;
                left: 0;
                background-color: #1e1e1e;
                z-index: 2;
            }
            [data-testid="stDataFrame"] th:nth-child(2),
            [data-testid="stDataFrame"] td:nth-child(2) {
                position: sticky;
                left: 150px;
                background-color: #1e1e1e;
                z-index: 2;
            }
            [data-testid="stDataFrame"] th:nth-child(1),
            [data-testid="stDataFrame"] th:nth-child(2) {
                z-index: 3;
            }
            </style>
            """
            st.markdown(sticky_css, unsafe_allow_html=True)
            
            # Render with safer fallback
            if df_table.empty:
                st.warning("⚠️ La tabla de indicadores está vacía. Verifica los datos.")
            else:
                try:
                    # Use map if available (pandas >= 2.1.0), else applymap
                    styler = df_table.style
                    if hasattr(styler, 'map'):
                        st.dataframe(styler.map(style_table), use_container_width=True, hide_index=True)
                    else:
                        st.dataframe(styler.applymap(style_table), use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"Error visualizando estilos: {e}")
                    st.dataframe(df_table, use_container_width=True, hide_index=True)
            
            st.caption("Nota: Los valores de Coordinación, NS, Abandono y Recobros son calculados directamente de la BBDD.")

        except Exception as e:
            st.error("❌ ERROR CRÍTICO AL GENERAR TABLA:")
            st.exception(e)
    
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
            style_dark_chart(fig)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            city_counts = df['ciudad'].value_counts().head(10)
            fig = px.bar(x=city_counts.index, y=city_counts.values,
                        title="Demanda por Ciudad",
                        color_discrete_sequence=[COLORS['purple']])
            style_dark_chart(fig)
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
            style_dark_chart(fig)
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
                style_dark_chart(fig)
                st.plotly_chart(fig, use_container_width=True)
    
    # ==========================================================================
    # METODOLOGÍA
    # ==========================================================================
    elif "Metodología" in selected_section:
        st.markdown('<h2 class="section-header">Metodología</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### Glosario de Términos
        - **Local**: Servicios categorizados como 'LOCAL' en el campo origen.
        - **Foráneo**: Servicios categorizados como 'FORANEO' en el campo origen.
        
        ---
        
        ### Cálculo de SLA (Service Level Agreement)
        
        **Definición**: Porcentaje de servicios atendidos dentro del tiempo máximo establecido.
        
        **Fórmula**:
        ```
        SLA = (Servicios Cumple / Total Servicios Válidos) × 100
        ```
        
        Donde:
        - `Duración = FechaContacto − FechaAsignación`
        - `Estado = CUMPLE si Duración ≤ Umbral, NO CUMPLE si Duración > Umbral`
        
        **Umbrales por Tipo de Servicio:**
        | Tipo | Local | Foráneo |
        |------|-------|---------|
        | Contactación Vial | 45 min | 90 min |
        | Contactación Legal | 35 min | 60 min |
        | Asignación | 10 min | 10 min |
        
        **Exclusiones:**
        - Servicios Programados (`servicios_programados = "No"`)
        - Estados: Cancelado, Fallida, Anulado
        - Keywords en motivos: "Cita", "Agendada", "Programada", "Posterior"
        
        ---
        
        ### Cálculo de NPS (Net Promoter Score)
        
        **Definición**: Índice de lealtad y recomendación del cliente.
        
        **Fórmula**:
        ```
        NPS = %Promotores − %Detractores
        ```
        
        **Clasificación (Escala 0-10):**
        | Tipo | Calificación |
        |------|-------------|
        | Promotores | 9-10 |
        | Pasivos | 7-8 |
        | Detractores | 0-6 |
        
        **Clasificación (Escala 1-5):**
        | Tipo | Calificación |
        |------|-------------|
        | Promotores | 5 |
        | Pasivos | 4 |
        | Detractores | 1-3 |
        
        ---
        
        ### Cálculo de Indicadores Mensuales
        
        #### 1. Cumplimiento del NS
        ```
        NS = (Servicios Concluidos / Total Servicios Válidos) × 100
        ```
        **Total Servicios Válidos**: Total de registros menos los siguientes estados excluidos:
        - Cancelado al momento
        - Cancelado posterior
        - Anulado, Abortado, Duplicado, Prueba
        
        #### 2. % Máximo de Abandono
        ```
        Abandono = ((Cancelado al momento + Cancelado posterior) / Total Bruto) × 100
        ```
        Se considera sobre el volumen total de ingresos.
        
        #### 3. Coordinación (Local y Foráneo)
        Mide el tiempo transcurrido entre la toma del servicio (Contacto) y la asignación del proveedor.
        - **Fórmula**: `(fec_asignacion + hrs_asignacion) - (fec_contacto + hrs_contacto)`
        - **Meta**: ≤ 10 minutos.
        
        ---
        
        ### Fuentes de Datos
        - **Dataset Principal**: Servicios brindados ADS 2025 (1).xlsx
        - **Hojas**: BBDD (raw data), TIEMPO (pre-calculated metrics)
        - **Periodo**: Enero - Octubre 2025
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
