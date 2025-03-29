
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Pip/Point values for different instruments (per standard lot, 1 lot)
pip_values = {
    'US100': 1, 'US500': 1, 'XAUUSD': 10,
    'EURUSD': 10, 'GBPUSD': 10, 'USDJPY': 10, 'USDCAD': 10,
    'AUDUSD': 10, 'NZDUSD': 10,
    'BTCUSD': 100, 'ETHUSD': 10, 'SOLUSD': 1, 'DOGEUSD': 1
}

class TradeCalculator:
    def __init__(self, instrument, desired_profit, permitted_loss):
        self.instrument = instrument
        self.desired_profit = desired_profit
        self.permitted_loss = permitted_loss
        self.pip_value = pip_values[instrument]

    def calculate_pips(self, amount):
        return amount / self.pip_value

    def calculate_lot_size(self):
        return abs(self.permitted_loss / self.pip_value)

    def recommended_setup(self):
        lot_size = self.calculate_lot_size()
        profit_pips = self.calculate_pips(self.desired_profit)
        loss_pips = self.calculate_pips(self.permitted_loss)

        setup = pd.DataFrame({
            'Metric': ['Lot Size', 'Profit Target (Pips)', 'Stop Loss (Pips)'],
            'Value': [round(lot_size, 2), round(profit_pips, 2), round(loss_pips, 2)]
        })
        return setup

    def plot_trade_setup(self, setup):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(setup['Metric'], setup['Value'], color=['purple', 'green', 'red'])
        ax.set_title(f'Trade Setup for {self.instrument}')
        ax.set_ylabel('Values (Lot Size or Pips)')
        st.pyplot(fig)

# Streamlit App
st.title('Trade Profit and Loss Calculator')

instrument = st.selectbox('Select Instrument', list(pip_values.keys()))
desired_profit = st.number_input('Desired Profit (€)', value=500.0)
permitted_loss = st.number_input('Permitted Loss (€)', value=250.0)

calculator = TradeCalculator(instrument, desired_profit, permitted_loss)
setup = calculator.recommended_setup()

st.write(f'## Recommended Trade Setup for {instrument}:')
st.write(setup)

calculator.plot_trade_setup(setup)
