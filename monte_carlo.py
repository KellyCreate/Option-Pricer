import numpy as np
import scipy.stats as stats

def delta_calculator(spot_price, strike_price, risk_free_rate, time_to_maturity, volatility, option_type='Call'):
    """
    
    """
    d1 = (np.log(spot_price/strike_price)+(risk_free_rate+volatility**2/2)*time_to_maturity)/(volatility*np.sqrt(time_to_maturity))
    if option_type == 'Call':
        delta = stats.norm.cdf(d1,0,1)
    else:
        delta = -stats.norm.cdf(-d1,0,1)
    return delta

def monte_carlo_pricing(spot_price, strike_price, risk_free_rate, time_to_maturity, volatility, number_of_simulation=10000, option_type="Call"):
    """
    Monte Carlo simulation to price a call option. Variance reduction is applied using the control variates method.
    """
    # Precomputed constants
    drift_of_log_returns = (risk_free_rate-0.5*volatility**2)*time_to_maturity
    volatility_scaled = volatility*np.sqrt(time_to_maturity)
    risk_free_growth_factor = np.exp(risk_free_rate*time_to_maturity)
    

    #  Simulate terminal stock prices
    Z = np.random.standard_normal(number_of_simulation)    # Sample form standard normal distribution 
    log_returns = drift_of_log_returns+volatility_scaled*Z
    price_at_maturity = spot_price*np.exp(log_returns) # Geometric Brownian Motion

    # Payoff and delta
    if option_type == "Call":
        payoff = np.maximum(price_at_maturity-strike_price, 0)
    elif option_type == "Put":
        payoff = np.maximum(strike_price-price_at_maturity,0)
    else:
        raise ValueError("option_type must be either 'Call' or Put'")
    delta_0 = delta_calculator(spot_price, strike_price, risk_free_rate, time_to_maturity, volatility, option_type)

    # Control variate using delta hedging over one step
    pnl =  delta_0*(price_at_maturity-spot_price*risk_free_growth_factor)

    # Combine payoff and control variate
    control_variate_coefficient = -1
    adjusted_payoff = payoff  + control_variate_coefficient*pnl

    # Discount to present value and calculate monte carlo value
    discounted_payoff = np.exp(-risk_free_rate*time_to_maturity)*adjusted_payoff
    option_price = np.mean(discounted_payoff)

    return option_price




