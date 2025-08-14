#!/usr/bin/env python3
"""
Script to check database table information and creation times
"""

import psycopg2
from datetime import datetime

# Database connection details
DB_USER = "postgres"
DB_PASSWORD = "tanu1234"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "ai_content_db"

def check_table_info():
    """Check table creation times and other info"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        print("🔍 Database Table Information:")
        print("=" * 50)
        
        # Method 1: Check table creation from system catalogs
        print("\n📋 Method 1: System Catalog Info")
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                tableowner,
                hasindexes,
                hasrules,
                hastriggers,
                rowsecurity
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """)
        
        tables = cursor.fetchall()
        for table in tables:
            print(f"Table: {table[1]}")
            print(f"  Owner: {table[2]}")
            print(f"  Has Indexes: {table[3]}")
            print(f"  Has Rules: {table[4]}")
            print(f"  Has Triggers: {table[5]}")
            print(f"  Row Security: {table[6]}")
            print()
        
        # Method 2: Check table statistics (approximate creation time)
        print("📊 Method 2: Table Statistics")
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                n_tup_ins as inserts,
                n_tup_upd as updates,
                n_tup_del as deletes,
                n_live_tup as live_rows,
                n_dead_tup as dead_rows,
                last_vacuum,
                last_autovacuum,
                last_analyze,
                last_autoanalyze
            FROM pg_stat_user_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """)
        
        stats = cursor.fetchall()
        for stat in stats:
            print(f"Table: {stat[1]}")
            print(f"  Inserts: {stat[2]}")
            print(f"  Updates: {stat[3]}")
            print(f"  Deletes: {stat[4]}")
            print(f"  Live Rows: {stat[5]}")
            print(f"  Dead Rows: {stat[6]}")
            print(f"  Last Vacuum: {stat[7]}")
            print(f"  Last Auto-vacuum: {stat[8]}")
            print(f"  Last Analyze: {stat[9]}")
            print(f"  Last Auto-analyze: {stat[10]}")
            print()
        
        # Method 3: Check table sizes
        print("📏 Method 3: Table Sizes")
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """)
        
        sizes = cursor.fetchall()
        for size in sizes:
            print(f"Table: {size[1]} - Size: {size[2]}")
        
        # Method 4: Check when database was created
        print("\n🗄️ Method 4: Database Creation Info")
        cursor.execute("""
            SELECT 
                datname,
                pg_size_pretty(pg_database_size(datname)) as size,
                datcollate,
                datctype
            FROM pg_database 
            WHERE datname = %s
        """, (DB_NAME,))
        
        db_info = cursor.fetchone()
        if db_info:
            print(f"Database: {db_info[0]}")
            print(f"Size: {db_info[1]}")
            print(f"Collation: {db_info[2]}")
            print(f"Character Type: {db_info[3]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def check_table_structure():
    """Check table structure"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = conn.cursor()
        
        print("\n🏗️ Table Structure:")
        print("=" * 50)
        
        # Check columns for each table
        cursor.execute("""
            SELECT 
                table_name,
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns 
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position
        """)
        
        columns = cursor.fetchall()
        current_table = None
        for col in columns:
            if col[0] != current_table:
                current_table = col[0]
                print(f"\n📋 Table: {current_table}")
                print("-" * 30)
            
            print(f"  {col[1]}: {col[2]} {'(NULL)' if col[3] == 'YES' else '(NOT NULL)'} {f'DEFAULT: {col[4]}' if col[4] else ''}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🔍 Checking Database Information...")
    print(f"Database: {DB_NAME}")
    print(f"Connected at: {datetime.now()}")
    print("=" * 60)
    
    check_table_info()
    check_table_structure()
    
    print("\n💡 Note: PostgreSQL doesn't store exact table creation timestamps.")
    print("   The statistics show when tables were last accessed/modified.")
    print("   Your tables were created when you ran 'python test_db.py'")

if __name__ == "__main__":
    main() 