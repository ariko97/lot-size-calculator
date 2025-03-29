import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import requests

# Custom background and styling
st.markdown('''
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
''', unsafe_allow_html=True)

# Function to fetch current price from CoinGecko
@st.cache_data

def get_crypto_price(crypto):
    url = f'https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd'
    try:
        response = requests.get(url).json()
        return response[crypto]['usd']
    except:
        return None

# Pip/Point values per instrument
pip_values = {
    'US100': 1, 'US500': 1, 'XAUUSD': 10,
    'EURUSD': 10, 'GBPUSD': 10, 'USDJPY': 10, 'USDCAD': 10,
    'AUDUSD': 10, 'NZDUSD': 10
}

crypto_assets = ['bitcoin', 'ethereum', 'solana', 'dogecoin']

class TradeCalculator:
    def __init__(self, account_balance, instrument, desired_profit, permitted_loss, pip_value):
        self.account_balance = account_balance
        self.instrument = instrument
        self.desired_profit = desired_profit
        self.permitted_loss = permitted_loss
        self.pip_value = pip_value

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
        st.pyplot(fig)

    def plot_profit_loss(self, setup):
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(['Profit Target', 'Stop Loss'], [setup.loc[1, 'Value'], setup.loc[2, 'Value']], color=['#FFD700', '#444444'])
        ax.set_title('Profit vs Loss (Points/Pips)', color='white')
        ax.set_ylabel('Points/Pips', color='white')
        st.pyplot(fig)

account_balance = st.number_input('Account Balance or Daily Loss Balance (€)', value=10000.0)
instrument = st.selectbox('Select Instrument', list(pip_values.keys()) + crypto_assets)
desired_profit = st.number_input('Desired Profit (€)', value=500.0)
permitted_loss = st.number_input('Permitted Loss (€)', value=70.0)
stop_loss_points = st.number_input('Desired Stop Loss (Points/Pips)', value=50.0)

# Fetch pip value based on instrument
if instrument in pip_values:
    pip_value = pip_values[instrument]
elif instrument == 'bitcoin':
    pip_value = get_crypto_price('bitcoin')
elif instrument == 'ethereum':
    pip_value = get_crypto_price('ethereum')
elif instrument == 'solana':
    sol_price = get_crypto_price('solana')
    pip_value = sol_price / 1000 if sol_price else 1  # 1 pip = 0.001
elif instrument == 'dogecoin':
    doge_price = get_crypto_price('dogecoin')
    pip_value = doge_price / 10000 if doge_price else 1  # 1 pip = 0.0001

if pip_value:
    calculator = TradeCalculator(account_balance, instrument, desired_profit, permitted_loss, pip_value)
    setup, risk_percentage = calculator.recommended_setup(stop_loss_points)

    st.write(f'## Recommended Trade Setup for {instrument}:')
    st.write(setup)

    calculator.plot_risk_pie(risk_percentage)
    calculator.plot_profit_loss(setup)

else:
    st.write('Unable to fetch the pip value. Please try again later.')
