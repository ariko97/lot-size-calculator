
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Pip values for different instruments (per standard lot, 1 lot)
pip_values = {
    'US100': 1,  # NASDAQ 100 (0.01 pip = $1 for 1 lot)
    'XAUUSD': 10,  # Gold (0.01 pip = $10 for 1 lot)
    'EURUSD': 10,  # Forex Major (0.0001 pip = $10 for 1 lot)
    'GBPUSD': 10,
    'USDJPY': 10,
    'USDCAD': 10,
    'AUDUSD': 10,
    'NZDUSD': 10,
    'BTCUSD': 1,  # Bitcoin (0.01 move = $1)
    'ETHUSD': 1,  # Ethereum (0.01 move = $1)
    'SOLUSD': 1,  # Solana (0.01 move = $1)
    'DOGEUSD': 1  # Dogecoin (0.0001 move = $1)
}

class LotSizeCalculator:
    def __init__(self, account_balance, daily_loss_limit, risk_per_trade_percentage, instrument):
        self.account_balance = account_balance
        self.daily_loss_limit = daily_loss_limit
        self.risk_per_trade_percentage = risk_per_trade_percentage
        self.instrument = instrument
        self.pip_value = pip_values[instrument]

    def calculate_risk_per_trade(self):
        return self.daily_loss_limit * (self.risk_per_trade_percentage / 100)

    def calculate_lot_size(self, average_loss):
        risk_per_trade = self.calculate_risk_per_trade()
        if average_loss == 0:
            return 0
        return abs(risk_per_trade / (average_loss / self.pip_value))
    
    def display_lot_sizes(self, average_loss):
        standard_lot_size = self.calculate_lot_size(average_loss)
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
st.title('Lot Size Calculator Tool')

account_balance = st.number_input('Account Balance (€)', value=10129.0)
daily_loss_limit = st.number_input('Daily Permitted Loss (€)', value=500.0)
risk_per_trade_percentage = st.number_input('Risk Per Trade (%)', value=2.0)
average_loss = st.number_input('Average Loss Per Trade (€)', value=18.79)
instrument = st.selectbox('Select Instrument', list(pip_values.keys()))

calculator = LotSizeCalculator(account_balance, daily_loss_limit, risk_per_trade_percentage, instrument)
lot_sizes = calculator.display_lot_sizes(average_loss)

st.write(f'## Lot Sizes for {instrument}:')
st.write(lot_sizes)

calculator.plot_lot_sizes(lot_sizes)
