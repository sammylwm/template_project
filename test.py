from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DB_URL")
print(db_url)  # Выведет: localhost:5432