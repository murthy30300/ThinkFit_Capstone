import streamlit as st
import os

st.set_page_config(page_title="Admin", page_icon="🔧")

if "user" not in st.session_state or not st.session_state.user or st.session_state.user.get("role") != "admin":
    st.error("Access Denied. Admins only.")
    st.stop()

st.title("Admin Panel")

st.write("Upload Markdown content for topics.")

uploaded_file = st.file_uploader("Choose a Markdown file", type="md")

if uploaded_file is not None:
    # Save the file to Data/topics
    # In a real app, we'd send this to the backend via API.
    # For MVP, since we are local, we can save directly or mock the upload.
    # Let's save directly to the shared folder for simplicity if running locally,
    # but strictly speaking we should use the backend. 
    # However, the prompt didn't specify an upload endpoint, just "Admin can upload".
    # Let's implement a simple save here since we have access to the file system.
    
    save_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Data", "topics", uploaded_file.name)
    
    if st.button("Save File"):
        try:
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Saved {uploaded_file.name} to {save_path}")
        except Exception as e:
            st.error(f"Error saving file: {e}")

st.divider()

st.subheader("Existing Topics")
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "Data", "topics")
if os.path.exists(data_dir):
    files = os.listdir(data_dir)
    for f in files:
        st.text(f)
else:
    st.warning("Data directory not found.")
