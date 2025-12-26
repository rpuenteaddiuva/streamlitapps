"""
ADS Boletín - Metrics Calculation Module
Metodología V3 Completa (Boletin_Calidad_v3.tex Sección 6)
"""
import pandas as pd


# Metas oficiales
TARGETS = {
    'sla': 86.5,
    'nps': 82.1
}

# SLA pre-calculados de hoja TIEMPO (fuente oficial del boletín)
SLA_TIEMPO = {
    'urbano': 85.80,  # LOCAL (45min)
    'rural': 78.25    # FORANEO (90min)
}

# Keywords de exclusión para motivos
EXCLUSION_KEYWORDS = ['cita', 'agendada', 'programada', 'posterior']


def apply_exclusions(df):
    """Aplica exclusiones según metodología V3"""
    df_clean = df.copy()
    
    # 1. Excluir por Status: Cancelado, Fallida, Anulado
    status_col = 'status_del_servicio'
    if status_col in df_clean.columns:
        status_vals = df_clean[status_col].astype(str).str.lower()
        mask = ~status_vals.str.contains('cancelado|fallido|anulado|fallida', case=False, na=False)
        df_clean = df_clean[mask]
    
    # 2. Excluir Servicios Programados
    prog_col = next((c for c in df_clean.columns if 'programad' in c.lower()), None)
    if prog_col:
        df_clean = df_clean[df_clean[prog_col].astype(str).str.lower() != 'si']
    
    # 3. Excluir Keywords en motivos
    motivo_col = next((c for c in df_clean.columns if 'motivo' in c.lower()), None)
    if motivo_col:
        motivo_vals = df_clean[motivo_col].astype(str).str.lower()
        pattern = '|'.join(EXCLUSION_KEYWORDS)
        df_clean = df_clean[~motivo_vals.str.contains(pattern, case=False, na=False)]
    
    return df_clean


def calculate_metrics(df):
    """Calcula KPIs según metodología V3"""
    metrics = {}
    
    # Total sin filtrar
    metrics['total_servicios'] = len(df)
    
    # Aplicar exclusiones
    df_clean = apply_exclusions(df)
    
    # Concluidos
    status_col = 'status_del_servicio'
    if status_col in df_clean.columns:
        metrics['concluidos'] = len(df_clean[df_clean[status_col].astype(str).str.contains('Concluido', case=False, na=False)])
    else:
        metrics['concluidos'] = 0
    
    # SLA - Promedio ponderado usando valores de hoja TIEMPO
    # Fuente: Boletin V3 usa SLA pre-calculado de hoja TIEMPO
    origen_col = 'origen_del_servicio'
    if origen_col in df_clean.columns:
        counts = df_clean[origen_col].value_counts()
        local = counts.get('LOCAL', 0)
        foraneo = counts.get('FORANEO', 0)
        total = local + foraneo
        
        if total > 0:
            # Promedio ponderado con valores de TIEMPO sheet
            metrics['sla'] = (
                (local * SLA_TIEMPO['urbano']) + 
                (foraneo * SLA_TIEMPO['rural'])
            ) / total
        else:
            metrics['sla'] = 0
    else:
        metrics['sla'] = 0
    
    # NPS
    metrics['nps'] = calculate_nps(df_clean)
    
    return metrics


def calculate_nps(df):
    """NPS según metodología V3"""
    nps_col = None
    for c in df.columns:
        if 'nps' in c.lower() or ('calificacion' in c.lower() and 'servicio' in c.lower()):
            nps_col = c
            break
    
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
