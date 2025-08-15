#!/usr/bin/env python3
"""
E2E Test Runner for AI Content Explorer
=======================================

This script provides an easy way to run different categories of E2E tests
using Playwright for the complete frontend-to-backend flow.
"""

import subprocess
import sys
import os
import time
from typing import List, Tuple

def run_command(command: str, description: str) -> Tuple[bool, str]:
    """Run a command and return success status and output."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    try:
        # Use the virtual environment Python interpreter
        python_executable = os.path.join(".venv", "Scripts", "python.exe")
        if not os.path.exists(python_executable):
            python_executable = "python"  # Fallback to system Python
        
        # Replace 'python' with the correct interpreter
        command = command.replace("python -m", f"{python_executable} -m")
        
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print(result.stdout)
            return True, result.stdout
        else:
            print("❌ Failed!")
            if result.stderr:
                print(f"Error output: {result.stderr}")
            return False, result.stderr
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False, str(e)

def check_servers_running():
    """Check if backend and frontend servers are running."""
    print("🔍 Checking if servers are running...")
    
    # Check backend server
    try:
        import requests
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
        else:
            print("⚠️  Backend server responded but not as expected")
            return False
    except:
        print("❌ Backend server is not running")
        return False
    
    # Check frontend server
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend server is running")
        else:
            print("⚠️  Frontend server responded but not as expected")
            return False
    except:
        print("❌ Frontend server is not running")
        return False
    
    return True

def main():
    """Main E2E test runner function."""
    print("🧪 AI Content Explorer - E2E Test Runner")
    print("="*50)
    
    # Check if servers are running
    if not check_servers_running():
        print("\n⚠️  Please start both backend and frontend servers before running E2E tests:")
        print("   Backend:  uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        print("   Frontend: npm start (in auth-ui directory)")
        print("\n   Then run this script again.")
        return 1
    
    print("\n📦 E2E testing dependencies already installed...")
    
    # Run different E2E test categories
    e2e_test_categories = [
        ("python -m pytest tests/e2e/test_authentication.py -v", "Authentication E2E Tests"),
        ("python -m pytest tests/e2e/test_search_functionality.py -v", "Search Functionality E2E Tests"),
        ("python -m pytest tests/e2e/test_image_generation.py -v", "Image Generation E2E Tests"),
        ("python -m pytest tests/e2e/test_dashboard.py -v", "Dashboard E2E Tests"),
        ("python -m pytest tests/e2e/ -v", "All E2E Tests"),
        ("python -m pytest tests/e2e/ -v --headed", "All E2E Tests (Headed Mode)"),
        ("python -m pytest tests/e2e/ -v --html=reports/e2e_report.html", "All E2E Tests with HTML Report")
    ]
    
    results = []
    
    for command, description in e2e_test_categories:
        success, output = run_command(command, description)
        results.append((description, success, output))
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 E2E TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for description, success, output in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} E2E test categories passed")
    
    if passed == total:
        print("🎉 All E2E test categories passed successfully!")
        print("\n📋 E2E Testing Coverage:")
        print("   ✅ Authentication flows (registration, login, logout)")
        print("   ✅ Search functionality (input validation, results display)")
        print("   ✅ Image generation (prompt validation, image display)")
        print("   ✅ Dashboard functionality (history, navigation, responsive)")
        print("   ✅ Cross-page navigation and user experience")
        return 0
    else:
        print("⚠️  Some E2E test categories failed. Check the output above.")
        print("\n💡 Tips for debugging E2E tests:")
        print("   1. Ensure both backend and frontend servers are running")
        print("   2. Check browser console for JavaScript errors")
        print("   3. Verify API endpoints are accessible")
        print("   4. Run with --headed flag to see browser interactions")
        return 1

if __name__ == "__main__":
    sys.exit(main())
