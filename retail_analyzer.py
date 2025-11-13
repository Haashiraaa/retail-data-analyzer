import numpy as np
from icecream import ic
import sys
import os
from pathlib import Path
import textwrap

# Toggle debug mode
DEBUG = False
if not DEBUG:
    ic.disable()
else:
    ic.enable()

# Sample retail data
PRICE = np.array([[120, 150, 90], [200, 250, 300], [80, 100, 120]])
TAXES = np.array([0.05, 0.10, 0.15])
DISCOUNT = np.array([[5, 10, 0], [10, 15, 20], [0, 5, 10]])
LINE = '=' * 18
TITLE = f"\n{LINE} Retail Data Analysis {LINE}"


def axis(ax="row"):
    """Returns axis value based on input: 'row' -> 1, 'col' -> 0."""
    ax = ax.lower().strip()
    if ax == "row":
        return 1
    elif ax == "col":
        return 0
    return None


def avg(arr, func=None):
    """Calculates mean of array. Optionally accepts axis."""
    if func is None:
        return np.mean(arr)
    return np.mean(arr, axis=func)


def add_tax(x=PRICE, y=TAXES):
    """Adds tax to each column of the price matrix."""
    return x + y


def add_discount(x, y=DISCOUNT):
    """Subtracts discount from price matrix. Ensures no negative values."""
    after_discount = x - y
    after_discount[after_discount < 0] = 0
    return after_discount


def binary_fmt(file=None, fn="discounted_data.npy", op="save"):
    """Handles saving/loading NumPy binary format (.npy)."""
    op = op.lower().strip()

    if op == "save":
        if file is None:
            print("\nEnter the file you wish to save!")
            return
        if not os.path.exists(fn):
            np.save(fn, file)
            print("\nSaved 'npy' file successfully.")
        else:
            ic(f"\n{fn} already exists!")

    elif op == "load":
        try:
            return np.load(fn)
        except FileNotFoundError:
            print(f"\n\n{fn} not found!")
            print("\n[Program finished.]")
            sys.exit()


def csv_fmt(file=None, fn="discounted_data.txt", op="save"):
    """Handles saving/loading text format (.txt) using CSV-style formatting."""
    op = op.lower().strip()

    if op == "save":
        if file is None:
            print("\nEnter the file you wish to save!")
            return
        if not os.path.exists(fn):
            np.savetxt(fn, file, fmt="%5f", delimiter=",")
            print("\nSaved 'txt' file successfully.")
        else:
            ic(f"\n{fn} already exists!")

    elif op == "load":
        try:
            return np.loadtxt(fn, delimiter=",")
        except FileNotFoundError:
            print(f"\n\n{fn} not found!")
            print("\n[Program finished.]")
            sys.exit()


def report(avg_price=0, max_price=0, min_price=0, med_price=None):
    """Generates a formatted summary report string."""
    return textwrap.dedent(f"""
        Average price: {avg_price}
        Maximum price: {max_price}
        Minimum price: {min_price}
        Median prices per column: {med_price}
    """)


def save_report(file, fn="report.txt"):
    """Appends report to file. Adds title if file is new."""
    path = Path(fn)
    new_file = not path.exists()
    with path.open("a", encoding="utf-8") as fc:
        if new_file:
            fc.write(TITLE + "\n\n")
            fc.write(file + "\n")
        print(f"\nYour '{fn}' has been saved in the current directory.")


def clear_screen():
    """Clears the terminal screen based on OS."""
    os.system("cls" if os.name == "nt" else "clear")


def main():
    """Main execution flow for retail data analysis."""
    clear_screen()

    # Apply tax and discount
    after_tax = add_tax()
    avg_price = avg(after_tax, axis())
    after_disc = add_discount(after_tax)

    # Save and load discounted data
    """
     Uncomment any of the format you'd like to save in..
     I chose binary format.
     If you wish to save and load in csv-like fmt..
     Comment out the binary_fmt line for save and load..
     And Uncomment the line for csvfmt..
     Both load and save.
    """
    binary_fmt(file=after_disc, op="save")
    # csv_fmt(file=after_disc, op="save")

    price_bnfmt = binary_fmt(op="load")
    # price_csvfmt = csv_fmt(op="load")

    # ic(price_bnfmt == price_csvfmt)  # Confirm both formats match

    # Final stats
    final_avg = round(avg(price_bnfmt), 2)
    max_price = np.max(price_bnfmt)
    min_price = np.min(price_bnfmt)
    price_med = np.median(np.sort(price_bnfmt), axis=0)

    # Generate and save report
    final_report = report(final_avg, max_price, min_price, price_med)
    save_report(final_report)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[Program finished.]")
        sys.exit()
