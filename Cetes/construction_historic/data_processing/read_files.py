import logging
import os
import pandas as pd
import polars as pl
import re


DATE_PATTERN = re.compile(r"(\d{8})")


def file_location(path: str, pattern: str) -> list[str]:
    return [os.path.join(path, file) for file in os.listdir(path) if pattern in file]


def data_filtering(data: pd.DataFrame) -> pd.DataFrame:
    df = data[(data["EMISORA"] == "CETES") & (data["DIAS X VENCER"].notna())]
    return df[["DIAS X VENCER", "RENDIMIENTO"]].copy()


READ_STRATEGY = {
    ".xlsx": lambda filepath, **params: pd.read_excel(filepath, **params).to_pandas(),
    ".xls": lambda filepath, **params: pd.read_excel(filepath, **params).to_pandas(),
    ".csv": lambda filepath, **params: pd.read_csv(
        filepath, encoding="latin-1", **params
    ),
}


def _read_file(filepath: str, params: dict = {}) -> pd.DataFrame | None:
    ext = os.path.splitext(filepath)[1]
    reader = READ_STRATEGY.get(ext)
    if not reader:
        raise ValueError(f"Extensión no soportada: {ext} para archivo {filepath}")
    return reader(filepath, **params)


def read_file(filepath: str, params: dict = {}) -> pd.DataFrame | None:
    try:
        return _read_file(filepath, params)
    except Exception as e:
        logging.error(f"Error: {e} para archivo {filepath}")
        return


def read_massive(files: list[str], params: dict = {}) -> dict[str, pd.DataFrame]:
    result = {}
    for filepath in files:
        match = DATE_PATTERN.search(filepath)
        if match:
            date_str = match.group(1)
            df = read_file(filepath, params)
            if df is not None:
                result[date_str] = data_filtering(
                    df
                )  # NOTE aqui se filtra el dataframe
            # print(df)
        else:
            print(f"Archivo ignorado (no se encontró fecha): {filepath}")

    return result
