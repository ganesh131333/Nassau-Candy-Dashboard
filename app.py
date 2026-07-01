import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Factory-to-Customer Shipping Dashboard",
    page_icon="📦",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

/* Main Background */
[data-testid="stAppViewContainer"]{
    background:#F4F7FC;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#0F172A;
}

[data-testid="stSidebar"] *{
    color:white;
}

/* Remove top padding */
.block-container{
    padding-top:2rem;
    padding-left:2rem;
    padding-right:2rem;
}

/* Dashboard Title */
h1{
    color:#1E3A8A;
    font-weight:700;
}

/* Sub Headers */
h2,h3{
    color:#2563EB;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():

    df = pd.read_csv("Nassau_Candy_Cleaned.csv")

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"],
        errors="coerce"
    )

    df["Ship_Date"] = pd.to_datetime(
        df["Ship_Date"],
        errors="coerce"
    )

    return df


df = load_data()

# ======================================================
# HEADER
# ======================================================

st.markdown("""
# 📦 Factory-to-Customer Shipping Route Efficiency Dashboard

### Nassau Candy Distributor

Analyze Sales • Shipping • Profit • Customer Performance

---
""")

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("🎛 Dashboard Filters")

st.sidebar.markdown("---")

# Region

region = st.sidebar.multiselect(

    "Region",

    options=sorted(df["Region"].dropna().unique()),

    default=sorted(df["Region"].dropna().unique())

)

# State

state = st.sidebar.multiselect(

    "State",

    options=sorted(df["State/Province"].dropna().unique()),

    default=sorted(df["State/Province"].dropna().unique())

)

# Ship Mode

ship_mode = st.sidebar.multiselect(

    "Ship Mode",

    options=sorted(df["Ship_Mode"].dropna().unique()),

    default=sorted(df["Ship_Mode"].dropna().unique())

)

# ======================================================
# FILTER DATA
# ======================================================

filtered_df = df[
    (df["Region"].isin(region))
    &
    (df["State/Province"].isin(state))
    &
    (df["Ship_Mode"].isin(ship_mode))
]

# ======================================================
# PRODUCT SEARCH
# ======================================================

search = st.sidebar.text_input(
    "🔍 Search Product"
)

if search:

    filtered_df = filtered_df[
        filtered_df["Product_Name"]
        .str.contains(search,
                      case=False,
                      na=False)
    ]

# ======================================================
# KPI CARDS
# ======================================================

st.subheader("📊 Dashboard Overview")

c1,c2,c3,c4,c5 = st.columns(5)

cards = [

("💰 Total Sales",
 f"${filtered_df['Sales'].sum():,.0f}",
 "#2563EB"),

("📈 Gross Profit",
 f"${filtered_df['Gross_Profit'].sum():,.0f}",
 "#10B981"),

("📦 Orders",
 filtered_df["Order_ID"].nunique(),
 "#F59E0B"),

("👥 Customers",
 filtered_df["Customer_ID"].nunique(),
 "#8B5CF6"),

("🛒 Units Sold",
 int(filtered_df["Units"].sum()),
 "#EF4444")

]

for col, card in zip(
        [c1,c2,c3,c4,c5],
        cards):

    title,value,color = card

    with col:

        st.markdown(f"""

<div style="
background:{color};
padding:18px;
border-radius:15px;
text-align:center;
color:white;
box-shadow:0px 5px 12px rgba(0,0,0,0.20);
">

<h4>{title}</h4>

<h2>{value}</h2>

</div>

""", unsafe_allow_html=True)

st.divider()

st.divider()

# ======================================================
# SALES & GROSS PROFIT BY REGION
# ======================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Sales by Region")

    sales_region = (
        filtered_df.groupby("Region", as_index=False)["Sales"]
        .sum()
        .sort_values(by="Sales", ascending=False)
    )

    fig_sales = px.bar(
        sales_region,
        x="Region",
        y="Sales",
        color="Sales",
        text_auto=".2s",
        color_continuous_scale="Blues"
    )

    fig_sales.update_layout(
        template="plotly_white",
        height=420,
        title="Sales by Region",
        title_x=0.25
    )

    st.plotly_chart(fig_sales, use_container_width=True)

