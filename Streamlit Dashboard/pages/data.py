import pandas
import streamlit as st
import pandas as pd
import numpy as np

st.title('Very Important Data')
DATE_COLUMN = 'date/time'
data = ('vending_machine_sales.csv')

#Load data
data_load_state = st.text('Loading data...')
data_load_state.text('Loading data...done!')
st.subheader('Raw data')
df = pd.read_csv(data)
st.write(df)

size = print('the size of the data is ' + str(df.shape))
st.write(size)


st.subheader('Products Sold (Annual)')
sales = df['Product'].value_counts()
sales



