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


import numpy as np
import matplotlib.pyplot as plt

def plot_payoff_diagram(K, price_lower_bound, price_upper_bound, premium=5, option_type='Long Put'):
    """
    Plot profit and loss diagram for a given strike price and a given range for the possible stock price.
    Includes clear placement of the breakeven point.
    """
    S_range = np.linspace(price_lower_bound, price_upper_bound, 300)  
    
    # Payoff and PnL
    if option_type == 'Long Call':
        payoff = np.maximum(S_range - K, 0)
        breakeven = K + premium
    else:  # Long Put
        payoff = np.maximum(K - S_range, 0)
        breakeven = K - premium
    
    pnl = payoff - premium

    # Create Figure
    fig, ax = plt.subplots(figsize=(10,6), facecolor="white")
    ax.set_facecolor("white")

    # Plot PnL
    ax.plot(S_range, pnl, color='#2ecc71', linewidth=2.2, label='PnL (includes premium)')
    ax.fill_between(S_range, pnl, 0, where=(pnl >= 0), color='#2ecc71', alpha=0.25)
    ax.fill_between(S_range, pnl, 0, where=(pnl < 0), color='#e74c3c', alpha=0.25)

    # Payoff
    ax.plot(S_range, payoff, linestyle='--', color='#2980b9', linewidth=2, label="Payoff (no cost)")

    # Reference lines
    ax.axhline(0, color='black', linewidth=1, linestyle='-')
    ax.axvline(K, color='#7f8c8d', linestyle=':', linewidth=1.3, label=f'Strike Price ({K})')

    # Add breakeven only if it lies inside plotted range
    if price_lower_bound <= breakeven <= price_upper_bound:
        ax.axvline(breakeven, 
                   color='#e67e22', linestyle='--', linewidth=1.5, 
                   label=f'Breakeven ({breakeven:.2f})')

    # Titles & labels
    ax.set_title(f"{option_type} Option: Payoff & PnL", fontsize=16, fontweight='bold', color='#1F2937')
    ax.set_xlabel("Stock Price at Expiration", fontsize=12, color='#1F2937')
    ax.set_ylabel("Profit / Loss", fontsize=12, color='#1F2937')

    # Legend
    ax.legend(frameon=False, fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.4, color="#bdc3c7")

    fig.tight_layout()
    return fig


