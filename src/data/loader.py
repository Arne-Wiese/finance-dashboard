
import datetime as dt
from functools import partial, reduce
from typing import Callable

import babel.dates
import i18n
import pandas as pd

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


class DataSchema:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"


def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure DATE column is in datetime format
    df[DataSchema.DATE] = pd.to_datetime(df[DataSchema.DATE], errors='coerce')

    # Check for NaT values (missing dates)
    if df[DataSchema.DATE].isna().any():
        print("Warning: Some dates could not be converted and will be NaT.")

    df[DataSchema.YEAR] = df[DataSchema.DATE].dt.year.astype("Int64").astype(str)  # Int64 allows NaT handling
    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.MONTH] = df[DataSchema.DATE].dt.month.astype("Int64").astype(str)
    return df


def convert_date_locale(df: pd.DataFrame, locale: str) -> pd.DataFrame:
    def date_repr(date):
        if pd.isna(date):  # Handle NaT values
            return "Unknown"
        return babel.dates.format_date(date, format="MMMM", locale=locale)

    df[DataSchema.MONTH] = df[DataSchema.DATE].apply(date_repr)
    return df


def translate_category_labels(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.CATEGORY] = df[DataSchema.CATEGORY].apply(i18n.t)
    return df


def create_preprocessor(locale: str) -> Preprocessor:
    return partial(preprocess_data, locale=locale)


def preprocess_data(df: pd.DataFrame, locale: str) -> pd.DataFrame:
    functions = [
        create_year_column,
        create_month_column,
        partial(convert_date_locale, locale=locale),
        translate_category_labels,
    ]

    return reduce(lambda f, g: lambda x: g(f(x)), functions)(df)


def load_transaction_data(file_path: str, locale: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)

    # Ensure required columns exist
    required_columns = [DataSchema.DATE, DataSchema.AMOUNT, DataSchema.CATEGORY]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    preprocessor = create_preprocessor(locale)
    return preprocessor(df)
