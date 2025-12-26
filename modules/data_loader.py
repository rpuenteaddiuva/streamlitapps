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
    
    # Try local files in order of preference
    paths = [
        os.path.join(os.path.dirname(__file__), "resultados", "analyzed_bbdd.xlsx"),
        os.path.join(os.path.dirname(__file__), "datos", "Servicios brindados ADS 2025 (1).xlsx"),
        "resultados/analyzed_bbdd.xlsx"
    ]
    
    for path in paths:
        if os.path.exists(path):
            try:
                if 'Servicios brindados' in path:
                    df = pd.read_excel(path, sheet_name='BBDD')
                else:
                    df = pd.read_excel(path)
                df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('.', '')
                return df
            except:
                continue
    
    return None


def get_month_order():
    """Return month order for sorting"""
    return {'Ene': 1, 'Feb': 2, 'Mar': 3, 'Abr': 4, 'May': 5, 'Jun': 6,
            'Jul': 7, 'Ago': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dic': 12}


def sort_months(months):
    """Sort months chronologically"""
    month_order = get_month_order()
    return sorted(months, key=lambda x: (
        int(str(x).split('-')[-1]) if '-' in str(x) else 0,
        month_order.get(str(x).split('-')[0], 0)
    ))
