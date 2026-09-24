import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'farmease_secret_key_2026_super_secure'
    
    # MySQL Database Settings
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'farmease_db'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
