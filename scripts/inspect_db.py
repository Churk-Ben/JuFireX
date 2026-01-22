import sys
import os
from pathlib import Path
import sqlite3

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from backend.config import Config

def inspect_sqlite_db(db_path):
    print(f"\n{'='*50}")
    print(f"Checking Database: {db_path}")
    print(f"{'='*50}")
    
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("No tables found.")
            return

        for table in tables:
            table_name = table[0]
            print(f"\n--- Table: {table_name} ---")
            
            # Get columns
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [info[1] for info in cursor.fetchall()]
            print(f"Columns: {', '.join(columns)}")
            
            # Get data
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
            rows = cursor.fetchall()
            
            if rows:
                for row in rows:
                    print(row)
            else:
                print("(Empty)")
                
        conn.close()
    except Exception as e:
        print(f"Error reading database: {e}")

if __name__ == "__main__":
    # Ensure directories exist (in case app hasn't run)
    Config.ensure_dirs()
    
    print("Inspecting Databases configured in Config...")
    
    # Check Users DB
    inspect_sqlite_db(Config.PROFILES_DB_PATH)
    
    # Check Navs DB
    inspect_sqlite_db(Config.NAVS_DB_PATH)

    # Check File Repos (Blogs & Projects)
    print(f"\n{'='*50}")
    print("Checking File Repositories")
    print(f"{'='*50}")

    try:
        from backend.data.repositories.blog_repo import BlogRepository
        from backend.data.repositories.project_repo import ProjectRepository

        print("\n--- Blogs ---")
        try:
            blogs = BlogRepository().list_items()
            if blogs:
                for b in blogs[:5]:
                    print(b)
            else:
                print("(Empty)")
        except Exception as e:
            print(f"Error reading blogs: {e}")

        print("\n--- Projects ---")
        try:
            projects = ProjectRepository().list_items()
            if projects:
                for p in projects[:5]:
                    print(p)
            else:
                print("(Empty)")
        except Exception as e:
            print(f"Error reading projects: {e}")
            
    except ImportError as e:
        print(f"Could not import repositories: {e}")
