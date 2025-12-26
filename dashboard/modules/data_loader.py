"""
ADS Boletín - Data Loading Module
"""
import pandas as pd
import streamlit as st
import os


@st.cache_data
def load_data(uploaded_file=None):
    """Load data from file or local source"""
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='latin1')
        else:
            df = pd.read_excel(uploaded_file)
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '')
        return df
    
    # Try local files (relative to dashboard folder)
    base = os.path.dirname(os.path.dirname(__file__))  # Go up one level from modules
    
    paths = [
        os.path.join(base, "resultados", "analyzed_bbdd.xlsx"),
        os.path.join(base, "..", "resultados", "analyzed_bbdd.xlsx"),
        os.path.join(base, "datos", "Servicios brindados ADS 2025 (1).xlsx"),
    ]
    
    for path in paths:
        if os.path.exists(path):
            try:
                if 'Servicios brindados' in path:
                    df = pd.read_excel(path, sheet_name='BBDD')
                else:
                    df = pd.read_excel(path)
                return df
            except:
                continue
    
    return None


def get_month_order():
    return {'Ene': 1, 'Feb': 2, 'Mar': 3, 'Abr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Ago': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dic': 12}


def sort_months(months):
    month_order = get_month_order()
    return sorted(months, key=lambda x: (
        int(str(x).split('-')[-1]) if '-' in str(x) else 0,
        month_order.get(str(x).split('-')[0], 0)
    ))
