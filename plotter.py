# read data from CSV file "ecai_authors_summary.csv" and plot statistics

import pandas as pd
import matplotlib.pyplot as plt

# read data from CSV file
df = pd.read_csv("ecai_authors_summary.csv")
# File is structured as follows:
# year, total_authors, gender, count, percentage, avg_probability
# We want to plot, for every year, the count of authors grouped by gender

male_df = df[df["gender"] == "male"]
female_df = df[df["gender"] == "female"]
other_df = df[df["gender"] == "unknown"]

# plot statistics
# grouped bar plot comparing genders per year

pivot = df.pivot_table(index='year', columns='gender', values='count', aggfunc='sum', fill_value=0)
x = np.arange(len(pivot))
width = 0.25

plt.figure(figsize=(10, 6))
plt.bar(x - width, pivot.get('male', pd.Series(0, index=pivot.index)), width, label='Male', color='blue')
plt.bar(x,        pivot.get('female', pd.Series(0, index=pivot.index)), width, label='Female', color='pink')
plt.bar(x + width, pivot.get('unknown', pd.Series(0, index=pivot.index)), width, label='Unknown', color='green')

plt.xticks(x, pivot.index, rotation=45)
plt.tight_layout()
plt.title("Number of Authors by Gender Over Years")
plt.xlabel("Year")
plt.ylabel("Number of Authors")
plt.legend()
plt.show()