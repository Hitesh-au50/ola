import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    # Read the CSV file into a DataFrame
    df = pd.read_csv("OLA_Final_Cleaned_Data.csv")
    return df

df = load_data()

# -------------------------------
# Dashboard Title & Sidebar
# -------------------------------
st.set_page_config(page_title="Ola Ride Insights", layout="wide")
st.title("🚖 Ola Ride Insights Dashboard")
st.markdown("A professional analytics dashboard built on OLA ride data.")

# Sidebar filters for Vehicle Type and Payment Method
st.sidebar.header("🔍 Filters")
vehicle_filter = st.sidebar.multiselect("Select Vehicle Type", df["Vehicle_Type"].unique())
payment_filter = st.sidebar.multiselect("Select Payment Method", df["Payment_Method"].unique())

# Apply filters to the dataset
filtered_df = df.copy()
if vehicle_filter:
    filtered_df = filtered_df[filtered_df["Vehicle_Type"].isin(vehicle_filter)]
if payment_filter:
    filtered_df = filtered_df[filtered_df["Payment_Method"].isin(payment_filter)]

# -------------------------------
# KPIs Section
# -------------------------------
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

# Calculate KPIs
total_bookings = len(filtered_df)
successful_rides = filtered_df[filtered_df['Booking_Status'] == 'Success'].shape[0]
canceled_by_driver = filtered_df[filtered_df['Booking_Status'] == 'Canceled By Driver'].shape[0]
canceled_by_customer = filtered_df[filtered_df['Booking_Status'] == 'Canceled By Customer'].shape[0]
cancelled_rides = canceled_by_driver + canceled_by_customer
total_revenue = filtered_df[filtered_df['Booking_Status'] == 'Success']['Booking_Value'].sum()

# Display KPIs
col1.metric("Total Bookings", f"{total_bookings:,}")
col2.metric("Successful Rides", f"{successful_rides:,}")
col3.metric("Cancelled Rides", f"{cancelled_rides:,}")
col4.metric("Revenue (₹)", f"{total_revenue:,.0f}")

st.markdown("---")

# -------------------------------
# Charts in Tabs
# -------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Ride Trends", 
    "🚘 Vehicle Analysis", 
    "💳 Payments", 
    "⭐ Ratings", 
    "❌ Cancellation Reasons"
])

# -------------------------------
# Tab 1: Ride Trends
# -------------------------------
with tab1:
    st.subheader("Ride Volume Over Time")
    # Group rides by Date
    ride_volume = filtered_df.groupby("Date").size().reset_index(name="Ride_Count")
    ride_volume["Date"] = pd.to_datetime(ride_volume["Date"])
    # Line chart of rides per day
    fig = px.line(ride_volume, x="Date", y="Ride_Count", title="Daily Ride Volume")
    fig.update_traces(mode="lines+markers")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Booking Status Breakdown")
    # Count booking statuses
    status_counts = filtered_df['Booking_Status'].value_counts().reset_index()
    status_counts.columns = ['Booking_Status', 'count']
    # Pie chart of booking status distribution
    fig = px.pie(status_counts, names="Booking_Status", values="count", title="Booking Status Distribution")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Tab 2: Vehicle Analysis
# -------------------------------
with tab2:
    st.subheader("Revenue by Vehicle Type")
    vehicle_revenue = filtered_df.groupby("Vehicle_Type")['Booking_Value'].sum().reset_index()
    # Bar chart of revenue by vehicle type
    fig = px.bar(vehicle_revenue, x="Vehicle_Type", y="Booking_Value", text_auto=True, title="Revenue by Vehicle Type")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Tab 3: Payments
# -------------------------------
with tab3:
    st.subheader("Revenue by Payment Method")
    payment_revenue = filtered_df.groupby("Payment_Method")['Booking_Value'].sum().reset_index()
    # Pie chart of revenue by payment method
    fig = px.pie(payment_revenue, names="Payment_Method", values="Booking_Value", title="Revenue by Payment Method")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Tab 4: Ratings
# -------------------------------
with tab4:
    st.subheader("Average Customer Ratings by Vehicle Type")
    ratings = filtered_df.groupby("Vehicle_Type")['Customer_Rating'].mean().reset_index()
    ratings['Customer_Rating'] = ratings['Customer_Rating'].round(2)
    # Bar chart of average customer ratings
    fig = px.bar(ratings, x="Vehicle_Type", y="Customer_Rating", text="Customer_Rating", title="Average Customer Ratings")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Average Driver Ratings by Vehicle Type")
    driver_ratings = filtered_df.groupby("Vehicle_Type")['Driver_Ratings'].mean().reset_index()
    driver_ratings['Driver_Ratings'] = driver_ratings['Driver_Ratings'].round(2)
    # Bar chart of average driver ratings
    fig2 = px.bar(driver_ratings, x="Vehicle_Type", y="Driver_Ratings", text="Driver_Ratings", title="Average Driver Ratings")
    st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Tab 5: Cancellation Reasons
# -------------------------------
with tab5:
    st.subheader("Cancellation Reasons")
    # Filter only cancellation-related statuses
    cancel_reasons = filtered_df[filtered_df['Booking_Status'].isin(['Canceled By Driver', 'Canceled By Customer'])]
    # Count cancellations by type
    reason_counts = cancel_reasons['Booking_Status'].value_counts().reset_index()
    reason_counts.columns = ['Reason', 'Count']
    # Bar chart of cancellation reasons
    fig = px.bar(reason_counts, x="Reason", y="Count", text_auto=True, title="Cancellation Reasons Breakdown")
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Top Customers
# -------------------------------
st.subheader("👥 Top 5 Customers by Booking Value")
top_customers = filtered_df.groupby("Customer_ID")['Booking_Value'].sum().nlargest(5).reset_index()
st.table(top_customers)

# -------------------------------
# Business Insights
# -------------------------------
st.subheader("💡 Business Insights & Recommendations")
st.info("""
- **Reduce Cancellations**: Incentivize drivers and enforce accountability.  
- **Promote Digital Payments**: Push UPI adoption to reduce cash handling.  
- **Reward Loyal Customers**: Offer loyalty programs to top riders.  
- **Improve Driver Allocation**: Optimize peak-hour assignments.  
- **Monitor Service Quality**: Train and support low-rated drivers.  
""")

# -------------------------------
# Download Option
# -------------------------------
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_ola_data.csv",
    mime="text/csv"
)
