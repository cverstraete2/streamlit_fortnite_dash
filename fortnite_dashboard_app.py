import streamlit as st
import pandas as pd
import requests

st.title("Fortnite Island Directory with Engagement Metrics (Live API)")

# Fetch island metadata with pagination
def fetch_islands(limit=10000):
    url = "https://api.fortnite.com/ecosystem/v1/islands"
    islands = []
    page = 1
    while len(islands) < limit:
        response = requests.get(url, params={"page": page, "limit": 100})
        data = response.json().get("data", [])
        if not data:
            break
        islands.extend(data)
        page += 1
    return islands[:limit]

# Fetch engagement metrics for a given island code and interval
def fetch_metrics(code, interval):
    url = f"https://api.fortnite.com/ecosystem/v1/islands/{code}/metrics/{interval}"
    try:
        response = requests.get(url)
        return response.json()
    except:
        return {}

# Fetch island metadata
islands = fetch_islands()

# Prepare combined data
combined_data = []
intervals = ["10m", "1h", "24h"]

for island in islands:
    island_info = {
        "Code": island.get("code"),
        "Creator Code": island.get("creatorCode"),
        "Display Name": island.get("displayName"),
        "Title": island.get("title"),
        "Category": island.get("category", "Unknown"),
        "Created In": island.get("createdIn"),
        "Tags": ", ".join(island.get("tags", []))
    }
    for interval in intervals:
        metrics = fetch_metrics(island_info["Code"], interval)
        island_info[f"Plays ({interval})"] = metrics.get("plays", 0)
        island_info[f"Minutes Played ({interval})"] = metrics.get("minutesPlayed", 0)
        island_info[f"Avg Minutes per Player ({interval})"] = metrics.get("averageMinutesPlayedPerPlayer", 0)
        island_info[f"Peak CCU ({interval})"] = metrics.get("peakConcurrentPlayers", 0)
        island_info[f"Unique Players ({interval})"] = metrics.get("uniquePlayers", 0)
    combined_data.append(island_info)

# Convert to DataFrame
df = pd.DataFrame(combined_data)

# Filter by category
categories = df["Category"].dropna().unique().tolist()
selected_category = st.selectbox("Filter by Category", ["All"] + categories)
if selected_category != "All":
    df = df[df["Category"] == selected_category]

# Sort by selected metric
sort_options = [col for col in df.columns if any(metric in col for metric in ["Plays", "Minutes Played", "Avg Minutes", "Peak CCU", "Unique Players"])]
sort_by = st.selectbox("Sort by Metric", sort_options)
sort_order = st.radio("Sort Order", ["Descending", "Ascending"])
ascending = sort_order == "Ascending"
df_sorted = df.sort_values(by=sort_by, ascending=ascending)

# Display sorted and filtered data
st.subheader("Filtered and Sorted Island Metrics")
st.dataframe(df_sorted) if not df_sorted.empty else st.warning("No data available.")
