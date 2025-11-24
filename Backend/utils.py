import re
import os
from typing import List, Dict
from models import ContentBlock

def parse_markdown_content(file_path: str, level: str, preferences: List[str]) -> List[ContentBlock]:
    """
    Parses a markdown file and extracts blocks based on level and preferences.
    """
    if not os.path.exists(file_path):
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = []
    
    # This is a simplified parser. In a real app, we might need a more robust one.
    # We assume blocks are marked like <!-- type:start --> ... <!-- type:end -->
    # and code blocks are ```lang ... ```
    
    # Map preferences to regex patterns or logic
    # For now, let's implement a basic extraction based on the prompt's block mapping
    
    block_mappings = {
        "examples": (r"<!-- examples:start -->", r"<!-- examples:end -->"),
        "practice_problems": (r"<!-- practice:start -->", r"<!-- practice:end -->"),
        "step_by_step": (r"<!-- steps:start -->", r"<!-- steps:end -->"),
        "visuals": (r"<!-- visuals:start -->", r"<!-- visuals:end -->"),
        "test_cases": (r"<!-- testcases:start -->", r"<!-- testcases:end -->"),
        "complexity": (r"<!-- complexity:start -->", r"<!-- complexity:end -->"),
        "summary": (r"<!-- summary:start -->", r"<!-- summary:end -->"),
        "interactive": (r"<!-- interactive:start -->", r"<!-- interactive:end -->"),
        "analogies": (r"<!-- analogies:start -->", r"<!-- analogies:end -->"),
        "pitfalls": (r"<!-- pitfalls:start -->", r"<!-- pitfalls:end -->"),
        "challenge": (r"<!-- challenge:start -->", r"<!-- challenge:end -->"),
        "gif_walkthrough": (r"<!-- gif:start -->", r"<!-- gif:end -->"),
        "post_read_quiz": (r"<!-- postquiz:start -->", r"<!-- postquiz:end -->"),
    }

    # Code blocks are special
    code_mappings = {
        "code_python": "python",
        "code_java": "java",
        "code_cpp": "cpp"
    }

    # First, let's try to filter by level if the file has level-specific sections
    # If the file is structured with level headers, we might need to extract that section first.
    # For this MVP, let's assume the file content is already appropriate for the level 
    # OR that we pass the level to filter specific level blocks if they exist.
    # The prompt says "markdown files split by level and block tags", which implies 
    # we might have `Binary Trees_Beginner.md` or sections. 
    # Let's assume separate files for simplicity or a single file with all content.
    # Given the prompt "Render only selected content blocks for the assigned level",
    # let's assume we look for a file named `{Topic}_{Level}.md` first.
    
    # Filter content by level if level tags exist
    level_pattern = re.compile(f"<!-- level:{level.lower()} -->(.*?)<!-- level:end -->", re.DOTALL | re.IGNORECASE)
    level_match = level_pattern.search(content)
    
    if level_match:
        # If level tags are found, only process the content within that level's block
        content_to_process = level_match.group(1)
    else:
        # If no level tags found, assume the file is generic or specific to this level already
        # (Or we could return empty if we want to be strict)
        content_to_process = content

    # Extended block mappings to include code tags if the user uses them (allows for headers inside)
    block_mappings.update({
        "code_python": (r"<!-- code_python:start -->", r"<!-- code_python:end -->"),
        "code_java": (r"<!-- code_java:start -->", r"<!-- code_java:end -->"),
        "code_cpp": (r"<!-- code_cpp:start -->", r"<!-- code_cpp:end -->"),
    })

    processed_prefs = set()

    for pref in preferences:
        if pref in block_mappings:
            start_tag, end_tag = block_mappings[pref]
            pattern = re.compile(f"{re.escape(start_tag)}(.*?){re.escape(end_tag)}", re.DOTALL)
            matches = pattern.findall(content_to_process)
            if matches:
                processed_prefs.add(pref)
                for match in matches:
                    # If it's a code block from tags, we use the tag name as title or derive it
                    title = pref.replace("_", " ").title()
                    if "Code" in title and "Code" not in title.replace("Code", ""): # Avoid "Code Code"
                         pass 
                    blocks.append(ContentBlock(type=pref, title=title, body_md=match.strip()))
        
        # Fallback for code blocks if no tags were found
        if pref in code_mappings and pref not in processed_prefs:
            lang = code_mappings[pref]
            pattern = re.compile(f"```?{lang}(.*?)```", re.DOTALL)
            matches = pattern.findall(content_to_process)
            for match in matches:
                blocks.append(ContentBlock(type=pref, title=f"{lang.capitalize()} Code", body_md=f"```{lang}\n{match.strip()}\n```"))

    return blocks

def calculate_score(answers: List[Dict]) -> float:
    """
    Calculates the score based on answers.
    Simple implementation: 1 point per correct answer.
    """
    # In a real app, we'd check against a key. 
    # For this MVP, let's assume we have a way to validate.
    # Since we don't have a database of correct answers yet, 
    # let's mock the correctness for the demo or assume the client sends correctness?
    # No, backend should validate.
    # Let's add a simple answer key mechanism or mock it.
    
    # Mock logic: If selected option is 'A', it's correct (just for MVP flow if no key provided)
    # OR better, we define the key in the questions data.
    
    correct_count = 0
    for ans in answers:
        # Placeholder logic
        if ans.selected == "A": 
            correct_count += 1
            
    return correct_count / len(answers) if answers else 0

def determine_category(score: float) -> str:
    if score >= 0.8:
        return "Advanced"
    elif score >= 0.5:
        return "Intermediate"
    else:
        return "Beginner"
