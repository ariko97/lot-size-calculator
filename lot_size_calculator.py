import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Set Streamlit background
st.markdown(
    """
    <style>
    .reportview-container {
        background: #222222;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
        stop_loss_points = st.number_input('Enter Desired Stop Loss (Points/Pips)', value=50.0)
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
            colors=['yellow', 'black'],
            autopct='%1.1f%%',
            pctdistance=0.75,
            textprops=dict(color='white', fontsize=14)
        )
        for text in texts:
            text.set_color('black')
        ax.set_title('Account Risk Ratio', color='white')
        st.pyplot(fig)

    def plot_profit_loss(self, setup):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['Profit Target', 'Stop Loss'], [setup.loc[1, 'Value'], setup.loc[2, 'Value']], color=['yellow', 'black'])
        ax.set_title('Profit vs Loss (Points/Pips)', color='white')
        ax.set_ylabel('Points/Pips', color='white')
        ax.tick_params(colors='white')
        fig.patch.set_facecolor('#222222')
        ax.set_facecolor('#222222')
        st.pyplot(fig)

# Streamlit App
st.markdown('<p style="color:pink; font-size:12px;">Made by Ariko with Love</p>', unsafe_allow_html=True)
st.title('Trade Profit and Loss Calculator with Risk Management')

account_balance = st.number_input('Account Balance (€)', value=10000.0)
instrument = st.selectbox('Select Instrument', list(pip_values.keys()))
desired_profit = st.number_input('Desired Profit (€)', value=500.0)
permitted_loss = st.number_input('Permitted Loss (€)', value=70.0)

calculator = TradeCalculator(account_balance, instrument, desired_profit, permitted_loss)
setup, risk_percentage = calculator.recommended_setup()

st.write(f'## Recommended Trade Setup for {instrument}:')
st.write(setup)

st.write('### Account Risk Ratio')
calculator.plot_risk_pie(risk_percentage)

st.write('### Profit vs Loss')
calculator.plot_profit_loss(setup)
