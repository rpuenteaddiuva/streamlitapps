import pandas as pd
import os

def debug_dates():
    input_path = "datos/Servicios brindados ADS 2025 (1).xlsx"
    print(f"Loading {input_path}...")
    df = pd.read_excel(input_path)
    
    df.columns = (df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('/', '_').str.replace('.', ''))
    
    print("\n--- TYPES ---")
    print(df[['fec_asignacion', 'hrs_asignacion', 'fec_contacto', 'hrs_contacto']].dtypes)
    
    print("\n--- SAMPLE VALUES (NON-NULL) ---")
    subset = df[['fec_asignacion', 'hrs_asignacion', 'fec_contacto', 'hrs_contacto']].dropna()
    print(subset.head(5))
    
    if not subset.empty:
        print("\n--- FIRST VALID ROW TYPES ---")
        row = subset.iloc[0]
        for c in ['fec_asignacion', 'hrs_asignacion', 'fec_contacto', 'hrs_contacto']:
            val = row[c]
            print(f"{c}: {val} (Type: {type(val)})")

if __name__ == "__main__":
    debug_dates()
