#!/usr/bin/env python3
"""
AI Content Explorer - Test Runner
=================================

This script provides a single command to run all tests with proper setup and reporting.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, cwd=None, shell=False, capture_output=False):
    """Run a command and return result"""
    try:
        if capture_output:
            result = subprocess.run(command, cwd=cwd, shell=shell, check=True, 
                                 capture_output=True, text=True)
            return True, result.stdout, result.stderr
        else:
            result = subprocess.run(command, cwd=cwd, shell=shell, check=True)
            return True, "", ""
    except subprocess.CalledProcessError as e:
        if capture_output:
            return False, e.stdout, e.stderr
        else:
            return False, "", ""

def check_backend_setup():
    """Check if backend is properly set up"""
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Check virtual environment
    if platform.system() == "Windows":
        venv_python = backend_dir / ".venv" / "Scripts" / "python.exe"
    else:
        venv_python = backend_dir / ".venv" / "bin" / "python"
    
    if not venv_python.exists():
        print("❌ Backend virtual environment not found")
        print("   Run: python setup.py")
        return False
    
    # Check requirements
    requirements_file = backend_dir / "requirements.txt"
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    return True

def run_unit_tests():
    """Run unit tests"""
    print("\n🧪 Running Unit Tests...")
    print("=" * 50)
    
    backend_dir = Path("backend")
    if platform.system() == "Windows":
        python_path = backend_dir / ".venv" / "Scripts" / "python.exe"
    else:
        python_path = backend_dir / ".venv" / "bin" / "python"
    
    success, stdout, stderr = run_command(
        [str(python_path), "-m", "pytest", "tests/unit", "-v", "--tb=short"],
        cwd=backend_dir,
        capture_output=True
    )
    
    if success:
        print("✅ Unit Tests PASSED")
        print(stdout)
    else:
        print("❌ Unit Tests FAILED")
        print(stderr)
    
    return success

def run_integration_tests():
    """Run integration tests"""
    print("\n🔗 Running Integration Tests...")
    print("=" * 50)
    
    backend_dir = Path("backend")
    if platform.system() == "Windows":
        python_path = backend_dir / ".venv" / "Scripts" / "python.exe"
    else:
        python_path = backend_dir / ".venv" / "bin" / "python"
    
    success, stdout, stderr = run_command(
        [str(python_path), "-m", "pytest", "tests/integration", "-v", "--tb=short"],
        cwd=backend_dir,
        capture_output=True
    )
    
    if success:
        print("✅ Integration Tests PASSED")
        print(stdout)
    else:
        print("❌ Integration Tests FAILED")
        print(stderr)
    
    return success

def run_e2e_tests():
    """Run E2E tests"""
    print("\n🌐 Running E2E Tests...")
    print("=" * 50)
    
    backend_dir = Path("backend")
    if platform.system() == "Windows":
        python_path = backend_dir / ".venv" / "Scripts" / "python.exe"
    else:
        python_path = backend_dir / ".venv" / "bin" / "python"
    
    success, stdout, stderr = run_command(
        [str(python_path), "-m", "pytest", "tests/e2e", "-v", "--tb=short"],
        cwd=backend_dir,
        capture_output=True
    )
    
    if success:
        print("✅ E2E Tests PASSED")
        print(stdout)
    else:
        print("❌ E2E Tests FAILED")
        print(stderr)
    
    return success

def run_all_tests_with_coverage():
    """Run all tests with coverage report"""
    print("\n📊 Running All Tests with Coverage...")
    print("=" * 50)
    
    backend_dir = Path("backend")
    if platform.system() == "Windows":
        python_path = backend_dir / ".venv" / "Scripts" / "python.exe"
    else:
        python_path = backend_dir / ".venv" / "bin" / "python"
    
    success, stdout, stderr = run_command(
        [str(python_path), "-m", "pytest", "tests", "-v", "--cov=app", "--cov-report=term-missing"],
        cwd=backend_dir,
        capture_output=True
    )
    
    if success:
        print("✅ All Tests PASSED")
        print(stdout)
    else:
        print("❌ Some Tests FAILED")
        print(stderr)
    
    return success

def run_specific_test_category(category):
    """Run tests for a specific category"""
    if category == "unit":
        return run_unit_tests()
    elif category == "integration":
        return run_integration_tests()
    elif category == "e2e":
        return run_e2e_tests()
    elif category == "all":
        return run_all_tests_with_coverage()
    else:
        print(f"❌ Unknown test category: {category}")
        return False

def main():
    """Main test runner function"""
    print("🚀 AI Content Explorer - Test Runner")
    print("=" * 50)
    
    # Check backend setup
    if not check_backend_setup():
        return False
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        category = sys.argv[1].lower()
        if category in ["unit", "integration", "e2e", "all"]:
            return run_specific_test_category(category)
        else:
            print(f"❌ Unknown test category: {category}")
            print("Available categories: unit, integration, e2e, all")
            return False
    
    # Default: run all tests with coverage
    print("📋 No category specified, running all tests with coverage...")
    return run_all_tests_with_coverage()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
    
    sys.exit(0 if success else 1)
