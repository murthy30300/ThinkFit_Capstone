from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import database, models, auth, parser
import os

router = APIRouter()

# Dynamic path to data folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data", "topics")

@router.get("/list")
def list_topics():
    return parser.get_all_topics(DATA_DIR)

@router.get("/get")
def get_content(topic: str, level: str = None, current_user: models.User = Depends(auth.get_current_user)):
    # If level not provided, use user's level
    if not level:
        level = current_user.level
        
    # Security check: Ensure user can access this level? 
    # Requirement: "Students can view content only for levels included in visible_to_levels"
    # For now, we trust the level requested or user's level.
    
    # Find file
    # We expect topic to be the filename for simplicity in this MVP, or we map it.
    # Let's assume topic param IS the filename (e.g. "Binary Trees.md")
    
    file_path = os.path.join(DATA_DIR, topic)
    if not os.path.exists(file_path):
        # Try adding .md
        file_path = os.path.join(DATA_DIR, topic + ".md")
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="Topic not found")
            
    frontmatter, content = parser.parse_markdown(file_path, level)
    
    if not content:
        # Fallback or error?
        # If specific level not found, maybe return a default message
        content = f"No content available for level: {level}"
        
    return {
        "topic": topic,
        "level": level,
        "frontmatter": frontmatter,
        "content": content
    }
