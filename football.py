import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.title("Analysis of Top 50 Transfers in Football")
st.markdown("""
This app is created by webscraping data from wikipedia related to the top 50 transfers in football history.
Created to get started with data analysis and understand core concepts by building a simple project.
* **Python libraries:** pandas, seaborn, matplotlib, streamlit
* **Data source:** [wikipedia](https://en.wikipedia.org/wiki/List_of_most_expensive_association_football_transfers)
* **Jupyter notebook:** [Notebook](https://jovian.ai/adhetya/football-transfer-analysis)
""")

st.sidebar.header('Filters')
st.sidebar.markdown("""
A list of filters that users can use to view what they want.
""")
url = "https://en.wikipedia.org/wiki/List_of_most_expensive_association_football_transfers"
html = pd.read_html(url, match = 'Top 50 most expensive association football transfers')
df = html[0]
df.drop(['Fee(£ mln)','Ref.'], inplace=True, axis=1)
df['Transfer year'] = df['Year'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
df['Fee in €(mln)'] = df['Fee(€ mln)'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(float)
df["Fee in €(mln)"].replace(to_replace= 845.0, value = 84.50, inplace=True )
df["Fee in €(mln)"].replace(to_replace= 823.0, value = 82.30, inplace=True )
df["Fee in €(mln)"].replace(to_replace= 756.0, value = 75.60, inplace=True )
df["Fee in €(mln)"].replace(to_replace= 695.0, value = 69.50, inplace=True )
df["Fee in €(mln)"].replace(to_replace= 678.0, value = 67.80, inplace=True )
df["Fee in €(mln)"].replace(to_replace= 655.0, value = 65.50, inplace=True )
df["Fee in €(mln)"].replace(to_replace= 652.0, value = 65.20, inplace=True )
df["Fee in €(mln)"].replace(to_replace= 645.0, value = 64.50, inplace=True )
df["Fee in €(mln)"].replace(to_replace= 637.0, value = 63.70, inplace=True )
df["Fee in €(mln)"].replace(to_replace= 625.0, value = 62.50, inplace=True )
df["Fee in €(mln)"].replace(to_replace= 625.0, value = 62.50, inplace=True )
df.drop(['Fee(€ mln)','Year'], inplace=True,axis=1)
transferStats = df

sorted_unique_buying_team = sorted(transferStats.To.unique())
selected_buying_team = st.sidebar.multiselect('Team', sorted_unique_buying_team, sorted_unique_buying_team)


unique_pos = ['Forward','Midfielder','Defender','Goalkeeper']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

df_selected_team = transferStats[(transferStats.To.isin(selected_buying_team))&(transferStats.Position.isin(selected_pos))]

st.header('Display Transfer Stats')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(transferStats)

st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='football_transfers.csv',
    mime='text/csv',
)

st.header('Data visualizations')

st.markdown("""
Click the buttons to see the visualizations one at a time.
""")

if(st.button('Bar Chart')):
    st.header('Money spent by clubs')
    buyingCount = transferStats.groupby(
        ['To'])['Fee in €(mln)'].sum().sort_values(ascending=False)
    st.bar_chart(buyingCount)

    st.header('Money earned by clubs')
    sellingCount = transferStats.groupby(
        ['From'])['Fee in €(mln)'].sum().sort_values(ascending=True)
    st.bar_chart(sellingCount)

    st.header("Total transfer spend on a yearly basis")
    transferYear = transferStats.groupby(['Transfer year'])['Fee in €(mln)'].sum()
    st.bar_chart(transferYear)

if(st.button('Pie Chart')):
    st.header('Pie chart')
    total = df['Fee in €(mln)'].sum()
    forward = (df.query("Position == 'Forward'")['Fee in €(mln)'].sum()/total)
    midfielder = (df.query("Position == 'Midfielder'")
              ['Fee in €(mln)'].sum()/total)
    defender = (df.query("Position == 'Defender'")['Fee in €(mln)'].sum()/total)
    gk = (df.query("Position == 'Goalkeeper'")['Fee in €(mln)'].sum()/total)
    data = [forward, midfielder, defender, gk]
    labels = ['Forward', 'Midfielder', 'Defender', 'Goalkeeper']
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=data,
            hoverinfo="label+percent",
            textinfo="value"
        ))
    st.plotly_chart(fig)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)



