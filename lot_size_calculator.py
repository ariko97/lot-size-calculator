
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Pip/Point values for different instruments (per standard lot, 1 lot)
pip_values = {
    'US100': 1,  # NASDAQ 100 - 1 point = $1 per lot
    'US500': 1,  # S&P 500 - 1 point = $1 per lot
    'XAUUSD': 10,  # Gold - 1 pip = $10 per lot (e.g., 2018 to 2019 is 1 pip)
    'EURUSD': 10,  # Forex Major - 1 pip = $10 per lot (0.0001 change)
    'GBPUSD': 10,
    'USDJPY': 10,
    'USDCAD': 10,
    'AUDUSD': 10,
    'NZDUSD': 10,
    'BTCUSD': 100,  # Bitcoin - 1 point = $100 per lot (e.g., 1500 to 1600)
    'ETHUSD': 10,  # Ethereum - 1 point = $10 per lot
    'SOLUSD': 1,  # Solana - 1 point = $1 per lot
    'DOGEUSD': 1  # Dogecoin - 1 point = $1 per lot
}

class LotSizeCalculator:
    def __init__(self, account_balance, per_trade_loss_limit, risk_per_trade_percentage, instrument):
        self.account_balance = account_balance
        self.per_trade_loss_limit = per_trade_loss_limit
        self.risk_per_trade_percentage = risk_per_trade_percentage
        self.instrument = instrument
        self.pip_value = pip_values[instrument]

    def calculate_risk_per_trade(self):
        return self.per_trade_loss_limit * (self.risk_per_trade_percentage / 100)

    def calculate_lot_size(self):
        risk_per_trade = self.calculate_risk_per_trade()
        return abs(risk_per_trade / self.pip_value)
    
    def display_lot_sizes(self):
        standard_lot_size = self.calculate_lot_size()
        aggressive_lot_size = standard_lot_size * 1.5
        reduced_lot_size = standard_lot_size * 0.5

        lot_sizes = pd.DataFrame({
            'Risk Level': ['Standard', 'Aggressive', 'Reduced'],
            'Lot Size': [standard_lot_size, aggressive_lot_size, reduced_lot_size]
        })

        return lot_sizes

    def plot_lot_sizes(self, lot_sizes):
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(lot_sizes['Risk Level'], lot_sizes['Lot Size'], color=['blue', 'green', 'red'])
        ax.set_title(f'Lot Size Comparison for {self.instrument}')
        ax.set_xlabel('Risk Level')
        ax.set_ylabel('Lot Size')
        st.pyplot(fig)

# Streamlit App
st.title('Per Trade Permitted Loss Calculator Tool')

account_balance = st.number_input('Account Balance (€)', value=10129.0)
per_trade_loss_limit = st.number_input('Per Trade Permitted Loss (€)', value=500.0)
risk_per_trade_percentage = st.number_input('Risk Per Trade (%)', value=2.0)
instrument = st.selectbox('Select Instrument', list(pip_values.keys()))

calculator = LotSizeCalculator(account_balance, per_trade_loss_limit, risk_per_trade_percentage, instrument)
lot_sizes = calculator.display_lot_sizes()

st.write(f'## Lot Sizes for {instrument}:')
st.write(lot_sizes)

calculator.plot_lot_sizes(lot_sizes)
