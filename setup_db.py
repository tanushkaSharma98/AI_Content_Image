#!/usr/bin/env python3
"""
Database setup script
This script will:
1. Create the database if it doesn't exist
2. Run all migrations
3. Create initial admin user (optional)
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from alembic.config import Config
from alembic import command
from app.core.config import settings
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    # Parse the database URL to get connection details
    db_url = settings.database_url
    if db_url.startswith('postgresql+psycopg2://'):
        db_url = db_url.replace('postgresql+psycopg2://', '')
    
    # Extract components
    if '@' in db_url:
        auth_part, rest = db_url.split('@', 1)
        if ':' in auth_part:
            username, password = auth_part.split(':', 1)
        else:
            username, password = auth_part, ''
        
        if '/' in rest:
            host_port, db_name = rest.split('/', 1)
            if ':' in host_port:
                host, port = host_port.split(':', 1)
            else:
                host, port = host_port, '5432'
        else:
            host, port = rest, '5432'
            db_name = ''
    else:
        print("Invalid database URL format")
        return False
    
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database='postgres'  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database: {db_name}")
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Database '{db_name}' created successfully!")
        else:
            print(f"Database '{db_name}' already exists.")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False


def run_migrations():
    """Run Alembic migrations"""
    try:
        # Create Alembic configuration
        alembic_cfg = Config("alembic.ini")
        
        # Run migrations
        print("Running database migrations...")
        command.upgrade(alembic_cfg, "head")
        print("Migrations completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error running migrations: {e}")
        return False


def main():
    """Main setup function"""
    print("Setting up database...")
    
    # Step 1: Create database if it doesn't exist
    if not create_database_if_not_exists():
        print("Failed to create database. Exiting.")
        sys.exit(1)
    
    # Step 2: Run migrations
    if not run_migrations():
        print("Failed to run migrations. Exiting.")
        sys.exit(1)
    
    print("Database setup completed successfully!")
    print("\nNext steps:")
    print("1. Copy env.example to .env and update the DATABASE_URL")
    print("2. Start the FastAPI server: uvicorn app.main:app --reload")
    print("3. Access the API docs at: http://localhost:8000/docs")


if __name__ == "__main__":
    main() 