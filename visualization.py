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
    fig1 = go.Figure(data=[go.Surface(x=V, y=T, z=prices, colorscale=[[0, "#081B41"], [0.5, "#1E3A8A"], [1, "#3B82F6"]],
                                    colorbar=dict(title="Option Price", thickness=15, tickcolor="black"))])
    fig1.update_layout(
        title=dict(text=f"{title} Option Price Surface", font=dict(size=18, color="#111827")),
        scene=dict(
            xaxis=dict(title="Volatility", tickfont=dict(size=14, color="#111827"), backgroundcolor="#F9FAFB"),
            yaxis=dict(title="Time to Maturity", tickfont=dict(size=14, color="#111827"), backgroundcolor="#F9FAFB"),
            zaxis=dict(title="Option Price", tickfont=dict(size=14, color="#111827"), backgroundcolor="#F9FAFB"),
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        template="plotly_white"
    )

    # --- Plot heatmap ---

    # Custom modern grey-blue colormap
    cmap = sns.color_palette("blend:#1E3A8A,#3B82F6,#E5E7EB", as_cmap=True)
    fig2, ax2 = plt.subplots(figsize=(10,5))

    sns.heatmap(prices, xticklabels=np.round(volatility_range,2), yticklabels=np.round(time_range,2), annot=True, fmt=".2f", cmap=cmap, ax=ax2, 
                linecolor="white", linewidths=0.5, cbar_kws={"label": "Option Price"})
    ax2.set_xlabel("Volatility", fontsize=12, weight="bold")
    ax2.set_ylabel("Time to Expiry", fontsize=12, weight="bold")
    ax2.set_title(f"{title} Option Price Heatmap", fontsize=14, weight="bold", pad=15)


    return fig1, fig2


