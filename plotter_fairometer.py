
"""Simple tachimeter/gauge using Plotly.

This script creates a simple 0-100 gauge with a needle pointing to a mid value
and exports the result to an HTML file (matching the export pattern used in
the other plotting scripts).
"""

from plotly import graph_objects as go
import math

DEFAULT_GAUGE_VALUE = 67.0


def make_gauge(value: float = DEFAULT_GAUGE_VALUE, min_val: float = 0.0, max_val: float = 100.0) -> go.Figure:
	"""Create a simple tachimeter/gauge (0..100) with a needle.

	The appearance is intentionally minimal: semicircular gauge, three colored
	ranges (green/yellow/red), and a needle pointing to `value`.
	"""
	# Base indicator (semi-circular gauge) — use Indicator for the arc and number
	fig = go.Figure(go.Indicator(
		mode="gauge+number",
		value=value,
		domain={"x": [0, 1], "y": [0, 1]},
		title={"text": "Fairometer", "font": {"size": 20}},
		gauge={
			"axis": {"range": [min_val, max_val], "tickmode": "auto"},
			"bar": {"color": "rgba(0,0,0,0)"},  # hide the filled bar, we'll draw a needle
			"steps": [
				{"range": [min_val, min_val + (max_val - min_val) * 0.6], "color": "rgba(116, 27, 96, 0.8)"},
				{"range": [min_val + (max_val - min_val) * 0.6, min_val + (max_val - min_val) * 0.85], "color": "rgba(27, 69, 116, 0.8)"},
				{"range": [min_val + (max_val - min_val) * 0.85, max_val], "color": "rgba(27, 116, 61, 0.8)"},
			],
		}
	))

	# Draw a needle as a line overlay in paper coordinates (0..1)
	# Map value -> angle over [pi, 0] (left=0 -> right=pi) to create a semicircle
	fraction = (value - min_val) / (max_val - min_val)
	fraction = max(0.0, min(1.0, fraction))
	angle = math.pi * (1 - fraction)  # 0..pi

	# center and radius in paper coords
	cx, cy = 0.5, 0.48
	radius = 0.38
	xend = cx + radius * math.cos(angle)
	yend = cy + radius * math.sin(angle)

	fig.add_shape(
		type="line",
		x0=cx, y0=cy, x1=xend, y1=yend,
		xref='paper', yref='paper',
		line=dict(color='#c7d2fe', width=4)
	)
	
	from plotly_template_initializer import initialize_plotly_template
	initialize_plotly_template()

	# center cap
	fig.add_trace(go.Scatter(
		x=[cx], y=[cy], mode='markers', marker=dict(size=14, color='black'), showlegend=False,
		xaxis='x', yaxis='y'
	))

	fig.update_layout(
		height=360,
		template='my_style',
		margin=dict(l=30, r=30, t=60, b=20),
		xaxis=dict(visible=False),
		yaxis=dict(visible=False),  
	)

	return fig


def export_gauge_html(value: float = DEFAULT_GAUGE_VALUE, html_path: str = 'docs/plots/gauge.html') -> None:
	"""Build and export the gauge as an HTML fragment (non-full HTML).

	By default it writes a file at `docs/plots/gauge.html` using the same
	include pattern as other scripts in this repo.
	"""
	fig = make_gauge(value=value)
	print(f"Writing gauge HTML (value={value}) to {html_path}...")
	fig.write_html(file=html_path, include_plotlyjs='../plotly-3.1.0.min.js', full_html=False)
	print("COMPLETED!")


if __name__ == "__main__":
	# Export a default mid-value gauge when run directly
	export_gauge_html()

