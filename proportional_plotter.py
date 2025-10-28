import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read data from CSV file
df = pd.read_csv("data/ecai_authors_summary.csv")

male_df = df[df["gender"] == "male"]
female_df = df[df["gender"] == "female"]
other_df = df[df["gender"] == "unknown"]


# plot statistics
# grouped bar plot comparing proportional genders per year

pivot = df.pivot_table(index='year', columns='gender', values='percentage', aggfunc='sum', fill_value=0)
x = np.arange(len(pivot))
width = 0.25

plt.figure(figsize=(10, 6))

x = pivot.index
male = pivot.get('male', pd.Series(0, index=pivot.index))
female = pivot.get('female', pd.Series(0, index=pivot.index))
unknown = pivot.get('unknown', pd.Series(0, index=pivot.index))

# Stackplot
plt.stackplot(x, male, female, unknown, labels=['Male', 'Female', 'Unknown'], colors=['blue', 'pink', 'green'])

# Labels and style
plt.xticks(x, pivot.index, rotation=45)
plt.tight_layout()
plt.title("Number of Authors by Gender Over Years")
plt.xlabel("Year")
plt.ylabel("Number of Authors")
plt.legend(loc='lower left')
plt.grid(color="gray", linestyle="dashed")
plt.show()
