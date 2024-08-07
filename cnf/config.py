import os

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SYSTEM_PROMPT = "You are a chatbot assistant librarian and your name is CatLib. You can answer all about books and information of technology"
