import pandas as pd
import numpy as np

def run_backtest(signals, initial_capital=100000.0):
    """
    Runs a backtest on the trading signals.

    Args:
        signals (pd.DataFrame): DataFrame with trading signals and prices.
        initial_capital (float): The starting capital for the backtest.

    Returns:
        pd.DataFrame, dict: A tuple containing the portfolio DataFrame and a dictionary of performance metrics.
    """
    portfolio = pd.DataFrame(index=signals.index).fillna(0.0)
    portfolio['holdings'] = 0.0
    portfolio['cash'] = initial_capital
    portfolio['total'] = initial_capital
    portfolio['returns'] = 0.0

    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    positions['asset'] = 0

    for i in range(len(signals.index)):
        if signals['positions'].iloc[i] == 1.0: # Buy signal
            positions['asset'] = initial_capital / signals['Close'].iloc[i]
            portfolio['cash'] -= positions['asset'] * signals['Close'].iloc[i]
        elif signals['positions'].iloc[i] == -1.0: # Sell signal
            portfolio['cash'] += positions['asset'] * signals['Close'].iloc[i]
            positions['asset'] = 0

        portfolio['holdings'].iloc[i] = positions['asset'] * signals['Close'].iloc[i]
        portfolio['total'].iloc[i] = portfolio['cash'] + portfolio['holdings'].iloc[i]
        if i > 0:
            portfolio['returns'].iloc[i] = (portfolio['total'].iloc[i] / portfolio['total'].iloc[i-1]) - 1

    # Performance Metrics
    total_return = (portfolio['total'].iloc[-1] / initial_capital) - 1
    returns = portfolio['returns']
    sharpe_ratio = np.sqrt(252) * (returns.mean() / returns.std()) if returns.std() != 0 else 0

    # Max Drawdown
    cumulative_returns = (1 + returns).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()

    # Win Rate
    trades = signals['positions'][signals['positions'] != 0]
    wins = 0
    for i in range(len(trades)):
        if trades.iloc[i] == 1.0: # Buy
            entry_price = signals['Close'][signals.index.get_loc(trades.index[i])]
            if i + 1 < len(trades) and trades.iloc[i+1] == -1.0: # Sell
                exit_price = signals['Close'][signals.index.get_loc(trades.index[i+1])]
                if exit_price > entry_price:
                    wins += 1

    num_trades = len(trades) / 2
    win_rate = (wins / num_trades) * 100 if num_trades > 0 else 0

    metrics = {
        'Total Return': f"{total_return:.2%}",
        'Sharpe Ratio': f"{sharpe_ratio:.2f}",
        'Max Drawdown': f"{max_drawdown:.2%}",
        'Win Rate': f"{win_rate:.2f}%"
    }

    return portfolio, metrics
