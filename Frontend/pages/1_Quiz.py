import streamlit as st
import requests
import time

API_URL = "http://127.0.0.1:8000/api"

st.set_page_config(page_title="Quiz", page_icon="📝")

st.title("Assessment Quiz")

if "questions" not in st.session_state:
    try:
        response = st.session_state.api_session.get(f"{API_URL}/questions", params={"topic": st.session_state.topic})
        if response.status_code == 200:
            st.session_state.questions = response.json()
        elif response.status_code == 401:
             st.error("Session expired. Please login again.")
             st.switch_page("pages/0_Login.py")
        else:
            st.error("Failed to load questions.")
            st.stop()
    except requests.exceptions.ConnectionError:
        st.error("Backend is not running. Please start the FastAPI backend.")
        st.stop()

if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0
    st.session_state.answers = []
    st.session_state.start_time = time.time()

questions = st.session_state.questions
current_index = st.session_state.current_q_index

if current_index < len(questions):
    q = questions[current_index]
    
    st.subheader(f"Question {current_index + 1} of {len(questions)}")
    st.write(q["text"])
    
    # Timer for this question (simple implementation: just tracking time spent)
    # In a real app, we might want a countdown.
    
    option = st.radio("Choose an option:", q["options"], key=f"q_{q['id']}")
    
    confidence = st.slider("Confidence Level (1-5)", 1, 5, 3, key=f"c_{q['id']}")
    
    if st.button("Next" if current_index < len(questions) - 1 else "Submit"):
        # Record answer
        elapsed = time.time() - st.session_state.start_time
        st.session_state.answers.append({
            "q_id": q["id"],
            "selected": option,
            "time": elapsed,
            "confidence": confidence
        })
        
        if current_index < len(questions) - 1:
            st.session_state.current_q_index += 1
            st.session_state.start_time = time.time() # Reset timer for next question
            st.rerun()
        else:
            # Submit quiz
            payload = {
                "user_id": st.session_state.user["username"], # Use actual username
                "topic": st.session_state.topic,
                "answers": st.session_state.answers
            }
            
            try:
                res = st.session_state.api_session.post(f"{API_URL}/submit", json=payload)
                if res.status_code == 200:
                    result = res.json()
                    st.session_state.score = result["score"]
                    st.session_state.category = result["category"]
                    st.session_state.breakdown = result["breakdown"]
                    st.success("Quiz Submitted!")
                    time.sleep(1)
                    st.switch_page("pages/2_Results.py")
                else:
                    st.error("Submission failed.")
            except Exception as e:
                st.error(f"Error submitting quiz: {e}")

else:
    st.write("Quiz completed.")
