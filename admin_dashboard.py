import streamlit as st
import pandas as pd
from storage import load_submissions

st.set_page_config(
    page_title="Fynd Feedback Admin",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Fynd AI Feedback – Admin Dashboard")
st.write("Monitor user feedback, AI summaries, and recommended actions in real time.")

# Reload data on each run
df = load_submissions()

if df.empty:
    st.info("No submissions yet. Ask users to submit feedback from the User Dashboard.")
else:
    # Top-level metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Submissions", len(df))
    with col2:
        st.metric("Average Rating", f"{df['rating'].mean():.2f}")
    with col3:
        st.metric("5-Star Share", f"{(df['rating'] == 5).mean() * 100:.1f}%")

    st.markdown("### Rating Distribution")
    rating_counts = df["rating"].value_counts().sort_index()
    st.bar_chart(rating_counts)

    st.markdown("### All Submissions")
    st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)

    # Filter tools
    st.markdown("### Filter & Inspect")
    ratings_filter = st.multiselect(
        "Filter by rating", options=sorted(df["rating"].unique()), default=sorted(df["rating"].unique())
    )

    filtered = df[df["rating"].isin(ratings_filter)].copy()
    st.write(f"Showing {len(filtered)} matching submissions.")

    # Detailed view
    for _, row in filtered.sort_values("timestamp", ascending=False).iterrows():
        with st.expander(f"{row['timestamp']} – ⭐ {row['rating']}"):
            st.markdown(f"**User review:** {row['review']}")
            st.markdown(f"**AI response to user:** {row['ai_response']}")
            st.markdown(f"**AI summary (internal):** {row['ai_summary']}")
            st.markdown(f"**AI recommended actions:** {row['ai_actions']}")

st.markdown("---")
st.caption("Admin dashboard reading from shared CSV storage.")
