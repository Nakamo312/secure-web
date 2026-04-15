import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://site_user:strong_password_123@db:5432/site_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "60"))
