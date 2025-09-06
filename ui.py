import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def setup_ui():
    """
    Sets up the user interface of the Streamlit app.

    Returns:
        tuple: A tuple containing the user inputs.
    """
    st.title('No-Code Algorithmic Trading Platform')

    st.sidebar.header('Strategy Parameters')
    ticker = st.sidebar.text_input('Stock Ticker', 'AAPL')
    start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input('End Date', pd.to_datetime('2023-01-01'))
    short_window = st.sidebar.number_input('Short MA Window', 10, 100, 40)
    long_window = st.sidebar.number_input('Long MA Window', 20, 200, 100)

    run_button = st.sidebar.button('Run Backtest')

    return ticker, start_date, end_date, short_window, long_window, run_button

def display_results(portfolio, metrics):
    """
    Displays the backtesting results.

    Args:
        portfolio (pd.DataFrame): The portfolio DataFrame with equity curve.
        metrics (dict): A dictionary of performance metrics.
    """
    st.header('Backtest Results')

    # Equity Curve
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=portfolio.index, y=portfolio['total'], mode='lines', name='Equity Curve'))
    fig.update_layout(title='Portfolio Value Over Time',
                      xaxis_title='Date',
                      yaxis_title='Portfolio Value ($)')
    st.plotly_chart(fig)

    # Performance Metrics
    st.subheader('Performance Metrics')
    cols = st.columns(4)
    for i, (metric, value) in enumerate(metrics.items()):
        cols[i].metric(metric, value)
