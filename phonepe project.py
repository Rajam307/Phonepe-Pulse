# 📦 Import Libraries
# ==============================
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import requests
from streamlit_lottie import st_lottie


import pandas as pd
from sqlalchemy import create_engine

#  NEON DB credentials
username = "neondb_owner"
password = "npg_hNu4bqHo5EPQ"
host = "ep-aged-bread-a1xghr1f-pooler.ap-southeast-1.aws.neon.tech"
database = "Raaji"

# ✅ Create engine with SSL mode
engine = create_engine(f"postgresql://{username}:{password}@{host}/{database}?sslmode=require")

# ✅ Define list of table names
tables = [
    "agg_trans", "agg_users", "agg_insu",
    "map_trans", "map_users", "map_insu",
    "top_insu", "top_trans", "top_users"
]

# ✅ Load all tables into dfs
dfs = {table: pd.read_sql(f"SELECT * FROM public.{table}", con=engine) for table in tables}

# ✅ Unpack the ones you'll frequently use
agg_trans = dfs["agg_trans"]
agg_users = dfs["agg_users"]
map_trans = dfs["map_trans"]
map_users = dfs["map_users"]
top_trans = dfs["top_trans"]
top_users = dfs["top_users"]



import pandas as pd

agg_trans = pd.read_sql("SELECT * FROM public.agg_trans", con=engine)
agg_users = pd.read_sql("SELECT * FROM public.agg_users", con=engine)
map_trans = pd.read_sql("SELECT * FROM public.map_trans", con=engine)
map_users = pd.read_sql("SELECT * FROM public.map_users", con=engine)
top_trans = pd.read_sql("SELECT * FROM public.top_trans", con=engine)
top_users = pd.read_sql("SELECT * FROM public.top_users", con=engine)









st.set_page_config(layout='wide')
st.title("PHONEPE PULSE DATA ANALYSIS AND VISUALIZATION")

with st.sidebar:
    select = option_menu("Main Menu", ["HOME", "DATA EXPLORATION", "ANALYSIS REPORT", "EXIT"])

