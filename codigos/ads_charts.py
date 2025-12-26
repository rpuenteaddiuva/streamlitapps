"""
ADS Charts Generator - Boletín de Calidad Style
Generates all charts matching the official bulletin format.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os

matplotlib.use('Agg')

# Color palette from bulletin
COLORS = {
    'primary_blue': '#0055a6',
    'light_blue': '#4a90d9',
    'dark_blue': '#003366',
    'green': '#2e7d32',
    'light_green': '#81c784',
    'purple': '#6a1b9a',
    'light_purple': '#9c4dcc',
    'yellow': '#ffc107',
    'gray': '#9e9e9e',
    'concluido': '#0055a6',
    'cancelado_momento': '#4a90d9',
    'cancelado_posterior': '#7fb3e0',
    'en_proceso': '#b8d4ed',
}

def setup_style():
    """Configure matplotlib for bulletin style"""
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.labelweight'] = 'bold'

def generate_historico_coordinacion(df, output_dir):
    """Generate stacked bar chart for monthly service history"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Aggregate by month and status
    df['mes_str'] = df['mes'].astype(str)
    pivot = df.groupby(['mes_str', 'status_del_servicio']).size().unstack(fill_value=0)
    
    # Reorder columns
    status_order = ['Concluido', 'Cancelado al momento', 'Cancelado posterior', 'En proceso']
    pivot = pivot.reindex(columns=[c for c in status_order if c in pivot.columns], fill_value=0)
    
    # Colors for each status
    colors = [COLORS['concluido'], COLORS['cancelado_momento'], 
              COLORS['cancelado_posterior'], COLORS['en_proceso']]
    
    pivot.plot(kind='bar', stacked=True, ax=ax, color=colors[:len(pivot.columns)], width=0.7)
    
    # Add totals on top
    for i, (idx, row) in enumerate(pivot.iterrows()):
        total = row.sum()
        ax.text(i, total + 10, str(int(total)), ha='center', fontweight='bold', fontsize=9)
    
    ax.set_xlabel('')
    ax.set_ylabel('Cantidad de Servicios')
    ax.set_title('HISTÓRICO COORDINACIÓN', fontsize=14, fontweight='bold', color=COLORS['primary_blue'])
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), ncol=4, frameon=False)
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'historico_coordinacion.png'), dpi=150, bbox_inches='tight')
    plt.close()