with col2:

    st.subheader("💰 Gross Profit by Region")

    profit_region = (
        filtered_df.groupby("Region", as_index=False)["Gross_Profit"]
        .sum()
        .sort_values(by="Gross_Profit", ascending=False)
    )

    fig_profit = px.bar(
        profit_region,
        x="Region",
        y="Gross_Profit",
        color="Gross_Profit",
        text_auto=".2s",
        color_continuous_scale="Greens"
    )

    fig_profit.update_layout(
        template="plotly_white",
        height=420,
        title="Gross Profit by Region",
        title_x=0.25
    )

    st.plotly_chart(fig_profit, use_container_width=True)

# ======================================================
# MONTHLY SALES TREND
# ======================================================

st.subheader("📅 Monthly Sales Trend")

monthly_df = filtered_df.copy()

monthly_df["Month"] = monthly_df["Order_Date"].dt.month_name()

month_order = [
    "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

monthly_sales = (
    monthly_df.groupby("Month", as_index=False)["Sales"]
    .sum()
)

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Month"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True
)

fig_month.update_layout(
    template="plotly_white",
    height=450,
    title="Monthly Sales Trend",
    title_x=0.35
)

st.plotly_chart(fig_month, use_container_width=True)

# ======================================================
# TOP PRODUCTS & SHIP MODE
# ======================================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df.groupby("Product_Name", as_index=False)["Sales"]
        .sum()
        .sort_values(by="Sales", ascending=False)
        .head(10)
    )

    fig_products = px.bar(
        top_products,
        x="Sales",
        y="Product_Name",
        orientation="h",
        color="Sales",
        text_auto=".2s",
        color_continuous_scale="Viridis"
    )

    fig_products.update_layout(
        template="plotly_white",
        height=500,
        title="Top 10 Products"
    )

    st.plotly_chart(fig_products, use_container_width=True)

with col2:

    st.subheader("🚚 Ship Mode Distribution")

    ship_mode_data = (
        filtered_df["Ship_Mode"]
        .value_counts()
        .reset_index()
    )

    ship_mode_data.columns = ["Ship_Mode", "Count"]

    fig_ship = px.pie(
        ship_mode_data,
        names="Ship_Mode",
        values="Count",
        hole=0.45
    )

    fig_ship.update_layout(
        template="plotly_white",
        height=500,
        title="Ship Mode Distribution"
    )

    st.plotly_chart(fig_ship, use_container_width=True)

# ======================================================
# TOP STATES
# ======================================================

st.subheader("🏙️ Top 10 States by Sales")

top_states = (
    filtered_df.groupby("State/Province", as_index=False)["Sales"]
    .sum()
    .sort_values(by="Sales", ascending=False)
    .head(10)
)

fig_states = px.bar(
    top_states,
    x="Sales",
    y="State/Province",
    orientation="h",
    color="Sales",
    text_auto=".2s",
    color_continuous_scale="Sunset"
)

fig_states.update_layout(
    template="plotly_white",
    height=500,
    title="Top 10 States"
)

st.plotly_chart(fig_states, use_container_width=True)

# ======================================================
# PROFIT MARGIN ANALYSIS
# ======================================================

st.subheader("📊 Profit Margin by Region")

margin_df = (
    filtered_df.groupby("Region", as_index=False)
    .agg({
        "Sales":"sum",
        "Gross_Profit":"sum"
    })
)

margin_df["Profit_Margin"] = (
    margin_df["Gross_Profit"] /
    margin_df["Sales"]
) * 100

