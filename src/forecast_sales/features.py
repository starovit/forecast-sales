import pandas as pd
import holidays
from datetime import timedelta

def mark_holiday_adjacent(df, country_code='UA', date_col='date', output_col='is_holiday_or_adjacent'):
    """
    Adds a boolean column to df indicating if a date is a holiday or adjacent (+/-1 day).
    
    Args:
        df : pd.DataFrame
            DataFrame with at least one date column.
        country_code : str
            Country code for official holidays (default 'UA').
        date_col : str
            Name of the date column in df (default 'date').
        output_col : str
            Name of the output boolean column (default 'is_holiday_or_adjacent').
    Returns:
        pd.DataFrame with added boolean column.
    """
    df = df.copy()
    
    # Make sure the date column is datetime
    df[date_col] = pd.to_datetime(df[date_col])

    years = range(df[date_col].dt.year.min(), df[date_col].dt.year.max() + 1)
    all_holidays = set(holidays.country_holidays(country_code, years=years).keys())
    holiday_plus_minus_1 = set()
    for day in all_holidays:
        holiday_plus_minus_1.add(day - timedelta(days=1))
        holiday_plus_minus_1.add(day)
        holiday_plus_minus_1.add(day + timedelta(days=1))
    # Assign boolean column
    df[output_col] = df[date_col].dt.date.isin(holiday_plus_minus_1)
    return df


def add_date_categorical_features(df, date_col='date', prefix=''):
    """
    Adds common categorical date features to a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    date_col : str, default='date'
        Name of the datetime column.
    prefix : str, optional
        Prefix to add to feature names.

    Returns
    -------
    pd.DataFrame
        DataFrame with new categorical features.
    """
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])

    df[f'{prefix}dayofweek'] = df[date_col].dt.dayofweek.astype('category') # 0=Monday, 6=Sunday
    df[f'{prefix}month'] = df[date_col].dt.month.astype('category') # 1..12
    df[f'{prefix}quarter'] = df[date_col].dt.quarter.astype('category') # 1..4

    return df
