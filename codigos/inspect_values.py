import pandas as pd
import os

def inspect():
    path = "resultados/analyzed_bbdd.xlsx"
    df = pd.read_excel(path)
    
    with open("debug_counts.txt", "w", encoding="utf-8") as f:
        # Prog
        col_prog = next((c for c in df.columns if 'programado' in c), None)
        f.write(f"COL PROG: {col_prog}\n")
        if col_prog:
            f.write(str(df[col_prog].value_counts(dropna=False).to_dict()) + "\n")
            
        # NPS
        col_nps = next((c for c in df.columns if 'nps' in c or 'calificacion' in c), None)
        f.write(f"COL NPS: {col_nps}\n")
        if col_nps:
            f.write(str(df[col_nps].value_counts(dropna=False).sort_index().to_dict()) + "\n")
            
        # Status
        col_status = next((c for c in df.columns if 'status' in c or 'estado' in c), None)
        f.write(f"COL STATUS: {col_status}\n")
        if col_status:
            f.write(str(df[col_status].value_counts().head(20).to_dict()) + "\n")

if __name__ == "__main__":
    inspect()
