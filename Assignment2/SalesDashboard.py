"""Sales Dashboard - a text-based dashboard built on Pandas pivot tables.

AI use: I used Claude to help with this assignment. Claude generated the first draft of several functions, 
including load_data and clean_data (loading, error handling and replacing missing values with zeros), parse_choices and 
ask_choices (validating menu input), side_by_side (printing two pivot tables next to each other), and the unit tests in 
test_sales_dashboard.py. The prompt was the assignment text. I read and ran each generated function, checked the pivot table 
results against the data, and adjusted the comments and menu list so I understand how they work. I also utilized copilot to identify 
and correct mistakes and any problems. The menu design (MENU_ITEMS), the pivot table functions and the overall structure were reviewed and edited by me.

Design notes (how the requirements are met):
- Every analytic is a function that RETURNS a pivot table (or None) and does
  not print. The menu loop does the printing. This makes the functions easy to
  test and lets the compare feature show two results side by side.
- The menu is a list of (label, function) tuples. To add, remove or reorder
  an item, edit MENU_ITEMS only. "Exit" is added automatically as the last item.
- Defensive programming: loading errors, missing columns, bad numbers and bad
  user input are all checked. Asserts document assumptions that must hold.
- The data has no sale price column, so "sales" = quantity * unit_price is
  added after loading. "sale type" in the assignment means order_type.
"""
import sys
import time

import pandas as pd

DRIVE_URL = "https://drive.google.com/uc?export=download&id=1Fv_vhoN4sTrUaozFPfzr0NCyHJLIeXEA"

# Columns the analytics need. A missing one only disables the analytics using it.
REQUIRED_COLUMNS = [
    "employee_id", "employee_name", "sales_region", "order_type",
    "customer_type", "customer_state", "product_category", "produce_name",
    "quantity", "unit_price",
]
NUMERIC_COLUMNS = ["quantity", "unit_price"]

# Fields offered in the custom pivot table generator.
CUSTOM_ROWS = ["employee_name", "sales_region", "product_category",
               "customer_state", "produce_name"]
CUSTOM_COLUMNS = ["order_type", "customer_type"]
CUSTOM_VALUES = ["quantity", "unit_price", "sales"]
CUSTOM_AGGREGATIONS = ["sum", "mean", "count", "min", "max"]


# ---------------------------------------------------------------- loading data
def load_data(source):
    """Read a CSV from a URL or file path. Returns (DataFrame, seconds taken).

    Raises ValueError with a readable message if the data cannot be used.
    """
    assert isinstance(source, str) and source, "source must be a non-empty string"
    start = time.time()
    try:
        df = pd.read_csv(source)
    except FileNotFoundError:
        raise ValueError(f"File not found: {source}")
    except pd.errors.EmptyDataError:
        raise ValueError("The file is empty.")
    except Exception as err:  # bad URL, no network, not a CSV, ...
        raise ValueError(f"Could not read the data: {err}")
    if df.empty:
        raise ValueError("The file has no rows of data.")
    return clean_data(df), time.time() - start


def clean_data(df):
    """Replace missing values with 0, force numeric columns to numbers and add
    the derived 'sales' column (quantity * unit_price)."""
    df = df.copy()
    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            # Text such as "abc" becomes NaN here and then 0 below.
            df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.fillna(0)
    if all(column in df.columns for column in NUMERIC_COLUMNS):
        df["sales"] = df["quantity"] * df["unit_price"]
    return df


def missing_columns(df):
    """Return the required columns that are not in the data."""
    return [column for column in REQUIRED_COLUMNS if column not in df.columns]


def load_interactively():
    """Ask which data to load, load it and report the result.

    Enter loads the default Google Drive file; typing a path or URL loads an
    alternate data set. Raises ValueError if loading fails.
    """
    text = input("Data to load - press Enter for the Google Drive file, "
                 "or type a file path/URL: ").strip()
    source = text if text else DRIVE_URL
    print("Loading data...", flush=True)
    df, seconds = load_data(source)
    print("Data loaded successfully.")
    print(f"Load time: {seconds:.2f} seconds")
    print(f"Rows: {len(df)}")
    print("Columns: " + ", ".join(df.columns))
    missing = missing_columns(df)
    if missing:
        print("WARNING: missing fields: " + ", ".join(missing))
        print("Some analytics may not work.")
    return df


