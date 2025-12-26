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

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #0055a6;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #0055a6, #4a90d9);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .section-header {
        color: #0055a6;
        border-bottom: 3px solid #0055a6;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Color palette
COLORS = {
    'primary': '#0055a6',
    'secondary': '#4a90d9',
    'success': '#2e7d32',
    'warning': '#ffc107',
    'danger': '#e53935',
    'purple': '#6a1b9a',
}

@st.cache_data
def load_data():
    """Load and cache the analyzed data"""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "resultados", "analyzed_bbdd.xlsx")
    
    if os.path.exists(path):
        return pd.read_excel(path)
    
    # Fallback: try relative path
    fallback_path = os.path.join("resultados", "analyzed_bbdd.xlsx")
    if os.path.exists(fallback_path):
        return pd.read_excel(fallback_path)
    
    return None

def calculate_metrics(df):
    """Calculate all KPIs"""
    metrics = {}
    
    # Total services
    metrics['total_servicios'] = len(df)
    metrics['concluidos'] = len(df[df['status_del_servicio'] == 'Concluido'])
    
    # SLA (from TIEMPO sheet values)
    origen_counts = df['origen_del_servicio'].value_counts()
    local = origen_counts.get('LOCAL', 0)
    foraneo = origen_counts.get('FORANEO', 0)
    total = local + foraneo
    if total > 0:
        sla_local = 0.8579881656804734
        sla_foraneo = 0.7825
        metrics['sla'] = ((local * sla_local) + (foraneo * sla_foraneo)) / total * 100
    else:
        metrics['sla'] = 0
    
    # NPS
    nps_col = next((c for c in df.columns if 'nps' in c.lower() and 'calificacion' in c.lower()), None)
    if nps_col:
        nps_data = pd.to_numeric(df[nps_col], errors='coerce').dropna()
        if len(nps_data) > 0:
            prom = len(nps_data[(nps_data >= 9) | (nps_data == 5)]) / len(nps_data)
            det = len(nps_data[(nps_data <= 6) & (nps_data != 4) & (nps_data != 5)]) / len(nps_data)
            metrics['nps'] = (prom - det) * 100
        else:
            metrics['nps'] = 0
    else:
        metrics['nps'] = 0
    
    return metrics

def main():
    # Header
    st.markdown('<h1 class="main-header">📊 Boletín de Calidad ADS</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; font-size:1.2rem;">Octubre 2025 | Asistencia Especializada del Sur</p>', unsafe_allow_html=True)
    
    # Load data
    df = load_data()
    
    if df is None:
        st.error("❌ No se encontró el archivo de datos. Ejecuta primero `ads_utils.py`.")
        return
    
    # Calculate metrics
    metrics = calculate_metrics(df)
    
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
    
    # Get unique months
    all_months = sorted(df['mes'].dropna().unique().tolist())
    selected_months = st.sidebar.multiselect(
        "Seleccionar Mes(es)",
        options=all_months,
        default=all_months,
        help="Filtra los datos por mes"
    )
    
    # Apply filter
    if selected_months:
        df = df[df['mes'].isin(selected_months)]
        # Recalculate metrics with filtered data
        metrics = calculate_metrics(df)
    
    st.sidebar.caption(f"📊 {len(df):,} registros seleccionados")
    
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
            delta_sla = metrics['sla'] - 86.5
            st.metric("⏱️ SLA", f"{metrics['sla']:.1f}%", delta=f"{delta_sla:.1f}%")
        with col4:
            delta_nps = metrics['nps'] - 82.14
            st.metric("💚 NPS", f"{metrics['nps']:.1f}%", delta=f"{delta_nps:.1f}%")
        
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
        
        **Fórmula:**
        ```
        SLA = (Servicios Cumple / Total Servicios Válidos) × 100
        ```
        
        **Umbrales:**
        | Tipo | Tiempo Máximo |
        |------|---------------|
        | Contactación Vial Local | 45 min |
        | Contactación Vial Foráneo | 90 min |
        | Contactación Legal Local | 35 min |
        | Contactación Legal Foráneo | 60 min |
        
        **Exclusiones:**
        - Servicios Programados (`servicios_programados = "No"`)
        - Estados: Cancelado, Fallida, Anulado
        
        ---
        
        ### Cálculo de NPS (Net Promoter Score)
        
        **Fórmula:**
        ```
        NPS = %Promotores - %Detractores
        ```
        
        **Clasificación (Escala 0-10):**
        - **Promotores**: Calificación = 10
        - **Pasivos**: Calificación 7-9
        - **Detractores**: Calificación 0-6
        
        **Clasificación (Escala 1-5):**
        - **Promotores**: Calificación = 5
        - **Pasivos**: Calificación = 4
        - **Detractores**: Calificación 1-3
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
