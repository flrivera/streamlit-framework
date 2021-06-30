import requests
import json 
import streamlit as st
import datetime as dt
from alpha_vantage.timeseries import TimeSeries
from bokeh.io import output_file, show
from bokeh.plotting import figure
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import numpy as np
import os
from Month_dict import month_dict
from dotenv import load_dotenv
from urllib.error import URLError


load_dotenv() # load my enviornment variables

API_key=os.getenv('API_key')


st.title('TDI-Milestone')

outputsize='full'


st.sidebar.header("Configuration")


ticker = st.sidebar.text_input('Stock-Ticker') # make selectbox with time 

#ticker=f'{ticker}'

year_options= np.linspace(1999,2021,22)
year_options=[int(year) for year in year_options]
#Year=st.multiselect(year_label, year_options)
Year = st.sidebar.selectbox('What year would you like data for?',options=year_options)

if Year==2021:
    
    #month_label='What month would you like data for?'
    month_options=['January','February','March','April','May','June']
#index=st.multiselect(month_label, month_options)
#Month=month_dict[f'index']
    Month = st.sidebar.selectbox(f'What month would you like data for?',options=month_options)
else:
    

#month_label='What month would you like data for?'
    month_options=['January','February','March','April','May','June','July','August',
               'September','October','November','December']
#index=st.multiselect(month_label, month_options)
#Month=month_dict[f'index']
    Month = st.sidebar.selectbox(f'What month would you like data for?',options=month_options)

Month_index=month_dict[f'{Month}']
#ticker = input('Ticker:  ')
#typ= input ('Data type-  "daily",  "weekly",   "monthly", "interval" :   ')

ts=TimeSeries(f'{API_key}',output_format='pandas')

aapl,metadata=ts.get_daily_adjusted(symbol=ticker,outputsize=outputsize)
aapl2,metadata2=ts.get_daily(symbol=ticker,outputsize=outputsize)

include=aapl[aapl.index.year==Year]
iinclude=aapl2[aapl2.index.year==Year]

include2=include[include.index.month==Month_index]
iinclude2=iinclude[iinclude.index.month==Month_index]

A=include2['4. close'].astype(float)
B=iinclude2['4. close'].astype(float)

A=pd.DataFrame(A)

jo=np.array(A['4. close'])

A['Date']=(A.index.day).astype(float)

jo_x=np.array(A['Date'])


B=pd.DataFrame(B)

B['Date']=(B.index.day).astype(float)


source = pd.DataFrame({
  'Day': jo_x,
  'Closing Value USD': jo
})




st.write(alt.Chart(source).mark_line(point=True).encode(
    alt.Y('Closing Value USD', scale=alt.Scale(zero=False)), x='Day'))

