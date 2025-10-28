
"""
This scripts creates a simple timeline using Plotly.

The timeline is represented as a horizontal arrow.
It starts at 2000 and it has a checkpoint at 2025. That's where we are now.
Then, it continues until the year PERFECT_PARITY_YEAR, which is the year
when we expect to reach gender parity if the current trend continues.
"""

from plotly import graph_objects as go

PERFECT_PARITY_YEAR = 2163


def make_timeline() -> go.Figure:
	"""Create a simple timeline from 2000 to PERFECT_PARITY_YEAR."""
	fig = go.Figure()

	# Add a horizontal line for the timeline
	fig.add_shape(
		type="line",
		x0=2000, y0=0, x1=2025, y1=0,
		line=dict(color="#5158bb", width=18),
		layer="below"
	)
	fig.add_shape(
        type="line",
        x0=2025, y0=0, x1=PERFECT_PARITY_YEAR, y1=0,
        line=dict(color="#27ae8c", width=18), 
		layer="below"
	)

	# Add checkpoints
	checkpoints = [2000, 2025, PERFECT_PARITY_YEAR]
	colors = {
        2000: "#5158bb",
        2025: "#517bbb",
        PERFECT_PARITY_YEAR: "#27ae8c"
    }
	labels = {
        2000: "2000",
        2025: "2025 - Today",
        PERFECT_PARITY_YEAR: str(PERFECT_PARITY_YEAR)
    }
	for year in checkpoints:
		fig.add_trace(go.Scatter(
			x=[year], y=[0], mode="markers+text",
			marker=dict(
				size=20, 
				color=colors[year], 
				symbol="diamond-tall",
				line=dict(width=1, color="white")
			),
			text=[str(year)], textposition="bottom center",
			name=labels[year],
		))
		
	from plotly_template_initializer import initialize_plotly_template
	initialize_plotly_template()

	fig.update_layout(
		xaxis=dict(visible=False, range=[1995, PERFECT_PARITY_YEAR + 5] ),
		yaxis=dict(visible=False),
		showlegend=False,
		template='my_style',
		height=100,
		width=(PERFECT_PARITY_YEAR - 2000) * 10,
        margin=dict(l=20, r=20, t=20, b=20)
	)

	return fig

def export_timeline_html(html_path: str = 'docs/plots/timeline.html') -> None:
	"""Build and export the timeline as an HTML fragment (non-full HTML).

	By default it writes a file at `docs/plots/timeline.html` using the same
	include pattern as other scripts in this repo.
	"""
	fig = make_timeline()
	print(f"Writing timeline HTML to {html_path}...")
	fig.write_html(file=html_path, include_plotlyjs='../plotly-3.1.0.min.js', full_html=False)
	print("COMPLETED!")
	
if __name__ == "__main__":
	export_timeline_html()