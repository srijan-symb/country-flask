import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASE_DIR, '../instance/countries.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "your_default_secret_key")
