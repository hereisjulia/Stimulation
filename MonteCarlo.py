import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from datetime import datetime, timedelta


tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NFLX', 'VTI', 'SPY', 'JNJ', 'KO', 'XLK', 'XLF']
Close = pd.DataFrame()
start_date = datetime(2010,1,1).date()
end_date = datetime.now().date()
start_date_rf = end_date - timedelta(days=365)

IRX = yf.download('^IRX', start= start_date_rf, end = end_date)
rf = IRX['Close'].pct_change().dropna().mean()

for ticker in tickers:
    Close[ticker] = yf.download(ticker, start= start_date, end= end_date)['Close']

print(Close.describe())

plt.plot(Close.index, Close)
plt.title('Stock close price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(Close, fontsize='small', loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()



Return = Close.pct_change()
Return = Return.dropna()
print(Return.describe())

plt.plot(Return.index, Return)
plt.title('Stock Daily Return')
plt.xlabel('Date')
plt.ylabel('Return')
plt.legend(Return, title = "Ticker", fontsize='small', loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()



mean_sd_return = pd.DataFrame({'mean': Return.mean(), 'std': Return.std()}).T
mat_cor = Return.corr()

plt.figure(figsize= (5, 3))
sns.heatmap(mat_cor, annot = True, cmap = 'coolwarm', fmt=".2f", annot_kws={"size": 6})
plt.title('Correlation Heatmap')
plt.show()


T = (Return.index.max() - Return.index.min()).days
n_simulation = 2000

simulation_output = {'weights': [], 'sharpe': [], 'perform': {'return': [], 'std': []}}

for i in range(0, n_simulation):

    weights = np.random.random(len(Return.columns))
    weights /= np.sum(weights)

    wtRet = (Return * weights).sum(axis=1)
    
    sharpe = (wtRet.mean() - rf) / wtRet.std()

    simulation_output['weights'].append(weights)
    simulation_output['sharpe'].append(sharpe)
    simulation_output['perform']['return'].append(wtRet.mean())
    simulation_output['perform']['std'].append(wtRet.std())

simulation_output['weights'] = pd.DataFrame(simulation_output['weights'])
perform = pd.DataFrame(simulation_output['perform'])


plt.title('Simulations')
plt.xlabel('STD')
plt.ylabel('Return')
plt.scatter(x = perform['std'], y = perform['return'])
plt.show()

maxSharpe_index = np.argmax(simulation_output['sharpe'])
maxSharpe_weights = simulation_output['weights'].iloc[maxSharpe_index]
maxSharpe_weights = pd.DataFrame({'ticker': tickers, 'weight': maxSharpe_weights})
maxSharpe_perform = perform.iloc[maxSharpe_index]


print([maxSharpe_weights, maxSharpe_perform])
