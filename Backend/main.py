from fastapi import FastAPI, HTTPException, Depends, status, Response, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List, Optional
from models import Attempt, ContentRequest, ContentResponse, QuizResult, Question, User, UserInDB, Token, TokenData, UserSignup
from utils import parse_markdown_content, calculate_score, determine_category
from auth import verify_password, get_password_hash, create_access_token, create_refresh_token, verify_token, generate_csrf_token
from database import get_user, create_user, get_questions_by_topic, users_db # users_db needed for direct check in login
import os
from datetime import timedelta

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        # Fallback to header for Swagger UI or other clients
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    return token

async def get_current_user(token: str = Depends(get_token_from_cookie)):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    
    user = get_user(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "topics")

@app.post("/api/signup", response_model=Token)
async def signup(user: UserSignup, response: Response):
    if get_user(user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Hash password
    hashed_password = get_password_hash(user.password)
    
    user_obj = UserInDB(
        username=user.username,
        hashed_password=hashed_password,
        role="user"
    )
    create_user(user_obj)
    
    # Auto-login
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(days=7)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    
    # Set cookies
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, samesite="lax", secure=False)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="lax", secure=False)
    csrf_token = generate_csrf_token()
    response.set_cookie(key="csrf_token", value=csrf_token, httponly=False, samesite="lax", secure=False)

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@app.post("/api/login", response_model=Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    print(f"Login attempt for: {form_data.username}")
    user = get_user(form_data.username)
    if not user:
        print("User not found")
        raise HTTPException(
        )
    print("Login successful")
    
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    refresh_token_expires = timedelta(days=7)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    
    # Set cookies
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=15 * 60,
        samesite="lax",
        secure=False # Set to True in production with HTTPS
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,
        samesite="lax",
        secure=False
    )
    
    # CSRF Token
    csrf_token = generate_csrf_token()
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False, # Accessible to JS for double submit
        samesite="lax",
        secure=False
    )

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@app.post("/api/refresh")
async def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    username = payload.get("sub")
    user_dict = users_db.get(username)
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
    # Rotate tokens
    access_token = create_access_token(data={"sub": username})
    new_refresh_token = create_refresh_token(data={"sub": username})
    
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, samesite="lax", secure=False)
    response.set_cookie(key="refresh_token", value=new_refresh_token, httponly=True, samesite="lax", secure=False)
    
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": new_refresh_token}

@app.get("/api/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post("/api/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    response.delete_cookie("csrf_token")
    return {"message": "Logged out successfully"}

@app.get("/api/questions", response_model=List[Question])
async def get_questions(topic: str, current_user: User = Depends(get_current_active_user)): # Protected
    questions = get_questions_by_topic(topic)
    if not questions:
        raise HTTPException(status_code=404, detail="Topic not found")
    return questions

@app.post("/api/submit", response_model=QuizResult)
async def submit_quiz(attempt: Attempt, current_user: User = Depends(get_current_active_user)): # Protected
    # Calculate score
    score = calculate_score(attempt.answers)
    category = determine_category(score)
    
    # In a real app, we would save the attempt to a DB here
    
    return QuizResult(
        score=score,
        category=category,
        breakdown={
            "accuracy": score,
            "time": sum(a.time for a in attempt.answers),
            "confidence": sum(a.confidence for a in attempt.answers) / len(attempt.answers) if attempt.answers else 0
        }
    )

@app.post("/api/content", response_model=ContentResponse)
async def get_content(request: ContentRequest, current_user: User = Depends(get_current_active_user)): # Protected
    # Construct file path based on topic and level
    # Assuming file naming convention: "{Topic}_{Level}.md" or just "{Topic}.md"
    # For this MVP, let's try "{Topic}.md" first
    
    filename = f"{request.topic}.md"
    file_path = os.path.join(DATA_DIR, filename)
    
    if not os.path.exists(file_path):
         # Try with level suffix if needed, or just fail gracefully
         raise HTTPException(status_code=404, detail=f"Content for topic '{request.topic}' not found")

    blocks = parse_markdown_content(file_path, request.level, request.preferences)
    
    return ContentResponse(
        topic=request.topic,
        level=request.level,
        blocks=blocks
    )

@app.get("/")
async def root():
    return {"message": "FastAPI Backend is running"}
