import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".java", ".kt", ".cpp", ".c", ".h", ".hpp", 
    ".php", ".rb", ".go", ".rs", ".cs", ".swift", ".scala",
}

