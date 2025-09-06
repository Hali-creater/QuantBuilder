import pandas as pd
import numpy as np

def run_backtest(signals, initial_capital=100000.0):
    """
    Runs a backtest on the trading signals with enhanced metrics.

    Args:
        signals (pd.DataFrame): DataFrame with trading signals and prices.
        initial_capital (float): The starting capital for the backtest.

    Returns:
        pd.DataFrame, dict: A tuple containing the portfolio DataFrame and a dictionary of performance metrics.
    """
    portfolio = pd.DataFrame(index=signals.index)
    portfolio['positions'] = signals['positions'].fillna(0)
    portfolio['asset_price'] = signals['Close']

    # Vectorized calculation of holdings
    portfolio['holdings'] = (portfolio['positions'].cumsum() * portfolio['asset_price'])

    # Vectorized calculation of cash
    portfolio['cash'] = initial_capital - (portfolio['positions'] * portfolio['asset_price']).cumsum()

    portfolio['total'] = portfolio['cash'] + portfolio['holdings']
    portfolio['returns'] = portfolio['total'].pct_change().fillna(0)

    # --- Enhanced Performance Metrics ---

    # 1. Total Return
    total_return = (portfolio['total'].iloc[-1] / initial_capital) - 1

    # 2. Annualized Return
    days = (portfolio.index[-1] - portfolio.index[0]).days
    annualized_return = ((1 + total_return) ** (365.0 / days)) - 1 if days > 0 else 0

    # 3. Sharpe Ratio
    annualized_volatility = portfolio['returns'].std() * np.sqrt(252)
    sharpe_ratio = (annualized_return / annualized_volatility) if annualized_volatility != 0 else 0

    # 4. Max Drawdown
    cumulative_returns = (1 + portfolio['returns']).cumprod()
    peak = cumulative_returns.cummax()
    drawdown = (cumulative_returns - peak) / peak
    max_drawdown = drawdown.min()

    # 5. Trade-level analysis
    trades = portfolio['positions'][portfolio['positions'] != 0]
    trade_pnl = []
    position = 0
    entry_price = 0
    for i in range(len(trades)):
        if trades.iloc[i] > 0: # Entry
            position = trades.iloc[i]
            entry_price = portfolio['asset_price'].loc[trades.index[i]]
        elif trades.iloc[i] < 0 and position > 0: # Exit
            exit_price = portfolio['asset_price'].loc[trades.index[i]]
            trade_pnl.append((exit_price - entry_price) * position)
            position = 0 # Reset position

    total_trades = len(trade_pnl)
    wins = [pnl for pnl in trade_pnl if pnl > 0]
    losses = [pnl for pnl in trade_pnl if pnl < 0]

    win_rate = (len(wins) / total_trades) * 100 if total_trades > 0 else 0
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))
    profit_factor = (gross_profit / gross_loss) if gross_loss > 0 else np.inf

    # 6. Sortino Ratio
    negative_returns = portfolio['returns'][portfolio['returns'] < 0]
    downside_deviation = negative_returns.std() * np.sqrt(252)
    sortino_ratio = (annualized_return / downside_deviation) if downside_deviation != 0 else np.inf

    metrics = {
        'Total Return': f"{total_return:.2%}",
        'Annualized Return': f"{annualized_return:.2%}",
        'Sharpe Ratio': f"{sharpe_ratio:.2f}",
        'Sortino Ratio': f"{sortino_ratio:.2f}",
        'Max Drawdown': f"{max_drawdown:.2%}",
        'Profit Factor': f"{profit_factor:.2f}",
        'Total Trades': total_trades,
        'Win Rate': f"{win_rate:.2f}%"
    }

    return portfolio, metrics
