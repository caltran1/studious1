"""
# Streamlit Data Dashboard Project
Using Sales Data from Vending Machines
"""

import numpy as np
import pandas as pd
import streamlit as st

from pandas.tseries.offsets import DateOffset

#Basic setup/cleaning
data = ('vending_machine_sales.csv')
df = pd.read_csv(data)
#convert sales to datetime objects
df_datetime = pd.to_datetime(df['TransDate'])
df['TransDate'] = df_datetime

#page setup
st.set_page_config(
    page_title=" Vending Machine Sales Dashboard",
    page_icon="🍫",
    layout="wide",)
st.title('Dashboard Home')

############## Top Bar: At a glance data for last month ##################

# create three columns
kpi1, kpi2, kpi3 = st.columns(3)

## Initialize month ##
#today
today_date = pd.to_datetime('now')
#offset for previous month and grab month # from timestamp object
"""
Note from 10/1/22: The data only runs up to Aug 2022. This dashboard was made in Sept 2022.
Code for correctly getting the previous month will remain, 
but will be hard coded to be August (8) now to demonstrate proper functionality of dashboard.
"""
#prev_month = today_date + DateOffset(months=-1)
#prev_month = prev_month.month
#hard coding previous month to be August as documented above
prev_month = 8

#note this project only has one year of data in it, only looking at the month value as a result
TransMonths = df['TransDate'].dt.month
transmonths_array = TransMonths.to_numpy()

#Revenue last month
#add cleaned column of transaction month to dataframe then filter by month and sum
df['TransMonth'] = pd.DataFrame(TransMonths)
prev_month_df = df[df.TransMonth == prev_month]
prev_month_revenue = prev_month_df['TransTotal'].sum()

#Number of Sales last month
sales = 0
for i in transmonths_array:
    if i == prev_month:
        sales +=1

#Putting these values into the Dashboard
kpi1.metric(
    label="$ Revenue Last Month 💵",
    #format dollar amount to two decimal places
    value ="{:.2f}".format(prev_month_revenue)
)

kpi2.metric(
    label="# Sales Last Month #️⃣",
    value=sales
)

kpi3.metric(
    label="Different Products 🍭",
    value=df['Product'].nunique()
)

##Columns
leftcolumn, centercolumn, rightcolumn = st.columns(3)
############## Ranking #############
#Product Ranking
with leftcolumn:
    st.subheader('Most Popular Products Last Month')
    prev_month_product_rank = prev_month_df['Product'].value_counts()
    prev_month_product_rank

#Location Ranking
#Set up each location for previous month
pvm_gutten = prev_month_df[prev_month_df.Location=='GuttenPlans']
pvm_earle = prev_month_df[prev_month_df.Location=='Earle Asphalt']
pvm_eblib = prev_month_df[prev_month_df.Location=='EB Public Library']
pvm_brunmall = prev_month_df[prev_month_df.Location=='Brunswick Sq Mall']

pvm_locations = [pvm_gutten, pvm_earle, pvm_eblib, pvm_brunmall]

#Loop for how much money each location made last month
pvm_location_revenue = []
for location in pvm_locations:
    location_sum = location.TransTotal.sum()
    pvm_location_revenue.append(location_sum)

#Loop for how many items each location sold last month
pvm_location_sales = []
for location in pvm_locations:
    location_total = location.TransTotal.count()
    pvm_location_sales.append(location_total)

#Each Location in a dataframe for display
df_summary = pd.DataFrame(list(zip(
    pvm_location_revenue, pvm_location_sales)),
    index = ['GuttenPlans', 'Earle Asphalt', 'EB Public Library',
       'Brunswick Sq Mall'],
    columns = [ 'revenue ($)', 'sales'])

with centercolumn:
    st.header('Sales Last Month')
    df_summary

######################## Location Timeline #######################
#store values to chart
chart_data_brunswick = []
chart_data_earle = []
chart_data_gutten = []
chart_data_eb = []

#loop through the year
for i in range(1,13):
    #filter dataframe on conditions of both month and location
    df_linechart = df[['Location', 'TransMonth', 'TransTotal']]
    filtered_df = df_linechart[(df_linechart.TransMonth == i) & (df_linechart.Location == 'Brunswick Sq Mall')]
    #sum sales and store value
    sum_transaction_month = filtered_df['TransTotal'].sum()
    chart_data_brunswick.append(sum_transaction_month)

## same process with 3 other locations
# earle/Earle Asphalt
for i in range(1, 13):
    filtered_df = df_linechart[(df_linechart.TransMonth == i) & (df_linechart.Location == 'Earle Asphalt')]
    sum_transaction_month = filtered_df['TransTotal'].sum()
    chart_data_earle.append(sum_transaction_month)
# gutten/GuttenPlans
for i in range(1, 13):
    filtered_df = df_linechart[(df_linechart.TransMonth == i) & (df_linechart.Location == 'GuttenPlans')]
    sum_transaction_month = filtered_df['TransTotal'].sum()
    chart_data_gutten.append(sum_transaction_month)
# eb/EB Public Library
for i in range(1, 13):
    filtered_df = df_linechart[(df_linechart.TransMonth == i) & (df_linechart.Location == 'EB Public Library')]
    sum_transaction_month = filtered_df['TransTotal'].sum()
    chart_data_eb.append(sum_transaction_month)

#combine lists with .zip()
data_zip = list(zip(chart_data_brunswick, chart_data_earle,chart_data_gutten,chart_data_eb))
chart_Data = pd.DataFrame(data=data_zip,
                          index=[1,2,3,4,5,6,7,8,9,10,11,12],
                          columns = ['Brunswick Sq Mall','Earle Asphalt','GuttenPlans','EB Public Library']
                          )
with rightcolumn:
    st.header('Revenue by Month and Location ($)')
    chart_Data

st.header('Revenue ($) by Month (Numerical) by Location')
st.line_chart(data=chart_Data)


########### Widget Practice #############
#widgets to further practice the implementation from the documentation
#these are nonfunctional in relation to the data

st.subheader('Widget Practice: Nonfunctional/set to Disneyland')

location_option = st.selectbox(
    'Select Location',
    pd.unique(df['Location']))
df = df[df['Location'] == location_option]
'You selected: ', location_option



#Map Widget (Disneyland and Random Array)
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [33.8, -117.9],
    columns=['lat', 'lon'])

st.map(map_data)

left_column, right_column = st.columns(2)
#Button Widget:
left_column.button('Confirm Selection')

#Selection Widget:
with right_column:
    chosen = st.radio(
        'Choose Location',
        ("GuttenPlans", "Earle Asphalt", "EB Public Library", "Brunswick Sq Mall"))
    st.write(f"You selected {chosen} Location.")

################ SIDEBAR ########################
# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'Select a Year(nonfunctional widget practice)',
    ('2022', '2021', '2020')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a Month Range \n (nonfunctional widget practice)',
    1, 12, (3, 9)
)