import pandas as pd
from alpaca_trade_api.rest import TimeFrame

def fetch_data(broker_api, ticker, start_date, end_date):
    """
    Fetches historical stock data from the Alpaca API.

    Args:
        broker_api: An authenticated Alpaca trade api object.
        ticker (str): The stock ticker symbol.
        start_date (str): The start date for the data in 'YYYY-MM-DD' format.
        end_date (str): The end date for the data in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: A DataFrame containing the OHLCV data, or None if the download fails.
    """
    try:
        # Alpaca's get_bars returns a list of bar objects. We can convert it to a DataFrame.
        bars = broker_api.get_bars(ticker, TimeFrame.Day, start=start_date, end=end_date).df

        if bars.empty:
            print(f"No data found for ticker {ticker} from {start_date} to {end_date}.")
            return None

        # Ensure the column names match what the rest of the app expects.
        # yfinance uses 'Adj Close', Alpaca uses 'close'. 'Close' is used in our app.
        # Alpaca's dataframe from .df has the correct column names already ('open', 'high', 'low', 'close', 'volume')
        # but we should ensure they are capitalized for consistency with the old yfinance format.
        bars.rename(columns={
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        }, inplace=True)

        return bars

    except Exception as e:
        print(f"An error occurred while fetching data for {ticker} from Alpaca: {e}")
        return None
