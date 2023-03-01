import streamlit as st
import pandas as pd
import datetime as dt
from datetime import date, timedelta
from datetime import time
import plotly.express as px
import numpy as np

st.title('Sales Dashbord')


df = pd.read_csv('/Users/ss/Desktop/sales_dashboard/data/online_retail.csv')
df['date'] = df['InvoiceDate'].apply(lambda x: x.split(" ", 1)[0])
df['date'] =  pd.to_datetime(df['date'], infer_datetime_format=True)
df['date'] = df['date'].dt.strftime('%Y-%m-%d')
df['total_price'] = df['Quantity'] * df['UnitPrice']
 

startdate = st.date_input(
    "Start Date",
    dt.date(2011, 7, 6)).strftime('%Y-%m-%d')
enddate = st.date_input(
    "finish Date",
    dt.date(2011, 7, 31)).strftime('%Y-%m-%d')

df1 = df[(df['date']>=startdate) & (df['date']<=enddate)]

daily_rev = df1.pivot_table(index='date',values='total_price',aggfunc='sum').reset_index()
#daily_rev = df.groupby('date')['total_price'].sum().reset_index()
st.subheader(('Daily Revenue between: ') + startdate +(' and ') + enddate) 

st.bar_chart(daily_rev,x='date',y='total_price')

daily_rev2 = df1.pivot_table(index='date',values='total_price',columns='Country',aggfunc='sum').reset_index()

countries = df1['Country'].unique()
rev_country = df1.groupby('Country')['total_price'].sum().reset_index().nlargest(3,'total_price',keep='all')
rev_country = rev_country['Country'].loc[rev_country.index[0:3]]

option1 = st.multiselect(
    'Please Select Countries:',
    countries,rev_country)

country_rev = df1.groupby('Country')['total_price'].sum().reset_index()
st.header('Countries by Revenue')
daily_rev2 = daily_rev2[option1]
col1, col2 =st.columns([1, 3])
with col1:
    st.write(country_rev.sort_values(by='total_price',ascending=False))
with col2:
    st.area_chart(daily_rev2)


items = df1.groupby('Description')['total_price'].sum().reset_index().sort_values(by='total_price',ascending=False)

pie_chart_df = items.nlargest(5,'total_price',keep='all')


pie_chart = px.pie(pie_chart_df,
                   title="Top 5 Product",
                  values= 'total_price',
                   names= 'Description')


fig = px.icicle(df1, path=[px.Constant("all"),'Country'], 
values='Quantity')
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

fig1 = px.sunburst(df1, path=['Country'], values='Quantity',
                  color='Quantity', hover_data=['Quantity'])


st.header('Revenue by Products')
col3, col4 =st.columns([1, 3])
with col3:
    st.write(items)
with col4:
    st.plotly_chart(pie_chart)
    

item_amount_by_country = df1.groupby('Country')['Quantity'].sum().reset_index().sort_values(by='Quantity',ascending=False)
item_amount = df1.groupby('Description')['Quantity'].sum().reset_index().sort_values(by='Quantity',ascending=False)

st.header('Number of products sold by Country')
col5, col7 = st.columns([1,3])
with col5:
    st.write(item_amount_by_country.set_index('Country', inplace=False))

with col7:
    st.plotly_chart(fig1)

    
#col8, col9 = st.columns([1,3])
#with col8:
#    st.write(item_amount.set_index('Description', inplace=False))


#st.text('row data')
#st.write(df)    