fig_margin = px.bar(
    margin_df,
    x="Region",
    y="Profit_Margin",
    color="Profit_Margin",
    text_auto=".2f",
    color_continuous_scale="Tealgrn"
)

fig_margin.update_layout(
    template="plotly_white",
    height=450,
    title="Profit Margin (%)",
    title_x=0.30
)

st.plotly_chart(fig_margin, use_container_width=True)

st.divider()

# ======================================================
# BUSINESS INSIGHTS
# ======================================================

st.subheader("📌 Business Insights")

col1, col2 = st.columns(2)

# ---------- Left Card ----------
with col1:

    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Gross_Profit"].sum()
    total_orders = filtered_df["Order_ID"].nunique()
    total_customers = filtered_df["Customer_ID"].nunique()

    st.success(f"""
### 📊 Overall Performance

💰 **Total Sales:** ${total_sales:,.2f}

📈 **Gross Profit:** ${total_profit:,.2f}

📦 **Total Orders:** {total_orders}

👥 **Customers:** {total_customers}
""")

# ---------- Right Card ----------
with col2:

    if not filtered_df.empty:

        top_region = (
            filtered_df.groupby("Region")["Sales"]
            .sum()
            .idxmax()
        )

        top_product = (
            filtered_df.groupby("Product_Name")["Sales"]
            .sum()
            .idxmax()
        )

        avg_delivery = filtered_df["Delivery_Days"].mean()

        st.info(f"""
### 🏆 Best Performance

🌍 **Top Region:** {top_region}

🍬 **Top Product:** {top_product}

🚚 **Average Delivery:** {avg_delivery:.1f} Days
""")

st.divider()

# ======================================================
# DATASET STATISTICS
# ======================================================

st.subheader("📊 Dataset Statistics")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric("Rows", filtered_df.shape[0])

with s2:
    st.metric("Columns", filtered_df.shape[1])

with s3:
    st.metric("Missing Values",
              int(filtered_df.isnull().sum().sum()))

with s4:
    st.metric("Unique Products",
              filtered_df["Product_Name"].nunique())

st.divider()

# ======================================================
# DOWNLOAD FILTERED DATA
# ======================================================

st.subheader("📥 Download Filtered Dataset")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="Filtered_Nassau_Candy_Data.csv",
    mime="text/csv"
)

st.divider()

# ======================================================
# DATA PREVIEW
# ======================================================

st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=500
)

st.divider()

# ======================================================
# QUICK SUMMARY
# ======================================================

st.subheader("📑 Dashboard Summary")

summary = pd.DataFrame({
    "Metric":[
        "Total Sales",
        "Gross Profit",
        "Orders",
        "Customers",
        "Products"
    ],

    "Value":[
        f"${total_sales:,.2f}",
        f"${total_profit:,.2f}",
        total_orders,
        total_customers,
        filtered_df["Product_Name"].nunique()
    ]
})

st.table(summary)

st.divider()

# ======================================================
# PROFESSIONAL FOOTER
# ======================================================

st.divider()

st.markdown("""
<style>

.footer{
    background: linear-gradient(90deg,#2563EB,#1E40AF);
    padding:20px;
    border-radius:15px;
    color:white;
    text-align:center;
    margin-top:20px;
}

.footer h3{
    color:white;
    margin-bottom:10px;
}

.footer p{
    font-size:16px;
    margin:4px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="footer">

<h3>📦 Factory-to-Customer Shipping Route Efficiency Dashboard</h3>

<p><b>Developed by Ganesh Talmadgi</b></p>

<p>
🐍 Python &nbsp; | &nbsp;
📊 Pandas &nbsp; | &nbsp;
📈 Plotly &nbsp; | &nbsp;
🌐 Streamlit &nbsp; | &nbsp;
📉 Power BI
</p>

<p>Interactive Data Analysis & Visualization Project</p>

<p>© 2026 All Rights Reserved</p>

</div>
""", unsafe_allow_html=True)
