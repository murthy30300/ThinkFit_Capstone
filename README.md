# Adaptive Learning Platform MVP

A Streamlit + FastAPI application for adaptive learning.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run Backend:
   ```bash
   cd backend
   uvicorn main:app --reload
   # OR
   python -m uvicorn main:app --reload
   ```

3. Run Frontend:
   ```bash
   cd frontend
   streamlit run app.py
   ```

## Features
- **Adaptive Quiz**: 5 questions, complex scoring (Accuracy, Time, Confidence).
- **Level-based Content**: Shows Beginner/Intermediate/Advanced content from Markdown files.
- **Admin Panel**: Upload new content.
