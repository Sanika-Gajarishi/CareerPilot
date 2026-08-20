SKILL_MAP = {

    "python": "Python",

    "fastapi": "FastAPI",
    "fast api": "FastAPI",

    "sql": "SQL",

    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",

    "mysql": "MySQL",

    "mongodb": "MongoDB",

    "git": "Git",

    "github": "GitHub",

    "docker": "Docker",

    "kubernetes": "Kubernetes",

    "redis": "Redis",

    "langchain": "LangChain",

    "langgraph": "LangGraph",

    "chromadb": "ChromaDB",

    "faiss": "FAISS",

    "streamlit": "Streamlit",

    "gradio": "Gradio",

    "tensorflow": "TensorFlow",

    "pytorch": "PyTorch",

    "scikit learn": "Scikit-learn",
    "sklearn": "Scikit-learn",

    "numpy": "NumPy",

    "pandas": "Pandas",

    "opencv": "OpenCV",

    "beautiful soup": "BeautifulSoup",
    "beautifulsoup": "BeautifulSoup",

    "playwright": "Playwright",

    "selenium": "Selenium",

    "gemini": "Google Gemini",

    "openai": "OpenAI",

    "claude": "Claude",

    "rag": "Retrieval-Augmented Generation (RAG)",

    "llm": "Large Language Models (LLMs)",

    "jwt": "JWT",

    "oauth": "OAuth",

    "react": "React",

    "typescript": "TypeScript",

    "javascript": "JavaScript",

    "html": "HTML",

    "css": "CSS",
}


def normalize_skills(skills: list[str]) -> list[str]:

    normalized = []

    seen = set()

    for skill in skills:

        clean = skill.strip().lower()

        clean = clean.replace("-", " ")

        value = SKILL_MAP.get(clean)

        if value is None:

            value = skill.strip()

        if value not in seen:

            normalized.append(value)

            seen.add(value)

    return sorted(normalized)