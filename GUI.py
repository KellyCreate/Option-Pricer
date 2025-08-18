import streamlit as st
import yfinance_data 
import historical_chart 
import pnl_chart
import black_scholes
import visualization
import binomial
import monte_carlo

def sidebar_model_parameter(spot_price, volatility):
    """
    Creates sidebar UI elements in Streamlit to input parameters for option pricing
    """
    st.subheader("📍 Specific Values for Point Calculation")
    input_spot_price = st.number_input("Spot Price", value=spot_price, format="%.2f")
    input_strike_price = st.number_input("Strike Price", value=spot_price, format="%.2f")
    input_interest_rate = st.number_input("Risk-free rate", value=0.02, format="%.4f")
    input_volatility = st.number_input("Volatility", value=volatility, format="%.4f")
    input_time_to_maturity = st.number_input("Time to Maturity (Years)", value=1.0, format="%.2f")

    st.markdown("""
    *These values are used to calculate and display the price at a single point on the surface.*
    """)

    st.subheader("📈 Strike Values for PnL")
    recommended_long_call_strike, recommended_long_put_strike = pnl_chart.get_strike_prices_for_long_options(spot_price, margin=0.05)

    long_call_strike_price = st.number_input("Long Call Strike Price", value=recommended_long_call_strike, format="%.2f")
    long_put_strike_price = st.number_input("Long Put Strike Price", value=recommended_long_put_strike, format="%.2f")


    st.subheader("🖼 Ranges for 3D Surface")
    volatility_range = st.slider("Volatility Range (for chart)",
                          min_value=0.01, max_value=1.0, value=(0.3,0.8), step=0.01)
    time_to_maturity_range = st.slider("Time Range (Years, for chart)",
                           min_value=0.0, max_value=5.0, value=(0.1,1.0), step=0.01)

    st.markdown("""
    *These ranges define the axes of the 3D chart to visualize how the price changes. Spot price, strike price and risk-free rate are the same as for single point calculation.*
    """)

    return input_spot_price, input_strike_price, input_interest_rate, input_volatility, input_time_to_maturity, volatility_range, time_to_maturity_range,  long_call_strike_price, long_put_strike_price


def model_visualization_streamlit_integration(model_pricing_call_option, model_pricing_put_option, spot_price, volatility_range, time_to_maturity_range, volatility_value, time_to_maturity_value,
                                              input_strike_price, title, long_call_strike_price, long_put_strike_price):
    """
    Integrates option pricing model results, payoff diagrams, and 3D surface visualizations into a Streamlit app.

    This function displays side-by-side outputs for call and put options, including:
    - Calculated option value at specific volatility and time to maturity.
    - Profit and loss (PnL) payoff diagrams for long call and long put strategies.
    - 3D surface and heatmap visualizations showing option price sensitivity to volatility and time to maturity.
    """

    column1, column2 = st.columns(2)
    lower_bound_price, upper_bound_price = pnl_chart.round_pnl_chart_bound(spot_price)

    # Column 1 for call option 
    with column1:
        call_value = round(model_pricing_call_option(volatility_value, time_to_maturity_value), 2)
        with st.container(border=True):
            st.write("**CALL VALUE**")
            center_col, _ = st.columns([1,2])
            with center_col:
                st.metric(
                    label="",
                    value=f"${call_value:.2f}",
                    delta="Call",
                    delta_color="normal",
                    label_visibility="collapsed"
                )
        # PnL Payoff diagram
        pnl_plot_long_call = pnl_chart.plot_payoff_diagram(long_call_strike_price, lower_bound_price, upper_bound_price, call_value, option_type='Long Call')
        st.pyplot(pnl_plot_long_call)

        # Integrate 3d surface and heatmap to streamlit 
        fig_surface, fig_heatmap = visualization.plot_3d_surface_and_heatmap(volatility_range[0], volatility_range[1], time_to_maturity_range[0], time_to_maturity_range[1], model_pricing_call_option, title)
        st.plotly_chart(fig_surface)
        st.pyplot(fig_heatmap)

    # Column 2 for put option 
    with column2:
        put_value = round(model_pricing_put_option(volatility_value, time_to_maturity_value), 2)
        with st.container(border=True):
            st.write("**PUT VALUE**")
            center_col, _ =  st.columns([1,2])
            with center_col:
                st.metric(
                    label="",
                    value=f"${put_value:.2f}",
                    delta="Put",
                    delta_color="normal",
                    label_visibility="collapsed"
                                )
        # PnL Payoff diagram
        pnl_plot_long_put = pnl_chart.plot_payoff_diagram(long_put_strike_price, lower_bound_price, upper_bound_price, call_value, option_type='Long Put')
        st.pyplot(pnl_plot_long_put)

        # Integrate 3d surface and heatmap to streamlit 
        fig_surface, fig_heatmap = visualization.plot_3d_surface_and_heatmap(volatility_range[0], volatility_range[1], time_to_maturity_range[0], time_to_maturity_range[1], model_pricing_put_option, title)
        st.plotly_chart(fig_surface)
        st.pyplot(fig_heatmap)



