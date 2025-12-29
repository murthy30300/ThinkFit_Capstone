import requests
import streamlit as st

API_URL = "http://localhost:8000"

def login(email, password):
    try:
        response = requests.post(
            f"{API_URL}/token",
            data={"username": email, "password": password} # OAuth2 expects 'username'
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def signup(email, password, full_name):
    # Not implemented in backend explicitly but we can add it or just use login for demo
    # For MVP, let's assume we just use login or add a simple signup endpoint if needed.
    # Wait, I didn't add a signup endpoint in auth.py, only login. 
    # I should probably add one or just auto-create user on login for this demo if not exists?
    # Let's stick to the plan. I'll add a signup helper that just calls a signup endpoint.
    # I need to add signup to backend/auth.py or just mock it?
    # The user said "Login / Signup (demo auth ok)".
    # I'll add a simple signup to backend/auth.py in a bit or just use a "create user" script.
    # Actually, I'll just add a signup endpoint to `auth.py` now to be safe.
    pass

def get_questions(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_URL}/quiz/questions", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []

def submit_quiz(token, answers, time_taken, confidence, hints_used):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "answers": answers,
        "time_taken": time_taken,
        "confidence": confidence,
        "hints_used": hints_used
    }
    response = requests.post(f"{API_URL}/quiz/submit", json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_topics():
    response = requests.get(f"{API_URL}/content/list")
    if response.status_code == 200:
        return response.json()
    return []

def get_content(token, topic, level=None):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"topic": topic}
    if level:
        params["level"] = level
    response = requests.get(f"{API_URL}/content/get", headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def init_session():
    # Check URL params for token
    if "token" in st.query_params:
        token = st.query_params["token"]
        if token:
            st.session_state.token = token
            if "level" in st.query_params:
                st.session_state.user_level = st.query_params["level"]
            if "email" in st.query_params:
                st.session_state.user_email = st.query_params["email"]
    
    # If token exists in session, ensure it's in URL (to persist on refresh)
    if "token" in st.session_state and st.session_state.token:
        st.query_params["token"] = st.session_state.token
        if st.session_state.user_level:
            st.query_params["level"] = st.session_state.user_level
        if st.session_state.user_email:
            st.query_params["email"] = st.session_state.user_email

def init_api_session():
    if "api_session" not in st.session_state:
        st.session_state.api_session = requests.Session()
