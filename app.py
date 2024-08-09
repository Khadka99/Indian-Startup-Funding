import streamlit as st
import pandas as  pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

st.set_page_config(layout='wide',page_title='Indian Startup Analysis')

df = pd.read_csv('clean_startup_funding.csv')
df['amount'] = df['amount'].replace(0,0.000001)


def check_nan(df):
    # Iterate through each column in the DataFrame
    for column in df.columns:
        if df[column].isnull().any():
            df[column].fillna('Information Not Available', inplace=True)

    # Return the updated DataFrame
    return df




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
        st.metric('Number of startup',str(num_startup))

    st.subheader('Month On Month Graph')
    selected_option = st.selectbox('Select Type',['Total','Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig5, ax5 = plt.subplots(figsize=(15, 6))
    ax5.plot(temp_df['x_axis'], temp_df['amount'])
    plt.xticks(rotation=60)

    st.pyplot(fig5)
    col1,col2 = st.columns(2)

    with col1:
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
    with col2:
        # Most amount funded round
        st.subheader("Top 5 Most Amount Funded Rounds")
        selected_option = st.selectbox('Select Type',['Total Amount','Total Count'])
        if selected_option == 'Total Amount':
            df_round = df.groupby('round')['amount'].sum().sort_values(ascending=False).head()
        else:
            df_round = df.groupby('round')['amount'].count().sort_values(ascending=False).head()
        fig7, ax7 = plt.subplots()
        ax7.pie(df_round, labels=df_round.index, autopct="%0.01f%%")
        st.pyplot(fig7)

    st.subheader("Top 10 City wise Funding")
    df_city = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
    color = ['red', 'green', 'yellow', 'blue', 'orange', 'black', 'purple','lightblue','grey','pink']
    fig8, ax8 = plt.subplots(figsize=(10,6))
    bars = ax8.bar(df_city.index,df_city.values,color = color)
    for bar in bars:
        yval = bar.get_height()
        # Position the text inside the bar
        ax8.text(
            bar.get_x() + bar.get_width() / 2.0,  # x position (center of the bar)
            yval - 1,  # y position (just below the top of the bar, adjust as needed)
            round(yval),  # Text to display
            ha='center',  # Horizontal alignment
            va='center',  # Vertical alignment
            color='black',  # Text color
            fontsize=10  # Font size
        )
    plt.xticks(rotation=90)
    st.pyplot(fig8)

    col1,col2 = st.columns(2)
    with col1:
#Maximum Amount funded In A startup In Each Year
        st.subheader('Startup Funded Year Wise')

        max_amt = df.groupby('year')['amount'].transform('max')
        result = df[df['amount'] == max_amt]
        result = result[['year', 'startup', 'amount']].sort_values('year')
        st.dataframe(result,width=700,hide_index=True)
    with col2:
        # Max amount funded year wise to the startup
        st.subheader("Startup/Investor Year Wise")
        max_amt = df.groupby('year')['amount'].transform('max')
        result = df[df['amount'] == max_amt]
        result = result[['year', 'investor', 'startup', 'amount']].sort_values('year')
        st.dataframe(result,width=700,hide_index=True)


    # Heatmap for funding
    st.subheader("Funding Heatmap")
    total_funding = round(df.groupby(['year', 'month'])['amount'].sum()).reset_index()

    # Pivot the data to prepare for plotting
    pivot_df = total_funding.pivot(index='month', columns='year', values='amount')

    # Plotting using seaborn heatmap
    fig9, ax9 = plt.subplots(figsize=(10, 6))
    sns.heatmap(pivot_df, annot=True, cmap='viridis', fmt='.1f')
    ax9.set_title('Total Funding Amount by Month and Year')
    ax9.set_xlabel('Year')
    ax9.set_ylabel('Month')
    st.pyplot(fig9)











def load_investors_detail(investor):
    st.title(investor)
 #load the recent 5 invetment of the investor
    last5_df = df[df['investor'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)

    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Biggest Investment')
        if investor:
                big_series = df[df['investor'].str.contains(investor)] \
                    .groupby('startup')['amount'].sum()\
                    .sort_values(ascending=False)\
                    .head(5)
                st.dataframe(big_series)


    with col2:
        st.subheader('Biggest Investment Chart')
        if big_series.empty:
            st.write(f"No data available to plot for the investor '{investor}'.")
        else:
            # Create a smaller figure
            fig0, ax0 = plt.subplots(figsize=(8, 6))  # Adjust figsize as necessary

            # Plotting
            bars = ax0.bar(big_series.index, big_series.values)

            # Adding text labels on the bars
            for bar in bars:
                yval = bar.get_height()
                ax0.text(
                    bar.get_x() + bar.get_width() / 2.0,  # x position (center of the bar)
                    yval + 0.01 * yval,  # y position (just above the top of the bar, adjust as needed)
                    round(yval),  # Text to display
                    ha='center',  # Horizontal alignment
                    va='bottom',  # Vertical alignment
                    color='black',  # Text color
                    fontsize=10  # Font size
                )
            st.pyplot(fig0)

            #Improve layout and avoid overlap
            #plt.xticks(rotation=45, ha='right')






    col1,col2,col3 = st.columns(3)
    with col1:
        vertical_series = df[df['investor'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(
            ascending=False).head(7)

        st.subheader('Top 7 Sectors Invested In')
        fig1, ax1 = plt.subplots(figsize=(10,5))
        ax1.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")

        st.pyplot(fig1)
    with col2:
        stage_series = df[df['investor'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(ascending=False)

        st.subheader('Stages Invested In')
        fig2, ax2 = plt.subplots(figsize=(10,5))
        ax2.pie(stage_series, labels=stage_series.index, autopct="%0.01f%%")

        st.pyplot(fig2)
    with col3:
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








def load_startup_analysis(startup):
    #Startup Details
        st.subheader("Startup Details")
        filtered_df = df[df['startup'] == startup]
        result = filtered_df[['year','startup','vertical','SubVertical','investor','city','amount']]
        st.dataframe(check_nan(result),hide_index=True)
        col1,col2 = st.columns(2)
        with col1:
            # Investment Round Year Wise
            st.subheader("Round Year Wise :-")
            st.subheader(startup)
            round_amt = df[df['startup'] == startup].groupby(['year' ,'round'])['amount'].sum().reset_index()
            st.dataframe(round_amt,hide_index=True)
        with col2:
            # Investment Round Year Wise Chart
             st.subheader("Investment Round Year Wise Chart")
             round_year = df[df['startup'] == startup].groupby(['year', 'round'])['amount'].sum()
            # fig10, ax10 = plt.subplots()
            # ax10.pie(round_year, labels=round_year.index, autopct="%0.01f%%")
            # st.pyplot(fig10)
             if round_year.empty:
                st.write(f"No data available to plot for the startup '{startup}'.")
             else:
                fig10, ax10 = plt.subplots()
                ax10.pie(round_year, labels=round_year.index, autopct="%0.01f%%")
                st.pyplot(fig10)



        # Similar Startup
        st.subheader("Similar Startup")
        demo_df = df[df['startup'] == startup]
        result = df[
            (df['vertical'] == demo_df['vertical'].values[0]) | (df['SubVertical'] == demo_df['SubVertical'].values[0])]
        result = result[['year', 'startup', 'vertical','SubVertical', 'amount']]
        st.dataframe(result,hide_index=True)














###########################################################################################################

st.sidebar.title("Stratup Funding Analysis")

option = st.sidebar.selectbox('Select one',['Overall Analysis','Startup','Investor'])
if option == 'Overall Analysis':
    # btn0 = st.sidebar.button('Show Overall Analysis')
    # if btn0:
        load_overall_analysis()

elif option == 'Startup':
    select_startup = st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Detalis')
    if btn1:
        load_startup_analysis(select_startup)
else:
    select_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investor'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Detalis')
    if btn2:
        load_investors_detail(select_investor)


