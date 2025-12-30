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



def calculate_monthly_kpis(df):
    """
    Calcula indicadores mensuales (NS, Abandono, Coordinación, Quejas, Recobros)
    Devuelve un diccionario anidado.
    """
    results = {}
    
    if 'mes' not in df.columns:
        return results
        
    # Exclusiones
    INVALID_STATUSES = ['Cancelado al momento', 'Cancelado posterior', 'Anulado', 'Abortado', 'Duplicado', 'Prueba']
    
    def combine_date_time(date_val, time_val):
        """Helper to combine date and time columns"""
        try:
            d = pd.to_datetime(date_val)
            if pd.isna(d): return pd.NaT
            
            # Formatos de hora pueden variar (str vs datetime.time)
            if pd.isna(time_val): return pd.NaT
            
            t_str = str(time_val).strip()
            # Si ya es datetime.time
            if hasattr(time_val, 'hour'):
                t_str = time_val.strftime('%H:%M:%S')
                
            # Combinar string
            dt_str = f"{d.strftime('%Y-%m-%d')} {t_str}"
            return pd.to_datetime(dt_str, errors='coerce')
        except:
            return pd.NaT

    # Agrupar por mes
    for mes, group in df.groupby('mes'):
        metrics = {}
        total_bruto = len(group)
        if total_bruto == 0: continue
        
        # Filtrar Validos (para NS y SLAs)
        status_col = 'status_del_servicio'
        if status_col in group.columns:
            # Excluir status invalidos para el denominador de eficiencia
            mask_valid = ~group[status_col].astype(str).isin(INVALID_STATUSES)
            group_valid = group[mask_valid]
            total_valid = len(group_valid)
            
            # 1. % Cumplimiento del NS (Concluidos / Total Valido)
            concluidos = group_valid[group_valid[status_col].astype(str).str.contains('Concluido', case=False, na=False)].shape[0]
            metrics['ns'] = (concluidos / total_valid * 100) if total_valid > 0 else 0
            
            # 2. % Máximo de Abandono (Cancelados / Total Válido)
            # Se excluyen Anulado, Abortado, Duplicado, Prueba del denominador
            mask_abandono = group_valid[status_col].astype(str).str.contains('Cancelado|Abandono', case=False, na=False)
            abandonos = mask_abandono.sum()
            metrics['abandono'] = (abandonos / total_valid * 100) if total_valid > 0 else 0
        else:
            metrics['ns'] = 0
            metrics['abandono'] = 0
            
        # 3. Coordinación (Tiempo contacto - asignacion <= 10 min)
        # Usa la lógica: Asignación ocurre primero, luego Contacto
        # Diff = Contacto - Asignación (positivo = tiempo de espera)
        cumple_coord = 0
        valid_coord_count = 0
        
        if {'fec_contacto', 'hrs_contacto', 'fec_asignacion', 'hrs_asignacion'}.issubset(group.columns):
            dt_contact = group.apply(lambda x: combine_date_time(x['fec_contacto'], x['hrs_contacto']), axis=1)
            dt_assign = group.apply(lambda x: combine_date_time(x['fec_asignacion'], x['hrs_asignacion']), axis=1)
            
            # FIXED: Contact - Assign (tiempo de espera desde asignación hasta contacto)
            diff_min = (dt_contact - dt_assign).dt.total_seconds() / 60
            
            # Filtrar solo no-nulos y no-negativos (negativos = error de datos)
            valid_mask = diff_min.notna() & (diff_min >= 0)
            valid_diffs = diff_min[valid_mask]
            
            if len(valid_diffs) > 0:
                cumple_coord = (valid_diffs <= 10).sum()
                valid_coord_count = len(valid_diffs)
                metrics['coordinacion'] = (cumple_coord / valid_coord_count) * 100
            else:
                metrics['coordinacion'] = 0
        else:
            metrics['coordinacion'] = 0

        # 4. % Quejas procedentes
        quejas_count = 0
        if 'es_queja' in group.columns:
            quejas_count = group[group['es_queja'].astype(str).str.lower() == 'si'].shape[0]
        elif 'tipo_de_servicio' in group.columns:
            quejas_count = group[group['tipo_de_servicio'].astype(str).str.contains('Queja', case=False, na=False)].shape[0]
            
        metrics['quejas'] = (quejas_count / total_bruto) * 100
        
        # 5. Suma de recobros
        # NO HAY DATOS DE COSTO. Se devuelve 0 explícitamente.
        metrics['recobros'] = 0
            
        results[mes] = metrics
        
    return results
