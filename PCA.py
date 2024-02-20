
import numpy as np
import pandas as pd
import yfinance as yf
from fredapi import Fred
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


fred = Fred(api_key = '02b2aeac0d19e1d7e68c5a966edceda6')
data = fred.get_series('FEDFUNDS')


TW0050 = [
    '2330.TW', '2454.TW', '2317.TW', '2308.TW', '2303.TW',
    '2382.TW', '2891.TW', '2881.TW', '3711.TW', '2412.TW'
]

SPY = ['MSFT', 'AAPL', 'NVDA', 'AMZN', 'META', 'GOOGL', 'GOOG', 'BRK-B', 'AVGO', 'TSLA']

start_date = datetime(2022,1,1).date()
end_date = datetime.now().date() #datetime.now().date()

#TW50 = {'holdings': TW0050, 'Close' : []}

Close = pd.DataFrame()
for ticker in TW0050:
    Close[ticker] = yf.download(ticker, start= start_date, end= end_date)['Close']

print(Close)
Close.columns

Return = Close.pct_change()
Return = Return.dropna()
print(Return)

matcorr = Return.corr()
plt.figure(figsize = (14,10))
sns.heatmap(matcorr, annot=True, cmap = 'OrRd')
plt.title('Correlation Heatmap')
plt.show()


## Start using PCA
pca = PCA(n_components=2)
pca.fit(Return)

pca.components_
pca.explained_variance_ratio_
pca.transform(Return)











