from __future__ import annotations
from pathlib import Path
from typing import Iterable, Iterator, Optional
import pandas as pd
from .config import CHUNK_SIZE, CSV_PATH, YEAR_MAX, YEAR_MIN

def iter_chunks(path: Path | str = CSV_PATH, *, usecols: Optional[Iterable[str]] = None, chunksize: int = CHUNK_SIZE):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Khong tim thay: {path}")
    yield from pd.read_csv(path, usecols=usecols, chunksize=chunksize)

def filter_years(df, year_min=YEAR_MIN, year_max=YEAR_MAX):
    return df[(df["Nam"] >= year_min) & (df["Nam"] <= year_max)]

def count_rows(path=CSV_PATH, year_min=YEAR_MIN, year_max=YEAR_MAX):
    counts = {}
    for chunk in iter_chunks(path, usecols=["Nam"]):
        chunk = filter_years(chunk, year_min, year_max)
        for year, n in chunk["Nam"].value_counts().items():
            counts[int(year)] = counts.get(int(year), 0) + int(n)
    return dict(sorted(counts.items()))

def load_provinces(path=None):
    from .config import PROVINCES_CSV
    return pd.read_csv(path or PROVINCES_CSV, dtype={"MaTinh": int})
