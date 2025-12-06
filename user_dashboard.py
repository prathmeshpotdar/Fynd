import streamlit as st
from llm_client import generate_feedback
from storage import append_submission

st.set_page_config(
    page_title="Fynd Feedback Portal",
    page_icon="⭐",
    layout="centered"
)

st.title("⭐ Fynd AI Feedback – User Portal")
st.write("Share your rating and review – our AI assistant will respond instantly.")

with st.form("feedback_form"):
    rating = st.slider("How would you rate your experience?", min_value=1, max_value=5, value=5)
    review = st.text_area("Write a short review", height=120, placeholder="Tell us what you liked or what could be improved...")
    submitted = st.form_submit_button("Submit Feedback")

if submitted:
    if not review.strip():
        st.error("Please write a review before submitting.")
    else:
        with st.spinner("Generating AI response..."):
            user_response, summary, actions = generate_feedback(rating, review)

            # Store in shared CSV
            append_submission(
                rating=rating,
                review=review.strip(),
                ai_response=user_response,
                ai_summary=summary,
                ai_actions=actions,
            )

        st.success("Thank you for your feedback! Here's our response:")
        st.markdown("### 💬 AI Response")
        st.write(user_response)

        with st.expander("What our system understood (internal preview)", expanded=False):
            st.markdown(f"**Summary:** {summary}")
            st.markdown(f"**Recommended actions:** {actions}")

st.markdown("---")
st.caption("Powered by Groq Llama-3.1 and built for the Fynd AI Intern assessment.")
