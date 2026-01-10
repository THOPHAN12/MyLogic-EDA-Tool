#!/usr/bin/env python3
"""
Test runner for MyLogic EDA Tool.

Usage:
    python tests/run_tests.py              # Run all tests
    python tests/run_tests.py --coverage    # Run with coverage
    python tests/run_tests.py --verbose     # Verbose output
"""

import sys
import os
import subprocess

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_tests(coverage=False, verbose=False, category=None):
    """Run pytest tests.
    
    Args:
        coverage: Run with coverage report
        verbose: Verbose output
        category: Test category to run ('unit', 'integration', 'examples', 'performance', None=all)
    """
    if category:
        test_path = f'tests/{category}/'
    else:
        test_path = 'tests/'
    
    cmd = ['python', '-m', 'pytest', test_path]
    
    if verbose:
        cmd.append('-v')
    else:
        cmd.append('-q')
    
    if coverage:
        cmd.extend(['--cov=core', '--cov=parsers', '--cov=cli', '--cov-report=html', '--cov-report=term'])
    
    cmd.extend(['-x', '--tb=short'])  # Stop on first failure, short traceback
    
    print("=" * 70)
    print("Running MyLogic EDA Tool Test Suite")
    print("=" * 70)
    print(f"Command: {' '.join(cmd)}")
    print("=" * 70)
    
    result = subprocess.run(cmd)
    return result.returncode == 0

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run MyLogic EDA Tool tests')
    parser.add_argument('--coverage', '-c', action='store_true', help='Run with coverage')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--category', choices=['unit', 'integration', 'examples', 'performance'],
                       help='Run tests from specific category only')
    
    args = parser.parse_args()
    
    if args.category:
        print(f"Running {args.category} tests only...")
    
    success = run_tests(coverage=args.coverage, verbose=args.verbose, category=args.category)
    sys.exit(0 if success else 1)