if select == "HOME":
        
        st.markdown("###")
        st.markdown("""
        <h3 style='text-align: center;'></h3>
        <p style='text-align: justify; font-size: 17px;'>
        This dashboard provides insightful visualizations of PhonePe transactions across India.
        Explore state-wise, year-wise, quarter-wise trends and compare top user engagement statistics.
        </p>
        """, unsafe_allow_html=True)

        # --- Lottie Animation ---
        def load_lottieurl(url):
            r = requests.get(url)
            if r.status_code != 200:
                return None
            return r.json()

        lottie_url = "https://assets6.lottiefiles.com/packages/lf20_9cyyl8i4.json"
        lottie_json = load_lottieurl(lottie_url)

        # --- Page Config ---
        st.set_page_config(page_title="PhonePe India - Home", layout="wide")

        # --- Title + Animation ---
        col_anim, col_title = st.columns([1, 5])
        with col_anim:
            st_lottie(lottie_json, height=120, key="header_anim")
        with col_title:
            st.title("📊 PhonePe India – Transaction Insights")

        st.markdown("---")

        # --- Load Data ---
        agg_trans = pd.read_sql("SELECT * FROM agg_trans", engine)
        map_users = pd.read_sql("SELECT * FROM map_users", engine)

        # --- Metric Calculations ---
        total_amount = agg_trans["Transaction_amount"].sum()
        total_txn_count = agg_trans["Transaction_count"].sum()
        total_users = map_users["RegisteredUsers"].sum()
        top_state_txn = agg_trans.groupby("States")["Transaction_count"].sum().idxmax()
        top_state_users = map_users.groupby("States")["RegisteredUsers"].sum().idxmax()

        # --- Metric Cards Styling ---
        st.markdown("""
        <style>
        .metric-card {
            background: linear-gradient(135deg, #1a1a40, #1f4068);
            padding: 20px;
            border-radius: 15px;
            color: white;
            font-weight: bold;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
            text-align: center;
            margin-bottom: 10px;
        }
        .metric-icon {
            font-size: 30px;
        }
        .metric-value {
            font-size: 22px;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">💸</div>
                    <div>Total Transaction Amount</div>
                    <div class="metric-value">₹{total_amount/1e7:.2f} Cr</div>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">🔢</div>
                    <div>Total Transaction Count</div>
                    <div class="metric-value">{int(total_txn_count/1e6)} Million</div>
                </div>
            """, unsafe_allow_html=True)

        # --- Dual Choropleth Map View (List 1) ---
        map_data = agg_trans.groupby("States")[["Transaction_count", "Transaction_amount"]].sum().reset_index()
        map_data["Txn_Count_Millions"] = (map_data["Transaction_count"] / 1e6).round(1)
        map_data["Txn_Amount_Billions"] = (map_data["Transaction_amount"] / 1e9).round(1)

        col3, col4 = st.columns(2)

        with col3:
            fig1 = px.choropleth(
                map_data,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='States',
                color='Txn_Count_Millions',
                color_continuous_scale='Blues',
                hover_name='States',
                title="Total Transaction Count (in Millions)"
            )
            fig1.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig1, use_container_width=True)

        with col4:
            fig2 = px.choropleth(
                map_data,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='States',
                color='Txn_Amount_Billions',
                color_continuous_scale='Greens',
                hover_name='States',
                title="Total Transaction Amount (in Billions)"
            )
            fig2.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # --- Summary Visuals (List 2) ---
        # 1. Bar Chart – Top 5 States by App Opens
        top_app = map_users.groupby("States")[["AppOpens"]].sum().reset_index().sort_values("AppOpens", ascending=False).head(5)
        fig_app = px.bar(top_app, x="States", y="AppOpens", title="📱 Top 5 States by App Opens", color="AppOpens", text_auto=True)

        # 2. Pie Chart – Transaction Type Share
        txn_type = agg_trans.groupby("Transaction_type")[["Transaction_count"]].sum().reset_index()
        fig_txn_type = px.pie(txn_type, names="Transaction_type", values="Transaction_count", title="🥧 Transaction Type Share", hole=0.4)

        # 3. Pie Chart – Top 5 States by Registered Users
        top_users = map_users.groupby("States")[["RegisteredUsers"]].sum().reset_index().sort_values("RegisteredUsers", ascending=False).head(5)
        fig_users = px.pie(top_users, names="States", values="RegisteredUsers", title="👥 Top 5 States - Registered Users", hole=0.4)

        # 4. Line Chart – Year-wise Transaction Growth
        yearly_txn = agg_trans.groupby("Years")[["Transaction_count"]].sum().reset_index()
        fig_yearly = px.line(yearly_txn, x="Years", y="Transaction_count", title="📈 Year-wise Transaction Growth", markers=True)

        # Display all 4 visuals in one row
        col5, col6, col7, col8 = st.columns(4)
        col5.plotly_chart(fig_app, use_container_width=True)
        col6.plotly_chart(fig_txn_type, use_container_width=True)
        col7.plotly_chart(fig_users, use_container_width=True)
        col8.plotly_chart(fig_yearly, use_container_width=True)
        st.success("Use the sidebar to start exploring!")

        st.markdown("---")
        st.markdown("💡 **Tip:** Use full-screen mode for best experience!")



