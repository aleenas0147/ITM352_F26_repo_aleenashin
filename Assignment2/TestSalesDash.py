"""Tests for sales_dashboard.py. Run with:  python -m unittest -v

Test data is small so every expected answer was worked out by hand:
  region North: Ann(E1) Retail 20, Ann Wholesale 40, Bob(E2) Retail 30
  region South: Cy(E3) Retail 60, Cy Wholesale 60, Di(E4) Retail 10
"""
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import pandas as pd

import SalesDashboard as sd

ROWS = [
    # id, name, region, order, customer, state, category, product, qty, price
    (1, "Ann", "North", "Retail", "Individual", "TX", "Oil", "Oil A", 2, 10),
    (1, "Ann", "North", "Wholesale", "Business", "TX", "Oil", "Oil A", 5, 8),
    (2, "Bob", "North", "Retail", "Business", "NY", "Bath", "Soap", 1, 30),
    (3, "Cy", "South", "Retail", "Individual", "FL", "Gift", "Basket", 3, 20),
    (3, "Cy", "South", "Wholesale", "Business", "FL", "Gift", "Basket", 4, 15),
    (4, "Di", "South", "Retail", "Individual", "GA", "Oil", "Oil A", 1, 10),
]
COLUMNS = ["employee_id", "employee_name", "sales_region", "order_type",
           "customer_type", "customer_state", "product_category",
           "produce_name", "quantity", "unit_price"]


def make_df():
    return sd.clean_data(pd.DataFrame(ROWS, columns=COLUMNS))


def run_with_input(function, answers, *args):
    """Call function with fake user input; return (result, printed text)."""
    out = io.StringIO()
    with patch("builtins.input", side_effect=answers), redirect_stdout(out):
        result = function(*args)
    return result, out.getvalue()


class TestLoading(unittest.TestCase):
    def write_csv(self, text):
        handle = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
        handle.write(text)
        handle.close()
        self.addCleanup(os.remove, handle.name)
        return handle.name

    def test_load_valid_file(self):
        path = self.write_csv("quantity,unit_price\n2,10\n3,5\n")
        df, seconds = sd.load_data(path)
        self.assertEqual(len(df), 2)
        self.assertGreaterEqual(seconds, 0)

    def test_missing_file(self):
        with self.assertRaises(ValueError):
            sd.load_data("no_such_file.csv")

    def test_empty_file(self):
        with self.assertRaises(ValueError):
            sd.load_data(self.write_csv(""))

    def test_header_only_file(self):
        with self.assertRaises(ValueError):
            sd.load_data(self.write_csv("quantity,unit_price\n"))

    def test_bad_source_type(self):
        with self.assertRaises(AssertionError):
            sd.load_data(None)

    def test_load_interactively_alternate_file(self):
        path = self.write_csv("quantity,unit_price\n2,10\n")
        df, text = run_with_input(sd.load_interactively, [path])
        self.assertEqual(len(df), 1)
        self.assertIn("loaded successfully", text)
        self.assertIn("WARNING: missing fields", text)

    def test_load_interactively_default_uses_drive_url(self):
        with patch.object(sd, "load_data", return_value=(make_df(), 0.1)) as mocked:
            run_with_input(sd.load_interactively, [""])
        mocked.assert_called_once_with(sd.DRIVE_URL)


class TestCleaning(unittest.TestCase):
    def test_missing_values_become_zero(self):
        df = pd.DataFrame({"quantity": [1, None], "unit_price": [5, 5],
                           "employee_name": ["A", None]})
        clean = sd.clean_data(df)
        self.assertEqual(clean["quantity"].tolist(), [1, 0])
        self.assertEqual(clean["employee_name"].tolist(), ["A", 0])

    def test_bad_number_text_becomes_zero(self):
        df = pd.DataFrame({"quantity": ["2", "abc"], "unit_price": [5, 5]})
        self.assertEqual(sd.clean_data(df)["sales"].tolist(), [10, 0])

    def test_sales_column(self):
        self.assertEqual(make_df()["sales"].tolist(), [20, 40, 30, 60, 60, 10])

    def test_no_sales_column_without_prices(self):
        clean = sd.clean_data(pd.DataFrame({"quantity": [1]}))
        self.assertNotIn("sales", clean.columns)

    def test_original_not_changed(self):
        df = pd.DataFrame({"quantity": [1], "unit_price": [2]})
        sd.clean_data(df)
        self.assertNotIn("sales", df.columns)

    def test_missing_columns(self):
        self.assertEqual(sd.missing_columns(make_df()), [])
        self.assertIn("quantity", sd.missing_columns(make_df().drop(columns="quantity")))


