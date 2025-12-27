import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from typing import Tuple, List


def configure_page() -> None:
    """Configure basic Streamlit page settings."""
    st.set_page_config(
        page_title="Sales Analytics Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load sales data from the data directory with caching.

    Returns
    -------
    pd.DataFrame
        Sales dataset with proper dtypes.
    """
    data_path = Path(__file__).parent / "data" / "sales_data.csv"
    df = pd.read_csv(data_path)
    df["order_date"] = pd.to_datetime(df["order_date"])
    return df


def sidebar_filters(df: pd.DataFrame) -> Tuple[pd.Timestamp, pd.Timestamp, List[str], List[str], List[str]]:
    """Render sidebar filters and return selected filter values."""
    st.sidebar.header("Filters")

    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()

    date_range = st.sidebar.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Ensure we always have a tuple of (start, end)
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = min_date
        end_date = max_date

    regions = sorted(df["region"].dropna().unique().tolist())
    selected_regions = st.sidebar.multiselect(
        "Region",
        options=regions,
        default=regions,
    )

    categories = sorted(df["product_category"].dropna().unique().tolist())
    selected_categories = st.sidebar.multiselect(
        "Product Category",
        options=categories,
        default=categories,
    )

    channels = sorted(df["sales_channel"].dropna().unique().tolist())
    selected_channels = st.sidebar.multiselect(
        "Sales Channel",
        options=channels,
        default=channels,
    )

    return pd.to_datetime(start_date), pd.to_datetime(end_date), selected_regions, selected_categories, selected_channels


def apply_filters(
    df: pd.DataFrame,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp,
    regions: List[str],
    categories: List[str],
    channels: List[str],
) -> pd.DataFrame:
    """Filter the dataset based on user selections."""
    mask = (
        (df["order_date"] >= start_date)
        & (df["order_date"] <= end_date)
        & (df["region"].isin(regions) if regions else True)
        & (df["product_category"].isin(categories) if categories else True)
        & (df["sales_channel"].isin(channels) if channels else True)
    )
    filtered = df.loc[mask].copy()
    return filtered


def render_kpis(df: pd.DataFrame) -> None:
    """Render top-level KPI metrics."""
    total_revenue = df["total_sales"].sum()
    total_profit = df["profit"].sum()
    total_orders = df["order_id"].nunique()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"${total_revenue:,.0f}")
    col2.metric("Total Profit", f"${total_profit:,.0f}")
    col3.metric("Total Orders", f"{total_orders:,}")
    col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")


def monthly_sales_trend(df: pd.DataFrame):
    """Create monthly sales trend line chart."""
    if df.empty:
        st.info("No data available for the selected filters.")
        return

    monthly = (
        df.groupby(pd.Grouper(key="order_date", freq="M"))["total_sales"]
        .sum()
        .reset_index()
        .sort_values("order_date")
    )
    monthly["month"] = monthly["order_date"].dt.strftime("%Y-%m")

    fig = px.line(
        monthly,
        x="month",
        y="total_sales",
        title="Monthly Sales Trend",
        markers=True,
    )
    fig.update_layout(xaxis_title="Month", yaxis_title="Total Sales", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)


def sales_by_region(df: pd.DataFrame):
    """Create sales by region bar chart."""
    regional = df.groupby("region", as_index=False)["total_sales"].sum().sort_values("total_sales", ascending=False)

    fig = px.bar(
        regional,
        x="region",
        y="total_sales",
        title="Sales by Region",
        color="region",
    )
    fig.update_layout(xaxis_title="Region", yaxis_title="Total Sales", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def profit_by_category(df: pd.DataFrame):
    """Create profit by product category bar chart."""
    category_profit = df.groupby("product_category", as_index=False)["profit"].sum().sort_values("profit", ascending=False)

    fig = px.bar(
        category_profit,
        x="product_category",
        y="profit",
        title="Profit by Product Category",
        color="product_category",
    )
    fig.update_layout(xaxis_title="Product Category", yaxis_title="Total Profit", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


def sales_channel_distribution(df: pd.DataFrame):
    """Create sales distribution by sales channel pie chart."""
    channel_sales = df.groupby("sales_channel", as_index=False)["total_sales"].sum()

    fig = px.pie(
        channel_sales,
        names="sales_channel",
        values="total_sales",
        title="Sales Channel Distribution",
        hole=0.3,
    )
    st.plotly_chart(fig, use_container_width=True)


def top_products_by_revenue(df: pd.DataFrame, top_n: int = 10):
    """Create horizontal bar chart for top N products by revenue."""
    product_sales = (
        df.groupby("product_name", as_index=False)["total_sales"]
        .sum()
        .sort_values("total_sales", ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        product_sales,
        x="total_sales",
        y="product_name",
        title=f"Top {top_n} Products by Revenue",
        orientation="h",
        color="total_sales",
        color_continuous_scale="Blues",
    )
    fig.update_layout(xaxis_title="Total Sales", yaxis_title="Product", yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)


def render_data_table(df: pd.DataFrame) -> None:
    """Render filtered data table with download option."""
    st.subheader("Filtered Data")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )


def main() -> None:
    """Main application entry point."""
    configure_page()

    st.title("📊 Sales Analytics Dashboard")
    st.markdown(
        "Gain insights into sales performance across regions, products, and channels "
        "with interactive filters and visuals."
    )

    df = load_data()
    start_date, end_date, regions, categories, channels = sidebar_filters(df)
    filtered_df = apply_filters(df, start_date, end_date, regions, categories, channels)

    st.markdown("### Key Performance Indicators")
    render_kpis(filtered_df)

    st.markdown("### Sales Performance")
    col1, col2 = st.columns(2)
    with col1:
        monthly_sales_trend(filtered_df)
    with col2:
        sales_by_region(filtered_df)

    col3, col4 = st.columns(2)
    with col3:
        profit_by_category(filtered_df)
    with col4:
        sales_channel_distribution(filtered_df)

    st.markdown("### Product Insights")
    top_products_by_revenue(filtered_df)

    render_data_table(filtered_df)


if __name__ == "__main__":
    main()


