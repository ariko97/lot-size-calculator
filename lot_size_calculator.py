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

    .stSlider label {
        color: #FFD700;
    }

    .stNumberInput label {
        color: #FFD700;
    }
    </style>
''', unsafe_allow_html=True)

# Displaying the "Made by Ariko with Love 💖" text at the top center above the title
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

def calculate_volatility_adjusted_setup(account_balance, permitted_loss, pip_value, AMR, volatility_factor=1.0):
    ADR = AMR / 20  
    stop_loss_pips = ADR * volatility_factor
    lot_size = permitted_loss / (stop_loss_pips * pip_value)
    setup = pd.DataFrame({
        'Metric': ['Average Daily Range (Pips)', 'Volatility Adjusted Stop Loss (Pips)', 'Recommended Lot Size', 'Risk (%)'],
        'Value': [round(ADR, 2), round(stop_loss_pips, 2), round(lot_size, 2), round((permitted_loss / account_balance) * 100, 2)]
    })
    return setup, stop_loss_pips

st.title('🌟 Volatility-Adjusted Trade Calculator')

account_balance = st.number_input('Permitted Daily Loss (€)', value=10000.0)
desired_profit = st.number_input('Desired Profit ($)', value=500.0)
permitted_loss = st.number_input('Voluntary Loss Taken ($)', value=70.0)
instrument = st.selectbox('Select Instrument', list(AMR_VALUES.keys()))

volatility_factor = st.slider(
    "Volatility Adjustment Factor (Drag to Adjust)",
    min_value=0.5,
    max_value=2.0,
    value=1.0,
    step=0.1
)

AMR = AMR_VALUES[instrument]
pip_value = PIP_VALUES[instrument]

setup, stop_loss_pips = calculate_volatility_adjusted_setup(account_balance, permitted_loss, pip_value, AMR, volatility_factor)

st.write(f'## Recommended Trade Setup for {instrument}:')
st.write(setup)

def plot_risk_pie(risk_percentage):
    fig, ax = plt.subplots(figsize=(6, 6))
    wedges, texts, autotexts = ax.pie(
        [risk_percentage, 100 - risk_percentage],
        labels=['Risk (%)', 'Remaining Balance (%)'],
        colors=['#FFD700', '#444444'],
        autopct='%1.1f%%',
        pctdistance=0.75,
        textprops=dict(color='white', fontsize=14)
    )
    for text in texts:
        text.set_color('white')
    ax.set_title('Account Risk Ratio', color='white')
    fig.patch.set_alpha(0)
    st.pyplot(fig)

risk_percentage = (permitted_loss / account_balance) * 100
plot_risk_pie(risk_percentage)

def plot_profit_loss(stop_loss_pips, instrument):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(['Stop Loss (Pips)', 'ADR (Pips)'], [stop_loss_pips, AMR / 20], color=['#FFD700', '#444444'])
    ax.set_title(f'Volatility-Based Stop Loss for {instrument}', color='white')
    ax.set_ylabel('Pips', color='white')
    ax.tick_params(colors='white')
    fig.patch.set_alpha(0)
    st.pyplot(fig)

plot_profit_loss(stop_loss_pips, instrument)

st.markdown("<div style='height: 200px;'></div>", unsafe_allow_html=True)
