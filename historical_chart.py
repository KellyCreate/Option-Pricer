import plotly.express as px
import yfinance_data

def plot_historical_price(price, display_name):
    """
    Create and return an interactive Plotly figure of historical stock price
    """
    fig = px.line(
        price,
        x=price.index,
        y=price.values,
        title=f"{display_name} - Historical Close Price",
        labels={"x": "Date", "y": "Price (USD)"},
        template="plotly_white"
    )

    # Improve design
    fig.update_traces(
        line=dict(color="#1f77b4", width=2),
        hovertemplate="Date: %{x}<br>Price: %{y:.2f} USD"
    )
    
    fig.update_layout(
        title=dict(font=dict(size=20, family="Arial", color="black"), x=0.4),
        xaxis=dict(showgrid=True, gridcolor="lightgray"),
        yaxis=dict(showgrid=True, gridcolor="lightgray"),
        hovermode="x unified"  # single hover label across the vertical line
    )

    return fig
