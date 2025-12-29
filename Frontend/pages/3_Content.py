import streamlit as st
import requests
from utils import init_api_session

API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="Content", page_icon="📚", layout="wide")

init_api_session()

if "category" not in st.session_state or st.session_state.category is None:
    st.warning("Please take the quiz first to get personalized content.")
    if st.button("Go to Quiz"):
        st.switch_page("pages/1_Quiz.py")
    st.stop()

st.title(f"Personalized Content: {st.session_state.topic}")
st.caption(f"Level: {st.session_state.category}")

# Layout: Two columns
col_sidebar, col_content = st.columns([1, 3])

with col_sidebar:
    st.header("Preferences")
    options = [
        "examples", "practice_problems", "step_by_step", "visuals", 
        "code_python", "code_java", "code_cpp", "test_cases", 
        "complexity", "summary", "interactive", "analogies", 
        "pitfalls", "challenge", "gif_walkthrough", "post_read_quiz"
    ]
    
    # Live update of preferences
    selected_prefs = st.multiselect(
        "Show me:", 
        options, 
        default=st.session_state.selected_preferences,
        key="prefs_sidebar"
    )
    
    # Update session state
    st.session_state.selected_preferences = selected_prefs

with col_content:
    # Fetch content
    payload = {
        "topic": st.session_state.topic,
        "level": st.session_state.category,
        "preferences": st.session_state.selected_preferences
    }
    
    try:
        response = st.session_state.api_session.post(f"{API_URL}/content", json=payload)
        if response.status_code == 200:
            data = response.json()
            blocks = data.get("blocks", [])
            
            if not blocks:
                st.info("No content matches your specific preferences for this topic.")
            
            for block in blocks:
                with st.container():
                    st.subheader(block["title"])
                    st.markdown(block["body_md"])
                    st.divider()
        elif response.status_code == 401:
             st.error("Session expired. Please login again.")
        else:
            st.error("Failed to load content.")
    except Exception as e:
        st.error(f"Error fetching content: {e}")

# Admin/Debug controls (optional, maybe hidden or at bottom)
with st.expander("Debug / Change Topic"):
    new_topic = st.text_input("Topic", value=st.session_state.topic)
    if st.button("Update Topic"):
        st.session_state.topic = new_topic
        st.rerun()
