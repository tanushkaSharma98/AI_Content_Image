#!/usr/bin/env python3
"""
Master setup script for AI Content Explorer
This script will:
1. Start the database using Docker Compose
2. Set up the backend environment
3. Run database migrations
4. Provide instructions for frontend setup
"""

import os
import sys
import subprocess
import time
from pathlib import Path


def run_command(command, cwd=None, check=True):
    """Run a shell command and return the result"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return e


def check_docker():
    """Check if Docker is installed and running"""
    print("Checking Docker installation...")
    result = run_command("docker --version", check=False)
    if result.returncode != 0:
        print("❌ Docker is not installed or not running!")
        print("Please install Docker Desktop and start it.")
        return False
    
    print("✅ Docker is installed and running")
    return True


def start_database():
    """Start PostgreSQL database using Docker Compose"""
    print("\n🚀 Starting PostgreSQL database...")
    
    # Check if containers are already running
    result = run_command("docker-compose ps", check=False)
    if "postgres" in result.stdout and "Up" in result.stdout:
        print("✅ Database is already running")
        return True
    
    # Start the database
    result = run_command("docker-compose up -d")
    if result.returncode != 0:
        print("❌ Failed to start database")
        return False
    
    print("✅ Database started successfully")
    
    # Wait for database to be ready
    print("⏳ Waiting for database to be ready...")
    time.sleep(5)
    
    return True


def setup_backend():
    """Set up the backend environment"""
    print("\n🐍 Setting up Python backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found!")
        return False
    
    # Check if virtual environment exists
    venv_dir = backend_dir / "venv"
    if not venv_dir.exists():
        print("Creating virtual environment...")
        result = run_command("python -m venv venv", cwd=backend_dir)
        if result.returncode != 0:
            print("❌ Failed to create virtual environment")
            return False
    
    # Install dependencies
    print("Installing Python dependencies...")
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/Mac
        pip_cmd = "venv/bin/pip"
    
    result = run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir)
    if result.returncode != 0:
        print("❌ Failed to install dependencies")
        return False
    
    # Copy environment file
    env_example = backend_dir / "env.example"
    env_file = backend_dir / ".env"
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from template...")
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env file")
        print("⚠️  Please edit backend/.env with your database credentials")
    
    return True


def run_migrations():
    """Run database migrations"""
    print("\n🗄️  Running database migrations...")
    
    backend_dir = Path("backend")
    if os.name == 'nt':  # Windows
        python_cmd = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        python_cmd = "venv/bin/python"
    
    result = run_command(f"{python_cmd} setup_db.py", cwd=backend_dir)
    if result.returncode != 0:
        print("❌ Failed to run migrations")
        return False
    
    print("✅ Database migrations completed")
    return True


def main():
    """Main setup function"""
    print("🎯 AI Content Explorer - Project Setup")
    print("=" * 50)
    
    # Step 1: Check Docker
    if not check_docker():
        sys.exit(1)
    
    # Step 2: Start database
    if not start_database():
        sys.exit(1)
    
    # Step 3: Setup backend
    if not setup_backend():
        sys.exit(1)
    
    # Step 4: Run migrations
    if not run_migrations():
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit backend/.env with your database credentials")
    print("2. Start the backend server:")
    print("   cd backend")
    print("   venv\\Scripts\\python -m uvicorn app.main:app --reload  # Windows")
    print("   venv/bin/python -m uvicorn app.main:app --reload       # Unix/Linux/Mac")
    print("3. Access the API at: http://localhost:8000")
    print("4. View API docs at: http://localhost:8000/docs")
    print("5. Access pgAdmin at: http://localhost:5050 (admin@admin.com / admin)")
    print("\n🔧 For frontend setup:")
    print("1. cd frontend")
    print("2. npm install")
    print("3. npm run dev")
    print("4. Access frontend at: http://localhost:5173")


if __name__ == "__main__":
    main() 