import pandas as pd
import pandas_ta as ta
import numpy as np

def get_indicator(data, indicator_name, params):
    """
    Calculates a technical indicator on the given data.

    Args:
        data (pd.DataFrame): The OHLCV data.
        indicator_name (str): The name of the indicator (e.g., 'SMA', 'RSI').
        params (dict): A dictionary of parameters for the indicator (e.g., {'length': 20}).

    Returns:
        pd.Series: The calculated indicator series.
    """
    if indicator_name.lower() == 'sma':
        return ta.sma(data['Close'], **params)
    elif indicator_name.lower() == 'rsi':
        return ta.rsi(data['Close'], **params)
    elif indicator_name.lower() == 'bbands':
        bbands = ta.bbands(data['Close'], **params)
        # For simplicity, let's allow users to select a specific band.
        # Defaulting to the middle band if not specified.
        band_select = params.get('band', 'BBM_20_2.0')
        return bbands[band_select] # e.g., 'BBU_20_2.0', 'BBM_20_2.0', 'BBL_20_2.0'
    elif indicator_name.lower() == 'close':
        return data['Close']
    # Add other indicators here as needed
    else:
        return None

def generate_signals(data, strategy_definition):
    """
    Generates trading signals based on a user-defined strategy.

    Args:
        data (pd.DataFrame): The OHLCV data.
        strategy_definition (dict): The definition of the strategy from the UI.

    Returns:
        pd.DataFrame: The data with a 'positions' column for trades.
    """
    signals = data.copy()
    signals['positions'] = 0

    # Get operand series
    op1_series = get_indicator(data, strategy_definition['entry']['operand1']['name'], strategy_definition['entry']['operand1']['params'])
    op2_series = get_indicator(data, strategy_definition['entry']['operand2']['name'], strategy_definition['entry']['operand2']['params'])

    # --- Entry Condition ---
    entry_operator = strategy_definition['entry']['operator']
    entry_condition = pd.Series(False, index=data.index)
    if entry_operator == 'crosses_above':
        entry_condition = (op1_series.shift(1) < op2_series.shift(1)) & (op1_series > op2_series)
    elif entry_operator == 'greater_than':
        entry_condition = op1_series > op2_series
    elif entry_operator == 'less_than':
        entry_condition = op1_series < op2_series

    # --- Exit Condition ---
    # For this simplified version, the exit is simply the reverse of the entry condition.
    # A more advanced implementation would have a separate definition for exit.
    exit_condition = pd.Series(False, index=data.index)
    if entry_operator == 'crosses_above': # The reverse is crossing below
        exit_condition = (op1_series.shift(1) > op2_series.shift(1)) & (op1_series < op2_series)
    else: # For greater/less than, the exit is when the condition is no longer true
        exit_condition = ~entry_condition

    # Apply signals
    signals.loc[entry_condition, 'positions'] = 1  # Buy
    signals.loc[exit_condition, 'positions'] = -1 # Sell

    # Forward fill positions to hold through the trade
    signals['positions'] = signals['positions'].replace(0, np.nan).ffill().fillna(0)
    # Get the actual trade execution points (the day after the signal)
    signals['positions'] = signals['positions'].diff()

    return signals
