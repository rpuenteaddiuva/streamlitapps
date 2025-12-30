import pandas as pd
import sys
import os

# Add modules to path
sys.path.append(os.path.join(os.getcwd(), 'modules'))
from data_loader import load_data

def analyze():
    output = []
    
    print("Loading data...")
    df = load_data()
    if df is None:
        return

    output.append(f"TOTAL ROWS: {len(df)}")
    output.append(f"COLUMNS: {list(df.columns)}")
    
    # 1. STATUS
    if 'status_del_servicio' in df.columns:
        output.append("\n--- STATUS COUNTS ---")
        output.append(df['status_del_servicio'].value_counts().to_string())

    # 2. ORIGEN (Rural vs Urbano)
    if 'origen_del_servicio' in df.columns:
        output.append("\n--- ORIGEN COUNTS ---")
        output.append(df['origen_del_servicio'].value_counts().to_string())

    # 3. RECOBROS
    potentials = [c for c in df.columns if 'cost' in c or 'mont' in c or 'imp' in c or 'recob' in c or 'cob' in c]
    output.append(f"\n--- POTENTIAL COST COLUMNS: {potentials} ---")
    for p in potentials:
        output.append(f"{p} sample: {df[p].dropna().head(5).tolist()}")

    # 4. COORDINATION (Time Check)
    output.append("\n--- TIME SAMPLES (hrs_) ---")
    if 'hrs_contacto' in df.columns and 'hrs_asignacion' in df.columns:
        output.append("hrs_contacto sample: " + str(df['hrs_contacto'].dropna().head(10).tolist()))
        output.append("hrs_asignacion sample: " + str(df['hrs_asignacion'].dropna().head(10).tolist()))
        
    output.append("\n--- DATE SAMPLES (Check for Time) ---")
    if 'fec_contacto' in df.columns and 'fec_asignacion' in df.columns:
        date_sample = df[['fec_contacto', 'fec_asignacion']].dropna().head(10)
        output.append(date_sample.to_string())
        
        # Check if they are just dates or datetimes
        output.append("\nData Types:")
        output.append(str(df[['fec_contacto', 'fec_asignacion']].dtypes))
        
        # Calculate diff in minutes for sample
        try:
            start = pd.to_datetime(df['fec_contacto'], errors='coerce')
            end = pd.to_datetime(df['fec_asignacion'], errors='coerce')
            diff = (end - start).dt.total_seconds() / 60
            valid_diff = diff.dropna()
            output.append(f"\nCalculated Diffs (Min) Sample: {valid_diff.head(10).tolist()}")
            output.append(f"Zero Min diffs (Auto-assign?): {(valid_diff == 0).sum()}")
            output.append(f"Total Valid Dates: {len(valid_diff)}")
        except Exception as e:
            output.append(f"Error calc diffs: {e}")

    output_path = "C:/Users/Ricardo/.gemini/antigravity/brain/61a8fe09-a053-40ef-bafc-2be2af91e16f/debug_output.txt"
    
    # DETAILED COORDINATION ANALYSIS
    output.append("\n\n=== DETAILED COORDINATION ANALYSIS ===")
    if {'fec_contacto', 'hrs_contacto', 'fec_asignacion', 'hrs_asignacion'}.issubset(df.columns):
        def combine_dt(row):
            try:
                d = pd.to_datetime(row['fec_contacto'])
                t = row['hrs_contacto']
                if pd.isna(d) or pd.isna(t): return pd.NaT
                t_str = str(t).strip()
                if hasattr(t, 'hour'): t_str = t.strftime('%H:%M:%S')
                return pd.to_datetime(f"{d.strftime('%Y-%m-%d')} {t_str}", errors='coerce')
            except:
                return pd.NaT
        
        def combine_dt_assign(row):
            try:
                d = pd.to_datetime(row['fec_asignacion'])
                t = row['hrs_asignacion']
                if pd.isna(d) or pd.isna(t): return pd.NaT
                t_str = str(t).strip()
                if hasattr(t, 'hour'): t_str = t.strftime('%H:%M:%S')
                return pd.to_datetime(f"{d.strftime('%Y-%m-%d')} {t_str}", errors='coerce')
            except:
                return pd.NaT
        
        df['_dt_contact'] = df.apply(combine_dt, axis=1)
        df['_dt_assign'] = df.apply(combine_dt_assign, axis=1)
        df['_diff_min'] = (df['_dt_assign'] - df['_dt_contact']).dt.total_seconds() / 60
        
        valid_diffs = df['_diff_min'].dropna()
        output.append(f"Total with valid diffs: {len(valid_diffs)}")
        output.append(f"Diffs <= 10 min: {(valid_diffs <= 10).sum()}")
        output.append(f"Diffs > 10 min: {(valid_diffs > 10).sum()}")
        output.append(f"Diffs == 0 min: {(valid_diffs == 0).sum()}")
        output.append(f"Diffs < 0 (negative): {(valid_diffs < 0).sum()}")
        
        output.append("\nDistribution of diffs (binned):")
        bins = [float('-inf'), 0, 5, 10, 30, 60, float('inf')]
        labels = ['<0', '0-5', '5-10', '10-30', '30-60', '>60']
        df['_diff_bin'] = pd.cut(valid_diffs, bins=bins, labels=labels)
        output.append(df['_diff_bin'].value_counts().to_string())
        
        output.append("\nSample of diffs > 10 min:")
        outliers = df[df['_diff_min'] > 10][['mes', 'fec_contacto', 'hrs_contacto', 'fec_asignacion', 'hrs_asignacion', '_diff_min']].head(10)
        output.append(outliers.to_string())
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output))
    print(f"Analysis written to {output_path}")

if __name__ == "__main__":
    analyze()
