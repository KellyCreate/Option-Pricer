#from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def plot_3d_surface_and_heatmap(min_volatility, max_volatility, min_time,  max_time, pricing_function, title):
    """
    Plot 3d surface to visualize how option prices depend on volatility and time  to expiry
    """
    # --- Prepare the data ---
    volatility_range = np.linspace(min_volatility, max_volatility, 10)
    time_range = np.linspace(min_time, max_time, 10)    # Time in years

    # Create meshgrid 
    V, T = np.meshgrid(volatility_range, time_range)

    # Compte option prices
    prices = np.zeros_like(V)

    for i in range(prices.shape[0]):
        for j in range(prices.shape[1]):
            prices[i,j] = pricing_function(V[i,j],T[i,j])

    # --- Plot 3D surface ---
    fig1 = go.Figure(data=[go.Surface(x=V, y=T, z=prices, colorscale='viridis', colorbar_title='Option Price')])
    fig1.update_layout(
        title=f"{title} Option Price Surface",
        scene=dict(
            xaxis_title= 'Volatility',
            yaxis_title= 'Time to maturity',
            zaxis_title= 'Option Price'
    )
    )

    # --- Plot heatmap ---
    fig2, ax2 = plt.subplots(figsize=(10,5))
    sns.heatmap(prices, xticklabels=np.round(volatility_range,2), yticklabels=np.round(time_range,2), annot=True, fmt=".2f", cmap='viridis', ax=ax2)
    ax2.set_xlabel('Volatility')
    ax2.set_ylabel('Time to expiry')
    ax2.set_title(f'{title} Option Price Heatmap')


    return fig1, fig2


