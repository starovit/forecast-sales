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
    list of str
        Names of added rolling mean features.
    """
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        df[date_col] = pd.to_datetime(df[date_col])

    dayofweek_name = f'{prefix}dayofweek'
    month_name = f'{prefix}month'
    quarter_name = f'{prefix}quarter'

    df[dayofweek_name] = df[date_col].dt.dayofweek.astype('category')  # 0=Monday, 6=Sunday
    df[month_name] = df[date_col].dt.month.astype('category')          # 1..12
    df[quarter_name] = df[date_col].dt.quarter.astype('category')      # 1..4

    feature_names = [dayofweek_name, month_name, quarter_name]

    return df, feature_names


def add_rolling_mean_features(
    df,
    days=[15, 30, 60, 120, 365, 1000],
    columns=None,
    groupby='sku_id',
    date_col='date'
):
    """
    Adds rolling mean features for specified columns and windows.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    days : list of int, optional
        List of rolling window sizes (in days).
    columns : list of str, optional
        List of column names to compute rolling means for.
    groupby : str, default='sku_id'
        Column to group by before computing rolling means.
    date_col : str, default='date'
        Date column name.

    Returns
    -------
    pd.DataFrame
        DataFrame with added rolling mean features.
    list of str
        Names of added rolling mean features.
    """
    df = df.copy()
    df = df.sort_values([groupby, date_col])
    feature_names = []

    if columns is None:
        raise ValueError("You must specify a list of columns for rolling means.")

    for col in columns:
        for window in days:
            feature_name = f'{col}_roll{window}_mean'
            df[feature_name] = (
                df.groupby(groupby)[col]
                .transform(lambda s: s.shift(1).rolling(window, min_periods=1).mean())
            )
            feature_names.append(feature_name)

    df = df.sort_values(date_col)
    return df, feature_names


def features_pipeline(
    df,
    days=[15, 30, 60, 120, 365, 1000],
    num_columns=['sales_quantity', 'sales_price']
    ):
    """
    Adds main features for modeling:
      - Holiday/adjacent indicator
      - Date categorical features (dayofweek, month, quarter)
      - Rolling mean sales and quantities features

    Parameters
    ----------
    df : pd.DataFrame
    days : list of int
        Rolling windows (in days)
    num_columns: list of str
        Columns for rolling mean 

    Returns
    -------
    df : pd.DataFrame
    cat_features : list of str
        List of categorical features
    all_features : list of str
        List of all features
    """
    df = mark_holiday_adjacent(df)
    df, date_feature_names = add_date_categorical_features(df)
    df, rolling_feature_names = add_rolling_mean_features(df, days=days, columns=num_columns)
    
    cat_features = ["is_holiday_or_adjacent"] + date_feature_names 
    all_features = cat_features + rolling_feature_names
    
    return df, cat_features, all_features