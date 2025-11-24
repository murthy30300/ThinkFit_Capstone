import json
import os
from typing import Dict, List
from models import UserInDB, Question
from auth import get_password_hash

DATA_DIR = os.path.join(os.path.dirname(__file__), "data_storage")
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, "users.json")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.json")

# Initial Mock Data
INITIAL_USERS = {
    "demo_user": {
        "username": "demo_user",
        "hashed_password": get_password_hash("password123"),
        "role": "user"
    },
    "admin": {
        "username": "admin",
        "hashed_password": get_password_hash("admin123"),
        "role": "admin"
    }
}

INITIAL_QUESTIONS = {
    "Binary Trees": [
        {"id": 1, "text": "What is the maximum number of nodes at level 'l' in a binary tree?", "options": ["2^l", "2^(l-1)", "2^(l+1)", "2l"]},
        {"id": 2, "text": "What is the time complexity of searching in a BST (average case)?", "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"]},
        {"id": 3, "text": "Which traversal visits the root first?", "options": ["Inorder", "Preorder", "Postorder", "Level Order"]},
        {"id": 4, "text": "A binary tree with n nodes has how many edges?", "options": ["n", "n-1", "n+1", "2n"]},
        {"id": 5, "text": "In a full binary tree, every node has how many children?", "options": ["0 or 2", "1 or 2", "0 or 1", "Exactly 2"]}
    ]
}

def load_users() -> Dict[str, dict]:
    if not os.path.exists(USERS_FILE):
        save_users(INITIAL_USERS)
        return INITIAL_USERS
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users: Dict[str, dict]):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_questions() -> Dict[str, List[dict]]:
    if not os.path.exists(QUESTIONS_FILE):
        save_questions(INITIAL_QUESTIONS)
        return INITIAL_QUESTIONS
    with open(QUESTIONS_FILE, "r") as f:
        return json.load(f)

def save_questions(questions: Dict[str, List[dict]]):
    with open(QUESTIONS_FILE, "w") as f:
        json.dump(questions, f, indent=4)

# In-memory cache
users_db = load_users()
questions_db = load_questions()

def get_user(username: str) -> UserInDB:
    user_data = users_db.get(username)
    if user_data:
        return UserInDB(**user_data)
    return None

def create_user(user: UserInDB):
    users_db[user.username] = user.dict()
    save_users(users_db)

def get_questions_by_topic(topic: str) -> List[Question]:
    qs = questions_db.get(topic, [])
    return [Question(**q) for q in qs]
