"""
ADS Boletín - Charts Module
Plotly charts for dashboard visualization
"""
import plotly.express as px
import plotly.graph_objects as go

# Color palette
COLORS = {
    'primary': '#0055a6',
    'secondary': '#4a90d9',
    'success': '#2e7d32',
    'warning': '#ffc107',
    'danger': '#e53935',
    'purple': '#6a1b9a',
}


def pie_chart(values, names, title, hole=0):
    """Create pie/donut chart"""
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['warning'], COLORS['success']]
    fig = px.pie(values=values, names=names, title=title, hole=hole,
                 color_discrete_sequence=colors)
    return fig


def bar_chart(x, y, title, orientation='v', color=None):
    """Create bar chart"""
    if orientation == 'h':
        fig = px.bar(x=y, y=x, orientation='h', title=title,
                     color_discrete_sequence=[color or COLORS['primary']])
        fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    else:
        fig = px.bar(x=x, y=y, title=title,
                     color_discrete_sequence=[color or COLORS['primary']])
    return fig


def stacked_bar(df_pivot, title):
    """Create stacked bar chart"""
    colors = [COLORS['primary'], COLORS['secondary'], COLORS['warning'], COLORS['success']]
    fig = px.bar(df_pivot, barmode='stack', title=title,
                 color_discrete_sequence=colors)
    return fig


def gauge_chart(value, title, target=None):
    """Create gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': COLORS['success']},
            'steps': [
                {'range': [0, 50], 'color': "#ffebee"},
                {'range': [50, 75], 'color': "#fff3e0"},
                {'range': [75, 100], 'color': "#e8f5e9"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': target or 82
            }
        }
    ))
    return fig
