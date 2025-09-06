import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def authentication_ui():
    """Displays the login/signup UI and returns user actions."""
    st.title("Welcome to the Algorithmic Trading Platform")
    if 'authenticated' not in st.session_state:
        st.session_state['authenticated'] = False
    choice = st.selectbox("Login / Signup", ["Login", "Sign Up"])
    if choice == "Sign Up":
        st.subheader("Create a New Account")
        new_username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up"):
            return "signup", new_username, new_password
    else:
        st.subheader("Login to Your Account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            return "login", username, password
    return None, None, None

def strategy_builder_ui():
    """UI for building a flexible trading strategy."""
    st.sidebar.header('Strategy Builder')
    indicators = ['SMA', 'RSI', 'Close']
    operators = ['crosses_above', 'greater_than', 'less_than']
    st.sidebar.subheader("Entry Condition")
    op1_name = st.sidebar.selectbox("Indicator 1", indicators, key="op1_name")
    op1_params = {}
    if op1_name == 'SMA':
        op1_params['length'] = st.sidebar.number_input("SMA 1 Period", 1, 100, 20, key="op1_sma")
    elif op1_name == 'RSI':
        op1_params['length'] = st.sidebar.number_input("RSI Period", 1, 100, 14, key="op1_rsi")
    operator = st.sidebar.selectbox("Operator", operators, key="operator")
    op2_name = st.sidebar.selectbox("Indicator 2", indicators, key="op2_name")
    op2_params = {}
    if op2_name == 'SMA':
        op2_params['length'] = st.sidebar.number_input("SMA 2 Period", 1, 200, 50, key="op2_sma")
    elif op2_name == 'RSI':
        op2_params['length'] = st.sidebar.number_input("RSI 2 Period", 1, 100, 70, key="op2_rsi")
    strategy_definition = {'entry': {'operand1': {'name': op1_name, 'params': op1_params}, 'operator': operator, 'operand2': {'name': op2_name, 'params': op2_params}}}
    return strategy_definition

def backtester_params_ui():
    """UI for getting the parameters for the backtester."""
    st.sidebar.header("Backtest Parameters")
    ticker = st.sidebar.text_input('Stock Ticker', 'AAPL')
    start_date = st.sidebar.date_input('Start Date', pd.to_datetime('2020-01-01'))
    end_date = st.sidebar.date_input('End Date', pd.to_datetime('2023-01-01'))
    run_button = st.sidebar.button('Run Backtest')
    return ticker, start_date, end_date, run_button

def broker_connection_ui():
    """UI for connecting to a broker."""
    st.subheader("Connect to Alpaca Paper Trading")
    api_key = st.text_input("Alpaca API Key", type="password", key="api_key")
    secret_key = st.text_input("Alpaca Secret Key", type="password", key="secret_key")
    connect_button = st.button("Connect to Alpaca")
    return api_key, secret_key, connect_button

def paper_trading_ui(account_info, strategy_def):
    """UI for the paper trading dashboard."""
    st.subheader("Paper Trading Dashboard")
    st.metric("Portfolio Value", f"${float(account_info.portfolio_value):,}")
    st.metric("Buying Power", f"${float(account_info.buying_power):,}")

    st.write("---")
    st.subheader("Live Strategy Execution")
    st.write("Your currently configured strategy is:")
    st.json(strategy_def)

    ticker = st.text_input("Ticker to Trade", "AAPL")
    qty = st.number_input("Quantity to Trade", 1, 1000, 10)

    execute_button = st.button("Run Strategy Check & Execute Trade")

    return ticker, qty, execute_button

def display_results(portfolio, metrics):
    """Displays the backtesting results with enhanced metrics."""
    st.header('Backtest Results')
    st.subheader('Equity Curve')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=portfolio.index, y=portfolio['total'], mode='lines', name='Equity Curve'))
    fig.update_layout(title='Portfolio Value Over Time', xaxis_title='Date', yaxis_title='Portfolio Value ($)')
    st.plotly_chart(fig, use_container_width=True)
    st.subheader('Performance Metrics')
    row1_cols = st.columns(4)
    row2_cols = st.columns(4)
    metric_keys = list(metrics.keys())
    for i in range(4):
        row1_cols[i].metric(metric_keys[i], metrics[metric_keys[i]])
    for i in range(4):
        row2_cols[i].metric(metric_keys[i+4], metrics[metric_keys[i+4]])
