import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


month_order = {
    'January': 1, 'February': 2, 'March': 3, 'April': 4,
    'May': 5, 'June': 6, 'July': 7, 'August': 8,
    'September': 9, 'October': 10, 'November': 11, 'December': 12
}
def create_season_bikes_sharing_df(df):
    season_bikes_sharing_df = df.groupby(by='season').agg({
        "casual" : "sum",
        "registered" : "sum"
    })

    season_bikes_sharing_df = season_bikes_sharing_df.reset_index()
    return season_bikes_sharing_df

def create_user_month_2011_df(df):
    df = df.sort_index()
    monthly_bikes_sharing_2011_df = df.loc['2011-01-01':'2011-12-31']
    monthly_bikes_sharing_2011_df['Month'] = monthly_bikes_sharing_2011_df.index.strftime('%B')
    monthly_bikes_sharing_2011_df = monthly_bikes_sharing_2011_df.reset_index()

    group_monthly_bikes_sharing_2011_df = monthly_bikes_sharing_2011_df.groupby(by='Month').agg({
    "cnt" : "sum"
    })
    group_monthly_bikes_sharing_2011_df['Month_Number'] = group_monthly_bikes_sharing_2011_df.index.map(month_order)

    group_monthly_bikes_sharing_2011_df = group_monthly_bikes_sharing_2011_df.sort_values('Month_Number')

    group_monthly_bikes_sharing_2011_df = group_monthly_bikes_sharing_2011_df.drop('Month_Number', axis=1)

    group_monthly_bikes_sharing_2011_df.sort_values(by='cnt',ascending=False)

    return group_monthly_bikes_sharing_2011_df

def create_user_month_2012_df(df):
    df = df.sort_index()
    monthly_bikes_sharing_2012_df = df.loc['2012-01-01':'2012-12-31']
    monthly_bikes_sharing_2012_df['Month'] = monthly_bikes_sharing_2012_df.index.strftime('%B')
    monthly_bikes_sharing_2012_df = monthly_bikes_sharing_2012_df.reset_index()

    group_monthly_bikes_sharing_2012_df = monthly_bikes_sharing_2012_df.groupby(by='Month').agg({
    "cnt" : "sum"
    })
    group_monthly_bikes_sharing_2012_df['Month_Number'] = group_monthly_bikes_sharing_2012_df.index.map(month_order)

    group_monthly_bikes_sharing_2012_df = group_monthly_bikes_sharing_2012_df.sort_values('Month_Number')

    group_monthly_bikes_sharing_2012_df = group_monthly_bikes_sharing_2012_df.drop('Month_Number', axis=1)

    group_monthly_bikes_sharing_2012_df.sort_values(by='cnt',ascending=False)
    
    return group_monthly_bikes_sharing_2012_df

def create_total_day_daily_sharing_df(df):
    day_daily_sharing_df = df.groupby(by='weekday', as_index=False).cnt.sum()
    day_daily_sharing_df = day_daily_sharing_df.sort_values(by='cnt', ascending=False)
    return day_daily_sharing_df
def create_avg_day_daily_sharing_df(df):
    avg_day_daily_sharing_df = df.groupby(by='weekday', as_index=False).cnt.mean()
    avg_day_daily_sharing_df = avg_day_daily_sharing_df.sort_values(by='cnt', ascending=False)
    return avg_day_daily_sharing_df

all_df = pd.read_csv("data.csv")
all_df['dteday'] = pd.to_datetime(all_df['dteday'])
all_df = all_df.set_index('dteday')

st.header("Dashboard Capital Bikeshare System :sparkles:")

min_date = all_df.index.min()
max_date = all_df.index.max()

with st.sidebar:
    st.image("capital.png",width=250)

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date,max_date]
    )

data_df = all_df[(all_df.index >= str(start_date)) &
                 (all_df.index <= str(end_date))]

season_bikes_sharing_df = create_season_bikes_sharing_df(data_df)
month_users_2011_df = create_user_month_2011_df(data_df)
month_users_2012_df = create_user_month_2012_df(data_df)
day_daily_sharing_df = create_total_day_daily_sharing_df(data_df)
avg_day_daily_sharing_df = create_avg_day_daily_sharing_df(data_df)


st.subheader("Total Users In 2011 And 2012")
col1,col2 = st.columns(2)

with col1:
    total_users_2011 = month_users_2011_df.cnt.sum()
    st.metric("Total Users in 2011", value=total_users_2011)

with col2:
    total_users_2012 = month_users_2012_df.cnt.sum()
    st.metric("Total Users in 2012", value=total_users_2012)

st.subheader("Development Bikes Sharing User in 2011 to 2012")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30,10))

sns.lineplot(
    x='Month',
    y='cnt',
    data=month_users_2011_df,
    ax=ax[0]
)

ax[0].set_title("Growth Total Users in 2011")
ax[0].set_xlabel("Month")
ax[0].set_ylabel("Total Users 2011")
ax[0].tick_params(axis='y', labelsize=12)

sns.lineplot(
    x='Month',
    y='cnt',
    data=month_users_2012_df,
    ax=ax[1]
)

ax[1].set_title("Growth Total Users in 2012")
ax[1].set_xlabel("Month")
ax[1].set_ylabel("Total Users 2012")
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)


st.subheader("Best Season For Users Casual and Registerd Bikes Sharing")

fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(35, 15))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    y='season',
    x='casual',
    data=season_bikes_sharing_df.sort_values(by='casual', ascending=False),
    palette=colors,
    ax=ax[0]
)

ax[0].set_title("Best Season For Users Casual Bikes Sharing")
ax[0].set_xlabel("Total Users")
ax[0].set_ylabel("Season")
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(
    y='season',
    x='registered',
    data=season_bikes_sharing_df.sort_values(by='registered', ascending=False),
    palette=colors,
    ax=ax[1]
)

ax[1].set_title("Best Season For Users Registered Bikes Sharing")
ax[1].set_xlabel("Total Users")
ax[1].set_ylabel("Season")
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)

st.subheader("Total and Average Day to Day Daily Users Bike Sharing")

fig, ax = plt.subplots(nrows=1,ncols=2,figsize=(35, 15))

colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#D3D3D3","#D3D3D3"]

sns.barplot(
    y='cnt',
    x='weekday',
    data=day_daily_sharing_df,
    palette=colors,
    ax=ax[0]
)

ax[0].set_title("Total Day to Day Users Bike Sharing")
ax[0].set_xlabel("Weekday")
ax[0].set_ylabel("Total Users")
ax[0].tick_params(axis='y', labelsize=12)

sns.barplot(
    y='cnt',
    x='weekday',
    data=avg_day_daily_sharing_df,
    palette=colors,
    ax=ax[1]
)

ax[1].set_title("Average Day to Day Users Bike Sharing")
ax[1].set_xlabel("Weekday")
ax[1].set_ylabel("Total Users")
ax[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig)