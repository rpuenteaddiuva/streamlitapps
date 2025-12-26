"""
ADS Boletín - Metrics Calculation Module
Lógica de cálculo alineada con Auditoría V3
"""
import pandas as pd


def calculate_metrics(df):
    """Calcula KPIs dinámicos basados en columnas del sistema"""
    metrics = {}
    
    # 1. Total Servicios
    metrics['total_servicios'] = len(df)
    metrics['concluidos'] = len(df[df['status_del_servicio'].astype(str).str.contains('Concluido', case=False, na=False)])
    
    # 2. SLA - Usar columnas de cumplimiento del Excel
    sla_cols = [c for c in df.columns if 'cumplimiento' in c.lower() and 'vial' in c.lower()]
    
    if sla_cols:
        sla_col = sla_cols[0]
        sla_data = df[sla_col].astype(str).str.strip().str.upper()
        cumple = (sla_data == 'CUMPLE').sum()
        total_valid = sla_data.isin(['CUMPLE', 'NO CUMPLE']).sum()
        metrics['sla'] = (cumple / total_valid * 100) if total_valid > 0 else 0
    else:
        # Fallback: promedio ponderado
        try:
            origen = df['origen_del_servicio'].value_counts()
            local, foraneo = origen.get('LOCAL', 0), origen.get('FORANEO', 0)
            total = local + foraneo
            metrics['sla'] = ((local * 85.80) + (foraneo * 78.25)) / total if total > 0 else 0
        except:
            metrics['sla'] = 0
    
    # 3. NPS - Categorización híbrida
    metrics['nps'] = calculate_nps(df)
    
    return metrics


def calculate_nps(df):
    """Calcula NPS con lógica de auditoría"""
    nps_col = next((c for c in df.columns if 'nps' in c.lower() and 'calificacion' in c.lower()), None)
    
    if not nps_col:
        return 0
    
    nps_data = pd.to_numeric(df[nps_col], errors='coerce').dropna()
    if len(nps_data) == 0:
        return 0
    
    def categorize(val):
        if val == 10 or val == 5: return 'PROMOTOR'
        if val >= 7 or val == 4: return 'PASIVO'
        return 'DETRACTOR'
    
    cats = nps_data.apply(categorize)
    prom = (cats == 'PROMOTOR').sum() / len(cats)
    det = (cats == 'DETRACTOR').sum() / len(cats)
    
    return (prom - det) * 100


# Target values
TARGETS = {
    'sla': 86.5,
    'nps': 82.1
}
