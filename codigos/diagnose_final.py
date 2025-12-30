import pandas as pd
import os

def diagnose():
    path = "resultados/analyzed_bbdd.xlsx"
    print(f"Loading {path}...")
    df = pd.read_excel(path)
    
    col_prog = next((c for c in df.columns if 'programado' in c), None)
    col_nps = next((c for c in df.columns if 'nps' in c or 'calificacion' in c), None)
    col_status = next((c for c in df.columns if 'status' in c or 'estado' in c), None)

    print("### PROG ###")
    if col_prog: print(df[col_prog].value_counts(dropna=False).to_dict())
    print("### NPS ###")
    if col_nps: print(df[col_nps].value_counts().sort_index().to_dict())
    print("### STATUS ###")
    if col_status: print(df[col_status].value_counts().head(10).to_dict())

if __name__ == "__main__":
    diagnose()
