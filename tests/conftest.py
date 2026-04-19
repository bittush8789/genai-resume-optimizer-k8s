import pytest
import os
import sys

# Make sure the project root is in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["DATABASE_URL"] = "sqlite:///./test_resume_analyzer.db"
os.environ["SECRET_KEY"] = "test-secret-key-for-ci"
os.environ["GEMINI_API_KEY"] = os.environ.get("GEMINI_API_KEY", "test-key")
