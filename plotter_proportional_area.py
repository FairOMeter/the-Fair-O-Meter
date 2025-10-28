from plotly import graph_objects as go
import pandas as pd


def make_proportional_area(csv_path: str = "data/ecai_authors_summary.csv") -> go.Figure:
	"""
	Create a stacked area Plotly chart showing number of authors by gender over years.
	"""
	df = pd.read_csv(csv_path)
	pivot = df.pivot_table(index='year', columns='gender', values='percentage', aggfunc='sum', fill_value=0)

	years = pivot.index.tolist()
	# keep consistent ordering of genders and provide defaults
	male = pivot.get('male', pd.Series(0, index=pivot.index)).astype(float)
	female = pivot.get('female', pd.Series(0, index=pivot.index)).astype(float)
	unknown = pivot.get('unknown', pd.Series(0, index=pivot.index)).astype(float)

	colors = {
		'male': '#5158bb',
		'female': '#EB4B98',
		'unknown': '#FFC857'
	}

	fig = go.Figure()
	fig.add_trace(
		go.Scatter(
			x=years,
			y=male.tolist(),
			mode='lines',
			name='Male',
			stackgroup='one',
			line=dict(color=colors['male'])
		)
	)
	fig.add_trace(
		go.Scatter(
			x=years,
			y=female.tolist(),
			mode='lines',
			name='Female',
			stackgroup='one',
			line=dict(color=colors['female'])
		)
	)
	fig.add_trace(
		go.Scatter(
			x=years,
			y=unknown.tolist(),
			mode='lines',
			name='Unknown',
			stackgroup='one',
			line=dict(color=colors['unknown'])
		)
	)

	from plotly_template_initializer import initialize_plotly_template
	initialize_plotly_template()
	
	fig.update_layout(
		title_text='Percentage of Authors by Gender',
		xaxis_title='Year',
		yaxis_title='% of Authors',
		template='my_style',
		legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
	)

	return fig


def export_proportional_html(csv_path: str = "data/ecai_authors_summary.csv", html_path: str = 'docs/plots/proportional_area.html') -> None:
	fig = make_proportional_area(csv_path=csv_path)
	print("Writing proportional stacked area chart HTML...")
	fig.write_html(file=html_path, include_plotlyjs='../plotly-3.1.0.min.js', full_html=False)
	print("COMPLETED!")


if __name__ == "__main__":
	export_proportional_html()
