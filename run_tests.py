#!/usr/bin/env python3
"""
Test runner script for the FastAPI application
"""

import subprocess
import sys
import os

def main():
    """Run all tests with coverage reporting"""
    print("🧪 Running FastAPI tests...")
    print("=" * 50)
    
    # Change to project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    try:
        # Run tests with coverage
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "--cov=src", 
            "--cov-report=term-missing",
            "--cov-report=html",
            "-v"
        ], check=True)
        
        print("\n✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/")
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print("❌ pytest not found. Please install requirements: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())