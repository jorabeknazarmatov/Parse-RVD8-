from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./products.db")

BASE_URL = os.getenv("BASE_URL")