import numpy as np
from math import exp

def binomial_pricing(spot_price, strike_price, risk_free_rate, time_to_maturity, volatility, steps=100, option_type="Call"):
    """
    Calculates the price of a European call option using the Binomial model. 
    The choice of the parameters u and d are made according to the Cox-Ross-Rubinstein (CRR) model
    """
    dt = time_to_maturity/steps     # Length of each time step in years. Smaller dt means a finer (more accurate) tree.
    u = exp(volatility*np.sqrt(dt))     # Upward movement factor. Represents the percentage increase in stock price after one time step if it moves up.
    d = 1/u    # Upward movement factor. Represents the percentage increase in stock price after one time step if it moves up.
    p = (exp(risk_free_rate*dt)-d)/(u-d)    # Upward movement factor. Represents the percentage increase in stock price after one time step if it moves up.
    discount = exp(-risk_free_rate*dt)    # Upward movement factor. Represents the percentage increase in stock price after one time step if it moves up.

    # Stock prices and call payoffs at maturity - Time step N
    prices = spot_price*d**np.arange(steps,-1,-1)*u**np.arange(0,steps+1,1)
    if option_type == "Call":
        values = np.maximum(prices-strike_price, 0)
    else:
        values = np.maximum(strike_price-prices,0)
    # Backward induction through the tree
    for i in range(steps-1, -1, -1):
        values = discount*(p*values[1:]+(1-p)*values[:-1])

    return values[0]

