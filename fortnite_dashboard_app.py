import streamlit as st
import pandas as pd
import requests
import io

# Streamlit dashboard title
st.title("Fortnite Creative Map Analytics Dashboard (Live API)")

# Input for island code
island_code = st.text_input("Enter Fortnite Island Code (e.g., 1234-5678-9101)")
interval = st.selectbox("Select Time Interval", ["10m", "1h", "24h"])

# Function to fetch metrics from Fortnite Data API
def fetch_island_metrics(code, interval):
    base_url = "https://api.fortnite.com/ecosystem/v1/islands"
    metrics_url = f"{base_url}/{code}/metrics/{interval}"
    retention_url = f"{base_url}/{code}/metrics/{interval}/retention"
    try:
        metrics = requests.get(metrics_url).json()
        retention = requests.get(retention_url).json()
        return metrics, retention
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None, None

# Fetch and display data
if island_code:
    metrics, retention = fetch_island_metrics(island_code, interval)
    if metrics and retention:
        data = {
            "Island Code": island_code,
            "Interval": interval,
            "Plays": metrics.get("plays", 0),
            "Minutes Played": metrics.get("minutesPlayed", 0),
            "Avg Minutes per Player": metrics.get("averageMinutesPlayedPerPlayer", 0),
            "Peak CCU": metrics.get("peakConcurrentPlayers", 0),
            "Unique Players": metrics.get("uniquePlayers", 0),
            "Retention D1": retention.get("day1", "N/A"),
            "Retention D7": retention.get("day7", "N/A")
        }
        df = pd.DataFrame([data])

        st.subheader("Island Metrics")
        st.dataframe(df)

        st.subheader("Charts")
        st.bar_chart(df[["Plays", "Minutes Played", "Peak CCU"]])

        st.subheader("Export Data")
        export_format = st.radio("Choose export format", ["Excel", "CSV"])
        if export_format == "Excel":
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
            st.download_button("Download Excel", data=output.getvalue(), file_name="fortnite_live_metrics.xlsx")
        else:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", data=csv, file_name="fortnite_live_metrics.csv")
