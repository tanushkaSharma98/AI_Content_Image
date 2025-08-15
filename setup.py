#!/usr/bin/env python3
"""
AI Content Explorer - Setup Script
==================================

This script automates the setup process for the AI Content Explorer project.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, cwd=None, shell=False):
    """Run a command and return success status"""
    try:
        if shell:
            result = subprocess.run(command, shell=True, cwd=cwd, check=True)
        else:
            result = subprocess.run(command, cwd=cwd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        return False
    except FileNotFoundError as e:
        print(f"❌ Command not found: {e}")
        return False

def check_prerequisites():
    """Check if required software is installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 11):
        print("❌ Python 3.11+ is required")
        return False
    print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check Node.js
    try:
        node_result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if node_result.returncode == 0:
            print(f"✅ Node.js {node_result.stdout.strip()}")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False
    
    # Check npm
    try:
        npm_result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if npm_result.returncode == 0:
            print(f"✅ npm {npm_result.stdout.strip()}")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False
    
    # Check PostgreSQL (basic check)
    try:
        psql_result = subprocess.run(["psql", "--version"], capture_output=True, text=True)
        if psql_result.returncode == 0:
            print(f"✅ PostgreSQL {psql_result.stdout.strip()}")
        else:
            print("⚠️  PostgreSQL not found - you'll need to install it")
    except FileNotFoundError:
        print("⚠️  PostgreSQL not found - you'll need to install it")
    
    return True

def setup_backend():
    """Set up the backend environment"""
    print("\n🐍 Setting up backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Create virtual environment
    print("📦 Creating virtual environment...")
    if not run_command([sys.executable, "-m", "venv", ".venv"], cwd=backend_dir):
        return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        pip_path = backend_dir / ".venv" / "Scripts" / "pip.exe"
        python_path = backend_dir / ".venv" / "Scripts" / "python.exe"
    else:
        pip_path = backend_dir / ".venv" / "bin" / "pip"
        python_path = backend_dir / ".venv" / "bin" / "python"
    
    print("📥 Installing Python dependencies...")
    if not run_command([str(pip_path), "install", "-r", "requirements.txt"], cwd=backend_dir):
        return False
    
    # Create .env file if it doesn't exist
    env_file = backend_dir / ".env"
    if not env_file.exists():
        print("🔧 Creating .env file...")
        env_content = """# Database
DATABASE_URL=postgresql://username:password@localhost:5432/ai_content_explorer

# JWT
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Keys
TAVILY_API_KEY=your-tavily-api-key
FLUX_API_TOKEN=your-flux-api-token

# App Settings
APP_NAME=AI Content Explorer
DEBUG=True
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ .env file created - please update with your actual values")
    
    print("✅ Backend setup complete!")
    return True

def setup_frontend():
    """Set up the frontend environment"""
    print("\n⚛️  Setting up frontend...")
    
    frontend_dir = Path("auth-ui")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    print("📥 Installing Node.js dependencies...")
    if not run_command(["npm", "install"], cwd=frontend_dir):
        return False
    
    print("✅ Frontend setup complete!")
    return True

def create_start_scripts():
    """Create start scripts for easy development"""
    print("\n📝 Creating start scripts...")
    
    # Windows batch file
    if platform.system() == "Windows":
        start_backend = """@echo off
cd backend
.venv\\Scripts\\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
"""
        start_frontend = """@echo off
cd auth-ui
npm start
pause
"""
        
        with open("start_backend.bat", "w") as f:
            f.write(start_backend)
        
        with open("start_frontend.bat", "w") as f:
            f.write(start_frontend)
        
        print("✅ Created start_backend.bat and start_frontend.bat")
    
    # Unix shell scripts
    else:
        start_backend = """#!/bin/bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
        start_frontend = """#!/bin/bash
cd auth-ui
npm start
"""
        
        with open("start_backend.sh", "w") as f:
            f.write(start_backend)
        
        with open("start_frontend.sh", "w") as f:
            f.write(start_frontend)
        
        # Make executable
        os.chmod("start_backend.sh", 0o755)
        os.chmod("start_frontend.sh", 0o755)
        
        print("✅ Created start_backend.sh and start_frontend.sh")

def run_tests():
    """Run the test suite to verify setup"""
    print("\n🧪 Running tests to verify setup...")
    
    backend_dir = Path("backend")
    if platform.system() == "Windows":
        python_path = backend_dir / ".venv" / "Scripts" / "python.exe"
    else:
        python_path = backend_dir / ".venv" / "bin" / "python"
    
    # Run a quick test to verify setup
    if run_command([str(python_path), "-m", "pytest", "tests/unit", "-v", "--tb=short"], cwd=backend_dir):
        print("✅ Tests passed! Setup is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. This might be expected if the database isn't set up yet.")
        return True

def main():
    """Main setup function"""
    print("🚀 AI Content Explorer - Setup Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please install required software.")
        return False
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed.")
        return False
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed.")
        return False
    
    # Create start scripts
    create_start_scripts()
    
    # Run tests
    run_tests()
    
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("📋 Next Steps:")
    print("1. Update backend/.env with your actual API keys and database settings")
    print("2. Set up your PostgreSQL database")
    print("3. Start the backend: ./start_backend.sh (or start_backend.bat on Windows)")
    print("4. Start the frontend: ./start_frontend.sh (or start_frontend.bat on Windows)")
    print("5. Access the application:")
    print("   - Frontend: http://localhost:3000")
    print("   - Backend API: http://localhost:8000")
    print("   - API Docs: http://localhost:8000/docs")
    print("\n🧪 To run tests:")
    print("   cd backend && .venv/Scripts/python.exe -m pytest tests -v")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
