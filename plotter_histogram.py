"""Create a grouped bar chart (by year) showing author counts per gender using Plotly.

This replaces the original Matplotlib-based script with Plotly and adds an
export function mirroring the style used in other scripts in the repo.
"""

from plotly import graph_objects as go
import plotly.io as pio
import pandas as pd


def make_grouped_histogram(csv_path: str = "data/ecai_authors_summary.csv") -> go.Figure:
	"""Build a grouped bar chart (per-year counts by gender) as a Plotly Figure.

	Expects CSV columns including: year, total_authors, gender, count, percentage, avg_probability
	"""
	df = pd.read_csv(csv_path)
	pivot = df.pivot_table(index='year', columns='gender', values='count', aggfunc='sum', fill_value=0)

	years = pivot.index.tolist()

	male = pivot.get('male', pd.Series(0, index=pivot.index)).astype(float).tolist()
	female = pivot.get('female', pd.Series(0, index=pivot.index)).astype(float).tolist()
	unknown = pivot.get('unknown', pd.Series(0, index=pivot.index)).astype(float).tolist()

	colors = {
		'male': '#5158bb',
		'female': '#EB4B98',
		'unknown': '#FFC857'
	}

	fig = go.Figure()
	fig.add_trace(go.Bar(x=years, y=male, name='Male', marker_color=colors['male']))
	fig.add_trace(go.Bar(x=years, y=female, name='Female', marker_color=colors['female']))
	fig.add_trace(go.Bar(x=years, y=unknown, name='Unknown', marker_color=colors['unknown']))

	from plotly_template_initializer import initialize_plotly_template
	initialize_plotly_template()

	fig.update_layout(
		barmode='group',
		title_text='Number of Authors by Gender',
		xaxis_title='Year',
		yaxis_title='Number of Authors',
		template='my_style',
		legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
	)

	return fig


def export_histogram_html(csv_path: str = "data/ecai_authors_summary.csv", html_path: str = 'docs/plots/histogram.html') -> None:
	fig = make_grouped_histogram(csv_path=csv_path)
	print("Writing grouped histogram HTML...")
	fig.write_html(file=html_path, include_plotlyjs='../plotly-3.1.0.min.js', full_html=False)
	print("COMPLETED!")


if __name__ == "__main__":
	export_histogram_html()