import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "devkey"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTHLIB_INSECURE_TRANSPORT = True  # Nur für dev
    UPLOAD_FOLDER = "app/static/uploads"
