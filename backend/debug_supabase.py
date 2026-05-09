import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print(f"URL: {url}")
print(f"KEY: {key[:10]}...")

try:
    client = create_client(url, key)
    print("Success!")
except Exception as e:
    print(f"Error: {e}")
