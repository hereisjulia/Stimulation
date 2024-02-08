import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NFLX', 'VTI', 'SPY', 'JNJ', 'KO', 'XLK', 'XLF']
Close = pd.DataFrame()
start_date = '2021-01-01'

for ticker in tickers:
    Close[ticker] = yf.download(ticker, start= start_date, end='2024-12-31')['Close']

print(Close.describe())

plt.plot(Close.index, Close)
plt.title('Stock close price')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(Close, fontsize='small', loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()



Return = Close.pct_change()
print(Return.describe())
Return = Return.dropna()

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
n_simulation = 20000

simulation_output = {'weights': [], 'perform': {'return': [], 'std': []}}

for i in range(0, n_simulation):

    weights = np.random.random(len(Return.columns))
    weights /= np.sum(weights)

    wtRet = (Return * weights).sum(axis=1)

    simulation_output['weights'].append(weights)
    simulation_output['perform']['return'].append(wtRet.mean())
    simulation_output['perform']['std'].append(wtRet.std())

simulation_output['weights'] = pd.DataFrame(simulation_output['weights'])
simulation_output['weights'].columns = tickers
perform = pd.concat([simulation_output['weights'],
                     pd.DataFrame(simulation_output['perform'])], axis = 1)


plt.title('Simulations')
plt.xlabel('Return')
plt.ylabel('STD')
plt.scatter(perform['std'], perform['return'])
plt.show()


