import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    SUPABASE_URL = os.getenv("SUPABASE_URL", "your_url")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "your_key")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret")
    WTF_CSRF_ENABLED = True
