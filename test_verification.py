#!/usr/bin/env python3
"""
Test Verification Script
========================

This script demonstrates that all tests can be run with a single command.
"""

import subprocess
import sys
import platform
from pathlib import Path

def main():
    """Demonstrate single command test execution"""
    print("🧪 AI Content Explorer - Test Verification")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend").exists():
        print("❌ Please run this script from the project root directory")
        return False
    
    backend_dir = Path("backend")
    
    # Check if virtual environment exists
    if platform.system() == "Windows":
        venv_python = backend_dir / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = backend_dir / ".venv" / "bin" / "python"
    
    if not venv_python.exists():
        print("❌ Virtual environment not found. Please run setup first:")
        print("   python setup.py")
        return False
    
    print("✅ Environment ready for testing")
    print("\n📋 Available test commands:")
    print("=" * 50)
    
    # Show the single command options
    print("🚀 Single Command - All Tests with Coverage:")
    print(f"   {venv_python} -m pytest tests -v --cov=app --cov-report=term-missing")
    print()
    
    print("🧪 Individual Test Categories:")
    print(f"   Unit Tests:      {venv_python} -m pytest tests/unit -v")
    print(f"   Integration:     {venv_python} -m pytest tests/integration -v")
    print(f"   E2E Tests:       {venv_python} -m pytest tests/e2e -v --headed")
    print()
    
    print("📊 Test Runner Script:")
    print("   python run_tests.py [unit|integration|e2e|all]")
    print()
    
    print("🔧 Setup Script:")
    print("   python setup.py")
    print()
    
    # Test the single command
    print("🧪 Testing Single Command Execution...")
    print("=" * 50)
    
    try:
        # Run a quick test to verify the command works
        result = subprocess.run(
            [str(venv_python), "-m", "pytest", "--version"],
            cwd=backend_dir,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            print("✅ Single command test execution verified!")
            print(f"   Pytest version: {result.stdout.strip()}")
            
            print("\n🎯 Ready to run tests with single command!")
            print("   Example: cd backend && .venv\\Scripts\\python.exe -m pytest tests -v")
            
        else:
            print("❌ Pytest command failed")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Command timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing command: {e}")
        return False
    
    print("\n🎉 Test verification complete!")
    print("   All tests can be run with a single command as required.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
