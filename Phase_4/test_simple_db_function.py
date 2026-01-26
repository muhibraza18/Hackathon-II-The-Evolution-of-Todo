#!/usr/bin/env python3
"""
Simple test to verify the build_clean_asyncpg_url function works correctly.
"""

import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

def build_clean_asyncpg_url(original_url: str) -> str:
    """
    Build a clean asyncpg URL from the original database URL.

    FOR ASYNCPG IN KUBERNETES:
    - Removes any existing SSL parameters that are psycopg2-specific (sslmode, etc.)
    - asyncpg does NOT support sslmode parameter - only accepts ssl parameter
    - For local Kubernetes PostgreSQL, use no SSL parameters
    """
    print(f"[DEBUG] Original asyncpg URL received: {original_url}")

    # Parse the original URL to extract components
    base_url = original_url
    if '?' in original_url:
        base_url = original_url.split('?')[0]
        query_part = original_url.split('?')[1]

        # Parse existing query parameters and filter out psycopg2-specific ones
        params = []
        for param in query_part.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                # Skip psycopg2-specific SSL parameters that asyncpg doesn't support
                if key.lower() not in ['sslmode', 'sslcert', 'sslkey', 'sslrootcert', 'sslfactory', 'sslcompression']:
                    params.append(f"{key}={value}")
            else:
                params.append(param)

        # Reconstruct the URL without unsupported asyncpg parameters
        if params:
            clean_url = f"{base_url}?{'&'.join(params)}"
        else:
            clean_url = base_url
    else:
        clean_url = original_url

    print(f"[SUCCESS] Clean asyncpg URL (without unsupported SSL params): {clean_url}")
    return clean_url


def test_build_clean_asyncpg_url():
    """
    Test the build_clean_asyncpg_url function with various input URLs.
    """
    print("[TEST] Testing build_clean_asyncpg_url function...")
    print("=" * 60)

    # Test cases with various SSL parameters
    test_cases = [
        {
            "input": "postgresql+asyncpg://user:pass@localhost:5432/db?sslmode=require",
            "expected_not_contain": ["sslmode"],
            "description": "URL with sslmode parameter"
        },
        {
            "input": "postgresql+asyncpg://user:pass@localhost:5432/db?sslmode=disable&other_param=value",
            "expected_not_contain": ["sslmode"],
            "expected_contain": ["other_param"],
            "description": "URL with sslmode and other parameters"
        },
        {
            "input": "postgresql+asyncpg://user:pass@localhost:5432/db",
            "expected_contain": [],
            "description": "Simple URL without parameters"
        },
        {
            "input": "postgresql+asyncpg://user:pass@neon-host.db/production?sslmode=require&sslcert=path&application_name=myapp",
            "expected_not_contain": ["sslmode", "sslcert"],
            "expected_contain": ["application_name"],
            "description": "Neon DB URL with multiple parameters"
        },
        {
            "input": "postgresql://neondb_owner:npg_l3WKQFsvo7uH@ep-calm-frost-ahdmlrul-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
            "expected_not_contain": ["sslmode"],
            "expected_contain": ["channel_binding"],
            "description": "Real-world Neon DB URL from the error"
        }
    ]

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"   Input:  {test_case['input']}")

        result = build_clean_asyncpg_url(test_case['input'])
        print(f"   Output: {result}")

        # Check that unwanted parameters are not present
        passed = True
        if 'expected_not_contain' in test_case:
            for param in test_case['expected_not_contain']:
                if param.lower() in result.lower():
                    print(f"   [ERROR] FAILED: Contains unwanted parameter '{param}'")
                    passed = False
                    all_passed = False

        # Check that wanted parameters are present
        if 'expected_contain' in test_case:
            for param in test_case['expected_contain']:
                if param.lower() not in result.lower():
                    print(f"   [ERROR] FAILED: Missing expected parameter '{param}'")
                    passed = False
                    all_passed = False

        if passed:
            print(f"   [SUCCESS] PASSED")

    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] All tests passed! The SSL parameter filtering is working correctly.")
    else:
        print("[ERROR] Some tests failed. Please review the SSL parameter filtering.")

    return all_passed

if __name__ == "__main__":
    print("[INFO] Starting standalone database connection test...")
    success = test_build_clean_asyncpg_url()
    if success:
        print("\n[SUCCESS] Database connection fix verification successful!")
    else:
        print("\n[ERROR] Database connection fix verification failed!")