elif select == "DATA EXPLORATION":
    tab1, tab2, tab3 = st.tabs(["Transaction", "User", "Top Charts"])

    with tab1:
        method_1 = st.radio("Select the method", ["State Analysis", "Year Analysis", "Quarter Analysis"])

        if method_1 == "State Analysis":
            st.subheader("Transaction State-wise View")

            #  Place this inside "State Analysis"
            view_option = st.selectbox("Select View", ["Total Transaction count map view", "Total Transaction amount map view"])

            if view_option == "Total Transaction count map view":
                query = """
                    SELECT "States", SUM("Transaction_count") AS transaction_count
                    FROM agg_trans
                    GROUP BY "States"
                    ORDER BY transaction_count DESC;
                """
                df = pd.read_sql(query, engine)

                df["Transaction_Count_Millions"] = (df["transaction_count"] / 1e6).round(0).astype(int)
                df_display = df[["States", "Transaction_Count_Millions"]]
                df_display.columns = ["States", "Transaction Count (in Millions)"]

                st.dataframe(df_display)

                fig = px.choropleth(
                    df,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='States',
                    color='Transaction_Count_Millions',
                    color_continuous_scale='Blues',
                    hover_name='States',
                    hover_data={'Transaction_Count_Millions': True}
                )
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(title="Transaction Count in Millions", margin={"r": 0, "t": 30, "l": 0, "b": 0})
                st.plotly_chart(fig, use_container_width=True)

            elif view_option == "Total Transaction amount map view":
                query = """
                    SELECT "States", SUM("Transaction_amount") AS transaction_amount
                    FROM agg_trans
                    GROUP BY "States"
                    ORDER BY transaction_amount DESC;
                """
                df = pd.read_sql(query, engine)

                df["Transaction_Amount_Billions"] = (df["transaction_amount"] / 1e9).round(0).astype(int)
                df_display = df[["States", "Transaction_Amount_Billions"]]
                df_display.columns = ["States", "Transaction Amount (in Billions)"]

                st.dataframe(df_display)

                fig = px.choropleth(
                    df,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='States',
                    color='Transaction_Amount_Billions',
                    color_continuous_scale='Greens',
                    hover_name='States',
                    hover_data={'Transaction_Amount_Billions': True}
                )
                fig.update_geos(fitbounds="locations", visible=False)
                fig.update_layout(title="Transaction Amount in Billions", margin={"r": 0, "t": 30, "l": 0, "b": 0})
                st.plotly_chart(fig, use_container_width=True)

    
        elif method_1 == "Year Analysis":
            st.subheader("📅 Year-wise Analysis")

            #  Step 1: Multiselect Year
            available_years = sorted(agg_trans["Years"].unique().tolist())
            selected_years = st.multiselect("Select Year(s)", available_years)

            if selected_years:
                #  Convert list to comma-separated string for SQL query
                years_string = ",".join(f"'{str(year)}'" for year in selected_years)

                #  Step 2: Query from agg_trans for selected years
                query_trans = f"""
                    SELECT * FROM agg_trans
                    WHERE "Years" IN ({years_string})
                """
                df_trans = pd.read_sql(query_trans, con=engine)

                #  Step 3: Query from agg_user for selected years
                query_user = f"""
                    SELECT * FROM map_users
                    WHERE "Years" IN ({years_string})
                """
                df_user = pd.read_sql(query_user, con=engine)

                #  Step 4: Metrics Calculation (Row 1)
                total_states = df_trans["States"].nunique()
                total_amount_billion = round(df_trans["Transaction_amount"].sum() / 1e9, 2)
                total_count_million = round(df_trans["Transaction_count"].sum() / 1e6, 2)

                #  Step 5: Metrics Calculation (Row 2)
                total_registered_users_million = round(df_user["RegisteredUsers"].sum() / 1e6, 2)
                total_app_opens_million = round(df_user["AppOpens"].sum() / 1e6, 2)
                total_transaction_types = df_trans["Transaction_type"].nunique()

                #  Step 6: Display Row 1 Metrics
                col1, col2, col3 = st.columns(3)
                col1.metric("🟪 Total Number of States", total_states)
                col2.metric("🟩 Total Transaction Amount (₹ Billion)", total_amount_billion)
                col3.metric("🟦 Total Transaction Count (Million)", total_count_million)

                #  Step 7: Display Row 2 Metrics
                col4, col5, col6 = st.columns(3)
                col4.metric("🟨 Total Registered Users (Million)", total_registered_users_million)
                col5.metric("🟥 Total App Opens (Million)", total_app_opens_million)
                col6.metric("🟧 Unique Transaction Types", total_transaction_types)

            else:
                st.info("Please select at least one year to view analysis.")



        elif method_1 == "Quarter Analysis":
            with st.container():
                st.markdown("### 📆 Quarter-wise Transaction Analysis")

                available_states = map_trans["States"].unique()
                available_years = sorted(map_trans["Years"].unique().tolist())
                default_years = ["2022"] if "2022" in available_years else [available_years[0]]

                selected_state = st.selectbox("Select State", available_states)
                selected_years = st.multiselect("Select Year(s)", available_years, default=default_years)
                selected_metric = st.radio("Select Metric", ["Transaction Count", "Transaction Amount"])

                #  Loop through each selected year and show pie chart
                for year in selected_years:
                    st.markdown(f"#### 📅 Year: {year}")

                    # Filter the data
                    df_year = map_trans[
                        (map_trans["States"] == selected_state) &
                        (map_trans["Years"] == year)
                    ]

                    # Group by Quarter
                    if selected_metric == "Transaction Count":
                        df_grouped = df_year.groupby("Quarters")["Transaction_count"].sum().reset_index()
                        metric_col = "Transaction_count"
                    else:
                        df_grouped = df_year.groupby("Quarters")["Transaction_amount"].sum().reset_index()
                        metric_col = "Transaction_amount"

                    # 🟣 Pie Chart
                    fig = px.pie(
                        df_grouped,
                        names="Quarters",
                        values=metric_col,
                        title=f"{selected_metric} - Quarter-wise for {selected_state} in {year}",
                        hole=0.4
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # 🔍 Max, Min, Avg Metrics
                    max_val = df_grouped[metric_col].max()
                    min_val = df_grouped[metric_col].min()
                    avg_val = df_grouped[metric_col].mean()

                    col1, col2, col3 = st.columns(3)
                    col1.metric(" Max", f"{max_val:,.2f}")
                    col2.metric(" Min", f"{min_val:,.2f}")
                    col3.metric(" Average", f"{avg_val:,.2f}")


    with tab2:
        method_2 = st.radio("Select the method", ["Registered Users", "Apps Opens", "Brands"])

        if method_2 == "Registered Users":
            st.subheader(" Registered Users: State → District → Chart View")

            # 1. Multiselect States
            selected_states = st.multiselect(" Select State(s)", sorted(map_users["States"].unique()))

            if selected_states:
                # 2. Filter districts based on selected states
                filtered_df = map_users[map_users["States"].isin(selected_states)]
                selected_districts = st.multiselect(" Select District(s)", sorted(filtered_df["Districts"].unique()))

                if selected_districts:
                    # 3. Final filtered data
                    final_df = filtered_df[filtered_df["Districts"].isin(selected_districts)]

                    if not final_df.empty:
                        # 4. Bar chart: Registered Users + Transaction Type
                        fig = px.bar(final_df, 
                                    x="Districts", 
                                    y="RegisteredUsers", 
                                    color="Years",
                                    barmode="group",
                                    title="Registered Users by District and Years")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("⚠️ No data for the selected districts.")
            else:
                st.info("Please select at least one state.")

        elif method_2 == "Apps Opens":
            st.subheader("📲 App Opens: State → District → Grouped Bar Chart")

            # 1. Multiselect States
            selected_states = st.multiselect("📍 Select State(s)", sorted(map_users["States"].unique()))

            if selected_states:
                # 2. Filter districts based on selected states
                filtered_df = map_users[map_users["States"].isin(selected_states)]
                selected_districts = st.multiselect(" Select District(s)", sorted(filtered_df["Districts"].unique()))

                if selected_districts:
                    # 3. Final filtered data
                    final_df = filtered_df[filtered_df["Districts"].isin(selected_districts)]

                    if not final_df.empty:
                        # 4. Bar Chart: AppOpens vs Districts (color by Year)
                        fig = px.bar(final_df, 
                                    x="Districts", 
                                    y="AppOpens", 
                                    color="Years", 
                                    barmode="group",
                                    title="App Opens by District and Year")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("⚠️ No data for the selected districts.")
            else:
                st.info("Please select at least one state.")

        elif method_2 == "Brands":
            st.subheader(" Mobile Brand Usage Analysis")

            # Optional Filter: Select State(s)
            selected_states = st.multiselect(" Select State(s) (Optional)", sorted(agg_users["States"].unique()))

            # Step 1: Filter the data if states are selected
            if selected_states:
                df_filtered = agg_users[agg_users["States"].isin(selected_states)]
            else:
                df_filtered = agg_users.copy()  # All India

            # Step 2: Group by Brands and Sum Transaction Count
            df_brand_usage = df_filtered.groupby("Brands")["Transaction_count"].sum().reset_index()

            # Step 3: Sort and get Top 10
            df_top_brands = df_brand_usage.sort_values(by="Transaction_count", ascending=False).head(10)

            # Step 4: Plot Horizontal Bar Chart
            fig = px.bar(
                df_top_brands,
                x="Transaction_count",
                y="Brands",
                orientation="h",
                color="Brands",
                title="🔝 Top 10 Mobile Brands by Transaction Count",
                color_discrete_sequence=px.colors.qualitative.Vivid
            )

            # Arrange bars in ascending order of count for nice view
            fig.update_layout(yaxis=dict(categoryorder='total ascending'))

            st.plotly_chart(fig, use_container_width=True)



    with tab3:
        st.subheader("📊 Top 10 Chart Insights")
        top_trans = dfs["top_trans"]
        map_users = dfs["map_users"]
        agg_users = dfs["agg_users"]
        agg_trans = dfs["agg_trans"]
        
        method_3 = st.radio(" Choose a Top 10 Chart to Explore", [
            "Top 10 States by Transaction Amount",
            "Top 10 States by Transaction Count",
            "Most Used Transaction Type by Transaction Count",
            "Top 10 States by Dominant Transaction Type",
            "Bottom 10 States by Registered Users",
            "Bottom 10 States by App Opens",
            "Top 10 States by App Opens",
            "District-wise Registered Users Trend (Year-wise)",
            
        ])

        if method_3 == "Top 10 States by Transaction Amount":
            st.write(" Chart 1: Top 10 States by Total Transaction Amount")
            #  Paste chart code here — horizontal bar chart
            df_filtered = agg_trans.groupby("States")["Transaction_amount"].sum().nlargest(10).reset_index()
            fig = px.bar(df_filtered, 
                         x="Transaction_amount", 
                         y="States", 
                         orientation="h",
                         color="Transaction_amount",
                         title="Top 10 States by Transaction Amount",  
                         color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)

        elif method_3 == "Top 10 States by Transaction Count":
            st.write(" Chart 2: Top 10 States by Transaction Count")
            df_filtered1 = agg_trans.groupby("States")["Transaction_count"].sum().nlargest(10).reset_index()
            fig = px.bar(df_filtered1, 
                        x="Transaction_count", 
                        y="States", 
                        orientation="h",
                        color="Transaction_count",
                        title="Top 10 States by Transaction Count",  
                        color_continuous_scale="Viridis")
            st.plotly_chart(fig, use_container_width=True)

        elif method_3 == "Most Used Transaction Type by Transaction Count":
             df_filtered2 = agg_trans.groupby("Transaction_type")["Transaction_count"].sum().reset_index().sort_values(by="Transaction_count", ascending=False)
             fig = px.pie(df_filtered2, 
                          names="Transaction_type", 
                          values="Transaction_count", 
                          title="Most Used Transaction Type by Transaction Count")
             st.plotly_chart(fig, use_container_width=True)

        elif method_3 == "Top 10 States by Dominant Transaction Type":
             df_filtered3 = agg_trans.groupby(["States", "Transaction_type"])["Transaction_count"].sum().reset_index()

                # Step 1: For each state, keep only the transaction type with max count (i.e., dominant)
             df_dominant = df_filtered3.sort_values("Transaction_count", ascending=False).drop_duplicates("States")

                # Step 2: Take top 10 states based on dominant transaction count
             df_top10 = df_dominant.sort_values("Transaction_count", ascending=False).head(10)

                # Step 3: Plot
             fig = px.bar(df_top10, x="Transaction_count", y="States", orientation="h",
                            color="Transaction_type", title="Top 10 States by Dominant Transaction Type")
             st.plotly_chart(fig, use_container_width=True)
        
        


        elif method_3 == "Bottom 10 States by Registered Users":
             df_filtered5 = map_users.groupby("States")["RegisteredUsers"].sum().reset_index().sort_values(by="RegisteredUsers", ascending=True).head(10)
             fig = px.bar( df_filtered5, 
                          x="RegisteredUsers", 
                          y="States", orientation="h", 
                          title="Bottom 10 States by Registered Users", 
                          color="RegisteredUsers")
             st.plotly_chart(fig, use_container_width=True)

        elif method_3 == "Bottom 10 States by App Opens":
    # Group by States and get bottom 10 by AppOpens
            df_filtered6 = map_users.groupby("States")["AppOpens"].sum().reset_index() \
                                    .sort_values(by="AppOpens", ascending=True).head(10)

            # Create donut chart
            fig = px.pie(
                df_filtered6,
                names="States",
                values="AppOpens",
                title="Bottom 10 States by App Opens",
                hole=0.4,  # 🍩 This creates donut effect
                color_discrete_sequence=px.colors.sequential.Blues
            )

            # Show percentage and label
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)

        elif method_3 == "Top 10 States by App Opens":
            # Group and get Top 10 states by AppOpens
            
            df_filtered7 = map_users.groupby("States")["AppOpens"].sum().reset_index() \
                         .sort_values(by="AppOpens", ascending=False).head(10)

            # Create donut chart
            fig = px.pie(
                df_filtered7,
                names="States",
                values="AppOpens",
                title="Top 10 States by App Opens",
                hole=0.4,  # 🍩 Donut effect
                color_discrete_sequence=px.colors.sequential.Greens
            )

            # Show percentage + state name
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)

        elif method_3 == "District-wise Registered Users Trend (Year-wise)":

            #  Step 1: State Selection
            selected_state = st.selectbox("Select a State", sorted(map_users["States"].unique()))

            #  Step 2: Filter Data by State
            state_df = map_users[map_users["States"] == selected_state]

            #  Step 3: Top Districts by Total Users (get top 5-10 for simplicity)
            top_districts = (
                state_df.groupby("Districts")["RegisteredUsers"]
                .sum()
                .sort_values(ascending=False)
                .head(5)
                .index
            )

            #  Step 4: Filter only those top districts
            top_districts_df = state_df[state_df["Districts"].isin(top_districts)]

            #  Step 5: Group and Plot Line Chart
            line_df = top_districts_df.groupby(["Years", "Districts"])["RegisteredUsers"].sum().reset_index()

            fig = px.line(
                line_df,
                x="Years",
                y="RegisteredUsers",
                color="Districts",
                markers=True,
                title=f" Year-wise Registered Users Trend – Top Districts in {selected_state}",
            )

            st.plotly_chart(fig, use_container_width=True)
        
        
