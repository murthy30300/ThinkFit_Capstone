from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class Question(BaseModel):
    id: int
    text: str
    options: List[str]

class Answer(BaseModel):
    q_id: int
    selected: str
    time: float
    confidence: int

class Attempt(BaseModel):
    user_id: str
    topic: str
    answers: List[Answer]
    score: Optional[float] = None
    category: Optional[str] = None
    created_at: Optional[datetime] = None

class ContentRequest(BaseModel):
    topic: str
    level: str
    preferences: List[str]

class ContentBlock(BaseModel):
    type: str
    title: str
    body_md: str

class ContentResponse(BaseModel):
    topic: str
    level: str
    blocks: List[ContentBlock]

class QuizResult(BaseModel):
    score: float
    category: str
    breakdown: Dict[str, float]

class User(BaseModel):
    username: str
    role: str = "user" # user, admin

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserSignup(BaseModel):
    username: str
    password: str
