import re

# Read the current file
with open('/app/app/database/connection.py', 'r') as f:
    content = f.read()

# Define the correct function implementation
correct_function = '''def build_clean_asyncpg_url(original_url: str) -> str:
    """
    Build a clean asyncpg URL from the original database URL.

    FOR ASYNCPG IN KUBERNETES:
    - Removes any existing SSL parameters that are psycopg2-specific (sslmode, etc.)
    - asyncpg does NOT support sslmode parameter - only accepts ssl parameter
    - For local Kubernetes PostgreSQL, use no SSL parameters
    """
    logger.info(f"🔧 MCP SERVER: Original asyncpg URL received: {original_url}")

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

    logger.info(f"✅ MCP SERVER: Clean asyncpg URL (without unsupported SSL params): {clean_url}")
    return clean_url
'''

# Find and replace the function using regex
# This looks for the entire function definition
pattern = r"def build_clean_asyncpg_url\(original_url: str\) -> str:[\s\S]*?(?=\n[a-zA-Z_#]|def |if |async |@|class |\Z)"

# Replace the entire function with the correct implementation
updated_content = re.sub(pattern, correct_function, content, count=1)

# Write the updated content back
with open('/app/app/database/connection.py', 'w') as f:
    f.write(updated_content)

print("Successfully updated build_clean_asyncpg_url function to properly remove SSL parameters")