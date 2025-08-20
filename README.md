# Option Pricer

**Interactive Option Pricing Tool** – A user-friendly Python app that lets users interactively price European options using classic models (Black-Scholes, Binomial, Monte Carlo) and visualize results—all powered by Streamlit.

---

##  Live Demo

[Open in Streamlit Cloud](https://option-pricer-kelly-palmy.streamlit.app)

---

##  Overview

**Option Pricer** is a streamlined, visually interactive toolkit designed for option pricing and analysis. It's built with the following goals:

- **Clarity**: Clean interfaces to intuitively explore option pricing models.
- **Depth**: Leverage trusted financial models (Black-Scholes, Binomial, Monte Carlo).
- **Insight**: Dynamic charts for historical data and profit-and-loss visualization.
- **Simplicity**: No heavy setup—just run with Streamlit and go.

---

##  Features

- 🏷  **Option Pricing Methods**:  
  - **Black-Scholes Model**  
  - **Binomial Model**  
  - **Monte Carlo Simulation**

-  **Interactive GUI with Streamlit**: Clean tabs and widgets for user input (spot, strike, volatility, etc.)

-  **Visualizations**:  
  - Historical price charts  
  - PnL curves based on your model parameters

-  **Easy Data Handling**: Fetches live data using `yfinance` and processes results via `pandas`.

---

##  Tech Stack

| Component             | Purpose                                      |
|----------------------|----------------------------------------------|
| **Python 3.x**       | Core programming language                    |
| **Streamlit**        | App interface and interactive controls       |
| **yfinance / pandas**| Data fetching and manipulation               |
| **Matplotlib / Streamlit Charts** | Visualization              |
| **Black-Scholes, Binomial, Monte Carlo** | Pricing algorithms    |

---

##  Installation & Setup

1. **Clone the repo**:
   ```bash
   git clone https://github.com/KellyCreate/Option-Pricer.git
   cd Option-Pricer

2. **Create annd activate a virtual environmen**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   
4. **Run the app locally**:
   ```bash
   streamlit run GUI.py

## Project Structure
```bash
Option-Pricer/
├── GUI.py                 # Main Streamlit app
├── binomial.py            # Binomial pricing logic
├── black_scholes.py       # Black-Scholes formula implementation
├── monte_carlo.py         # Monte Carlo simulation logic
├── yfinance_data.py       # Data retrieval from Yahoo Finance
├── historical_chart.py    # Price charting utilities
├── pnl_chart.py           # Profit & Loss visualization tools
├── visualization.py       # Shared plotting logic
├── requirements.txt       # Dependencies
└── .gitignore             # Ignored files (pycache, venv, etc.)

