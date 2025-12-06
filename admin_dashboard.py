import streamlit as st
import pandas as pd
from storage import load_submissions

st.set_page_config(
    page_title="Fynd Feedback – Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Fynd AI Feedback – Admin Dashboard")
st.write("Monitor real-time user feedback, AI summaries, and recommended actions.")

df = load_submissions()

if df.empty:
    st.info("No submissions yet.")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Feedback", len(df))
    col2.metric("Average Rating", f"{df['rating'].mean():.2f}")
    col3.metric("5★ Percentage", f"{(df['rating'] == 5).mean() * 100:.1f}%")

    st.markdown("### ⭐ Rating Distribution")
    st.bar_chart(df["rating"].value_counts().sort_index())

    st.markdown("### 📋 All Submissions")
    st.dataframe(df, use_container_width=True)

    st.markdown("### 🔍 Detailed Review Explorer")
    selected_ratings = st.multiselect(
        "Filter by Rating:",
        options=sorted(df["rating"].unique()),
        default=sorted(df["rating"].unique())
    )

    filtered = df[df["rating"].isin(selected_ratings)]

    for _, row in filtered.iterrows():
        with st.expander(f"{row['timestamp']} — ⭐ {row['rating']}"):
            st.markdown(f"**User Review:** {row['review']}")
            st.markdown(f"**AI Response:** {row['ai_response']}")
            st.markdown(f"**AI Summary:** {row['ai_summary']}")
            st.markdown(f"**AI Actions:** {row['ai_actions']}")

st.caption("Admin-only dashboard • Powered by Groq + Google Sheets backend")
