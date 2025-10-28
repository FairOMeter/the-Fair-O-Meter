from plotly import graph_objects as go
import pandas as pd


def make_animated_pie(csv_path: str = "data/ecai_authors_summary.csv") -> go.Figure:
    """Create a Plotly animated pie chart (frames + slider) from the summary CSV.
    """
    df = pd.read_csv(csv_path)
    pivot = df.pivot_table(index='year', columns='gender', values='percentage', aggfunc='sum', fill_value=0)

    years = list(pivot.index)
    labels = list(pivot.columns)
    # Ensure values follow the same label ordering for every year
    values_by_year = [pivot.loc[y].reindex(labels).tolist() for y in years]

    # Initial pie (first year)
    fig = go.Figure(
        data=[
            go.Pie(labels=labels, values=values_by_year[0], hole=0.2, sort=False, textinfo='percent+label')
        ],
        frames=[
            go.Frame(
                data=[go.Pie(labels=labels, values=vals, hole=0.2, sort=False, textinfo='percent+label')],
                name=str(year),
                layout=go.Layout(title_text=f"Gender distribution in {year}")
            )
            for year, vals in zip(years, values_by_year)
        ],
    )
    fig.update_traces(marker=dict(colors=["pink", "teal", "lime"], line=dict(color='rgba(255, 255, 255, 200)', width=2)))

    # Slider steps for each frame/year
    steps = []
    for year in years:
        steps.append(
            dict(
                method="animate",
                args=[[str(year)], {"frame": {"duration": 400, "redraw": True}, "mode": "immediate"}],
                label=str(year),
            )
        )

    sliders = [
        dict(
            active=0,
            pad={"t": 50},
            steps=steps,
        )
    ]

    # Play / Pause buttons
    updatemenus = [
        dict(
            type="buttons",
            showactive=False,
            y=0,
            x=1.05,
            xanchor="right",
            yanchor="top",
            pad={"t": 0, "r": 10},
            buttons=[
                dict(
                    label="Play",
                    method="animate",
                    args=[None, {"frame": {"duration": 800, "redraw": True}, "fromcurrent": True, "mode": "immediate"}],
                ),
                dict(
                    label="Pause",
                    method="animate",
                    args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                ),
            ],
        )
    ]

    fig.update_layout(
        title_text=f"Gender distribution in {years[0]}",
        updatemenus=updatemenus,
        sliders=sliders,
    )

    return fig


def export_animated_pie_html(csv_path: str = "data/ecai_authors_summary.csv", html_path: str = 'docs/plots/animated_pie.html') -> None:
    fig = make_animated_pie(csv_path=csv_path)
    print("Writing animated pie chart HTML...")
    fig.write_html(file=html_path, include_plotlyjs='../plotly-3.1.0.min.js', full_html=False)
    # Assuming we have a "plotly.min.js" script in the root directory of the web page
    print("COMPLETED!")

if __name__ == "__main__":
    export_animated_pie_html()