from sqlmodel import create_engine
import os
from dotenv import load_dotenv
from backend.authentication.encryption import hash_password

load_dotenv()

postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_db = os.getenv("POSTGRES_DB")
postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
engine = create_engine(postgres_url)
admin_email = os.getenv("ADMIN_EMAIL")
admin_password = hash_password(os.getenv("ADMIN_PASSWORD"))