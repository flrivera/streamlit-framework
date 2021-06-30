import requests
import json 
import streamlit as st
import datetime as dt
from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import numpy as np
import os
from Month_dict import month_dict
from dotenv import load_dotenv
from urllib.error import URLError
import SessionState


state = SessionState.get(chat_list=[])

load_dotenv() # load my enviornment variables

API_key=os.getenv('API_key')


st.title('TDI-Milestone')

outputsize='full'


st.sidebar.header("Configuration")


ticker = st.sidebar.text_input('Stock-Ticker') # make selectbox with time 



year_options= np.linspace(1999,2021,22)
year_options=[int(year) for year in year_options]

Year = st.sidebar.selectbox('What year would you like data for?',options=year_options)

if Year==2021:
    
   
    month_options=['January','February','March','April','May','June']

    Month = st.sidebar.selectbox(f'What month would you like data for?',options=month_options)
else:
    


    month_options=['January','February','March','April','May','June','July','August',
               'September','October','November','December']

    Month = st.sidebar.selectbox(f'What month would you like data for?',options=month_options)

Month_index=month_dict[f'{Month}']


if st.sidebar.button("Post Stock Info"):
    state.chat_list.append((ticker, Year, Month))
    
if len(state.chat_list) > 10:
    del (state.chat_list[0])

    
try:
    ticker,Year,Month = zip(*state.chat_list)
    
    ts=TimeSeries(f'{API_key}',output_format='pandas')
    
    try:

        aapl,metadata=ts.get_daily_adjusted(symbol=ticker,outputsize=outputsize)
        aapl2,metadata2=ts.get_daily(symbol=ticker,outputsize=outputsize)
    except ValueError:
        
        st.title("Incorrect Stock Ticker") 
    
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




    st.write(alt.Chart(source,title=f'{str(ticker[0])} daily closing values USD for {str(Month[0])} of {str(Year[0])}').mark_line(point=True).encode(
        alt.Y('Closing Value USD', scale=alt.Scale(zero=False)), x='Day'))
    
except ValueError:
    st.title("Enter the Stock , Year, and Month you want to be shown, then click post!")    

