from __future__ import annotations
import yaml
import pandas as pd

def _check_dtype(series: pd.Series, expected: str) -> bool:
    if expected == "string":
        return True
    if expected == "integer":
        try:
            pd.to_numeric(series.dropna(), errors="raise").astype("int64")
            return True
        except Exception:
            return False
    if expected == "float":
        try:
            pd.to_numeric(series.dropna(), errors="raise").astype("float64")
            return True
        except Exception:
            return False
    if expected == "datetime":
        try:
            pd.to_datetime(series.dropna(), errors="raise")
            return True
        except Exception:
            return False
    return True

def validate_dataframe(df: pd.DataFrame, contract_path: str) -> None:
    with open(contract_path, "r") as f:
        contract = yaml.safe_load(f)

    required = contract["required_columns"]
    missing_cols = [c for c in required if c not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")

    for col, expected_type in required.items():
        if not _check_dtype(df[col], expected_type):
            raise TypeError(f"Column {col} failed type check for expected type {expected_type}")

    rules = contract.get("rules", {})
    for col in rules.get("not_null_columns", []):
        if df[col].isna().any():
            raise ValueError(f"Column {col} contains null values")

    for col in rules.get("non_negative_columns", []):
        numeric = pd.to_numeric(df[col], errors="coerce")
        if (numeric < 0).any():
            raise ValueError(f"Column {col} contains negative values")

    print("Contract validation passed.")