import streamlit as st
import requests

st.set_page_config(
    page_title="Learning App",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Session for Cookies
if "api_session" not in st.session_state:
    st.session_state.api_session = requests.Session()

API_URL = "http://127.0.0.1:8000/api"

# Check Auth
if "user" not in st.session_state:
    try:
        # Try to get current user (in case cookies are already set)
        res = st.session_state.api_session.get(f"{API_URL}/me")
        if res.status_code == 200:
            st.session_state.user = res.json()
        else:
            st.session_state.user = None
    except:
        st.session_state.user = None

if not st.session_state.user:
    st.warning("Please login to access the application.")
    st.switch_page("pages/0_Login.py")

st.title(f"Welcome, {st.session_state.user['username']}!")

st.markdown("""
### How it works:
1. **Take the Quiz**: Assess your knowledge level.
2. **Get Your Level**: Beginner, Intermediate, or Advanced.
3. **Personalize**: Choose what kind of content you want (Examples, Code, Visuals, etc.).
4. **Learn**: Explore content tailored just for you.
""")

if st.button("Go to Quiz"):
    st.switch_page("pages/1_Quiz.py")

# Initialize session state if not present
if "attempt_id" not in st.session_state:
    st.session_state.attempt_id = None
if "category" not in st.session_state:
    st.session_state.category = None
if "topic" not in st.session_state:
    st.session_state.topic = "Binary Trees" # Default for MVP
if "selected_preferences" not in st.session_state:
    st.session_state.selected_preferences = []
