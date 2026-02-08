#!/usr/bin/env python3
"""
Test script to verify that the database connection fixes are working properly.
"""

from backend.app.database.connection import build_clean_asyncpg_url

def test_build_clean_asyncpg_url():
    """
    Test the build_clean_asyncpg_url function with various input URLs.
    """
    print("🧪 Testing build_clean_asyncpg_url function...")
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
                    print(f"   ❌ FAILED: Contains unwanted parameter '{param}'")
                    passed = False
                    all_passed = False

        # Check that wanted parameters are present
        if 'expected_contain' in test_case:
            for param in test_case['expected_contain']:
                if param.lower() not in result.lower():
                    print(f"   ❌ FAILED: Missing expected parameter '{param}'")
                    passed = False
                    all_passed = False

        if passed:
            print(f"   ✅ PASSED")

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! The SSL parameter filtering is working correctly.")
    else:
        print("❌ Some tests failed. Please review the SSL parameter filtering.")

    return all_passed

if __name__ == "__main__":
    print("🚀 Starting database connection test...")
    success = test_build_clean_asyncpg_url()
    if success:
        print("\n✅ Database connection fix verification successful!")
    else:
        print("\n❌ Database connection fix verification failed!")