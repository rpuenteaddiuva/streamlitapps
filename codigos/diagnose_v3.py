import pandas as pd
import os

def diagnose():
    path = "resultados/analyzed_bbdd.xlsx"
    print(f"Loading {path}...")
    df = pd.read_excel(path)
    
    # 1. NPS Diagnosis
    nps_col = [c for c in df.columns if 'nps' in c or 'calificacion_cliente' in c][0]
    print("\n### NPS STATS ###")
    print(df[nps_col].value_counts().sort_index().to_dict())
    
    # Restoring Filters
    status_col = next((c for c in df.columns if 'status' in c or 'estado' in c), 'status_del_servicio')
    mask_cancelados = df[status_col].astype(str).str.contains('Cancelado|Fallida|Anulado', case=False, na=False)
    mask_programada = pd.Series([False] * len(df))
    for col in [c for c in df.columns if 'motivo' in c or 'sub_motivo' in c or 'servicio_brindado' in c]:
        mask_programada |= df[col].astype(str).str.contains('Programada|Cita|Agendada|Posterior', case=False, na=False)
    
    df_sla = df[~mask_cancelados & ~mask_programada & df['duracion_minutos'].notnull()].copy()

    print("\n### SLA DIAGNOSIS ###")
    print(f"Total Valid: {len(df_sla)}")
    print(f"Mean Dur: {df_sla['duracion_minutos'].mean():.1f}")
    
    df_sla['is_bad'] = df_sla['duracion_minutos'] > 45
    bad_ones = df_sla[df_sla['is_bad']]
    print(f"Bad > 45m: {len(bad_ones)} ({len(bad_ones)/len(df_sla)*100:.1f}%)")
    col_tipo = 'tipo_de_servicio' if 'tipo_de_servicio' in df_sla.columns else df_sla.columns[0]
    print(bad_ones[['duracion_minutos', col_tipo, status_col]].head(5))

if __name__ == "__main__":
    diagnose()
