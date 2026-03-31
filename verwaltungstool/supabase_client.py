from supabase import create_client, Client
from verwaltungstool.config import settings
from dotenv import load_dotenv

load_dotenv()

supabase: Client = create_client(settings.SUPABASE_API_URL, settings.SUPABASE_API_KEY)