# ✅ Final Full Version with All 5 Scenarios Fixed for ANALYSIS REPORT tab

# Connection details
username = "rajam"
password = "BxvBus45OU2tt1zO3lzPV3HcXT9yyjRO"
host = "dpg-d1h2a7ili9vc73b83ou0-a.singapore-postgres.render.com"
port = "5432"
database = "raji"

# Step 1: Create engine
engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")


# ⛳ ANALYSIS REPORT Tab Setup
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# 1️⃣ Put this at the top-level (before any tabs or inside if select == "ANALYSIS REPORT")
db_url = "postgresql+psycopg2://neondb_owner:npg_hNu4bqHo5EPQ@ep-aged-bread-a1xghr1f-pooler.ap-southeast-1.aws.neon.tech/Raaji?sslmode=require"
engine = create_engine(
    db_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=2
)

# 2️⃣ Inside your tab logic
if select == "ANALYSIS REPORT":
    st.title("📑 Analysis Report – PhonePe Pulse")
    st.markdown("Real business insights with SQL + Visuals")

    tab5, tab6, tab7, tab8, tab9 = st.tabs([
        "Scenario 1: Decoding Transaction Dynamics",
        "Scenario 2: Device Dominance & User Engagement",
        "Scenario 3: Market Expansion Strategy",
        "Scenario 4: Performance Monitoring",
        "Scenario 5: User Growth Strategy"
    ])

    # ---------------- SCENARIO 1 ----------------
    with tab5:
        st.markdown("**Usage:** Understand overall growth in digital transactions over the years to measure platform adoption.")
        st.subheader("1️⃣ Total Transaction Volume Over Years")
        try:
            df1 = pd.read_sql("""
                SELECT "Years", SUM("Transaction_count") AS total_transactions
                FROM agg_trans
                GROUP BY "Years"
                ORDER BY "Years";
            """, con=engine)

            fig1 = px.bar(df1, x="Years", y="total_transactions",
                          title="Total Transaction Count (2018–2024)")
            st.plotly_chart(fig1, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error fetching transaction count data: {e}")

        st.subheader("2️⃣ Total Transaction Value Over Years")
        try:
            df2 = pd.read_sql("""
                SELECT "Years", SUM("Transaction_amount") AS total_value
                FROM agg_trans
                GROUP BY "Years"
                ORDER BY "Years";
            """, con=engine)

            fig2 = px.bar(df2, x="Years", y="total_value",
                          title="Total Transaction Value (2018–2024)",
                          labels={"total_value": "Total Value (₹)"})
            st.plotly_chart(fig2, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error fetching transaction value data: {e}")

    # ---------------- SCENARIO 2 ----------------
    with tab6:
        st.markdown("**Usage:** Track user registration and app engagement trends to improve device-specific performance.")
        st.subheader("1️⃣ App Opens vs Registered Users Over Years")
        try:
            df3 = pd.read_sql("""
                SELECT "Years", SUM("RegisteredUsers") AS registered_users, SUM("AppOpens") AS app_opens
                FROM map_users
                GROUP BY "Years"
                ORDER BY "Years";
            """, con=engine)

            fig3 = px.bar(df3, x="Years", y=["registered_users", "app_opens"],
                          barmode="group",
                          title="App Opens vs Registered Users (2018–2024)",
                          labels={"value": "Count", "variable": "Metric"})
            st.plotly_chart(fig3, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error fetching user engagement data: {e}")

        st.subheader("2️⃣ Device-Wise Transaction Count")
        try:
            df4 = pd.read_sql("""
                SELECT "Transaction_type", SUM("Transaction_count") AS total_count
                FROM agg_trans
                GROUP BY "Transaction_type"
                ORDER BY total_count DESC;
            """, con=engine)

            fig4 = px.pie(df4, names="Transaction_type", values="total_count",
                          title="Transaction Distribution by Type")
            st.plotly_chart(fig4, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error fetching device-type transaction data: {e}")

    # ---------------- SCENARIO 3 ----------------
    with tab7:
        st.markdown("**Usage:** Identify high- and low-performing regions to plan targeted regional growth strategies.")
        st.subheader("1️⃣ Top 10 States by Transaction Value")
        try:
            df5 = pd.read_sql("""
                SELECT "States", SUM("Transaction_amount") AS total_value
                FROM agg_trans
                GROUP BY "States"
                ORDER BY total_value DESC
                LIMIT 10;
            """, con=engine)

            fig5 = px.bar(df5, x="total_value", y="States",
                          orientation="h",
                          title="Top 10 States by Total Transaction Value",
                          labels={"total_value": "Total Value (₹)", "States": "State"})
            st.plotly_chart(fig5, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error fetching state-wise transaction data: {e}")

        st.subheader("2️⃣ Top 10 Districts by Registered Users")
        try:
            df6 = pd.read_sql("""
                SELECT "Districts", SUM("RegisteredUsers") AS total_users
                FROM map_users
                GROUP BY "Districts"
                ORDER BY total_users DESC
                LIMIT 10;
            """, con=engine)

            fig6 = px.bar(df6, x="Districts", y="total_users",
                          title="Top 10 Districts by Registered Users",
                          labels={"total_users": "Users", "Districts": "District"})
            st.plotly_chart(fig6, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error fetching district-wise user data: {e}")

        # ---------------- SCENARIO 4 ----------------
    with tab8:
        st.markdown("**Usage:** Monitor quarterly activity trends to optimize infrastructure and marketing timing.")
        st.subheader("1️⃣ Quarterly Transaction Trend")
        try:
            df7 = pd.read_sql("""
                SELECT "Years", "Quarters", SUM("Transaction_count") AS total_txn
                FROM agg_trans
                GROUP BY "Years", "Quarters"
                ORDER BY "Years", "Quarters";
            """, con=engine)

            df7["Quarter_Label"] = df7["Years"].astype(str) + " Q" + df7["Quarters"].astype(str)

            fig7 = px.line(df7, x="Quarter_Label", y="total_txn",
                           title="Quarterly Transaction Trend (2018–2024)",
                           labels={"total_txn": "Total Transactions"})
            st.plotly_chart(fig7, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error fetching quarterly transaction data: {e}")

        st.subheader("2️⃣ Quarterly App Opens Trend")
        try:
            df8 = pd.read_sql("""
                SELECT "Years", "Quarters", SUM("AppOpens") AS total_opens
                FROM map_users
                GROUP BY "Years", "Quarters"
                ORDER BY "Years", "Quarters";
            """, con=engine)

            df8["Quarter_Label"] = df8["Years"].astype(str) + " Q" + df8["Quarters"].astype(str)

            fig8 = px.line(df8, x="Quarter_Label", y="total_opens",
                           title="Quarterly App Opens Trend (2018–2024)",
                           labels={"total_opens": "Total App Opens"})
            st.plotly_chart(fig8, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error fetching quarterly app opens data: {e}")

    # ---------------- SCENARIO 5 ----------------
    with tab9:
        st.markdown("**Usage:** Analyze user growth patterns to drive adoption in new and underperforming regions.")
        st.subheader("1️⃣ Year-wise Growth of Registered Users")
        try:
            df9 = pd.read_sql("""
                SELECT "Years", SUM("RegisteredUsers") AS total_users
                FROM map_users
                GROUP BY "Years"
                ORDER BY "Years";
            """, con=engine)

            fig9 = px.area(df9, x="Years", y="total_users",
                           title="Growth of Registered Users Over Years",
                           labels={"total_users": "Registered Users"})
            st.plotly_chart(fig9, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error fetching registered user growth data: {e}")

        st.subheader("2️⃣ State-wise User Penetration (Top 10)")
        try:
            df10 = pd.read_sql("""
                SELECT "States", SUM("RegisteredUsers") AS total_users
                FROM map_users
                GROUP BY "States"
                ORDER BY total_users DESC
                LIMIT 10;
            """, con=engine)

            fig10 = px.bar(df10, x="States", y="total_users",
                           title="Top 10 States by User Penetration",
                           labels={"total_users": "Registered Users"})
            st.plotly_chart(fig10, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Error fetching state-wise user data: {e}")
elif select == "EXIT":
    st.markdown("<h2 style='text-align: center; color: #FF5733;'>🙏 Thank You for Visiting!</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; font-size: 18px;'>
            We hope you enjoyed exploring the PhonePe Pulse Dashboard!<br>
            <br>
            Built with ❤️ using Python, Streamlit, and PostgreSQL.<br>
            <br>
            📊 Keep analyzing. Keep learning. Keep growing!
        </div>
    """, unsafe_allow_html=True)

    st.image("https://media.tenor.com/BS2zM9iT5SAAAAAC/thank-you.gif", use_container_width=True)

    st.markdown("###")
    st.success("Feel free to explore other sections from the sidebar.")
















