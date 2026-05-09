import os


def read_secret(path: str | None, default: str | None = None) -> str | None:
    if not path:
        return default

    try:
        with open(path, "r", encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        return default


class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")

    DB_PASSWORD = read_secret(
        os.getenv("DB_PASSWORD_FILE")
    )

    SECRET_KEY = read_secret(
        os.getenv("SECRET_KEY_FILE")
    )

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TOKEN_EXPIRE_MINUTES = int(
        os.getenv("TOKEN_EXPIRE_MINUTES", "60")
    )
