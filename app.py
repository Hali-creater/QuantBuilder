import streamlit as st
import database as db
from ui import (authentication_ui, strategy_builder_ui, backtester_params_ui,
                broker_connection_ui, paper_trading_ui, display_results)
from data import fetch_data
from strategy import generate_signals
from backtester import run_backtest
from broker import AlpacaBroker
import pandas as pd

def handle_backtester_tab(strategy_def):
    """Handles the logic for the backtester tab."""
    st.header("Run a Backtest")
    if 'broker' not in st.session_state or st.session_state.broker is None:
        st.warning("Please connect to your Alpaca account on the 'Paper Trading' tab to fetch data for backtesting.")
        return

    ticker, start_date, end_date, run_button = backtester_params_ui()
    if run_button:
        if not ticker:
            st.error("Please enter a stock ticker.")
            return
        with st.spinner('Running backtest...'):
            data = fetch_data(st.session_state.broker.api, ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            if data is not None and not data.empty:
                signals = generate_signals(data, strategy_def)
                portfolio, metrics = run_backtest(signals)
                display_results(portfolio, metrics)
            else:
                st.error(f"Could not fetch data for ticker {ticker} in the given date range.")

def handle_paper_trading_tab(strategy_def):
    """Handles the logic for the paper trading tab."""
    st.header("Paper Trading with Alpaca")
    if 'broker' not in st.session_state:
        st.session_state.broker = None

    if st.session_state.broker is None:
        api_key, secret_key, connect_button = broker_connection_ui()
        if connect_button:
            if not api_key or not secret_key:
                st.error("Please enter both API Key and Secret Key.")
            else:
                with st.spinner("Connecting to Alpaca..."):
                    broker = AlpacaBroker(api_key, secret_key)
                    if broker.connect():
                        st.session_state.broker = broker
                        st.success("Successfully connected to Alpaca!")
                        st.rerun()
                    else:
                        st.error("Connection to Alpaca failed. Check your API keys.")
    else:
        account_info = st.session_state.broker.get_account_info()
        if account_info:
            ticker, qty, execute_button = paper_trading_ui(account_info, strategy_def)
            if execute_button:
                with st.spinner("Checking strategy and executing trade..."):
                    live_data = fetch_data(st.session_state.broker.api, ticker, pd.Timestamp.now() - pd.Timedelta(days=100), pd.Timestamp.now())
                    if live_data is not None:
                        signals = generate_signals(live_data, strategy_def)
                        latest_signal = signals['positions'].iloc[-1]
                        position = st.session_state.broker.get_position(ticker)

                        if latest_signal == 1.0 and position is None:
                            order = st.session_state.broker.place_order(ticker, qty, 'buy')
                            st.success(f"Buy order for {qty} shares of {ticker} placed successfully!")
                            st.write(order)
                        elif latest_signal == -1.0 and position is not None:
                            order = st.session_state.broker.place_order(ticker, abs(int(position.qty)), 'sell')
                            st.success(f"Sell order for {abs(int(position.qty))} shares of {ticker} placed successfully!")
                            st.write(order)
                        else:
                            st.info("Strategy conditions not met for a new trade. No order was placed.")
        else:
            st.error("Failed to fetch account information from Alpaca.")

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(layout="wide")
    db.init_db()

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        action, username, password = authentication_ui()
        if action == "signup":
            if not username or not password: st.error("Username and password cannot be empty.")
            elif db.add_user(username, password): st.success("Account created! Please login.")
            else: st.error("Username already exists.")
        elif action == "login":
            if db.verify_user(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.rerun()
            else: st.error("Invalid username or password.")
    else:
        st.sidebar.success(f"Welcome, {st.session_state.username}!")
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.session_state.broker = None
            st.rerun()

        st.title("Algorithmic Trading Platform")

        strategy_def = strategy_builder_ui()

        backtester_tab, paper_trader_tab = st.tabs(["Backtester", "Paper Trading"])

        with backtester_tab:
            handle_backtester_tab(strategy_def)

        with paper_trader_tab:
            handle_paper_trading_tab(strategy_def)

if __name__ == "__main__":
    main()
