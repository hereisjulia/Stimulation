import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.title("Monte Carlo on Stocks")

st.header("Choose tickers!")
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NFLX', 'VTI', 'SPY', 'JNJ', 'KO', 'XLK', 'XLF']

selected_tickers = st.multiselect("Tickers:",tickers)

start_date = '2021-01-01'

Close = pd.DataFrame()
for ticker in selected_tickers:
    Close[ticker] = yf.download(ticker, start= start_date, end='2024-12-31')['Close']

#st!
st.write('Price')
st.line_chart(Close)

Return = Close.pct_change()
print(Return.describe())
Return = Return.dropna()

# st!
st.write('Returns')
st.line_chart(Return)


mean_sd_return = pd.DataFrame({'mean': Return.mean(), 'std': Return.std()}).T
mat_cor = Return.corr()

plt.figure(figsize= (5, 3))
sns.heatmap(mat_cor, annot = True, cmap = 'coolwarm', fmt=".2f", annot_kws={"size": 6})
plt.title('Correlation Heatmap')
plt.show()

# st!
st.write('Correlation Map')
fig1, ax1 = plt.subplots()
sns.heatmap(mat_cor, annot = True, cmap = 'coolwarm', fmt=".2f", annot_kws={"size": 6}, ax=ax1)
plt.title('Correlation Heatmap')
fig1.set_facecolor('black')
ax1.tick_params(colors='white', which='both')  # 'both' refers to minor and major axes
st.write(fig1)

T = (Return.index.max() - Return.index.min()).days


st.header('Select number of Simulation')
n_simulation = st.slider('Number of Simulation', 1000, 20000)
button2 = st.button('Start Stimulating!')

simulation_output = {'weights': [], 'perform': {'return': [], 'std': []}}

if button2:
    for i in range(0, n_simulation):

        weights = np.random.random(Return.shape[1])
        weights /= np.sum(weights)

        wtRet = (Return * weights).sum(axis=1)

        simulation_output['weights'].append(weights)
        simulation_output['perform']['return'].append(wtRet.mean())
        simulation_output['perform']['std'].append(wtRet.std())

    simulation_output['weights'] = pd.DataFrame(simulation_output['weights'])
    perform = pd.DataFrame(simulation_output['perform'])
    st.write('Stimulation Scatter Plot')
    st.scatter_chart(perform, x = 'std', y = 'return')




