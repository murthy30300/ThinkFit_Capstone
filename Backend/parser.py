import re
import yaml
import os

def parse_markdown(file_path: str, level: str):
    if not os.path.exists(file_path):
        return None, None

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract Frontmatter
    frontmatter = {}
    if content.startswith("---"):
        try:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])
                content = parts[2]
        except Exception as e:
            print(f"Error parsing frontmatter: {e}")

    # Extract Level Content
    # Pattern: <!-- Level --> ... <!-- /Level -->
    # Case insensitive search for level
    pattern = re.compile(f"<!--\\s*{level}\\s*-->(.*?)<!--\\s*/{level}\\s*-->", re.DOTALL | re.IGNORECASE)
    match = pattern.search(content)

    if match:
        return frontmatter, match.group(1).strip()
    
    return frontmatter, None

def get_all_topics(data_dir: str):
    topics = []
    if not os.path.exists(data_dir):
        return topics
        
    for filename in os.listdir(data_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(data_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                # Read just the first bit to get frontmatter
                content = f.read(1024) 
                if content.startswith("---"):
                    try:
                        parts = content.split("---", 2)
                        if len(parts) >= 2:
                            fm = yaml.safe_load(parts[1])
                            topics.append({
                                "filename": filename,
                                "topic": fm.get("topic", filename),
                                "auth_required": fm.get("auth_required", False)
                            })
                    except:
                        pass
    return topics
