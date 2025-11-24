import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="Login", page_icon="🔒")

st.title("Login")

if "user" in st.session_state and st.session_state.user:
    st.success(f"Logged in as {st.session_state.user['username']}")
    if st.button("Logout"):
        try:
            st.session_state.api_session.post(f"{API_URL}/logout")
        except:
            pass
        st.session_state.user = None
        st.session_state.api_session.cookies.clear()
        st.rerun()
    st.stop()

tab1, tab2 = st.tabs(["Login", "Sign Up"])

with tab1:
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Login"):
        if not username or not password:
            st.error("Please enter both username and password")
        else:
            try:
                # Use the session to persist cookies
                res = st.session_state.api_session.post(
                    f"{API_URL}/login", 
                    data={"username": username, "password": password}
                )
                
                if res.status_code == 200:
                    st.success("Login successful!")
                    # Fetch user info
                    user_res = st.session_state.api_session.get(f"{API_URL}/me")
                    if user_res.status_code == 200:
                        st.session_state.user = user_res.json()
                        st.switch_page("app.py")
                    else:
                        st.error("Failed to fetch user info")
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Login failed: {e}")

with tab2:
    new_username = st.text_input("Choose a Username", key="signup_user")
    new_password = st.text_input("Choose a Password", type="password", key="signup_pass")
    
    if st.button("Sign Up"):
        if not new_username or not new_password:
            st.error("Please enter both username and password")
        else:
            try:
                payload = {"username": new_username, "password": new_password}
                res = st.session_state.api_session.post(f"{API_URL}/signup", json=payload)
                
                if res.status_code == 200:
                    st.success("Signup successful! Logging you in...")
                    # Fetch user info
                    user_res = st.session_state.api_session.get(f"{API_URL}/me")
                    if user_res.status_code == 200:
                        st.session_state.user = user_res.json()
                        st.switch_page("app.py")
                    else:
                        st.error("Failed to fetch user info")
                elif res.status_code == 400:
                    st.error("Username already exists")
                else:
                    st.error("Signup failed")
            except Exception as e:
                st.error(f"Signup failed: {e}")

st.info("Demo Credentials: demo_user / password123")