def generate_demanda_geografica(df, output_dir):
    """Generate bar charts for province and city demand"""
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    
    # Province chart
    provincia_counts = df['provincia'].value_counts().head(10)
    bars1 = axes[0].bar(range(len(provincia_counts)), provincia_counts.values, color=COLORS['purple'])
    axes[0].set_xticks(range(len(provincia_counts)))
    axes[0].set_xticklabels(provincia_counts.index, rotation=45, ha='right', fontsize=8)
    axes[0].set_title('DEMANDA POR PROVINCIA', fontweight='bold', color=COLORS['purple'])
    
    for i, (val, pct) in enumerate(zip(provincia_counts.values, provincia_counts.values/provincia_counts.sum()*100)):
        axes[0].text(i, val + 5, f"{int(val)}\n{pct:.0f}%", ha='center', fontsize=8)
    
    # City chart
    ciudad_counts = df['ciudad'].value_counts().head(10)
    bars2 = axes[1].bar(range(len(ciudad_counts)), ciudad_counts.values, color=COLORS['light_purple'])
    axes[1].set_xticks(range(len(ciudad_counts)))
    axes[1].set_xticklabels(ciudad_counts.index, rotation=45, ha='right', fontsize=8)
    axes[1].set_title('DEMANDA POR CIUDAD', fontweight='bold', color=COLORS['purple'])
    
    for i, (val, pct) in enumerate(zip(ciudad_counts.values, ciudad_counts.values/ciudad_counts.sum()*100)):
        axes[1].text(i, val + 5, f"{int(val)}\n{pct:.0f}%", ha='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'demanda_geografica.png'), dpi=150, bbox_inches='tight')
    plt.close()

def generate_tipo_servicio(df, output_dir):
    """Generate service type distribution charts"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    tipo_counts = df['tipo_de_servicio'].value_counts().head(8)
    colors = [COLORS['primary_blue'], COLORS['light_blue'], COLORS['dark_blue'], 
              COLORS['green'], COLORS['light_green'], COLORS['gray'], 
              COLORS['purple'], COLORS['light_purple']]
    
    bars = ax.barh(range(len(tipo_counts)), tipo_counts.values, color=colors[:len(tipo_counts)])
    ax.set_yticks(range(len(tipo_counts)))
    ax.set_yticklabels(tipo_counts.index, fontsize=9)
    ax.set_title('LÍNEAS DE SERVICIO', fontweight='bold', color=COLORS['primary_blue'])
    ax.invert_yaxis()
    
    for i, val in enumerate(tipo_counts.values):
        pct = val / tipo_counts.sum() * 100
        ax.text(val + 5, i, f"{int(val)} ({pct:.1f}%)", va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'tipo_servicio.png'), dpi=150, bbox_inches='tight')
    plt.close()

def generate_origen_distribucion(df, output_dir):
    """Generate LOCAL vs FORANEO donut chart"""
    fig, ax = plt.subplots(figsize=(6, 6))
    
    origen_counts = df['origen_del_servicio'].value_counts()
    colors = [COLORS['primary_blue'], COLORS['light_blue']]
    
    wedges, texts, autotexts = ax.pie(origen_counts.values, labels=origen_counts.index,
                                       autopct='%1.0f%%', colors=colors,
                                       wedgeprops=dict(width=0.5), pctdistance=0.75)
    
    ax.set_title('DISTRIBUCIÓN LOCAL / FORÁNEO', fontweight='bold', color=COLORS['primary_blue'])
    
    # Add center text with counts
    center_text = '\n'.join([f"{k}: {v}" for k, v in origen_counts.items()])
    ax.text(0, 0, center_text, ha='center', va='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'origen_distribucion.png'), dpi=150, bbox_inches='tight')
    plt.close()

def generate_satisfaccion_charts(df, output_dir):
    """Generate satisfaction and NPS charts"""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    
    # NPS distribution
    nps_col = next((c for c in df.columns if 'nps' in c.lower() and 'calificacion' in c.lower()), None)
    if nps_col:
        nps_data = df[nps_col].dropna()
        nps_counts = nps_data.value_counts().sort_index()
        
        colors = []
        for val in nps_counts.index:
            if val >= 9 or val == 5:
                colors.append(COLORS['green'])
            elif val >= 7 or val == 4:
                colors.append(COLORS['yellow'])
            else:
                colors.append('#e53935')
        
        axes[0].bar(nps_counts.index.astype(str), nps_counts.values, color=colors)
        axes[0].set_title('Distribución NPS', fontweight='bold', color=COLORS['green'])
        axes[0].set_xlabel('Calificación')
        
        # Calculate NPS score
        prom = len(nps_data[(nps_data >= 9) | (nps_data == 5)]) / len(nps_data)
        det = len(nps_data[(nps_data <= 6) & (nps_data != 4) & (nps_data != 5)]) / len(nps_data)
        nps_score = (prom - det) * 100
        
        # NPS Gauge (simplified)
        axes[1].pie([nps_score, 100-nps_score], colors=[COLORS['green'], COLORS['gray']],
                    startangle=90, counterclock=False,
                    wedgeprops=dict(width=0.3))
        axes[1].text(0, 0, f"{nps_score:.1f}%", ha='center', va='center', fontsize=20, fontweight='bold')
        axes[1].set_title('NPS Score', fontweight='bold', color=COLORS['green'])
    
    # Satisfaction summary
    sat_col = next((c for c in df.columns if 'satisfaccion' in c.lower() or 'general' in c.lower()), None)
    if sat_col:
        sat_data = df[sat_col].dropna()
        sat_counts = sat_data.value_counts().sort_index()
        axes[2].bar(sat_counts.index.astype(str), sat_counts.values, color=COLORS['light_green'])
        axes[2].set_title('Satisfacción General', fontweight='bold', color=COLORS['green'])
    else:
        axes[2].text(0.5, 0.5, 'N/A', ha='center', va='center', fontsize=20)
        axes[2].set_title('Satisfacción General', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'satisfaccion_charts.png'), dpi=150, bbox_inches='tight')
    plt.close()

def generate_sla_chart(df, output_dir, sla_value):
    """Generate SLA compliance pie chart"""
    fig, ax = plt.subplots(figsize=(6, 6))
    
    colors = [COLORS['primary_blue'], '#e53935']
    ax.pie([sla_value, 100-sla_value], labels=['Cumple', 'No Cumple'],
           autopct='%1.1f%%', colors=colors, startangle=90)
    ax.set_title('CUMPLIMIENTO SLA\n(Contactación Vial)', fontweight='bold', color=COLORS['primary_blue'])
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'sla_chart.png'), dpi=150, bbox_inches='tight')
    plt.close()

def generate_all_charts(df, output_dir, sla_value=82.71):
    """Generate all charts for the bulletin"""
    setup_style()
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print("Generando gráficos del boletín...")
    
    generate_historico_coordinacion(df, output_dir)
    print("  ✓ Histórico Coordinación")
    
    generate_demanda_geografica(df, output_dir)
    print("  ✓ Demanda Geográfica")
    
    generate_tipo_servicio(df, output_dir)
    print("  ✓ Tipo de Servicio")
    
    generate_origen_distribucion(df, output_dir)
    print("  ✓ Origen Distribución")
    
    generate_satisfaccion_charts(df, output_dir)
    print("  ✓ Satisfacción & NPS")
    
    generate_sla_chart(df, output_dir, sla_value)
    print("  ✓ SLA Chart")
    
    print(f"\nTodos los gráficos guardados en: {output_dir}")

if __name__ == "__main__":
    # Load data
    data_path = os.path.join("resultados", "analyzed_bbdd.xlsx")
    if os.path.exists(data_path):
        df = pd.read_excel(data_path)
        output_dir = os.path.join("reportes", "v3_final", "graficas")
        generate_all_charts(df, output_dir)
    else:
        print(f"Error: No se encontró {data_path}")