class TestInputHelpers(unittest.TestCase):
    def test_parse_valid(self):
        self.assertEqual(sd.parse_choices("1, 3", ["a", "b", "c"]), ["a", "c"])

    def test_parse_duplicates_ignored(self):
        self.assertEqual(sd.parse_choices("1,1", ["a", "b"]), ["a"])

    def test_parse_invalid(self):
        for bad in ["", "0", "4", "x", "1,,2", "-1", "1;2"]:
            self.assertIsNone(sd.parse_choices(bad, ["a", "b", "c"]), bad)

    def test_ask_choices_retries(self):
        result, text = run_with_input(sd.ask_choices, ["9", "abc", "2"],
                                      "Pick:", ["a", "b"])
        self.assertEqual(result, ["b"])
        self.assertIn("Invalid", text)

    def test_ask_choices_optional(self):
        result, _ = run_with_input(sd.ask_choices, [""], "Pick:", ["a"], True)
        self.assertEqual(result, [])

    def test_ask_choices_required_rejects_empty(self):
        result, _ = run_with_input(sd.ask_choices, ["", "1"], "Pick:", ["a"])
        self.assertEqual(result, ["a"])

    def test_ask_choices_exactly(self):
        result, text = run_with_input(sd.ask_choices, ["1", "1,2"],
                                      "Pick:", ["a", "b"], False, 2)
        self.assertEqual(result, ["a", "b"])
        self.assertIn("exactly 2", text)

    def test_can_run(self):
        df = make_df()
        self.assertTrue(sd.can_run(df, ["sales"]))
        result, text = run_with_input(sd.can_run, [], df, ["nope"])
        self.assertFalse(result)
        self.assertIn("nope", text)


class TestShowFirstRows(unittest.TestCase):
    def test_skip(self):
        result, _ = run_with_input(sd.show_first_rows, [""], make_df())
        self.assertIsNone(result)

    def test_all(self):
        result, _ = run_with_input(sd.show_first_rows, ["ALL"], make_df())
        self.assertEqual(len(result), 6)

    def test_number(self):
        result, _ = run_with_input(sd.show_first_rows, ["2"], make_df())
        self.assertEqual(len(result), 2)

    def test_invalid_then_valid(self):
        result, text = run_with_input(sd.show_first_rows,
                                      ["0", "7", "-1", "abc", "3"], make_df())
        self.assertEqual(len(result), 3)
        self.assertEqual(text.count("Invalid"), 4)

    def test_tells_row_count(self):
        _, text = run_with_input(sd.show_first_rows, [""], make_df())
        self.assertIn("1 to 6", text)


