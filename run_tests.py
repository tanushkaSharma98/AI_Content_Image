#!/usr/bin/env python3
"""
Test Runner for AI Content Explorer
===================================

This script provides an easy way to run different categories of tests
and generate comprehensive reports.
"""

import subprocess
import sys
import os
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

def main():
    """Main test runner function."""
    print("🧪 AI Content Explorer - Test Runner")
    print("="*50)
    
    # Skip dependency installation since we already have everything
    print("\n📦 Dependencies already installed, skipping installation...")
    
    # Run different test categories
    test_categories = [
        ("python -m pytest tests/unit/ -v", "Unit Tests"),
        ("python -m pytest tests/integration/ -v", "Integration Tests"),
        ("python -m pytest tests/ -v --cov=app --cov-report=term-missing", "All Tests with Coverage"),
        ("python -m pytest tests/ --cov=app --cov-report=html", "Generate HTML Coverage Report"),
        ("python -m pytest tests/e2e/ -v --headed", "E2E Tests (Headed Mode)"),
        ("python -m pytest tests/e2e/ -v", "E2E Tests (Headless Mode)")
    ]
    
    results = []
    
    for command, description in test_categories:
        success, output = run_command(command, description)
        results.append((description, success, output))
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = 0
    total = len(results)
    
    for description, success, output in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description}: {status}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} test categories passed")
    
    if passed == total:
        print("🎉 All test categories passed successfully!")
        return 0
    else:
        print("⚠️  Some test categories failed. Check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
