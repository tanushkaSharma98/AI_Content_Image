#!/usr/bin/env python3
"""
Simple database setup script
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

# Database connection details
DB_USER = "postgres"
DB_PASSWORD = "tanu1234"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ai_content_db"

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database='postgres'  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database: {DB_NAME}")
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"Database '{DB_NAME}' created successfully!")
        else:
            print(f"Database '{DB_NAME}' already exists.")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def create_env_file():
    """Create .env file with database URL"""
    env_content = f"""# Database Configuration
DATABASE_URL=postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}

# JWT Settings
JWT_SECRET_KEY=your-super-secret-jwt-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# MCP Server URLs
MCP_TAVILY_URL=https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp
MCP_FLUX_URL=https://server.smithery.ai/@falahgs/flux-imagegen-mcp-server/mcp

# App Settings
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("Created .env file with database configuration")

def main():
    """Main setup function"""
    print("Setting up database...")
    
    # Step 1: Create .env file
    create_env_file()
    
    # Step 2: Create database
    if not create_database():
        print("Failed to create database. Exiting.")
        return
    
    print("Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Run: alembic upgrade head")
    print("2. Start the server: uvicorn app.main:app --reload")

if __name__ == "__main__":
    main() 