class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.df = make_df()

    def test_total_sales_region_order_type(self):
        t = sd.total_sales_by_region_order_type(self.df)
        self.assertEqual(t.loc["North", "Retail"], 50)
        self.assertEqual(t.loc["North", "Wholesale"], 40)
        self.assertEqual(t.loc["South", "Retail"], 70)
        self.assertEqual(t.loc["South", "Wholesale"], 60)

    def test_total_matches_overall_sum(self):
        t = sd.total_sales_by_region_order_type(self.df)
        self.assertEqual(t.to_numpy().sum(), self.df["sales"].sum())

    def test_average_sales_region_state(self):
        t = sd.average_sales_by_region_state(self.df)
        self.assertEqual(t.loc[("North", "TX"), "Retail"], 20)
        self.assertEqual(t.loc[("North", "TX"), "Wholesale"], 40)
        self.assertEqual(t.loc[("North", "NY"), "Wholesale"], 0)  # no sales -> 0
        self.assertEqual(t.loc[("South", "FL"), "Retail"], 60)

    def test_sales_customer_order_state(self):
        t = sd.sales_by_customer_order_type_state(self.df)
        self.assertEqual(t.loc[("TX", "Individual", "Retail"), "sales"], 20)
        self.assertEqual(t.loc[("TX", "Business", "Wholesale"), "sales"], 40)
        self.assertEqual(t.loc[("GA", "Individual", "Retail"), "sales"], 10)

    def test_quantity_price_region_product(self):
        t = sd.quantity_price_by_region_product(self.df)
        self.assertEqual(t.loc[("North", "Oil A"), "quantity"], 7)
        self.assertEqual(t.loc[("North", "Oil A"), "sales"], 60)
        self.assertEqual(t.loc[("South", "Basket"), "quantity"], 7)
        self.assertEqual(t.loc[("South", "Basket"), "sales"], 120)

    def test_quantity_price_customer_type(self):
        t = sd.quantity_price_by_customer_type(self.df)
        self.assertEqual(t.loc[("Retail", "Individual"), "quantity"], 6)
        self.assertEqual(t.loc[("Retail", "Individual"), "sales"], 90)
        self.assertEqual(t.loc[("Wholesale", "Business"), "sales"], 100)

    def test_max_min_price(self):
        t = sd.max_min_price_by_category(self.df)
        self.assertEqual(t.loc["Oil", ("max", "unit_price")], 10)
        self.assertEqual(t.loc["Oil", ("min", "unit_price")], 8)
        self.assertEqual(t.loc["Bath", ("max", "unit_price")], 30)
        self.assertEqual(t.loc["Gift", ("min", "unit_price")], 15)

    def test_unique_employees(self):
        t = sd.unique_employees_by_region(self.df)
        self.assertEqual(t.loc["North", "employee_id"], 2)  # Ann counted once
        self.assertEqual(t.loc["South", "employee_id"], 2)

    def test_missing_column_returns_none(self):
        no_region = self.df.drop(columns="sales_region")
        for function in [sd.total_sales_by_region_order_type,
                         sd.average_sales_by_region_state,
                         sd.quantity_price_by_region_product,
                         sd.unique_employees_by_region]:
            result, text = run_with_input(function, [], no_region)
            self.assertIsNone(result)
            self.assertIn("Missing: sales_region", text)

    def test_missing_price_returns_none(self):
        no_price = self.df.drop(columns=["unit_price", "sales"])
        result, _ = run_with_input(sd.max_min_price_by_category, [], no_price)
        self.assertIsNone(result)


class TestCustomPivot(unittest.TestCase):
    def setUp(self):
        self.df = make_df()

    def test_rows_columns_values_sum(self):
        # rows=sales_region(2), no columns, values=sales(3), sum(1)
        t, _ = run_with_input(sd.custom_pivot, ["2", "", "3", "1"], self.df)
        # rows are listed in CUSTOM_ROWS order: employee_name, sales_region, ...
        self.assertEqual(t.loc["North", ("sum", "sales")], 90)
        self.assertEqual(t.loc["South", ("sum", "sales")], 130)

    def test_with_columns_and_mean(self):
        # rows=sales_region(2), columns=order_type(1), values=quantity(1), mean(2)
        t, _ = run_with_input(sd.custom_pivot, ["2", "1", "1", "2"], self.df)
        self.assertEqual(t.loc["North", ("mean", "quantity", "Retail")], 1.5)

    def test_invalid_input_retries(self):
        t, text = run_with_input(sd.custom_pivot,
                                 ["x", "2", "", "99", "3", "1"], self.df)
        self.assertIsNotNone(t)
        self.assertIn("Invalid", text)

    def test_row_not_offered_as_column(self):
        _, text = run_with_input(sd.custom_pivot, ["2", "", "3", "1"], self.df)
        self.assertIn("1. order_type", text)

    def test_missing_fields(self):
        df = self.df[["employee_id"]]
        result, text = run_with_input(sd.custom_pivot, [], df)
        self.assertIsNone(result)
        self.assertIn("does not have", text)


