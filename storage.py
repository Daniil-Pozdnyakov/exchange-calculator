import csv


def convert_from_csv(path_to_file: str):
    data = []
    with open(f"./cache/{path_to_file}", newline="") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            data.append(row)
    return data