# ---------------------------------------------------------------- input helpers
def parse_choices(text, options):
    """Turn '1,3' into ['first option', 'third option'].
    Returns None if the text is not valid. Duplicates are ignored."""
    chosen = []
    for part in text.split(","):
        part = part.strip()
        if not part.isdigit() or not 1 <= int(part) <= len(options):
            return None
        item = options[int(part) - 1]
        if item not in chosen:
            chosen.append(item)
    return chosen


def ask_choices(title, options, optional=False, exactly=None):
    """Show a numbered list and keep asking until the choice is valid.
    optional: Enter returns []. exactly: required number of choices."""
    print(f"\n{title}")
    for number, option in enumerate(options, 1):
        print(f"{number}. {option}")
    prompt = "Enter the number(s) of your choice(s), separated by commas"
    prompt += " (enter for none): " if optional else ": "
    while True:
        text = input(prompt).strip()
        if text == "" and optional:
            return []
        chosen = parse_choices(text, options)
        if chosen is None:
            print(f"Invalid. Use numbers 1 to {len(options)} separated by commas.")
        elif exactly is not None and len(chosen) != exactly:
            print(f"Please choose exactly {exactly}.")
        else:
            return chosen


def can_run(df, columns):
    """True if df has all columns; otherwise explain which are missing."""
    missing = [column for column in columns if column not in df.columns]
    if missing:
        print("Cannot run this analytic. Missing: " + ", ".join(missing))
    return not missing


# ---------------------------------------------------------------- analytics
def show_first_rows(df):
    """Menu 1: ask how many rows to show. Returns those rows (or None)."""
    total = len(df)
    print("\nEnter rows to display:")
    print(f"- Enter a number 1 to {total}")
    print("- To see all rows, enter 'all'")
    print("- To skip preview, press Enter")
    while True:
        choice = input("Your choice: ").strip().lower()
        if choice == "":
            return None
        if choice == "all":
            return df
        if choice.isdigit() and 1 <= int(choice) <= total:
            return df.head(int(choice))
        print(f"Invalid. Enter 1 to {total}, 'all', or press Enter.")


def total_sales_by_region_order_type(df):
    """Menu 2: total sales by region, columns = order_type."""
    if not can_run(df, ["sales_region", "order_type", "sales"]):
        return None
    return pd.pivot_table(df, index="sales_region", columns="order_type",
                          values="sales", aggfunc="sum", fill_value=0)


def average_sales_by_region_state(df):
    """Menu 3: average sales by region and state, columns = order_type."""
    if not can_run(df, ["sales_region", "customer_state", "order_type", "sales"]):
        return None
    return pd.pivot_table(df, index=["sales_region", "customer_state"],
                          columns="order_type", values="sales",
                          aggfunc="mean", fill_value=0)


def sales_by_customer_order_type_state(df):
    """Menu 4: sales by state, then customer type, then order type."""
    if not can_run(df, ["customer_state", "customer_type", "order_type", "sales"]):
        return None
    return pd.pivot_table(df, index=["customer_state", "customer_type", "order_type"],
                          values="sales", aggfunc="sum", fill_value=0)


def quantity_price_by_region_product(df):
    """Menu 5: summed quantity and sales by region and product."""
    if not can_run(df, ["sales_region", "produce_name", "quantity", "sales"]):
        return None
    return pd.pivot_table(df, index=["sales_region", "produce_name"],
                          values=["quantity", "sales"], aggfunc="sum", fill_value=0)


def quantity_price_by_customer_type(df):
    """Menu 6: summed quantity and sales by order type and customer type."""
    if not can_run(df, ["order_type", "customer_type", "quantity", "sales"]):
        return None
    return pd.pivot_table(df, index=["order_type", "customer_type"],
                          values=["quantity", "sales"], aggfunc="sum", fill_value=0)


def max_min_price_by_category(df):
    """Menu 7: max and min unit price by product category."""
    if not can_run(df, ["product_category", "unit_price"]):
        return None
    return pd.pivot_table(df, index="product_category",
                          values="unit_price", aggfunc=["max", "min"])


def unique_employees_by_region(df):
    """Menu 8: number of distinct employees in each region."""
    if not can_run(df, ["sales_region", "employee_id"]):
        return None
    return pd.pivot_table(df, index="sales_region", values="employee_id",
                          aggfunc="nunique")


