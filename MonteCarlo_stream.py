import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from datetime import datetime, timedelta

st.title("Monte Carlo on Stocks")

st.header("Choose tickers!")
tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NFLX', 'VTI', 'SPY', 'JNJ', 'KO', 'XLK', 'XLF']

selected_tickers = st.multiselect("Tickers:",tickers)

start_date = datetime(2010,1,1).date()
end_date = datetime.now().date()
start_date_rf = end_date - timedelta(days=365)

IRX = yf.download('^IRX', start= start_date_rf, end = end_date)
rf = IRX['Close'].pct_change().dropna().mean()


Close = pd.DataFrame()
for ticker in selected_tickers:
    Close[ticker] = yf.download(ticker, start= start_date, end= end_date)['Close']

Return = Close.pct_change()
print(Return.describe())
Return = Return.dropna()

mean_sd_return = pd.DataFrame({'Daily Return': Return.mean(), 'std': Return.std()}).T
mat_cor = Return.corr()

#st!
st.write('Price')
st.line_chart(Close)

# st!
st.write('Returns')
st.line_chart(Return)

# st!
st.write('Performance: mean return and standard deviation')
st.table(mean_sd_return)


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

simulation_output = {'weights': [], 'sharpe': [], 'perform': {'return': [], 'std': []}}

if button2:
    for i in range(0, n_simulation):

        weights = np.random.random(Return.shape[1])
        weights /= np.sum(weights)

        wtRet = (Return * weights).sum(axis=1)
        
        sharpe = (wtRet.mean() - rf) / wtRet.std()

        simulation_output['weights'].append(weights)
        simulation_output['sharpe'].append(sharpe)
        simulation_output['perform']['return'].append(wtRet.mean())
        simulation_output['perform']['std'].append(wtRet.std())

    simulation_output['weights'] = pd.DataFrame(simulation_output['weights'])
    perform = pd.DataFrame(simulation_output['perform'])
    st.write('Stimulation Scatter Plot')
    st.scatter_chart(perform, x = 'std', y = 'return')
    
    maxSharpe_index = np.argmax(simulation_output['sharpe'])
    maxSharpe_weights = simulation_output['weights'].iloc[maxSharpe_index]
    maxSharpe_weights = pd.DataFrame({'ticker': selected_tickers, 'weight': maxSharpe_weights})
    maxSharpe_perform = pd.DataFrame(perform.iloc[maxSharpe_index])
    
    st.write('Sharpe Ratios')
    st.bar_chart(simulation_output['sharpe'])
    st.write('Highest Sharpe Ratio:' + str(round(max(simulation_output['sharpe']),4)))
    
    st.write('Performance under highest Sharpe Ratio')
    st.table(maxSharpe_perform)
    
    st.write('Weights for each stock')
    st.bar_chart(maxSharpe_weights, x = 'ticker', y = 'weight')



