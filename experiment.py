"""
Charting financial data using trading_view library 
"""
from time import sleep
import pandas as pd 
from lightweight_charts import Chart 
from pathlib import Path

if __name__ == '__main__':
    chart = Chart()
    # df0 = pd.read_csv('./BashBoard/cu2404.20240222.csv')
    # df = pd.read_csv('./DashBoard/cu2404.20240222.csv')
    
    file_path = Path(__file__).resolve().parents[0]/'data'
    ticker = 'CU'
    timeframe = '1min'
    filetype = 'parquet'
    files = sorted(list(file_path.glob(f'{ticker}*{timeframe}*.{filetype}')))
    
    dfs = [pd.read_parquet(file) for file in files]
    df = pd.concat(dfs)
    df0 = df.iloc[0:10, :]
    df1 = df.iloc[11:, :]
    # df['time'] = df['market_time']
    chart.set(df0)
    chart.show()
    # chart.show(block=True)
    for i, series in df1.iterrows():
        chart.update(series)
        last_close = series['close']
        sleep(0.1)
        