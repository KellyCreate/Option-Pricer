from math import log, sqrt, exp
from scipy.stats import norm
import numpy as np
from functools import partial

def black_scholes_pricing_call(spot_price, strike_price, risk_free_rate, time_to_maturity, volatility):
    """
    Takes the parameters and return the black scholes price for call option
    """
    d1 = (log(spot_price/strike_price)+(risk_free_rate+(volatility**2)/2)*time_to_maturity)/(volatility*sqrt(time_to_maturity))
    d2 = d1-volatility*sqrt(time_to_maturity)

    price = spot_price*norm.cdf(d1)-strike_price*exp(-risk_free_rate*time_to_maturity)*norm.cdf(d2)
    return price 

def black_scholes_pricing_put(spot_price, strike_price, risk_free_rate, time_to_maturity, volatility):
    """
    Takes the parameters and return the black scholes price for put option
    """
    d1 = (log(spot_price/strike_price)+(risk_free_rate+(volatility**2)/2)*time_to_maturity)/(volatility*sqrt(time_to_maturity))
    d2 = d1-volatility*sqrt(time_to_maturity)

    price =  -spot_price*norm.cdf(-d1)+strike_price*exp(-risk_free_rate*time_to_maturity)*norm.cdf(-d2)
    return price
