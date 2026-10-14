
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="ShopSage AI",
    page_icon="📊",
    layout="wide"
)


st.title("📊 ShopSage AI")
st.subheader("Your AI-Powered Business Decision Assistant")

st.markdown(
    """
    Turn raw sales data into clear business decisions.
    Upload your sales CSV, explore performance, and discover
    actionable opportunities for your business.
    """
)

st.divider()

# Dashboard Navigation Overview
st.markdown("### Explore ShopSage AI")

nav1, nav2, nav3, nav4 = st.columns(4)

nav1.markdown("**📊 Sales Analytics**")
nav2.markdown("**🧹 Data Quality**")
nav3.markdown("**💡 Business Insights**")
nav4.markdown("**📥 Reports**")

st.caption(
    "Scroll through the dashboard to explore each section. "
    "All analytics respond to your selected sales filters."
)

st.divider()


st.write(
    "Analyze sales data and discover useful business insights."
)


# Upload sales data or use the sample dataset
st.sidebar.header("Sales Data")

uploaded_file = st.sidebar.file_uploader(
    "Upload your sales CSV",
    type=["csv"]
)


if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("Your file was uploaded!")
    except Exception as e:
        st.error(f"Could not read the CSV file: {e}")
        st.stop()
else:
    df = pd.read_csv("data/sample_sales.csv")
    st.sidebar.info("Using sample sales data.")

# Check required columns
required_columns = [
    "order_id",
    "order_date",
    "product",
    "category",
    "quantity",
    "unit_price"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        "Your CSV is missing these required columns: "
        + ", ".join(missing_columns)
    )
    st.stop()

# Check missing values
missing_values = int(df[required_columns].isna().sum().sum())

if missing_values > 0:
    st.warning(
        f"Your data contains {missing_values} missing values "
        "in required columns. Please clean the file before analysis."
    )
    st.stop()

# Convert and validate numeric fields
try:
    df["quantity"] = pd.to_numeric(df["quantity"], errors="raise")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="raise")
except (ValueError, TypeError):
    st.error("Quantity and unit_price must contain numeric values.")
    st.stop()

if (df["quantity"] <= 0).any() or (df["unit_price"] < 0).any():
    st.error(
        "Quantity must be positive and unit_price cannot be negative."
    )
    st.stop()

if df.empty:
    st.error("The uploaded CSV contains no sales records.")
    st.stop()



# Data Quality Report
st.subheader("🔎 Data Quality Report")

quality_col1, quality_col2, quality_col3 = st.columns(3)

# Check for duplicate rows
duplicate_rows = int(df.duplicated().sum())

# Check for missing values
missing_cells = int(df[required_columns].isna().sum().sum())

# Check for invalid dates
parsed_dates = pd.to_datetime(df["order_date"], errors="coerce")
invalid_dates = int(parsed_dates.isna().sum())

quality_col1.metric("Duplicate Rows", f"{duplicate_rows:,}")
quality_col2.metric("Missing Required Values", f"{missing_cells:,}")
quality_col3.metric("Invalid Dates", f"{invalid_dates:,}")

if duplicate_rows > 0:
    st.warning(
        f"Found {duplicate_rows} duplicate row(s). "
        "Review them before using the results."
    )
elif missing_cells == 0 and invalid_dates == 0:
    st.success("No duplicate rows, missing required values, or invalid dates detected.")
else:
    st.warning("Some data quality issues were detected. Review the metrics above.")

# Calculate revenue for each row
df["revenue"] = df["quantity"] * df["unit_price"]

# Interactive sales filters
st.sidebar.header("Filter Sales")

# Convert order dates into datetime format
df["order_date"] = pd.to_datetime(
    df["order_date"], errors="coerce"
)

# Remove rows with invalid dates
df = df.dropna(subset=["order_date"])

if df.empty:
    st.error("No valid sales dates were found in your data.")
    st.stop()

# Product filter
products = sorted(df["product"].dropna().unique().tolist())
selected_products = st.sidebar.multiselect(
    "Select Products",
    options=products,
    default=products
)

