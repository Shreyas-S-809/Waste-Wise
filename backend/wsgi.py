"""WSGI entry point for Vercel Flask service."""
from app import create_app

app = create_app('production')

