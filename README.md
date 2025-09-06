# No-Code Algorithmic Trading Platform

This project is a Streamlit application that provides a no-code interface for building, backtesting, and analyzing algorithmic trading strategies. This initial version focuses on a simple moving average crossover strategy.

## Project Structure

The project is organized into several modules to ensure a clean and scalable architecture:

-   `app.py`: The main entry point for the Streamlit application. It orchestrates the overall workflow.
-   `ui.py`: Contains all the code related to the user interface, built with Streamlit.
-   `data.py`: Handles fetching historical stock data from Yahoo Finance using the `yfinance` library.
-   `strategy.py`: Implements the trading logic for the moving average crossover strategy.
-   `backtester.py`: The backtesting engine that simulates trades and calculates key performance metrics.
-   `requirements.txt`: A list of all the Python dependencies required to run the project.
-   `PROMPT.md`: The original detailed prompt that this project is based on.

## Getting Started

To run the application on your local machine, please follow these steps:

### 1. Prerequisites

Make sure you have Python 3.8 or higher installed on your system.

### 2. Installation

First, clone the repository to your local machine. Then, navigate to the project directory and install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

### 3. Running the Application

Once the dependencies are installed, you can run the Streamlit application with the following command:

```bash
streamlit run app.py
```

This will start the web server and open the application in your default web browser. From there, you can configure the strategy parameters and run your first backtest.
