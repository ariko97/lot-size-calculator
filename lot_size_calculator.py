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

def calculate_volatility_adjusted_setup(account_balance, permitted_loss, pip_value, AMR, desired_profit, volatility_factor=1.0):
    ADR = AMR / 20  
    stop_loss_pips = ADR * volatility_factor
    take_profit_pips = (desired_profit / pip_value)
    lot_size = permitted_loss / (stop_loss_pips * pip_value)

    setup = pd.DataFrame({
        'Metric': ['Average Daily Range (Pips)', 'Volatility Adjusted Stop Loss (Pips)', 'Take Profit Pips', 'Recommended Lot Size'],
        'Value': [round(ADR, 2), round(stop_loss_pips, 2), round(take_profit_pips, 2), round(lot_size, 2)]
    })
    return setup, stop_loss_pips

st.title('🌟 Enhanced Volatility-Adjusted Trade Calculator')

# User Inputs
account_balance = st.number_input('Total Account Balance ($)', value=10000.0)
risk_choice = st.radio(
    "Select Risk Type",
    ("Risk Full Account Balance", "Risk Permitted Daily Loss"),
    index=1
)

if risk_choice == "Risk Permitted Daily Loss":
    permitted_loss = st.number_input('Permitted Daily Loss ($)', value=100.0)
else:
    permitted_loss = account_balance  # Using the full account balance as risk

desired_profit = st.number_input('Desired Profit ($)', value=500.0)
instrument = st.selectbox('Select Instrument', list(AMR_VALUES.keys()))

# Market Volatility Conditions Slider
volatility_factor = st.slider(
    "Market Volatility Conditions (Drag to Adjust)",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1
)

AMR = AMR_VALUES[instrument]
pip_value = PIP_VALUES[instrument]

setup, stop_loss_pips = calculate_volatility_adjusted_setup(account_balance, permitted_loss, pip_value, AMR, desired_profit, volatility_factor)

st.write(f'## Recommended Trade Setup for {instrument}:')
st.write(setup)

# Adding dead space at the bottom to avoid Streamlit banner overlap
st.markdown("<div style='height: 200px;'></div>", unsafe_allow_html=True)
