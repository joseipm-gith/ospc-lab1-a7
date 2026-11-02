"""Number of orders per region, quarter and order size (segments.csv)."""

import os

import numpy as np
import pandas as pd

DATA = os.environ.get("DATA", os.path.expanduser("~/data/sales_2025.csv"))
OUT = os.environ.get("OUT", os.path.expanduser("~/data/out"))
os.makedirs(OUT, exist_ok=True)

orders = pd.read_csv(DATA, usecols=["order_date", "region", "quantity", "unit_price"])

# Work on whole columns instead of calling segment() once per order (8.4 million
# strptime calls in the interpreter). Keep quarter and size as small integers and
# build the text labels only for the final table, so memory stays low.
quarter = pd.to_datetime(orders.pop("order_date"), format="%Y-%m-%d").dt.quarter.rename("quarter")
value = orders.pop("quantity") * orders.pop("unit_price")
size = pd.Series(
    np.select([value >= 500, value >= 100], [2, 1], default=0).astype("int8"),
    index=orders.index, name="size",
)
del value

counts = orders.groupby([orders["region"], quarter, size]).size()

names = ["small", "medium", "large"]
segment = [f"Q{q} {names[s]}" for q, s in zip(counts.index.get_level_values("quarter"),
                                               counts.index.get_level_values("size"))]
counts.index = pd.MultiIndex.from_arrays(
    [counts.index.get_level_values("region"), segment], names=["region", "segment"])

table = counts.unstack(fill_value=0)
table.to_csv(os.path.join(OUT, "segments.csv"))
print("segments: done")
