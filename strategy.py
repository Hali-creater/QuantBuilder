import pandas as pd
import numpy as np

def moving_average_crossover_strategy(data, short_window, long_window):
    """
    Generates trading signals based on a moving average crossover strategy.

    Args:
        data (pd.DataFrame): DataFrame with historical stock data (must contain 'Close' prices).
        short_window (int): The window size for the short moving average.
        long_window (int): The window size for the long moving average.

    Returns:
        pd.DataFrame: The original DataFrame with additional columns for moving averages and signals.
    """
    signals = data.copy()
    signals['short_mavg'] = data['Close'].rolling(window=short_window, min_periods=1, center=False).mean()
    signals['long_mavg'] = data['Close'].rolling(window=long_window, min_periods=1, center=False).mean()

    # Create signals
    signals['signal'] = 0.0
    signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)

    # Generate trading orders
    signals['positions'] = signals['signal'].diff()

    return signals
