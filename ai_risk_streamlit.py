import streamlit as st
import json

# Load simplified question list
with open("streamlit_question_list.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# Track session state
if "step" not in st.session_state:
    st.session_state.step = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

# Show current question
if st.session_state.step < len(questions):
    q = questions[st.session_state.step]
    
    st.markdown("### Risk classification of AI systems")
    st.markdown(f"**{q['title']}**")
    response = st.radio("", q["options"], key=q["id"])
    
    if q.get("explanation"):
        st.caption(q["explanation"])
    
    col1, col2 = st.columns([1, 5])
    with col2:
        if st.button("Next"):
            st.session_state.answers[q["id"]] = response
            st.session_state.step += 1
else:
    st.success("✅ You completed the initial questions.")
    st.subheader("Collected Answers:")
    st.json(st.session_state.answers)
