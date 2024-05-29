import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts

import json
import numpy as np
# import yfinance as yf
import pandas as pd
import pandas_ta as ta
from pathlib import Path

file_path = Path(__file__).resolve().parents[0]/'data'
ticker = 'CU'
timeframe = '1min'
filetype = 'parquet'
files = sorted(list(file_path.glob(f'{ticker}*{timeframe}*.{filetype}')))

dfs = [pd.read_parquet(file) for file in files]
df = pd.concat(dfs).reset_index(drop=True) # for some version of pandas maybe, this is line essential

COLOR_BULL = 'rgba(38,166,154,0.9)' # #26a69a
COLOR_BEAR = 'rgba(239,83,80,0.9)'  # #ef5350

# Request historic pricing data via finance.yahoo.com API

# Some data wrangling to match required format
# df = df.reset_index()
# df.columns = ['time','open','high','low','close','volume']                  # rename columns
# df['time'] = df['time'].dt.strftime('%Y-%m-%d')                             # Date to string
df['color'] = np.where(  df['open'] > df['close'], COLOR_BEAR, COLOR_BULL)  # bull or bear
df.ta.macd(close='close', fast=6, slow=12, signal=5, append=True)           # calculate macd

# export to JSON format
candles = json.loads(df.to_json(orient = "records"))
volume = json.loads(df.rename(columns={"volume": "value",}).to_json(orient = "records"))
macd_fast = json.loads(df.rename(columns={"MACDh_6_12_5": "value"}).to_json(orient = "records"))
macd_slow = json.loads(df.rename(columns={"MACDs_6_12_5": "value"}).to_json(orient = "records"))
df['color'] = np.where(  df['MACD_6_12_5'] > 0, COLOR_BULL, COLOR_BEAR)  # MACD histogram color
macd_hist = json.loads(df.rename(columns={"MACD_6_12_5": "value"}).to_json(orient = "records"))

st.sidebar.title('Trading Statistics')
# Slider for width
width = st.sidebar.slider('Chart Width', min_value=1000, max_value=2000, value=1600, step=100)
st.write('Selected chart width:', width)

# Slider for height
height = st.sidebar.slider('Chart Height', min_value=200, max_value=600, value=400, step=50)
st.write('Selected chart height:', height)

# Checkbox for watermark visibility
watermark_visible = st.sidebar.checkbox('Watermark Visible', value=True)
st.write('Watermark visible:', watermark_visible)

# Slider for watermark font size
watermark_font_size = st.sidebar.slider('Watermark Font Size', min_value=10, max_value=100, value=48, step=2)
st.write('Selected watermark font size:', watermark_font_size)


st.sidebar.info('This app is a simple example of using Streamlit to create a trading dashboard.')

# You can also use markdown
st.sidebar.markdown('## Some Useful Links')
st.sidebar.markdown('[Streamlit Documentation](https://docs.streamlit.io/en/stable/)')

# Or even output dataframes
st.sidebar.markdown('## DataFrame Head')
st.sidebar.dataframe(df.head())


# Create a selectbox for the tabs
tab = st.selectbox('Choose a tab', ['Tab 1', 'Tab 2', 'Tab 3'])

# Display the selected tab content
if tab == 'Tab 1':
    st.write('You selected Tab 1.')
    # Add the content for Tab 1 here
elif tab == 'Tab 2':
    st.write('You selected Tab 2.')
    # Add the content for Tab 2 here
else:
    st.write('You selected Tab 3.')
    # Add the content for Tab 3 here

chartMultipaneOptions = [
    {
    "width": width,
    "height": height,
    "watermark": {
        "visible": watermark_visible,
        "fontSize": watermark_font_size,
    },  
    },
    {
        "width": 1600,
        "height": 400,
        "layout": {
            "background": {
                "type": "solid",
                "color": 'white'
                # "color":'black'
            },
            "textColor": "black"
        },
        "grid": {
            "vertLines": {
                "color": "rgba(197, 203, 206, 0.5)"
                },
            "horzLines": {
                "color": "rgba(197, 203, 206, 0.5)"
            }
        },
        "crosshair": {
            "mode": 0
        },
        "priceScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)"
        },
        "timeScale": {
            "borderColor": "rgba(197, 203, 206, 0.8)",
            "barSpacing": 15
        },
        "watermark": {
            "visible": True,
            "fontSize": 48,
            "horzAlign": 'center',
            "vertAlign": 'center',
            "color": 'rgba(171, 71, 188, 0.3)',
            "text": ticker + ' ' + timeframe,
        }
    },
    {
        "width": 1600,
        "height": 100,
        "layout": {
            "background": {
                "type": 'solid',
                "color": 'transparent'
            },
            "textColor": 'black',
        },
        "grid": {
            "vertLines": {
                "color": 'rgba(42, 46, 57, 0)',
            },
            "horzLines": {
                "color": 'rgba(42, 46, 57, 0.6)',
            }
        },
        "timeScale": {
            "visible": False,
        },
        "watermark": {
            "visible": True,
            "fontSize": 18,
            "horzAlign": 'left',
            "vertAlign": 'top',
            "color": 'rgba(171, 71, 188, 0.7)',
            "text": 'Volume',
        }
    },
    {
        "width": 1600,
        "height": 200,
        "layout": {
            "background": {
                "type": "solid",
                "color": 'white'
            },
            "textColor": "black"
        },
        "timeScale": {
            "visible": False,
        },
        "watermark": {
            "visible": True,
            "fontSize": 18,
            "horzAlign": 'left',
            "vertAlign": 'center',
            "color": 'rgba(171, 71, 188, 0.7)',
            "text": 'MACD',
        }
    }
]

seriesCandlestickChart = [
    {
        "type": 'Candlestick',
        "data": candles,
        "options": {
            "upColor": COLOR_BULL,
            "downColor": COLOR_BEAR,
            "borderVisible": False,
            "wickUpColor": COLOR_BULL,
            "wickDownColor": COLOR_BEAR
        }
    }
]

seriesVolumeChart = [
    {
        "type": 'Histogram',
        "data": volume,
        "options": {
            "priceFormat": {
                "type": 'volume',
            },
            "priceScaleId": "" # set as an overlay setting,
        },
        "priceScale": {
            "scaleMargins": {
                "top": 0,
                "bottom": 0,
            },
            "alignLabels": False
        }
    }
]

seriesMACDchart = [
    {
        "type": 'Line',
        "data": macd_fast,
        "options": {
            "color": 'blue',
            "lineWidth": 2
        }
    },
    {
        "type": 'Line',
        "data": macd_slow,
        "options": {
            "color": 'green',
            "lineWidth": 2
        }
    },
    {
        "type": 'Histogram',
        "data": macd_hist,
        "options": {
            "color": 'red',
            "lineWidth": 1
        }
    }
]

st.subheader("Quotes")

renderLightweightCharts([
    {
        "chart": chartMultipaneOptions[0],
        "series": seriesCandlestickChart
    },
    {
        "chart": chartMultipaneOptions[1],
        "series": seriesVolumeChart
    },
    {
        "chart": chartMultipaneOptions[2],
        "series": seriesMACDchart
    }
], 'multipane') #type:ignore