# Category filter
categories = sorted(df["category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=categories,
    default=categories
)

# Date range filter
min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply the filters
filtered_df = df[
    df["product"].isin(selected_products)
    & df["category"].isin(selected_categories)
].copy()

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered_df = filtered_df[
        filtered_df["order_date"].dt.date.between(
            start_date, end_date
        )
    ]
if filtered_df.empty:
    st.warning(
        "No sales records match your selected filters. "
        "Please choose different filters."
    )
    st.stop()

st.success("Sales data loaded successfully!")

# Display the dataset
st.subheader("Sample Sales Data")
st.dataframe(df, use_container_width=True)


# Filtered Sales Data Preview
st.subheader("📋 Filtered Sales Data")

available_columns = filtered_df.columns.tolist()

selected_columns = st.multiselect(
    "Choose columns to display",
    options=available_columns,
    default=available_columns
)

if selected_columns:
    st.dataframe(
        filtered_df[selected_columns],
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("Please select at least one column to display.")
# Download filtered sales report
st.download_button(
    label="📥 Download Filtered Sales Report",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="shopsage_sales_report.csv",
    mime="text/csv"
)

# Calculate filtered business metrics
total_revenue = filtered_df["revenue"].sum()
total_units = filtered_df["quantity"].sum()
total_orders = filtered_df["order_id"].nunique()

col1, col2, col3 = st.columns(3, gap="large")

col1.metric("Total Revenue", f"{total_revenue:,.0f}")
col2.metric("Units Sold", f"{total_units:,}")
col3.metric("Unique Orders", f"{total_orders:,}")


# Revenue by product

product_revenue = (
    filtered_df.groupby("product", as_index=False)["revenue"]
    .sum()
    .sort_values("revenue", ascending=False)
)


st.subheader("Revenue by Product")

fig = px.bar(
    product_revenue,
    x="product",
    y="revenue",
    title="Total Revenue for Each Product",
    labels={"product": "Product", "revenue": "Revenue"}
)

st.plotly_chart(fig, use_container_width=True)

# Sales Insights Summary
st.subheader("💡 Sales Insights Summary")

insights_by_product = (
    filtered_df.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

if not insights_by_product.empty:
    best_product = insights_by_product.index[0]
    best_revenue = insights_by_product.iloc[0]

    lowest_product = insights_by_product.index[-1]
    lowest_revenue = insights_by_product.iloc[-1]

    insight_col1, insight_col2 = st.columns(2)

    insight_col1.metric(
        "Highest Revenue Product",
        best_product,
        f"{best_revenue:,.2f} revenue"
    )

    insight_col2.metric(
        "Lowest Revenue Product",
        lowest_product,
        f"{lowest_revenue:,.2f} revenue"
    )

    st.info(
        f"{best_product} generated the most revenue in the "
        f"selected data. Review {lowest_product}'s sales and "
        "customer demand before deciding whether to change "
        "its pricing, promotion, or stock levels."
    )

# Product Performance Table
st.subheader("🏆 Product Performance")

product_performance = (
    filtered_df.groupby("product", as_index=False)
    .agg(
        Revenue=("revenue", "sum"),
        Units_Sold=("quantity", "sum"),
        Unique_Orders=("order_id", "nunique")
    )
    .sort_values("Revenue", ascending=False)
)

product_performance["Revenue Share (%)"] = (
    product_performance["Revenue"]
    / product_performance["Revenue"].sum()
    * 100
).round(2)

st.dataframe(
    product_performance,
    use_container_width=True,
    hide_index=True
)

# Top 5 Products by Revenue
st.subheader("🥇 Top 5 Products by Revenue")

top_5_products = product_performance.head(5).sort_values(
    "Revenue", ascending=True
)

top_5_fig = px.bar(
    top_5_products,
    x="Revenue",
    y="product",
    orientation="h",
    title="Highest Revenue-Generating Products",
    labels={
        "Revenue": "Revenue",
        "product": "Product"
    },
    text="Revenue"
)

top_5_fig.update_layout(
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(top_5_fig, use_container_width=True)

# Product Revenue Share
st.subheader("🍩 Product Revenue Share")

revenue_share_fig = px.pie(
    product_performance,
    names="product",
    values="Revenue",
    title="Each Product's Contribution to Revenue",
    hole=0.45
)

revenue_share_fig.update_traces(
    textinfo="label+percent"
)

st.plotly_chart(
    revenue_share_fig,
    use_container_width=True
)


# Daily sales trend
st.subheader("Daily Revenue Trend")

daily_revenue = (
    filtered_df.groupby(
        filtered_df["order_date"].dt.date,
        as_index=False
    )["revenue"]
    .sum()
)

daily_revenue.columns = ["order_date", "revenue"]

trend_fig = px.line(
    daily_revenue,
    x="order_date",
    y="revenue",
    title="Daily Revenue Over Time",
    labels={
        "order_date": "Order Date",
        "revenue": "Revenue"
    },
    markers=True
)

st.plotly_chart(trend_fig, use_container_width=True)

# Daily Sales Summary Table
st.subheader("📅 Daily Sales Summary")

daily_summary = (
    filtered_df.groupby(
        filtered_df["order_date"].dt.date,
        as_index=False
    )
    .agg(
        Revenue=("revenue", "sum"),
        Units_Sold=("quantity", "sum"),
        Unique_Orders=("order_id", "nunique")
    )
)

daily_summary.columns = [
    "Order Date",
    "Revenue",
    "Units Sold",
    "Unique Orders"
]

daily_summary = daily_summary.sort_values(
    "Order Date",
    ascending=False
)

st.dataframe(
    daily_summary,
    use_container_width=True,
    hide_index=True
)


# Category performance
st.subheader("Revenue by Category")


category_revenue = (
    filtered_df.groupby("category", as_index=False)["revenue"]
    .sum()
    .sort_values("revenue", ascending=False)
)


category_fig = px.pie(
    category_revenue,
    names="category",
    values="revenue",
    title="Revenue Contribution by Category",
    hole=0.4
)

st.plotly_chart(category_fig, use_container_width=True)

# Category Revenue Breakdown
st.subheader("📊 Category Revenue Breakdown")

category_breakdown = (
    filtered_df.groupby("category", as_index=False)
    .agg(
        Revenue=("revenue", "sum"),
        Units_Sold=("quantity", "sum")
    )
    .sort_values("Revenue", ascending=False)
)

category_breakdown["Revenue Share (%)"] = (
    category_breakdown["Revenue"]
    / category_breakdown["Revenue"].sum()
    * 100
).round(2)

st.dataframe(
    category_breakdown,
    use_container_width=True,
    hide_index=True
)

category_bar_fig = px.bar(
    category_breakdown,
    x="category",
    y="Revenue",
    title="Revenue by Category",
    labels={
        "category": "Category",
        "Revenue": "Revenue"
    },
    text="Revenue"
)

st.plotly_chart(category_bar_fig, use_container_width=True)

# Revenue Goal Tracker
st.subheader("🎯 Revenue Goal Tracker")

revenue_goal = st.number_input(
    "Enter your revenue goal",
    min_value=1.0,
    value=10000.0,
    step=500.0
)

goal_progress = total_revenue / revenue_goal
progress_percent = min(goal_progress, 1.0) * 100
remaining_revenue = max(revenue_goal - total_revenue, 0)

goal_col1, goal_col2 = st.columns(2)

goal_col1.metric(
    "Revenue Goal",
    f"{revenue_goal:,.2f}"
)

goal_col2.metric(
    "Revenue Still Needed",
    f"{remaining_revenue:,.2f}"
)

st.progress(goal_progress if goal_progress < 1 else 1.0)

st.write(f"**Goal achieved:** {progress_percent:.1f}%")

# Revenue Goal Status
if goal_progress >= 1:
    st.success("Status: Revenue goal achieved!")
elif goal_progress >= 0.75:
    st.info("Status: Nearly there — at least 75% of the goal achieved.")
elif goal_progress >= 0.40:
    st.warning("Status: In progress — keep monitoring sales.")
else:
    st.write("Status: Early progress — review sales opportunities.")


if total_revenue >= revenue_goal:
    st.success("Congratulations! Your selected sales data has reached the revenue goal.")
else:
    st.info(
        f"You need another {remaining_revenue:,.2f} in revenue "
        "to reach your goal."
    )


# Smart Business Recommendations
st.subheader("Smart Business Recommendations")

# Identify the best-performing product and category
product_revenue = (
    filtered_df.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

category_revenue = (
    filtered_df.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
)

top_product = product_revenue.index[0]
top_product_revenue = product_revenue.iloc[0]

top_category = category_revenue.index[0]
top_category_revenue = category_revenue.iloc[0]

col1, col2 = st.columns(2)

with col1:
    st.metric("Top Product", top_product)
    st.write(f"Revenue: {top_product_revenue:,.0f}")

with col2:
    st.metric("Top Category", top_category)
    st.write(f"Revenue: {top_category_revenue:,.0f}")

st.markdown("### Recommended Actions")

# Recommendation 1: Best-performing product
st.info(
    f"**Product opportunity:** {top_product} generates the "
    f"highest revenue ({top_product_revenue:,.0f}) in the "
    "currently selected data. Review its stock availability "
    "and sales consistency before increasing inventory."
)

# Recommendation 2: Category performance
st.info(
    f"**Category opportunity:** {top_category} leads with "
    f"revenue of {top_category_revenue:,.0f}. Consider "
    "reviewing customer demand and the performance of other "
    "products in this category."
)

# Recommendation 3: Revenue per unique order
average_order_value = (
    total_revenue / total_orders if total_orders > 0 else 0
)

st.info(
    f"**Order value:** Average revenue per unique order is "
    f"{average_order_value:,.2f}. Compare this metric across "
    "different periods to understand changes in purchasing."
)

st.caption(
    "These recommendations are generated from sales patterns. "
    "They are decision-support suggestions, not guarantees."
)
# Downloadable Business Summary
st.subheader("📄 Business Summary")

summary_text = f"""
SHOPSAGE AI — SALES SUMMARY
===========================

Total Revenue: {total_revenue:,.2f}
Total Units Sold: {total_units:,}
Unique Orders: {total_orders:,}
Average Revenue per Order: {average_order_value:,.2f}

TOP-PERFORMING PRODUCT
---------------------
Product: {top_product}
Revenue: {top_product_revenue:,.2f}

TOP-PERFORMING CATEGORY
----------------------
Category: {top_category}
Revenue: {top_category_revenue:,.2f}

BUSINESS RECOMMENDATIONS
------------------------
1. Review stock availability for the top revenue-generating product.
2. Monitor category performance to identify sales opportunities.
3. Compare average order value across different periods.

Note: Recommendations are based on the selected sales data.
Review business context before making inventory or pricing decisions.
"""

st.download_button(
    label="📥 Download Business Summary",
    data=summary_text,
    file_name="shopsage_business_summary.txt",
    mime="text/plain"
)
# Download Key Performance Indicators
st.subheader("📈 Export Key Business Metrics")

kpi_report = pd.DataFrame({
    "Metric": [
        "Total Revenue",
        "Units Sold",
        "Unique Orders",
        "Average Revenue per Order",
        "Revenue Goal",
        "Goal Achieved (%)"
    ],
    "Value": [
        total_revenue,
        total_units,
        total_orders,
        average_order_value,
        revenue_goal,
        round(progress_percent, 2)
    ]
})

st.download_button(
    label="📥 Download KPI Report",
    data=kpi_report.to_csv(index=False).encode("utf-8"),
    file_name="shopsage_kpi_report.csv",
    mime="text/csv"
)


# ShopSage AI Business Question-Answering Assistant
st.divider()
st.header("🤖 Ask ShopSage AI")
st.write(
    "Ask questions about your sales data in simple English. "
    "Answers use your currently selected filters."
)

question = st.text_input(
    "What would you like to know?",
    placeholder="e.g. Which product generated the most revenue?"
)

if st.button("Get Answer", type="primary"):
    if not question.strip():
        st.warning("Please enter a question first.")
    else:
        q = question.lower().strip()

        if any(word in q for word in ["revenue", "sales", "income"]):
            if any(word in q for word in ["category", "categories"]):
                group = filtered_df.groupby("category")["revenue"].sum()
                if any(word in q for word in ["lowest", "worst", "least"]):
                    name = group.idxmin()
                    st.info(
                        f"{name} has the lowest revenue: "
                        f"{group.min():,.2f}."
                    )
                else:
                    name = group.idxmax()
                    st.success(
                        f"{name} has the highest category revenue: "
                        f"{group.max():,.2f}."
                    )

            elif any(word in q for word in ["product", "item"]):
                group = filtered_df.groupby("product")["revenue"].sum()
                if any(word in q for word in ["lowest", "worst", "least"]):
                    name = group.idxmin()
                    st.info(
                        f"{name} has the lowest product revenue: "
                        f"{group.min():,.2f}."
                    )
                else:
                    name = group.idxmax()
                    st.success(
                        f"{name} has the highest product revenue: "
                        f"{group.max():,.2f}."
                    )

            elif any(word in q for word in ["day", "date", "daily"]):
                group = filtered_df.groupby(
                    filtered_df["order_date"].dt.date
                )["revenue"].sum()
                best_day = group.idxmax()
                st.success(
                    f"The highest-sales day was {best_day}, "
                    f"with revenue of {group.max():,.2f}."
                )

            else:
                st.success(
                    f"Total revenue for your selected data is "
                    f"{total_revenue:,.2f}."
                )

        elif any(word in q for word in ["unit", "quantity", "items sold"]):
            st.success(f"Total units sold: {total_units:,.0f}.")

        elif any(word in q for word in ["order", "transaction"]):
            st.success(f"Unique orders: {total_orders:,}.")

        elif any(word in q for word in ["average", "aov", "per order"]):
            st.success(
                f"Average revenue per unique order: "
                f"{average_order_value:,.2f}."
            )

        elif any(word in q for word in ["recommend", "improve", "advice"]):
            st.info(
                f"Start by reviewing {top_product}, your highest-revenue "
                f"product, and {top_category}, your highest-revenue "
                "category. Check stock, demand, and profit margins "
                "before making business changes."
            )

        else:
            st.warning(
                "I cannot answer that question yet. Try asking about "
                "revenue, products, categories, sales days, units sold, "
                "orders, average order value, or business recommendations."
            )

st.caption(
    "Answers are calculated from your selected sales data. "
    "This initial assistant uses predefined question patterns, "
    "not a generative AI model."
)



