# config.py
DB_FILE = "chat_feedback.db"
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "mistralai/Mistral-7B-Instruct-v0.3"  
)