def custom_pivot(df):
    """Menu 9: let the user choose rows, columns, values and aggregations."""
    row_options = [c for c in CUSTOM_ROWS if c in df.columns]
    value_options = [c for c in CUSTOM_VALUES if c in df.columns]
    if not row_options or not value_options:
        print("The data does not have the fields needed for a custom pivot table.")
        return None
    rows = ask_choices("Select rows:", row_options)
    # A field already used as a row cannot also be a column.
    column_options = [c for c in CUSTOM_COLUMNS
                      if c in df.columns and c not in rows]
    columns = []
    if column_options:
        columns = ask_choices("Select columns (optional):", column_options,
                              optional=True)
    values = ask_choices("Select values:", value_options)
    functions = ask_choices("Select aggregation function:", CUSTOM_AGGREGATIONS)
    try:
        return pd.pivot_table(df, index=rows, columns=columns or None,
                              values=values, aggfunc=functions, fill_value=0)
    except Exception as err:
        print(f"Could not build the pivot table: {err}")
        return None


# Analytics that return a pivot table with no further questions.
# Used by the menu and by the compare feature.
ANALYTICS = [
    ("Total sales by region and order_type", total_sales_by_region_order_type),
    ("Average sales by region with average sales by state and sale type",
     average_sales_by_region_state),
    ("Sales by customer type and order type by state",
     sales_by_customer_order_type_state),
    ("Total sales quantity and price by region and product",
     quantity_price_by_region_product),
    ("Total sales quantity and price customer type",
     quantity_price_by_customer_type),
    ("Max and min sales price of sales by category", max_min_price_by_category),
    ("Number of unique employees by region", unique_employees_by_region),
]


# ---------------------------------------------------------------- display
def format_table(table):
    """Text version of a pivot table, money/averages shown with 2 decimals."""
    return table.to_string(float_format="{:,.2f}".format)


def side_by_side(left_title, left_table, right_title, right_table):
    """Return two tables as one text block, placed next to each other."""
    left = [left_title, "-" * len(left_title)] + format_table(left_table).split("\n")
    right = [right_title, "-" * len(right_title)] + format_table(right_table).split("\n")
    width = max(len(line) for line in left) + 4
    lines = []
    for i in range(max(len(left), len(right))):
        left_line = left[i] if i < len(left) else ""
        right_line = right[i] if i < len(right) else ""
        lines.append(left_line.ljust(width) + right_line)
    return "\n".join(lines)


def compare_analytics(df):
    """Menu 10: run two predefined analytics and print them side by side."""
    labels = [label for label, _ in ANALYTICS]
    first, second = ask_choices("Select two analytics to compare:", labels, exactly=2)
    functions = dict(ANALYTICS)
    left, right = functions[first](df), functions[second](df)
    if left is None or right is None:
        print("Cannot compare: one of the analytics could not run.")
        return None
    print("\n" + side_by_side(first, left, second, right))
    return None


def choose_dataset(df):
    """Menu 11: load a different data set. Keeps the current one on failure."""
    try:
        return load_interactively()
    except ValueError as err:
        print(f"Error: {err}\nKeeping the current data.")
        return df


# ---------------------------------------------------------------- menu
# (label, function). Each function takes the data and returns a table or None.
MENU_ITEMS = [
    ("Show the first n rows of sales data", show_first_rows),
    *ANALYTICS,
    ("Create a custom pivot table", custom_pivot),
    ("Compare two analytics side by side", compare_analytics),
    ("Load a different data set", choose_dataset),
]


def run_menu(df):
    """Show the menu until the user exits."""
    exit_number = len(MENU_ITEMS) + 1
    while True:
        print("\n--- Sales Data Dashboard ---")
        for number, (label, _) in enumerate(MENU_ITEMS, 1):
            print(f"{number}. {label}")
        print(f"{exit_number}. Exit")
        choice = input("Your choice: ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= exit_number:
            print(f"Invalid choice. Enter a number 1 to {exit_number}.")
            continue
        if int(choice) == exit_number:
            print("Goodbye.")
            return
        label, function = MENU_ITEMS[int(choice) - 1]
        try:
            result = function(df)
        except Exception as err:  # last line of defence so the menu never crashes
            print(f"Error running '{label}': {err}")
            continue
        if function is choose_dataset:
            df = result  # the only item that replaces the data
        elif isinstance(result, pd.DataFrame):
            print(f"\n=== {label} ===")
            print(format_table(result))


def main():
    """Load the data (exit with an error if impossible) and start the menu."""
    try:
        df = load_interactively()
    except ValueError as err:
        print(f"Error: {err}")
        sys.exit(1)
    run_menu(df)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye.")