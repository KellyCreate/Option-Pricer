import yfinance as yf
import numpy as np

class stockData:
    def __init__(self, ticker):
        """
        Initialize with the stock Ticker symbol
        """
        self.ticker = ticker.upper()
        self.data = yf.Ticker(self.ticker)
    
    def get_display_name(self):
        """
        Get the display name of the stock
        """
        return self.data.info['displayName']


    def get_spot_price(self):
        """
        Get the latest spot price (last close)
        """
        price = self.data.history(period="1d")['Close'][-1]
        return price
    

    def get_annual_volatility(self, period="1y"):
        """
        Estimate annual volatility from historical daily returns.
        period: lookback period , e.g., '1y', '6mo' 
        """
        hist = self.data.history(period=period)
        daily_returns  =  hist['Close'].pct_change().dropna()
        volatility = np.std(daily_returns)*np.sqrt(252)
        return volatility
    
    
    def get_historical_data(self, period="1y"):
        """
        Get historical data for selected period
        """
        return self.data.history(period=period)['Close']