class TestDisplayAndCompare(unittest.TestCase):
    def test_format_table_two_decimals(self):
        self.assertIn("1,234.50", sd.format_table(pd.DataFrame({"a": [1234.5]})))

    def test_side_by_side(self):
        left = pd.DataFrame({"a": [1]}, index=["x"])
        right = pd.DataFrame({"b": [2, 3]}, index=["y", "z"])
        lines = sd.side_by_side("LEFT", left, "RIGHT", right).split("\n")
        self.assertIn("LEFT", lines[0])
        self.assertIn("RIGHT", lines[0])
        self.assertEqual(len(lines), 5)  # uneven heights are padded

    def test_compare_prints_both(self):
        # choose analytics 1 and 7
        _, text = run_with_input(sd.compare_analytics, ["1,7"], make_df())
        self.assertIn("Total sales by region and order_type", text)
        self.assertIn("Number of unique employees by region", text)
        self.assertIn("Wholesale", text)
        self.assertIn("North", text)

    def test_compare_rejects_one_choice(self):
        _, text = run_with_input(sd.compare_analytics, ["1", "1,2"], make_df())
        self.assertIn("exactly 2", text)

    def test_compare_with_missing_data(self):
        df = make_df().drop(columns="sales_region")
        _, text = run_with_input(sd.compare_analytics, ["1,7"], df)
        self.assertIn("Cannot compare", text)


class TestMenu(unittest.TestCase):
    def test_menu_items_are_valid(self):
        labels = [label for label, _ in sd.MENU_ITEMS]
        self.assertEqual(len(labels), len(set(labels)))
        for label, function in sd.MENU_ITEMS:
            self.assertTrue(callable(function), label)

    def test_exit(self):
        exit_number = str(len(sd.MENU_ITEMS) + 1)
        _, text = run_with_input(sd.run_menu, [exit_number], make_df())
        self.assertIn("Sales Data Dashboard", text)
        self.assertIn("Goodbye", text)

    def test_invalid_choice_then_exit(self):
        exit_number = str(len(sd.MENU_ITEMS) + 1)
        _, text = run_with_input(sd.run_menu, ["abc", "0", "99", exit_number],
                                 make_df())
        self.assertEqual(text.count("Invalid choice"), 3)

    def test_runs_analytic_and_prints_table(self):
        exit_number = str(len(sd.MENU_ITEMS) + 1)
        _, text = run_with_input(sd.run_menu, ["2", exit_number], make_df())
        self.assertIn("=== Total sales by region and order_type ===", text)
        self.assertRegex(text, r"South\s+70\s+60")

    def test_function_error_does_not_crash(self):
        def broken(df):
            raise RuntimeError("boom")
        with patch.object(sd, "MENU_ITEMS", [("Broken", broken)]):
            _, text = run_with_input(sd.run_menu, ["1", "2"], make_df())
        self.assertIn("boom", text)

    def test_load_different_dataset(self):
        handle = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
        handle.write("\n".join(",".join(map(str, r)) for r in [COLUMNS] + ROWS[:2]))
        handle.close()
        self.addCleanup(os.remove, handle.name)
        load_number = str([l for l, _ in sd.MENU_ITEMS].index(
            "Load a different data set") + 1)
        exit_number = str(len(sd.MENU_ITEMS) + 1)
        # load the 2-row file, then show all rows
        _, text = run_with_input(sd.run_menu,
                                 [load_number, handle.name, "1", "all", exit_number],
                                 make_df())
        self.assertIn("Rows: 2", text)

    def test_failed_reload_keeps_data(self):
        result, text = run_with_input(sd.choose_dataset, ["missing.csv"], "old")
        self.assertEqual(result, "old")
        self.assertIn("Keeping the current data", text)


class TestMain(unittest.TestCase):
    def test_bad_file_exits_with_error(self):
        with patch("builtins.input", side_effect=["missing.csv"]), \
                redirect_stdout(io.StringIO()) as out:
            with self.assertRaises(SystemExit) as caught:
                sd.main()
        self.assertEqual(caught.exception.code, 1)
        self.assertIn("Error", out.getvalue())


if __name__ == "__main__":
    unittest.main()