# -------------------------------------------------------------- Page Config --------------------------------------------------------------------

st.set_page_config(page_title='Option Pricer', 
                   page_icon='📈', 
                   layout='wide', 
                   initial_sidebar_state='expanded')



# -------------------------------------------------------------- Top of Sidebar --------------------------------------------------------------------

with st.sidebar:
    st.title('⚙️ Control Center')
    st.write('#### Connect with me ✌️:')
    linkedin_url = 'https://ca.linkedin.com/in/kalagi-kelly’ande-palmy-710328287'
    st.markdown(
        f'<a href="{linkedin_url}" target="_blank">'
        '<img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20">'
        " Kalagi Kelly Ande Palmy</a>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # --- Ticker input ---
    ticker =  st.text_input("**Ticker Symbol**", "NVDA")
    stock = yfinance_data.stockData(ticker)
    display_name = stock.get_display_name()
    spot_price = round(stock.get_spot_price(),2)
    volatility = round(stock.get_annual_volatility(),5)
    st.info(f"**Stock Name:** {display_name}")
    # Sidebar slider to select period
    historical_data_period = st.select_slider(
        "Select the maximum period for historical data",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"],
        value="1y"  # default
    )
    historical_data = stock.get_historical_data(period=historical_data_period)
    
    st.markdown("---")

# ---------------- MAIN HEADER ----------------
st.title("💹 Interactive Option Pricer")
st.caption("Explore Black-Scholes, Binomial, and Monte Carlo pricing models with dynamic visualizations.")

# Historical chart
with st.expander("📜 View Historical Price Data"):
    historical_plot = historical_chart.plot_historical_price(historical_data, display_name)
    st.plotly_chart(historical_plot)

# --- How to use this app ---
with st.sidebar:
    st.sidebar.info("""
    📊 **How to use this app:**
    - Enter specific Black-Scholes parameters to compute the price at a single point.
    - Adjust the ranges to plot the 3D surface over different volatilities and times to expiry.
    """)

# -------------------------------------------------------------- Tabs For Models --------------------------------------------------------------------
tab_black_scholes, tab_binomial, tab_monte_carlo = st.tabs(["Black-Scholes", "Binomial",  "Monte Carlo"])


# -------------------------------------------------------------- Black-Scholes Model --------------------------------------------------------------------
with tab_black_scholes:

    with st.sidebar.form('form1'):

        st.header("Black-Scholes")
        
        with st.expander("Parameters"):

            input_spot_price, input_strike_price, input_interest_rate, input_volatility, input_time_to_maturity, volatility_range, time_to_maturity_range, long_call_strike_price, long_put_strike_price = sidebar_model_parameter(spot_price, volatility)

        submit = st.form_submit_button("Update Chart")

    st.header("Black-Scholes Model", divider="grey", width="content")

    model_pricing_call_option = lambda volatility, time_to_maturity: black_scholes.black_scholes_pricing_call(spot_price=input_spot_price, 
                                                                                                        strike_price=input_strike_price, 
                                                                                                        risk_free_rate=input_interest_rate, 
                                                                                                        time_to_maturity=time_to_maturity, 
                                                                                                        volatility=volatility)
    model_pricing_put_option = lambda volatility, time_to_maturity: black_scholes.black_scholes_pricing_put(spot_price=input_spot_price, 
                                                                                                        strike_price=input_strike_price, 
                                                                                                        risk_free_rate=input_interest_rate, 
                                                                                                        time_to_maturity=time_to_maturity, 
                                                                                                        volatility=volatility)
    model_visualization_streamlit_integration(model_pricing_call_option, model_pricing_put_option, spot_price, volatility_range, time_to_maturity_range,
                                            input_volatility, input_time_to_maturity,  input_strike_price, "Black-Scholes",  long_call_strike_price, long_put_strike_price)

# -------------------------------------------------------------- Binomial Model --------------------------------------------------------------------
with tab_binomial:
        
    with st.sidebar.form('form2'):

        st.header('Binomial')

        with st.expander("Parameters"):

            input_spot_price, input_strike_price, input_interest_rate, input_volatility, input_time_to_maturity, volatility_range, time_to_maturity_range, long_call_strike_price, long_put_strike_price = sidebar_model_parameter(spot_price, volatility)
            input_step = int(st.text_input("Number of time steps",100))

        submit = st.form_submit_button("Update Chart")

    st.header("Binomial Model", divider="grey",  width="content")

    model_pricing_call_option = lambda volatility, time_to_maturity: binomial.binomial_pricing(spot_price=input_spot_price, 
                                                                                                        strike_price=input_strike_price, 
                                                                                                        risk_free_rate=input_interest_rate, 
                                                                                                        time_to_maturity=time_to_maturity, 
                                                                                                        volatility=volatility,
                                                                                                        steps = input_step,
                                                                                                        option_type = "Call")
    model_pricing_put_option = lambda volatility, time_to_maturity: binomial.binomial_pricing(spot_price=input_spot_price, 
                                                                                                        strike_price=input_strike_price, 
                                                                                                        risk_free_rate=input_interest_rate, 
                                                                                                        time_to_maturity=time_to_maturity, 
                                                                                                        volatility=volatility,
                                                                                                        steps = input_step,
                                                                                                        option_type = "Put")
    model_visualization_streamlit_integration(model_pricing_call_option, model_pricing_put_option, spot_price, volatility_range, time_to_maturity_range,
                                            input_volatility, input_time_to_maturity,  input_strike_price, "Binomial",  long_call_strike_price, long_put_strike_price)


# -------------------------------------------------------------- Monte Carlo Model --------------------------------------------------------------------
with tab_monte_carlo:
    with st.sidebar.form('form3'):

        st.header('Monte Carlo')

        with st.expander("Parameters"):

            input_spot_price, input_strike_price, input_interest_rate, input_volatility, input_time_to_maturity, volatility_range, time_to_maturity_range, long_call_strike_price, long_put_strike_price = sidebar_model_parameter(spot_price, volatility)

        submit = st.form_submit_button("Update Chart")

    st.header("Monte Carlo Model", divider="grey",  width="content")

    model_pricing_call_option = lambda volatility, time_to_maturity: monte_carlo.monte_carlo_pricing(spot_price=input_spot_price, 
                                                                                                        strike_price=input_strike_price, 
                                                                                                        risk_free_rate=input_interest_rate, 
                                                                                                        time_to_maturity=time_to_maturity, 
                                                                                                        volatility=volatility,
                                                                                                        option_type = "Call")

    model_pricing_put_option = lambda volatility, time_to_maturity: monte_carlo.monte_carlo_pricing(spot_price=input_spot_price, 
                                                                                                        strike_price=input_strike_price, 
                                                                                                        risk_free_rate=input_interest_rate, 
                                                                                                        time_to_maturity=time_to_maturity, 
                                                                                                        volatility=volatility,
                                                                                                        option_type = "Put")

    model_visualization_streamlit_integration(model_pricing_call_option, model_pricing_put_option, spot_price, volatility_range, time_to_maturity_range,
                                            input_volatility, input_time_to_maturity,  input_strike_price, "Monte Carlo",  long_call_strike_price, long_put_strike_price)
