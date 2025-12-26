import pandas as pd
import numpy as np
import os
import argparse
import datetime

def clean_data(file_path):
    """
    Carga datos, estandariza columnas a snake_case y gestiona fechas.
    """
    print("--- Iniciando Limpieza de Datos ---")
    
    # Detección de formato (CSV o Excel)
    if file_path.endswith('.csv'):
        try:
            df = pd.read_csv(file_path, encoding='latin1', on_bad_lines='skip') 
        except:
            df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
    else:
        df = pd.read_excel(file_path)

    # 1. Estandarización de columnas (Snake Case)
    df.columns = (df.columns
                  .str.strip()
                  .str.lower()
                  .str.replace(' ', '_')
                  .str.replace('/', '_')
                  .str.replace('.', '')
                  .str.replace('á', 'a').str.replace('é', 'e').str.replace('í', 'i').str.replace('ó', 'o').str.replace('ú', 'u')
                  )
    
    # 2. Procesamiento de Fechas y Horas para SLA
    
    def parse_datetime(date_series, time_series):
        # Handle Excel Serial Dates (floats)
        def to_dt(x):
            if pd.isna(x): return pd.NaT
            if isinstance(x, (int, float)):
                # Excel base date
                return pd.to_datetime(x, unit='D', origin='1899-12-30')
            return pd.to_datetime(x, errors='coerce')

        dates = date_series.apply(to_dt)
        
        def extract_time(val):
            if pd.isna(val): return None
            # If it's already a time object (from Excel)
            if isinstance(val, datetime.time):
                return val
            # If it's a datetime object (has .time() method)
            if hasattr(val, 'time'):
                return val.time()
            # If string
            if isinstance(val, str):
                val = val.strip()
                # Try parsing
                try:
                    dt = pd.to_datetime(val, format='%H:%M:%S')
                    return dt.time()
                except:
                    try:
                        dt = pd.to_datetime(val) # infer
                        return dt.time()
                    except:
                        pass
            return None

        times = time_series.apply(extract_time)
        
        # Combine
        combined = []
        for d, t in zip(dates, times):
            if pd.notna(d) and t is not None:
                try:
                    combined.append(pd.Timestamp.combine(d.date(), t))
                except:
                    combined.append(pd.NaT)
            else:
                combined.append(pd.NaT)
                
        return pd.Series(combined)

    # Flexible column detection
    cols = df.columns
    fec_asig = next((c for c in cols if 'fec' in c and 'asig' in c), 'fec_asignacion')
    hrs_asig = next((c for c in cols if 'ho' in c and 'asig' in c), 'hrs_asignacion')
    fec_cont = next((c for c in cols if 'fec' in c and 'cont' in c), 'fec_contacto')
    hrs_cont = next((c for c in cols if 'ho' in c and 'cont' in c), 'hrs_contacto')
    
    print(f"Usando columnas de tiempo: {fec_asig}, {hrs_asig} -> {fec_cont}, {hrs_cont}")

    print("Calculando timestamps...")
    df['ts_asignacion'] = parse_datetime(df[fec_asig], df[hrs_asig])
    df['ts_contacto'] = parse_datetime(df[fec_cont], df[hrs_cont])

    # Force datetime type
    df['ts_asignacion'] = pd.to_datetime(df['ts_asignacion'], errors='coerce')
    df['ts_contacto'] = pd.to_datetime(df['ts_contacto'], errors='coerce')

    # Cálculo de duración en minutos
    df['duracion_minutos'] = (df['ts_contacto'] - df['ts_asignacion']).dt.total_seconds() / 60
    
    # Limpieza de valores negativos o nulos lógicos
    df.loc[df['duracion_minutos'] < 0, 'duracion_minutos'] = np.nan

    return df

def analyze_data(df):
    """
    Realiza cálculos base y guarda el dataset maestro procesado.
    """
    print("--- Iniciando Análisis ---")
    
    # Guardar resultado intermedio robusto
    if not os.path.exists("resultados"):
        os.makedirs("resultados")
        
    output_file = os.path.join("resultados", 'analyzed_bbdd.xlsx')
    df.to_excel(output_file, index=False)
    print(f"Data procesada guardada en: {output_file}")
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', choices=['clean', 'analyze', 'conclude'], required=False) 
    parser.add_argument('--input', required=False, default="Servicios brindados ADS 2025 (1).xlsx")
    args = parser.parse_args()

    # Ajusta la ruta a tu archivo real
    file_path = args.input
    if os.path.exists(file_path):
        df = clean_data(file_path)
        analyze_data(df)
    else:
        print(f"Archivo no encontrado: {file_path}")
