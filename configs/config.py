import os

# MongoDB configuration
MONGO_URL = os.environ.get("MONGO_URL", "mongodb://mongod:27017/")
MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "google-gemini-model-history-db")
MONGO_COLLECTION_NAME = os.environ.get("MONGO_COLLECTION_NAME", "gemini-2.5-flash-lite-preview-06-17")

# Google Gemini API configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyBSfnmiVwjmYa-UyTVGheYbtfiqAn_JpYI") # This is left intentionally for evaluation purposes. Once evaluated this key will be deprecated
GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.5-flash-lite-preview-06-17")
GEMINI_MODEL_TEMPERATURE = int(os.environ.get("GEMINI_MODEL_TEMPERATURE", "0"))
GEMINI_MODEL_RESPONSE_MIME_TYPE = os.environ.get("GEMINI_MODEL_RESPONSE_MIME_TYPE", "application/json")
