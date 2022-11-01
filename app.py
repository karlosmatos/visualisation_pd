import pandas as pd
import plotly_express as px
import streamlit as st

# emmojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Sales Visualisation", 
                    page_icon="📊", 
                    layout="wide")

# Upload xlsx file button
#uploaded_file = st.file_uploader("Upload your input file", type=["xlsx"])

# Load data
try:
    df = pd.read_excel("data.xlsx")

# Sidebar
    st.sidebar.header("Filter Here:")

    owner = st.sidebar.multiselect(
        "Owner", 
        options=df["Deal - Owner"].unique(),
        default=df["Deal - Owner"].unique()
    )
    
    try:
        language = st.sidebar.multiselect(
            "Language", 
            options=df["Deal - Language"].unique(),
            default=df["Deal - Language"].unique()
        )
    except:
        st.sidebar.write("No language column found")
    
    try:
        industry = st.sidebar.multiselect(
            "Industry",
            options=df["Deal - Industry"].unique(),
            default=df["Deal - Industry"].unique()
        )
    except:
        st.sidebar.write("No industry column found")

    try:
        department = st.sidebar.multiselect(
            "Department",
            options=df["Deal - Department"].unique(),
            default=df["Deal - Department"].unique()
        )
    except:
        st.sidebar.write("No department column found")


    # Filter data
    try:
        df_selection = df.query(
            "(`Deal - Owner` in @owner) & (`Deal - Language` in @language) & (`Deal - Industry` in @industry) & (`Deal - Department` in @department)"
        )
    except:
        df_selection = df.query(
            "(`Deal - Owner` in @owner)"
        )
    st.dataframe(df_selection)



    # Main
    st.title("Sales Visualisation")
    
    
    # Total sales and average sale per deal
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown("## Total Sales")
        st.subheader(f"**{df_selection['Deal - Value'].sum():,.0f}** CZK".replace(",", " "))

    with right_column:
        st.markdown("## Deal Average")
        st.subheader(f"**{df_selection['Deal - Value'].mean():,.0f}** CZK".replace(",", " "))    


    # Reply rates by industry
    try:
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown("## Industry reply rate")
            industry_reply_rate = df_selection.groupby("Deal - Industry")["Deal - Last email received"].count().reset_index()
            industry_contacted = df_selection.groupby("Deal - Industry")["Deal - Last email sent"].count().reset_index()
            industry_reply_rate = pd.merge(industry_contacted, industry_reply_rate, on="Deal - Industry")
            industry_reply_rate["Reply Rate (%)"] = industry_reply_rate["Deal - Last email received"] / industry_reply_rate["Deal - Last email sent"] * 100
            industry_reply_rate.columns = ["Industry", "Contacted", "Replied", "Reply Rate (%)"]
            industry_reply_rate = industry_reply_rate.sort_values(by="Reply Rate (%)", ascending=False)
            st.dataframe(industry_reply_rate)

        with right_column:
            fig = px.bar(industry_reply_rate, x="Industry", y="Reply Rate (%)", color="Reply Rate (%)", color_continuous_scale=px.colors.sequential.RdBu)
            st.plotly_chart(fig)
    except:
        st.write("No industry column found")


    # Sales by owner
    try:
        st.markdown("## Sales by Owner")
        st.write(px.bar(df_selection, x="Deal - Owner", y="Deal - Value", color="Deal - Owner"), use_container_width=True)
    except:
        st.write("No owner column found")


    # Sales by language
    try:
        st.markdown("## Sales by Language")
        st.write(px.pie(df_selection, values="Deal - Value", names="Deal - Language"), use_container_width=True)
    except:
        st.write("No language column found")


    # Sales by industry
    try:
        st.markdown("## Sales by Industry")
        st.write(px.bar(df_selection, x="Deal - Industry", y="Deal - Value", color="Deal - Industry"))
    except:
        st.write("No industry column found")


    # Sales by department
    try:
        st.markdown("## Sales by Department")
        st.write(px.bar(df_selection, x="Deal - Department", y="Deal - Value", color="Deal - Department"))
    except:
        st.write("No department column found")
    

    # Sales by country
    try:
        st.markdown("## Sales by Country")
        st.write(px.bar(df_selection, x="Deal - Country", y="Deal - Value", color="Deal - Country"))
    except:
        st.write("No country column found")
    

    # Sales over months
    try:
        st.markdown("## Sales over months")
        df_selection["Deal - Won time"] = pd.to_datetime(df_selection["Deal - Won time"])
        df_selection["Deal - Won time"] = df_selection["Deal - Won time"].dt.strftime("%Y-%m")
        st.write(px.bar(df_selection, x="Deal - Won time", y="Deal - Value", color="Deal - Won time"))
        st.bar_chart(df_selection.groupby("Deal - Won time")["Deal - Value"].sum())
    except:
        st.write("No won time column found")


except:
    st.write("Please upload a file.")
