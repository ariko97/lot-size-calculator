import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Custom CSS Styling with Background Image and Font
st.markdown('''
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500&display=swap');

    .stApp {
        background-image: url('https://raw.githubusercontent.com/ariko97/lot-size-calculator/main/background.png');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }

    .block-container {
        background-color: rgba(0, 0, 0, 0.75);
        padding: 20px;
        border-radius: 15px;
        margin-top: 40px;
    }

    .top-layer {
        position: sticky;
        top: 0;
        left: 50%;
        color: #ffb6c1;
        font-size: 20px;
        font-weight: bold;
        padding: 10px;
        z-index: 10000;
        text-align: center;
    }

    h1, h2 {
        color: #FFD700;
    }

    .stSlider label, .stNumberInput label, .stSelectbox label {
        color: #FFD700;
    }
    </style>
''', unsafe_allow_html=True)

st.markdown('<div class="top-layer">Made by Ariko with Love 💖</div>', unsafe_allow_html=True)

# Define the AMR values for each instrument
AMR_VALUES = {
    'EURUSD': 360.3,
    'USDJPY': 796.08,
    'USDCAD': 419.58,
    'US100': 15067.33,
    'XAUUSD': 19308.17,
    'BTCUSD': 20582.5,
    'ETHUSD': 91756.17,
    'US500': 30819.67,
    'DOGEUSD': 16186.24,
    'XRPUSD': 19103.1,
    'EURGBP': 156.37,
    'US30': 16762.83
}

PIP_VALUES = {
    'EURUSD': 10,
    'USDJPY': 9.09,
    'USDCAD': 7.69,
    'US100': 1,
    'XAUUSD': 1,
    'BTCUSD': 1,
    'ETHUSD': 1,
    'US500': 1,
    'DOGEUSD': 0.01,
    'XRPUSD': 0.001,
    'EURGBP': 12.5,
    'US30': 1
}

def calculate_lot_size(account_balance, voluntary_loss, pip_value, AMR, desired_profit, volatility_factor, risk_multiplier):
    ADR = AMR / 20  # Average Daily Range
    stop_loss_pips = ADR / (volatility_factor * risk_multiplier)  # Adjusted Stop Loss Pips
    take_profit_pips = desired_profit / pip_value

    # Scaled lot size calculation
    lot_size = (voluntary_loss / (stop_loss_pips * pip_value)) * (account_balance / 1000)
    risk_percentage = (voluntary_loss / account_balance) * 100

    setup = pd.DataFrame({
        'Metric': ['Recommended Lot Size', 'Risk (%)', 'Take Profit Pips', 'Stop Loss Pips'],
        'Value': [round(lot_size, 2), round(risk_percentage, 2), round(take_profit_pips, 2), round(stop_loss_pips, 2)]
    })
    return setup, stop_loss_pips, risk_percentage

st.title('📊 Trade Profit and Loss with Risk Management')

# User Inputs
account_balance = st.number_input('Total Account Balance ($)', value=10000.0)
voluntary_loss = st.number_input('Voluntary Loss ($)', value=600.0)
desired_profit = st.number_input('Desired Profit ($)', value=500.0)
instrument = st.selectbox('Select Instrument', list(AMR_VALUES.keys()))

# Trade Type Selector
trade_type = st.selectbox(
    "Select Trade Type",
    ("Scalping", "Day Trading", "Swing Trading")
)

# Risk Multiplier Based on Trade Type
risk_multipliers = {"Scalping": 2.0, "Day Trading": 1.0, "Swing Trading": 0.5}
risk_multiplier = risk_multipliers[trade_type]

# Improved Volatility Slider
volatility_factor = st.slider(
    label="Less Volatile Market (Left) ➔ Highly Volatile Market (Right)",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1
)

AMR = AMR_VALUES[instrument]
pip_value = PIP_VALUES[instrument]

setup, stop_loss_pips, risk_percentage = calculate_lot_size(
    account_balance, voluntary_loss, pip_value, AMR, desired_profit, volatility_factor, risk_multiplier
)

st.write(f'## Recommended Trade Setup for {instrument}:')
st.write(setup)
