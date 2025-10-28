import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from plotly import graph_objects as go

def make_linear_regression_plot() -> go.Figure:  

	df = pd.read_csv("data/ecai_authors_summary.csv")

	percentage_female = df.loc[df['gender'] == 'female', 'percentage'].to_numpy()
	percentage_male   = df.loc[df['gender'] == 'male', 'percentage'].to_numpy()
	years			 = df.loc[df['gender'] == 'female', 'year'].to_numpy().reshape(-1, 1)

	y = (percentage_male - percentage_female)
	X = years

	reg = LinearRegression().fit(X, y)
	a = reg.coef_[0]
	b = reg.intercept_

	# --- Predict until the gap reaches 0 ---
	zero_year = -b / a
	zero_year = int(np.ceil(zero_year))

	last_year = int(X.max())
	future_years = np.arange(last_year + 1, zero_year + 1).reshape(-1, 1)
	future_gap = reg.predict(future_years)

	# --- Create Plotly figure ---
	fig = go.Figure()

	# Observed data
	fig.add_trace(go.Scatter(
		x=years.flatten(), y=y,
		mode='markers',
		name='Observed',
		marker=dict(color='rgba(255, 255, 255, 0.3)', size=10, line=dict(width=1, color='#FFC857'))
	))

	# Fitted trend line (historical)
	fig.add_trace(go.Scatter(
		x=years.flatten(), y=reg.predict(X),
		mode='lines',
		name='Fitted trend',
		line=dict(color='#5158bb', width=3)
	))

	# Future predictions
	fig.add_trace(go.Scatter(
		x=future_years.flatten(), y=future_gap,
		mode='lines',
		name='Predicted until gap=0',
		line=dict(color='#5158bb', width=3, dash='dash')
	))

	# Horizontal line at gap = 0
	fig.add_hline(
		y=0, line_dash="dot", line_color="#FFC857",
		annotation_text="Parity (gap = 0)", annotation_position="right"
	)
		
	from plotly_template_initializer import initialize_plotly_template
	initialize_plotly_template()

	# Layout
	fig.update_layout(
		title="Prediction of When the Gender Gap Will Close",
		xaxis_title="Year",
		yaxis_title="Gender Gap (% male - female)",
		template="my_style"
	)
	return fig


def export_linear_regression_html(html_path: str = 'docs/plots/linear_regression.html') -> None:
	"""Build and export the linear regression plot as an HTML fragment (non-full HTML).

	By default it writes a file at `docs/plots/linear_regression.html` using the same
	include pattern as other scripts in this repo.
	"""
	fig = make_linear_regression_plot()
	print(f"Writing linear regression HTML to {html_path}...")
	fig.write_html(file=html_path, include_plotlyjs='../plotly-3.1.0.min.js', full_html=False)
	print("COMPLETED!")


if __name__ == "__main__":
	export_linear_regression_html()