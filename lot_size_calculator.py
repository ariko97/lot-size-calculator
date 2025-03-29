import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Custom background and styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500&display=swap'); /* Cooler Font */

.stApp {
    background-image: url('https://raw.githubusercontent.com/ariko97/lot-size-calculator/main/background.png');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #FFFFFF;
    padding-bottom: 100px; /* Adding bottom padding to avoid overlap with Streamlit banner */
}

.block-container {
    background-color: rgba(0, 0, 0, 0.75);
    padding: 15px;
    border-radius: 10px;
    margin-top: 60px;
}

.top-layer {
    position: sticky;
    top: 0;
    left: 700%; /* Shifted way more to the right */
    color: #ffb6c1;  /* baby pink */
    font-size: 18px;
    font-family: 'Montserrat', sans-serif;  /* New Cooler Font */
    font-weight: bold;
    padding: 8px;
    z-index: 10000;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Displaying the "Made by Ariko with Love 💖" text at the top center above the title
st.markdown('<div class="top-layer">Made by Ariko with Love 💖</div>', unsafe_allow_html=True)

# Title of the tool
st.title('Trade Profit and Loss Calculator with Risk Management')

# Pip/Point values per instrument
pip_values = {
    'US100': 1, 'US500': 1, 'XAUUSD': 10,
    'EURUSD': 10, 'GBPUSD': 10, 'USDJPY': 10, 'USDCAD': 10,
    'AUDUSD': 10, 'NZDUSD': 10,
    'BTCUSD': 100, 'ETHUSD': 10, 'SOLUSD': 1, 'DOGEUSD': 1
}

class TradeCalculator:
    def __init__(self, account_balance, instrument, desired_profit, permitted_loss):
        self.account_balance = account_balance
        self.instrument = instrument
        self.desired_profit = desired_profit
        self.permitted_loss = permitted_loss
        self.pip_value = pip_values[instrument]

    def calculate_lot_size(self, stop_loss_points):
        return abs(self.permitted_loss / (stop_loss_points * self.pip_value))

    def recommended_setup(self, stop_loss_points):
        lot_size = self.calculate_lot_size(stop_loss_points)
        profit_target_points = (self.desired_profit / self.permitted_loss) * stop_loss_points
        risk_percentage = (self.permitted_loss / self.account_balance) * 100

        setup = pd.DataFrame({
            'Metric': ['Recommended Lot Size', 'Profit Target (Points/Pips)', 'Stop Loss (Points/Pips)', 'Risk Percentage (%)'],
            'Value': [round(lot_size, 2), round(profit_target_points, 2), round(stop_loss_points, 2), round(risk_percentage, 2)]
        })
        return setup, risk_percentage

    def plot_risk_pie(self, risk_percentage):
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

    def plot_profit_loss(self, setup):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['Profit Target', 'Stop Loss'], [setup.loc[1, 'Value'], setup.loc[2, 'Value']], color=['#FFD700', '#444444'])
        ax.set_title('Profit vs Loss (Points/Pips)', color='white')
        ax.set_ylabel('Points/Pips', color='white')
        ax.tick_params(colors='white')
        fig.patch.set_alpha(0)
        st.pyplot(fig)

# User Inputs
account_balance = st.number_input('Account Balance (€)', value=10000.0)
instrument = st.selectbox('Select Instrument', list(pip_values.keys()))
desired_profit = st.number_input('Desired Profit (€)', value=500.0)
permitted_loss = st.number_input('Permitted Loss (€)', value=70.0)
stop_loss_points = st.number_input('Desired Stop Loss (Points/Pips)', value=50.0)

# Calculator
calculator = TradeCalculator(account_balance, instrument, desired_profit, permitted_loss)
setup, risk_percentage = calculator.recommended_setup(stop_loss_points)

st.write(f'## Recommended Trade Setup for {instrument}:')
st.write(setup)

calculator.plot_risk_pie(risk_percentage)
calculator.plot_profit_loss(setup)
