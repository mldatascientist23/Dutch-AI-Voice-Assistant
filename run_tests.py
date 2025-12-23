#!/usr/bin/env python3
"""Simple test runner to verify all tests pass"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import subprocess

def run_tests():
    """Run all test modules"""
    test_modules = [
        'tests/test_api.py',
        'tests/test_call_manager.py',
        'tests/test_flows.py',
    ]
    
    all_passed = True
    for module in test_modules:
        print(f"\n{'='*60}")
        print(f"Running {module}")
        print('='*60)
        result = subprocess.run(
            ['python', '-m', 'pytest', module, '-v', '--tb=short'],
            cwd='/home/runner/work/Dutch-AI-Voice-Assistant/Dutch-AI-Voice-Assistant',
            timeout=30
        )
        if result.returncode != 0:
            all_passed = False
            print(f"✗ {module} FAILED")
        else:
            print(f"✓ {module} PASSED")
    
    return all_passed

if __name__ == '__main__':
    try:
        success = run_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)
