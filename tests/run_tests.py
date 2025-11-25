#!/usr/bin/env python3
"""
Test runner for Iago Deluxe
"""

import sys
import os
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def run_tests():
    """Run all tests"""
    test_dir = os.path.dirname(__file__)

    # Find all test files
    test_files = []
    for file in os.listdir(test_dir):
        if file.startswith("test_") and file.endswith(".py"):
            test_files.append(os.path.join(test_dir, file))

    print(f"Running {len(test_files)} test files...")

    passed = 0
    failed = 0

    for test_file in test_files:
        print(f"\nRunning {os.path.basename(test_file)}...")
        try:
            # Import and run the test module
            module_name = os.path.basename(test_file)[:-3]  # Remove .py
            spec = importlib.util.spec_from_file_location(module_name, test_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Run test functions
            test_functions = [
                getattr(module, name)
                for name in dir(module)
                if name.startswith("test_") and callable(getattr(module, name))
            ]

            for test_func in test_functions:
                try:
                    test_func()
                    print(f"  ✓ {test_func.__name__}")
                    passed += 1
                except Exception as e:
                    print(f"  ✗ {test_func.__name__}: {e}")
                    failed += 1

        except Exception as e:
            print(f"  Error loading {test_file}: {e}")
            failed += 1

    print(f"\nResults: {passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    import importlib.util

    success = run_tests()
    sys.exit(0 if success else 1)
