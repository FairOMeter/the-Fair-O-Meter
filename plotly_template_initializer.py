# This script initializes a custom Plotly template for consistent styling across charts.
# To use this template, set the template parameter to 'my_style' in your Plotly figure layout,
# after importing this module.
from plotly import graph_objects as go
import plotly.io as pio

def initialize_plotly_template():
    """Initialize and register a custom Plotly template for consistent styling."""
    my_template = go.layout.Template(
        layout=dict(
            font=dict(
                family="'Segoe UI', Arial, sans-serif",
                size=14,
                color="#c7d2fe"
            ),
            paper_bgcolor='rgba(255, 255, 255, 0)',
            plot_bgcolor="rgba(255, 255, 255, 0)",
            
            #colorway=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'],
            
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.4)',
                linecolor='rgba(255, 255, 255, 0.2)',
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(255, 255, 255, 0.4)',
                linecolor='rgba(255, 255, 255, 0.2)',
                tickfont=dict(size=12)
            ),
            
            title=dict(
                font=dict(size=22, color='rgba(255, 255, 255, 0.8)'),
                x=0.5,
                xanchor='center'
            )
        )
    )
    pio.templates["my_style"] = my_template