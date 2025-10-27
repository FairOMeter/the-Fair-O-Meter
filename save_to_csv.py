import csv

def names_to_csv(data):
    with open("authors.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "year", "author_name", "nr_of_instances"])
        writer.writeheader()
        writer.writerows(data)