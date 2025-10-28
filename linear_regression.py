import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

if __name__ == "__main__":  

    df = pd.read_csv("data/ecai_authors_summary.csv")

    percentage_female = df.loc[df['gender'] == 'female', 'percentage'].to_numpy()
    percentage_male   = df.loc[df['gender'] == 'male', 'percentage'].to_numpy()
    years             = df.loc[df['gender'] == 'female', 'year'].to_numpy().reshape(-1, 1)

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
        marker=dict(color='blue', size=8)
    ))

    # Fitted trend line (historical)
    fig.add_trace(go.Scatter(
        x=years.flatten(), y=reg.predict(X),
        mode='lines',
        name='Fitted trend',
        line=dict(color='green', width=2)
    ))

    # Future predictions
    fig.add_trace(go.Scatter(
        x=future_years.flatten(), y=future_gap,
        mode='lines',
        name='Predicted until gap=0',
        line=dict(color='red', dash='dash')
    ))

    # Horizontal line at gap = 0
    fig.add_hline(
        y=0, line_dash="dot", line_color="black",
        annotation_text="Parity (gap = 0)", annotation_position="bottom right"
    )

    # Layout
    fig.update_layout(
        title="Predicted Gender Gap Over Time",
        xaxis_title="Year",
        yaxis_title="Male - Female % Difference",
        legend_title="Legend",
        template="plotly_white"
    )

    fig.show()
