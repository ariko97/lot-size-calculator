import pandas as pd
import streamlit as st
import plotly.express as px

# Custom background and styling
st.markdown("""
<style>
.stApp {
    background-image: url('https://raw.githubusercontent.com/ariko97/lot-size-calculator/main/background.png');
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #FFFFFF;
}
[data-testid="stNumberInput"], [data-testid="stSelectbox"] {
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 10px;
    padding: 5px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p style="color:pink; font-size:12px;">Made by Ariko with Love 💖</p>', unsafe_allow_html=True)

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

    def recommended_setup(self):
        stop_loss_points = st.number_input('Desired Stop Loss (Points/Pips)', value=50.0)
        lot_size = self.calculate_lot_size(stop_loss_points)
        profit_target_points = (self.desired_profit / self.permitted_loss) * stop_loss_points
        risk_percentage = (self.permitted_loss / self.account_balance) * 100

        setup = pd.DataFrame({
            'Metric': ['Lot Size', 'Profit Target', 'Stop Loss', 'Risk %'],
            'Value': [round(lot_size, 2), round(profit_target_points, 2), round(stop_loss_points, 2), round(risk_percentage, 2)]
        })
        return setup, risk_percentage

    def plot_risk_pie(self, risk_percentage):
        fig = px.pie(
            names=['Risk (%)', 'Remaining Balance (%)'],
            values=[risk_percentage, 100 - risk_percentage],
            color_discrete_sequence=['#FF6361', '#58508D'],
            hole=0.4,
            title='Account Risk Ratio'
        )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')
        st.plotly_chart(fig)

    def plot_profit_loss(self, setup):
        fig = px.bar(
            setup.iloc[1:3], x='Metric', y='Value',
            color='Metric', color_discrete_sequence=['#FFA600', '#BC5090'],
            title='Profit vs. Loss (Points/Pips)'
        )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', showlegend=False)
        st.plotly_chart(fig)

# Streamlit App
st.title('📈 Trade Calculator with Risk Management')

account_balance = st.number_input('Account Balance (€)', value=10000.0)
instrument = st.selectbox('Instrument', list(pip_values.keys()))
desired_profit = st.number_input('Desired Profit (€)', value=500.0)
permitted_loss = st.number_input('Permitted Loss (€)', value=70.0)

calculator = TradeCalculator(account_balance, instrument, desired_profit, permitted_loss)
setup, risk_percentage = calculator.recommended_setup()

st.subheader(f'Recommended Setup for {instrument}:')
st.dataframe(setup, hide_index=True, use_container_width=True)

calculator.plot_risk_pie(risk_percentage)
calculator.plot_profit_loss(setup)
