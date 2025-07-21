import pandas as pd


def load_and_prepare_data(path, date_col='date', index_col=0, reset_index=True):
    """
    Load CSV to DataFrame, parse date, sort by date, and reset index.

    Parameters
    ----------
    path : str
        Path to CSV file.
    date_col : str, default='date'
        Name of the date column.
    index_col : int or str, default=0
        Index column in the CSV.

    Returns
    -------
    pd.DataFrame
        Prepared DataFrame.
    """
    df = pd.read_csv(path, index_col=index_col, parse_dates=[date_col])
    df = df.sort_values(date_col)
    if reset_index:
        df = df.reset_index(drop=True)
    return df
    
    
def create_full_dataset(df):
    """
    Expand the DataFrame to include every SKU × date combination,
    filling missing sales and propagating price and category forward/backward.

    Parameters
    ----------
    df : pd.DataFrame
        Original data with columns ['sku_id', 'date', 'sales_quantity',
        'sales_price', 'category_id'].

    Returns
    -------
    pd.DataFrame
        Expanded DataFrame with:
        - 'added' flag for rows that were inserted (no original sales),
        - filled 'sales_quantity',
        - forward/backward-filled 'sales_price' and 'category_id'.
    """
    df = df.copy()
    
    # Find all SKUs and dates
    all_skus = df['sku_id'].unique()
    all_dates = pd.date_range(df['date'].min(), df['date'].max(), freq='D')

    full_idx = pd.MultiIndex.from_product(
        [all_skus, all_dates],
        names=['sku_id', 'date']
    )

    # Reindex to full grid
    df = (
        df
        .set_index(['sku_id','date'])
        .reindex(full_idx)
        .reset_index()
    )

    # Mark rows that were added
    df['added'] = df['sales_quantity'].isna()

    # Fill in the real data
    df['sales_quantity'] = df['sales_quantity'].fillna(0)
    df['sales_price'] = (
        df
        .groupby('sku_id')['sales_price']
        .transform(lambda s: s.ffill().bfill()) # Last price
    )
    df['category_id'] = (
        df
        .groupby('sku_id')['category_id']
        .transform(lambda s: s.ffill().bfill())
    )

    # Final sorting
    df = df.sort_values('date').reset_index(drop=True)
    
    return df