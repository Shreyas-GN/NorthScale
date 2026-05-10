"""
core/dependencies.py

FastAPI dependencies.
"""

from db.supabase import get_supabase_client
from supabase import Client
from fastapi import Request

def get_db() -> Client:
    client = get_supabase_client()
    if not client:
        raise RuntimeError("Database connection not available")
    return client
