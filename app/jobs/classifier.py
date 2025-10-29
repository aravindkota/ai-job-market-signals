"""PURPOSE: Maps jobs to target domains (GenAI agents, Traditional ML, Computer Vision).
"""


# PURPOSE: Map free-text jobs to a domain using simple keyword rules (extend with ontology IDs later).

DOMAIN_KEYWORDS = {
    "GenAI agents": ["genai agent", "agentic ai", "autonomous agent", "langchain", "autogen", "crewai", "rag"],
    "Traditional ML": ["machine learning", "scikit-learn", "xgboost", "catboost", "time series"],
    "Computer Vision": ["computer vision", "opencv", "yolo", "detectron2", "object detection", "ocr"],
}

def classify(text: str) -> str | None:
    t = (text or "").lower()
    for domain, words in DOMAIN_KEYWORDS.items():
        if any(w in t for w in words):
            return domain
    return None
