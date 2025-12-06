import streamlit as st
from llm_client import generate_feedback
from storage import append_submission

st.set_page_config(
    page_title="Fynd AI Feedback – User Portal",
    page_icon="⭐",
    layout="centered"
)

st.title("⭐ Fynd AI Feedback – User Portal")
st.write("Share your rating and review — our AI assistant will respond instantly.")

with st.form("feedback_form"):
    rating = st.slider("Your rating:", 1, 5, 5)
    review = st.text_area("Write a short review:", height=120)
    submitted = st.form_submit_button("Submit Review")

if submitted:
    if not review.strip():
        st.error("Please write a review before submitting.")
    else:
        with st.spinner("Generating AI response..."):
            user_response, summary, actions = generate_feedback(rating, review)

            # Store in Google Sheets
            append_submission(
                rating=rating,
                review=review.strip(),
                ai_response=user_response,
                ai_summary=summary,
                ai_actions=actions
            )

        st.success("Your feedback has been submitted!")
        st.markdown("### 💬 AI Response")
        st.write(user_response)

        with st.expander("Internal AI Summary & Actions (Preview)"):
            st.markdown(f"**Summary:** {summary}")
            st.markdown(f"**Actions:** {actions}")

st.caption("Powered by Groq Llama 3.3 • Stored securely in Google Sheets")
