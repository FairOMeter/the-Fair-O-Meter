from plotly import graph_objects as go
import plotly.io as pio
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
	
	# Definisci il template personalizzato
	my_template = go.layout.Template(
		layout=dict(
			font=dict(
				family="'Segoe UI', Arial, sans-serif",
				size=14,
				color="#c7d2fe"
			),
			paper_bgcolor='rgba(255, 255, 255, 0)',
			plot_bgcolor="#070708",
			
			#colorway=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'],
			
			xaxis=dict(
				showgrid=True,
				gridcolor='#ecf0f1',
				linecolor='#bdc3c7',
				tickfont=dict(size=12)
			),
			yaxis=dict(
				showgrid=True,
				gridcolor='#ecf0f1',
				linecolor='#bdc3c7',
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

	fig.update_layout(
		title_text='Number of Authors by Gender Over Years',
		xaxis_title='Year',
		yaxis_title='Number of Authors',
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
