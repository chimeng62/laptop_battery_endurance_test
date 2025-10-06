#!/usr/bin/env python3
"""
Quick Process Management Test Runner

This script provides a simple way to test the new process management functionality
without running the full battery test suite.
"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    print("Laptop Battery Test - Process Management Test")
    print("=" * 50)
    print()
    print("This will test the new process management system by:")
    print("1. Opening and tracking simple applications")
    print("2. Testing browser process management")
    print("3. Testing Office application handling")
    print("4. Verifying force-kill functionality")
    print()
    
    response = input("Do you want to run the tests? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        try:
            from test_process_management import main as run_tests
            run_tests()
        except ImportError as e:
            print(f"Error importing test module: {e}")
            print("Make sure all dependencies are installed (pip install -r requirements.txt)")
        except Exception as e:
            print(f"Error running tests: {e}")
    else:
        print("Tests cancelled.")

if __name__ == "__main__":
    main()