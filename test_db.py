#!/usr/bin/env python3
"""
Simple database test script
"""

import os
from sqlalchemy import create_engine, text
from app.db.base import Base
from app.db.models import user, history

# Database connection details
DATABASE_URL = "postgresql+psycopg2://postgres:tanu1234@localhost:5432/ai_content_db"

def test_connection():
    """Test database connection"""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Database connected successfully!")
            print(f"PostgreSQL version: {version}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_tables():
    """Create tables directly"""
    try:
        engine = create_engine(DATABASE_URL)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ Tables created successfully!")
        
        # List created tables
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            print(f"📋 Created tables: {tables}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to create tables: {e}")
        return False

def main():
    """Main function"""
    print("🔍 Testing database connection...")
    
    if not test_connection():
        return
    
    print("\n🗄️ Creating tables...")
    if not create_tables():
        return
    
    print("\n🎉 Database setup completed successfully!")
    print("You can now start the server with: uvicorn app.main:app --reload")

if __name__ == "__main__":
    main() 