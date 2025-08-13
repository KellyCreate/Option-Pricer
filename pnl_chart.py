import numpy as np 
import math
import matplotlib.pyplot as plt

def round_pnl_chart_bound(spot_price, buffer_ratio=0.2):
    """
    Determine appropriate upper bound for PnL chart.
    """
    round_to = 1
    if spot_price < 20:
        round_to =  1
    elif spot_price < 100: 
        round_to = 5
    elif spot_price < 500:
        round_to = 10
    elif spot_price < 1000:
        round_to = 50
    else:
        round_to = 50
    
    buffer = spot_price*buffer_ratio
    raw_lower = spot_price-buffer
    raw_upper = spot_price+buffer

    lower = math.floor(raw_lower/round_to)*round_to
    upper = math.ceil(raw_upper/round_to)*round_to

    return lower, upper

def get_strike_prices_for_long_options(spot_price, margin=0.05):
    """
    Returns recommended strike prices for long call and long put options        
    based on the spot price.
    """
    call_strike = round(spot_price * (1 + margin), 2)
    put_strike = round(spot_price * (1 - margin), 2)
    return call_strike, put_strike



def plot_payoff_diagram(K, price_lower_bound, price_upper_bound, premium=5, option_type='Long Put'):
    """
    Plot profit and loss diagram for a given strike price and a given range for the possible stock price
    """
    S_range = np.linspace(price_lower_bound, price_upper_bound, 200) # Possible stock prices at expiry

    # Payoff and PnL
    payoff = np.maximum(S_range-K,0) if option_type == 'Long Call' else np.maximum(K-S_range,0)
    pnl = payoff  - premium
    
    # Create a Figure and Axes explicitly
    fig, ax = plt.subplots(figsize=(10,5))

    ax.plot(S_range,  payoff, label="Payoff  (no cost)", linestyle='--')
    ax.plot(S_range, pnl, label='PnL (includes premium)', color='green')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(K, color='grey', linestyle=':',  label='Stike Price')
    ax.axvline(K+premium, color='red', linestyle=':', label='Breakeven point')
    ax.set_title(f"PnL and Payoff Diagram for {option_type} Option Strategy")
    ax.set_xlabel('Stock price at expiration')
    ax.set_ylabel('Profit/Loss')
    ax.legend()
    ax.grid(True)
    fig.tight_layout()

    return fig
