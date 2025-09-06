import streamlit as st
from data import fetch_data
from strategy import moving_average_crossover_strategy
from backtester import run_backtest
from ui import setup_ui, display_results

def main():
    """
    Main function to run the Streamlit application.
    """
    ticker, start_date, end_date, short_window, long_window, run_button = setup_ui()

    if run_button:
        if not ticker:
            st.error("Please enter a stock ticker.")
            return

        data = fetch_data(ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))

        if data is not None:
            signals = moving_average_crossover_strategy(data, short_window, long_window)
            portfolio, metrics = run_backtest(signals)
            display_results(portfolio, metrics)
        else:
            st.error(f"Could not fetch data for ticker {ticker}.")

if __name__ == "__main__":
    main()
