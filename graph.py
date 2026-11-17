#!/usr/bin/env python3

import argparse
import csv

import matplotlib.pyplot as plt


def read_csv_data(path, x_column, y_column):
    x_values = []
    y_values = []

    with open(path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None or x_column not in reader.fieldnames or y_column not in reader.fieldnames:
            raise ValueError(
                f"CSV must contain columns {x_column!r} and {y_column!r}."
            )
        for row_number, row in enumerate(reader, start=2):
            try:
                x_values.append(float(row[x_column]))
                y_values.append(float(row[y_column]))
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid numeric data on CSV row {row_number}."
                ) from error

    if not x_values:
        raise ValueError("CSV contains no data rows.")
    if any(value <= 0 for value in y_values):
        raise ValueError("All y values must be positive for the logarithmic axis.")

    return x_values, y_values


def plot_histogram(x_values, y_values):
    plt.bar(x_values, y_values, edgecolor="black")
    plt.xlabel("DM Mass (MeV)")
    plt.ylabel("# of Signal Events")
    plt.title("# of Signal Events")
    plt.yscale("log")
    plt.tight_layout()
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description="Plot histogram-style bars from x and y columns in a CSV file."
    )
    parser.add_argument("csv_file", help="CSV file with a header row")
    parser.add_argument("--x-column", default="x", help="CSV column for the x-axis (default: x)")
    parser.add_argument("--y-column", default="y", help="CSV column for the y-axis (default: y)")
    args = parser.parse_args()

    try:
        x_values, y_values = read_csv_data(
            args.csv_file, args.x_column, args.y_column
        )
    except (OSError, ValueError) as error:
        parser.error(str(error))
    plot_histogram(x_values, y_values)


if __name__ == "__main__":
    main()
