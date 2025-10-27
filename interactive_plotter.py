import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pandas as pd

df = pd.read_csv("ecai_authors_summary.csv")
pivot = df.pivot_table(index='year', columns='gender', values='percentage', aggfunc='sum', fill_value=0)
initial_year = pivot.index[0]

fig, ax = plt.subplots(figsize=(6, 6))
plt.subplots_adjust(bottom=0.25)  # make room for slider

# Plot initial pie
values = pivot.loc[initial_year]
wedges, texts, autotexts = ax.pie(
    values, 
    labels=values.index,
    autopct='%1.1f%%',
    colors=['blue', 'pink', 'green']
)
ax.set_title(f"Gender Distribution in {initial_year}")

# Slider setup
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.05])
slider = Slider(
    ax=ax_slider,
    label='Year ',
    valmin=0,
    valmax=len(pivot.index) - 1,
    valinit=0,
    valstep=1
)

# Update function
def update(val):
    year_index = int(slider.val)
    year = pivot.index[year_index]
    ax.clear()
    values = pivot.loc[year]
    ax.pie(values, labels=values.index, autopct='%1.1f%%', colors=['pink', 'blue', 'green'])
    ax.set_title(f"Gender Distribution in {year}")
    fig.canvas.draw_idle()

slider.on_changed(update)

plt.show()