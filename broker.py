import alpaca_trade_api as tradeapi

class AlpacaBroker:
    """
    A wrapper for the Alpaca Trade API to handle broker interactions.
    """
    def __init__(self, api_key, secret_key, paper=True):
        self.api_key = api_key
        self.secret_key = secret_key
        self.paper = paper
        self.api = None

    def connect(self):
        """
        Connects to the Alpaca API.
        Returns the API object on success, None on failure.
        """
        try:
            base_url = 'https://paper-api.alpaca.markets' if self.paper else 'https://api.alpaca.markets'
            self.api = tradeapi.REST(self.api_key, self.secret_key, base_url, api_version='v2')
            account = self.api.get_account()
            if account.status == 'ACTIVE':
                return self.api
            else:
                return None
        except Exception as e:
            print(f"Error connecting to Alpaca: {e}")
            return None

    def get_account_info(self):
        """
        Retrieves account information.
        """
        if not self.api:
            return None
        try:
            return self.api.get_account()
        except Exception as e:
            print(f"Error getting account info: {e}")
            return None

    def place_order(self, symbol, qty, side, order_type='market', time_in_force='gtc'):
        """
        Places an order with the broker.

        Args:
            symbol (str): The stock ticker.
            qty (int): The number of shares.
            side (str): 'buy' or 'sell'.
            order_type (str): 'market', 'limit', etc.
            time_in_force (str): 'gtc', 'day', etc.

        Returns:
            The order object if successful, else None.
        """
        if not self.api:
            return None
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=order_type,
                time_in_force=time_in_force
            )
            return order
        except Exception as e:
            print(f"Error placing order: {e}")
            return None

    def get_position(self, symbol):
        """
        Retrieves the current position for a given symbol.
        """
        if not self.api:
            return None
        try:
            position = self.api.get_position(symbol)
            return position
        except tradeapi.rest.APIError as e:
            if e.status_code == 404: # Position not found
                return None
            else:
                raise e
