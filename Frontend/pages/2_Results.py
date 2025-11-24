import streamlit as st

st.set_page_config(page_title="Results", page_icon="🏆")

st.title("Your Results")

if "category" not in st.session_state or st.session_state.category is None:
    st.warning("No results found. Please take the quiz first.")
    if st.button("Go to Quiz"):
        st.switch_page("pages/1_Quiz.py")
    st.stop()

st.header(f"You are assigned: {st.session_state.category}")
st.metric("Score", f"{st.session_state.score * 100:.0f}%")

if "breakdown" in st.session_state:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg Confidence", f"{st.session_state.breakdown['confidence']:.1f}/5")
    with col2:
        st.metric("Total Time", f"{st.session_state.breakdown['time']:.1f}s")

st.divider()

st.subheader("Customize Your Learning Experience")
st.write("Select the content types you prefer:")

options = [
    "examples", "practice_problems", "step_by_step", "visuals", 
    "code_python", "code_java", "code_cpp", "test_cases", 
    "complexity", "summary", "interactive", "analogies", 
    "pitfalls", "challenge", "gif_walkthrough", "post_read_quiz"
]

selected = st.multiselect("Preferences", options, default=["examples", "code_python", "visuals"])

if st.button("Generate My Learning View"):
    st.session_state.selected_preferences = selected
    st.switch_page("pages/3_Content.py")
