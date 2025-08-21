
import streamlit as st
import pandas as pd
import requests

# Streamlit dashboard title
st.title("Fortnite Island Directory (Live API)")

# Function to fetch island metadata from Fortnite Data API
def fetch_islands():
    url = "https://api.fortnite.com/ecosystem/v1/islands"
    try:
        response = requests.get(url)
        islands = response.json().get("data", [])
        return islands
    except Exception as e:
        st.error(f"Error fetching island list: {e}")
        return []

# Fetch and display island metadata
islands = fetch_islands()

if islands:
    # Extract relevant fields
    island_data = []
    for island in islands:
        island_data.append({
            "Code": island.get("code"),
            "Creator Code": island.get("creatorCode"),
            "Display Name": island.get("displayName"),
            "Title": island.get("title"),
            "Category": island.get("category"),
            "Created In": island.get("createdIn"),
            "Tags": ", ".join(island.get("tags", []))
        })

    df = pd.DataFrame(island_data)
    st.subheader("Available Islands (Top 1000)")
    st.dataframe(df)
else:
    st.warning("No island data available.")
