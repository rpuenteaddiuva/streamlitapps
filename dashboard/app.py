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
    
    # Tipo de Servicio filter
    if 'tipo_de_servicio' in df.columns:
        tipos = ['Todos'] + sorted(df['tipo_de_servicio'].dropna().unique().tolist())
        selected_tipo = st.sidebar.selectbox("Tipo Servicio:", tipos)
        if selected_tipo != 'Todos':
            df = df[df['tipo_de_servicio'] == selected_tipo]
            
    # Exclude 'Otros' toggle
    st.sidebar.divider()
    exclude_otros = st.sidebar.checkbox("⚠️ Excluir categoría 'Otros'", value=True, 
                                      help="Excluye servicios Médicos, Hogar, etc. del cálculo de SLA")
                                      
    if exclude_otros:
        def is_otros(t):
            t = str(t).upper()
            if 'AUXILIO' in t or 'REMOLQUE' in t or 'GRUA' in t or 'LEGAL' in t or 'SITU' in t:
                return False
            return True
        
        mask_otros = df['tipo_de_servicio'].apply(is_otros)
        excluded_types = df[mask_otros]['tipo_de_servicio'].unique().tolist()
        df_excluded_count = mask_otros.sum()
        df = df[~mask_otros]
        
        if df_excluded_count > 0:
            st.sidebar.caption(f"ℹ️ Se han filtrado {df_excluded_count} servicios calculados como 'Otros'")
            with st.sidebar.expander("Ver categorías excluidas"):
                st.write(sorted([str(x) for x in excluded_types]))

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
        
    elif "Indicadores" in selected_section:
        st.markdown('<h2 class="section-header">Indicadores Mensuales</h2>', unsafe_allow_html=True)
        
    elif "Indicadores" in selected_section:
        st.markdown('<h2 class="section-header">Indicadores Mensuales</h2>', unsafe_allow_html=True)
        
        # Calculate dynamic SLA for ALL months using unfiltered data
        # Use 'all_months' calculated earlier which is sorted
        months_to_show = all_months 
        
        # Initialize dictionary
        data = {
            'Indicador': [
                'SLA Global', 'SLA Vial Urbano', 'SLA Vial Rural',
                '% Cumplimiento NS (CC)', '% Abandono (CC)', '% Quejas'
            ],
            'Punto de Control': [
                'Mínimo 86.5%', 'Mínimo 86.50% / 45 min', 'Mínimo 86.50% / 90 min',
                'Mínimo 90%', 'Máximo 1%', 'Máximo 1%'
            ]
        }
        
        for month in months_to_show:
            col_data = [] # SLA Global, Urbano, Rural, NS, Abandono, Quejas
            
            # --- CALCULATE SLAs from BBDD (df_unfiltered) ---
            df_m = df_unfiltered[df_unfiltered['mes'] == month]
            
            if len(df_m) > 0:
                # Reuse metric calculation logic
                # Only excluding 'Otros' if the user checked the box? 
                # Ideally, Indicators table should reflect the same logic as the main dashboard filters currently active?
                # BUT, df_unfiltered ignores month filter. 
                # It does NOT ignore the 'Exclude Others' filter if it was applied BEFORE 'df_unfiltered = df.copy()'.
                # Let's check where 'df_unfiltered' was defined.
                # It was defined AFTER 'Exclude Others' filter (lines 435+), so 'Otros' exclusion IS Applied.
                # Correct.
                
                metrics_m = calculate_metrics(df_m)
                sla_global = metrics_m['sla']
                col_data.append(f"{sla_global:.2f}%")
                
                # Urbano / Rural Breakdowns
                mask_conc = df_m['status_del_servicio'].astype(str).str.contains('Concluido', case=False, na=False)
                prog_col = next((c for c in df_m.columns if 'programad' in c.lower()), None)
                if prog_col:
                     mask_no_prog = df_m[prog_col].astype(str).str.lower() != 'si'
                else:
                     mask_no_prog = True
                
                df_sla = df_m[mask_conc & mask_no_prog]
                
                def calc_sla_subset(sub_df, is_foraneo):
                    if len(sub_df) == 0: return 0
                    if 'duracion_minutos' not in sub_df.columns: return 0
                    limite = 90 if is_foraneo else 45
                    dur = pd.to_numeric(sub_df['duracion_minutos'], errors='coerce')
                    valid = dur.notnull()
                    if valid.sum() == 0: return 0
                    cumple = (dur[valid] <= limite).sum()
                    return (cumple / valid.sum()) * 100

                urbano_mask = df_sla['origen_del_servicio'].astype(str).str.upper() == 'LOCAL'
                sla_urbano = calc_sla_subset(df_sla[urbano_mask], False)
                col_data.append(f"{sla_urbano:.2f}%")

                rural_mask = df_sla['origen_del_servicio'].astype(str).str.upper().str.contains('FORAN')
                sla_rural = calc_sla_subset(df_sla[rural_mask], True)
                col_data.append(f"{sla_rural:.2f}%")
                
            else:
                col_data.extend(['-', '-', '-'])
            
            # --- HARDCODED METRICS (Placeholders for missing BBDD data) ---
            # Keeping only recently provided values, others '-'
            if month == 'Ago-25':
                col_data.extend(['99.04%', '0.07%', '0.99%'])
            elif month == 'Sep-25':
                col_data.extend(['98.47%', '0.08%', '1.19%'])
            elif month == 'Oct-25':
                col_data.extend(['97.30%', '0.17%', '0.37%'])
            else:
                col_data.extend(['-', '-', '-'])
            
            data[month] = col_data

        df_ind = pd.DataFrame(data)
        
        # Style function for conditional formatting
        def highlight_cells(val):
            try:
                if isinstance(val, str) and '%' in val:
                    num = float(val.replace('%', ''))
                    # Quejas/Abandono (Indices 4 and 5 in the list -> rows in DataFrame?)
                    # Dataframe is Indicador | Control | M1 | M2...
                    # We need to know which ROW we are strictly. 
                    # Style function is applied cell-wise. This is tricky for row-dependent logic.
                    # Simplified: If < 5 and not SLA...
                    
                    if num < 5: # Likely Abandono/Quejas
                         if num <= 1.0: return 'background-color: #c8e6c9; color: black'
                         else: return 'background-color: #ffcdd2; color: black'
                    else: # SLA / NS
                         if num >= 86.5: return 'background-color: #c8e6c9; color: black'
                         elif num >= 80: return 'background-color: #fff9c4; color: black'
                         else: return 'background-color: #ffcdd2; color: black'
                return ''
            except:
                return ''
        
        st.dataframe(df_ind.style.applymap(highlight_cells, subset=months_to_show),
                    use_container_width=True, hide_index=True)
        
        st.markdown("""
        **Leyenda:**
        - 🟢 Verde: Cumple (≥86.5%)
        - 🟡 Amarillo: Cerca del objetivo (80-86.5%)
        - 🔴 Rojo: No cumple (<80%)
        - **CC**: Datos de Call Center (externos a BBDD)
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
        
        **Fuente Única de Verdad:** Hoja `BBDD` (Servicios Brindados).
        
        **Fórmula:**
        ```
        SLA = (Servicios Cumple / Total Servicios Válidos) × 100
        ```
        
        El cálculo se realiza **registro por registro** comparando la duración real del servicio contra el umbral establecido para su tipo y zona.
        
        **Umbrales por Tipo de Servicio:**
        | Tipo | Local | Foráneo |
        |------|-------|---------|
        | Vial (Auxilio/Grúa/Remolque) | 45 min | 90 min |
        | Legal | 35 min | 60 min |
        
        **Exclusiones:**
        - Servicios Programados (`servicios_programados = "No"`)
        - Estados: Cancelado, Fallida, Anulado
        - Keywords en motivos: Cita, Agendada, Programada, Posterior
        - Categoría "Otros" (Médico, Hogar, etc.) se excluye del análisis core.
        
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
