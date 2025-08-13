import matplotlib.pyplot as plt
import yfinance_data

def plot_historical_price(price, display_name):
    """
    Create and return a matplotlib figure of historical stock price
    """
    # Create a Figure and Axes explicitly
    fig, ax = plt.subplots(figsize=(10,5))
    # Use artist layer: call methods on `ax`
    ax.plot(price.index, price, label='Close Price', color='blue')
    ax.set_title(f"{display_name} Historical Close Price (1Y)")
    ax.set_xlabel('Date')
    ax.set_ylabel('Price (USD)')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    fig.tight_layout()

    return fig

