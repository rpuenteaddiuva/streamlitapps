"""
Boletín de Calidad ADS - Dashboard Modular
"""
import streamlit as st
import pandas as pd
import sys
import os

# Add modules to path
sys.path.insert(0, os.path.dirname(__file__))

from modules.data_loader import load_data, sort_months
from modules.metrics import calculate_metrics, TARGETS
from modules.charts import pie_chart, bar_chart, stacked_bar, gauge_chart, COLORS

# Page config
st.set_page_config(page_title="Boletín de Calidad ADS", page_icon="📊", layout="wide")

# CSS
st.markdown("""
<style>
    .main-header { font-size: 2.5rem; color: #0055a6; font-weight: bold; text-align: center; }
    .section-header { color: #0055a6; border-bottom: 3px solid #0055a6; padding-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)


def render_sidebar(df):
    """Render sidebar filters and return filtered dataframe"""
    st.sidebar.title("🔧 Panel de Control")
    
    # File uploader
    st.sidebar.subheader("📂 Datos")
    uploaded = st.sidebar.file_uploader("Cargar Excel/CSV", type=["xlsx", "csv"])
    
    if uploaded:
        if uploaded.name.endswith('.csv'):
            df = pd.read_csv(uploaded, encoding='latin1')
        else:
            df = pd.read_excel(uploaded)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        st.sidebar.success(f"✅ {uploaded.name}")
    
    # Section selector
    st.sidebar.divider()
    section = st.sidebar.radio("📍 Sección", [
        "📈 Resumen", "📊 Histórico", "🗺️ Geografía", 
        "😊 Satisfacción", "📋 Metodología"
    ])
    
    # Filters
    st.sidebar.divider()
    st.sidebar.subheader("🗓️ Filtros")
    
    all_months = sort_months(df['mes'].dropna().unique().tolist())
    select_all = st.sidebar.checkbox("Todos los meses", value=True)
    
    if select_all:
        months = all_months
    else:
        months = st.sidebar.multiselect("Meses:", all_months, placeholder="Elegir...")
    
    if months:
        df = df[df['mes'].isin(months)]
    
    # Drill-down
    if 'nombre_del_plan' in df.columns:
        plans = ['Todos'] + sorted(df['nombre_del_plan'].dropna().unique().tolist())
        plan = st.sidebar.selectbox("Plan:", plans)
        if plan != 'Todos':
            df = df[df['nombre_del_plan'] == plan]
    
    st.sidebar.caption(f"📊 {len(df):,} registros")
    
    return df, section


def render_resumen(df, metrics):
    """Render executive summary section"""
    st.markdown('<h2 class="section-header">Resumen Ejecutivo</h2>', unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🚗 Servicios", f"{metrics['total_servicios']:,}")
    c2.metric("✅ Concluidos", f"{metrics['concluidos']:,}")
    c3.metric(f"⏱️ SLA ({TARGETS['sla']}%)", f"{metrics['sla']:.1f}%", 
              delta=f"{metrics['sla'] - TARGETS['sla']:.1f}%")
    c4.metric(f"💚 NPS ({TARGETS['nps']}%)", f"{metrics['nps']:.1f}%",
              delta=f"{metrics['nps'] - TARGETS['nps']:.1f}%")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        status = df['status_del_servicio'].value_counts()
        st.plotly_chart(pie_chart(status.values, status.index, "Status"), use_container_width=True)
    with col2:
        origen = df['origen_del_servicio'].value_counts()
        st.plotly_chart(pie_chart(origen.values, origen.index, "Local/Foráneo", hole=0.4), use_container_width=True)


def render_historico(df):
    """Render historical section"""
    st.markdown('<h2 class="section-header">Histórico</h2>', unsafe_allow_html=True)
    
    df['mes_str'] = df['mes'].astype(str)
    monthly = df.groupby(['mes_str', 'status_del_servicio']).size().unstack(fill_value=0)
    st.plotly_chart(stacked_bar(monthly, "Servicios por Mes"), use_container_width=True)


def render_geografia(df):
    """Render geographic section"""
    st.markdown('<h2 class="section-header">Demanda Geográfica</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        prov = df['provincia'].value_counts().head(10)
        st.plotly_chart(bar_chart(prov.index, prov.values, "Por Provincia", color=COLORS['purple']), use_container_width=True)
    with col2:
        city = df['ciudad'].value_counts().head(10)
        st.plotly_chart(bar_chart(city.index, city.values, "Por Ciudad", color=COLORS['purple']), use_container_width=True)


def render_satisfaccion(metrics):
    """Render satisfaction section"""
    st.markdown('<h2 class="section-header">Satisfacción</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(gauge_chart(metrics['nps'], "NPS Score", TARGETS['nps']), use_container_width=True)
    with col2:
        st.plotly_chart(gauge_chart(metrics['sla'], "SLA Score", TARGETS['sla']), use_container_width=True)


def render_metodologia():
    """Render methodology section"""
    st.markdown('<h2 class="section-header">Metodología</h2>', unsafe_allow_html=True)
    st.markdown("""
    ### SLA
    - Columnas de cumplimiento del sistema
    - Umbrales: Local 45min, Foráneo 90min
    
    ### NPS
    - Escala híbrida: 10/5=Promotor, 7-9/4=Pasivo, resto=Detractor
    - Fórmula: `%Promotores - %Detractores`
    """)


def main():
    st.markdown('<h1 class="main-header">📊 Boletín de Calidad ADS</h1>', unsafe_allow_html=True)
    
    df = load_data()
    if df is None:
        st.info("👋 Sube un archivo para comenzar")
        return
    
    df, section = render_sidebar(df)
    metrics = calculate_metrics(df)
    
    if "Resumen" in section:
        render_resumen(df, metrics)
    elif "Histórico" in section:
        render_historico(df)
    elif "Geografía" in section:
        render_geografia(df)
    elif "Satisfacción" in section:
        render_satisfaccion(metrics)
    elif "Metodología" in section:
        render_metodologia()


if __name__ == "__main__":
    main()
