
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY=os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
    DB_USER=os.getenv("DB_USER")
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")
    ALLOWED_EXTENSIONS = [ext.strip() for ext in ALLOWED_EXTENSIONS.split(',') if ext.strip()]
    MAX_FILE_SIZE = os.getenv("MAX_FILE_SIZE")
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(os.getenv("PERMANENT_SESSION_LIFETIME")))




    