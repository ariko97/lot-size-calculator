

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Correct Pip/Point values per instrument (value per 1 lot, per point/pip move)
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

    def recommended_setup(self):
        # Suggesting realistic stop loss (points/pips)
        stop_loss_points = st.number_input('Enter Desired Stop Loss (Points/Pips)', value=50.0)
        lot_size = self.calculate_lot_size(stop_loss_points)
        profit_target_points = (self.desired_profit / self.permitted_loss) * stop_loss_points
        risk_percentage = (self.permitted_loss / self.account_balance) * 100

        setup = pd.DataFrame({
            'Metric': ['Recommended Lot Size', 'Profit Target (Points/Pips)', 'Stop Loss (Points/Pips)', 'Risk Percentage (%)'],
            'Value': [round(lot_size, 2), round(profit_target_points, 2), round(stop_loss_points, 2), round(risk_percentage, 2)]
        })
        return setup

    def plot_trade_setup(self, setup):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(setup['Metric'], setup['Value'], color=['purple', 'green', 'red', 'blue'])
        ax.set_title(f'Trade Setup for {self.instrument}')
        ax.set_ylabel('Values')
        st.pyplot(fig)

# Streamlit App
st.title('Trade Profit and Loss Calculator with Realistic Risk Management')

account_balance = st.number_input('Account Balance (€)', value=10000.0)
instrument = st.selectbox('Select Instrument', list(pip_values.keys()))
desired_profit = st.number_input('Desired Profit (€)', value=500.0)
permitted_loss = st.number_input('Permitted Loss (€)', value=70.0)

calculator = TradeCalculator(account_balance, instrument, desired_profit, permitted_loss)
setup = calculator.recommended_setup()

st.write(f'## Recommended Trade Setup for {instrument}:')
st.write(setup)

calculator.plot_trade_setup(setup)
