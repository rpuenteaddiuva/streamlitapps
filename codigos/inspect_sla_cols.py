import pandas as pd

def inspect():
    df = pd.read_excel("resultados/analyzed_bbdd.xlsx")
    
    print("\n--- SLA PROXY COLUMNS ---")
    cols = [c for c in df.columns if 'cumplimiento' in c or 'tiempo' in c]
    print(f"Columns: {cols}")
    
    for c in cols:
        print(f"\nVALUES for {c}:")
        print(df[c].value_counts(dropna=False).head(5))

    # Also check if 'tiempo_asignacion' is duration?
    if 'tiempo_asignacion' in df.columns:
        print("\nTIME ASIGNACION Stats:")
        # clean text like '10 min'
        try:
             # Assuming mixed types
            print(df['tiempo_asignacion'].describe())
        except:
            print("Cannot describe, showing head:")
            print(df['tiempo_asignacion'].head(10))

if __name__ == "__main__":
    inspect()
