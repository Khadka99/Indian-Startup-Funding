import streamlit as st
import pandas as  pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

st.set_page_config(layout='wide',page_title='Startup Analysis')

df = pd.read_csv('clean_stratup.csv')
df['date'] = pd.to_datetime(df['date'],format = 'mixed',errors = 'coerce')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month


#st.dataframe(df)
#df['Investors Name'] = df['Investors Name'].fillna('Undisclosed')

def load_overall_analysis():
    st.title("Overall Analysis")
    #total invested amount
    total = round(df['amount'].sum())
    #maximum amount infused in startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head().values[0]
    #Average ticket size
    avg_funding = round(df.groupby('startup')['amount'].sum().mean())
    # Total funded startup
    num_startup = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + ' CR')
    with col2:
        st.metric('Max Amount Infused', str(max_funding) + ' CR')
    with col3:
        st.metric('Average Funding',str(avg_funding) + ' CR')
    with col4:
        st.metric('Number of startup',str(num_startup) + ' CR')

    st.subheader('Month On Month Graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig5)
# Top sectors funded
    st.subheader('Top Sectors Funded')
    selected_option = st.selectbox('Select Type',['Amount','Count'])
    if selected_option == "Amount":
        top_sector = df.groupby(['vertical'])['amount'].sum().sort_values(ascending=False).head()
    else:
        top_sector = df.groupby(['vertical'])['amount'].count().sort_values(ascending=False).head()

    fig6, ax6 = plt.subplots()
    ax6.pie(top_sector, labels=top_sector.index, autopct="%0.01f%%")

    st.pyplot(fig6)


def load_investors_detail(investor):
    st.title(investor)
    #load the recent 5 invetment of the investor
    last5_df = df[df['investor'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)

    col1,col2 = st.columns(2)
    with col1:
        # Biggest investment
        big_series = df[df['investor'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        st.dataframe(big_series)
    with col2:
        st.subheader('Biggest Investment Chart')
        fig, ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)

    vertical_series = df[df['investor'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(
        ascending=False).head(7)

    st.subheader('Top 7 Sectors Invested In')
    fig1, ax1 = plt.subplots()
    ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")

    st.pyplot(fig1)

    stage_series = df[df['investor'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(ascending=False)

    st.subheader('Stages Invested In')
    fig2, ax2 = plt.subplots()
    ax2.pie(stage_series, labels=stage_series.index, autopct="%0.01f%%")

    st.pyplot(fig2)

    city_series = df[df['investor'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(ascending=False).head()
    st.subheader('City Invested In')
    fig3, ax3 = plt.subplots()
    ax3.pie(city_series, labels=city_series.index, autopct="%0.01f%%")

    st.pyplot(fig3)

    st.subheader('Year On Year Investment')
    year_series = df[df['investor'].str.contains(investor)].groupby('year')['amount'].sum()

    fig4, ax4 = plt.subplots()
    ax4.plot(year_series.index, year_series.values)

    st.pyplot(fig4)

st.sidebar.title("Stratup Funding Analysis")

option = st.sidebar.selectbox('Select one',['Overall Analysis','Startup','Investor'])
if option == 'Overall Analysis':

    # btn0 = st.sidebar.button('Show Overall Analysis')
    # if btn0:
        load_overall_analysis()

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Detalis')
    st.title('Startup Analysis')
else:
    select_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investor'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Detalis')
    if btn2:
        load_investors_detail(select_investor)


