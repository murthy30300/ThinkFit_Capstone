from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, auth
import json
import os
from typing import List

router = APIRouter()

# Dynamic path to data folder
# backend/routers/quiz.py -> backend/routers -> backend -> CAPSTONE -> data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
QUESTIONS_FILE = os.path.join(BASE_DIR, "data", "questions.json")

def load_questions():
    if os.path.exists(QUESTIONS_FILE):
        with open(QUESTIONS_FILE, "r") as f:
            return json.load(f)
    return []

@router.get("/questions", response_model=List[models.QuestionPublic])
def get_questions(current_user: models.User = Depends(auth.get_current_user)):
    questions = load_questions()
    # Hide correct answer for frontend
    public_questions = []
    for q in questions:
        pq = q.copy()
        if "correct_index" in pq:
            del pq["correct_index"]
        public_questions.append(pq)
    return public_questions

@router.post("/submit")
def submit_quiz(submission: models.QuizSubmission, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    questions = load_questions()
    correct_count = 0
    total_questions = len(questions)
    
    # Calculate Accuracy
    for q_id, answer_index in submission.answers.items():
        # Find question by ID (assuming simple list index or id match)
        question = next((q for q in questions if q["id"] == int(q_id)), None)
        if question and question["correct_index"] == answer_index:
            correct_count += 1
            
    accuracy = correct_count / total_questions if total_questions > 0 else 0
    
    # Scoring Formula
    # score = clamp(0,1, 0.5*accuracy + 0.15*(1 - avg_time/time_cap) + 0.15*((confidence-1)/4) + 0.15*difficulty_score - 0.1*(hints_used/5))
    
    # Assumptions
    time_cap = 60 * 5 # 5 minutes cap for 5 questions
    avg_time = submission.time_taken
    confidence = submission.confidence # 1-5
    difficulty_score = 0.5 # Average difficulty assumed for now
    hints_used = submission.hints_used
    
    # Normalize components
    time_component = max(0, 1 - (avg_time / time_cap))
    confidence_component = (confidence - 1) / 4
    hints_penalty = (hints_used / 5)
    
    raw_score = (0.5 * accuracy) + (0.15 * time_component) + (0.15 * confidence_component) + (0.15 * difficulty_score) - (0.1 * hints_penalty)
    score = max(0, min(1, raw_score))
    
    # Determine Category
    if score < 0.45:
        category = "Beginner"
    elif score < 0.75:
        category = "Intermediate"
    else:
        category = "Advanced"
        
    # Update User
    current_user.level = category
    db.commit()
    
    # Save Result
    result = models.QuizResult(
        user_id=current_user.id,
        score=score,
        category=category,
        details={"accuracy": accuracy, "raw_score": raw_score}
    )
    db.add(result)
    db.commit()
    
    return {"score": score, "category": category}
