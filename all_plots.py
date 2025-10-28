import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd


# read data from CSV file "ecai_authors_summary.csv" and plot statistics
if __name__ == "__main__":  

    df = pd.read_csv("data/ecai_authors_summary.csv")

    # Pivot by 'count' and 'percentage'
    pivot_count = df.pivot_table(index='year', columns='gender', values='count', aggfunc='sum', fill_value=0)
    pivot_pct = df.pivot_table(index='year', columns='gender', values='percentage', aggfunc='sum', fill_value=0)

    # Set up figure with 3 subplots (2 static, 1 interactive)
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.3, 1])
    ax_bar = fig.add_subplot(gs[0, 0])
    ax_stack = fig.add_subplot(gs[1, 0])
    ax_pie = fig.add_subplot(gs[:, 1])

    plt.subplots_adjust(bottom=0.15, hspace=0.4)

    # Grouped Bar Plot
    x = np.arange(len(pivot_count))
    width = 0.25
    ax_bar.bar(x - width, pivot_count.get('male', 0), width, label='Male', color='blue')
    ax_bar.bar(x, pivot_count.get('female', 0), width, label='Female', color='pink')
    ax_bar.bar(x + width, pivot_count.get('unknown', 0), width, label='Unknown', color='green')

    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(pivot_count.index, rotation=45)
    ax_bar.set_title("Number of Authors by Gender Over Years")
    ax_bar.set_xlabel("Year")
    ax_bar.set_ylabel("Number of Authors")
    ax_bar.grid(color="lightgray", linestyle="dashed")
    ax_bar.legend()

    # Stackplot 
    x_stack = pivot_pct.index
    male = pivot_pct.get('male', pd.Series(0, index=pivot_pct.index))
    female = pivot_pct.get('female', pd.Series(0, index=pivot_pct.index))
    unknown = pivot_pct.get('unknown', pd.Series(0, index=pivot_pct.index))

    ax_stack.stackplot(x_stack, male, female, unknown, labels=['Male', 'Female', 'Unknown'], colors=['blue', 'pink', 'green'])
    ax_stack.set_xticks(x_stack)
    ax_stack.set_xticklabels(x_stack, rotation=45)
    ax_stack.set_title("Percentage of Authors by Gender Over Years")
    ax_stack.set_xlabel("Year")
    ax_stack.set_ylabel("Percentage")
    ax_stack.grid(color="gray", linestyle="dashed")
    ax_stack.legend(loc='lower left')

    # Interactive Pie Chart 
    initial_year = pivot_pct.index[0]
    values = pivot_pct.loc[initial_year]

    wedges, texts, autotexts = ax_pie.pie(
        values,
        labels=values.index,
        autopct='%1.1f%%',
        colors=['pink', 'blue', 'green']
    )
    ax_pie.set_title(f"Gender Distribution in {initial_year}")

    # Add slider
    ax_slider = plt.axes([0.62, 0.1, 0.25, 0.03])  # position of slider
    slider = Slider(
        ax=ax_slider,
        label='Year',
        valmin=2000,
        valmax=2024,
        valinit=0,
        valstep=1, 
        color="pink"
    )

    def update(val):
        year_index = int(slider.val)-2000
        year = pivot_pct.index[year_index]
        ax_pie.clear()
        values = pivot_pct.loc[year]
        ax_pie.pie(values, labels=values.index, autopct='%1.1f%%', colors=['pink', 'blue', 'green'])
        ax_pie.set_title(f"Gender Distribution in {year}")
        fig.canvas.draw_idle()

    slider.on_changed(update)

    plt.show()
