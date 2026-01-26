#!/usr/bin/env python3
"""
Script to fix the SSL parameter issue in the connection.py file in the MCP pod.
"""

import subprocess
import tempfile
import os

# The correct implementation of the build_clean_asyncpg_url function
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

# Create a temporary file with the fix
with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
    temp_file.write(correct_function)
    temp_file_path = temp_file.name

print(f"Created temporary file with fix: {temp_file_path}")

# Get the pod name
result = subprocess.run(['kubectl', 'get', 'pods', '-l', 'app.kubernetes.io/name=mcp-server', '-o', 'jsonpath={.items[0].metadata.name}'],
                       capture_output=True, text=True)
pod_name = result.stdout.strip()

if not pod_name:
    # Try alternative selector
    result = subprocess.run(['kubectl', 'get', 'pods', '-l', 'app=mcp-service', '-o', 'jsonpath={.items[0].metadata.name}'],
                           capture_output=True, text=True)
    pod_name = result.stdout.strip()

if not pod_name:
    # Get any pod with mcp in the name
    result = subprocess.run(['kubectl', 'get', 'pods', '-o', 'jsonpath={.items[?(@.metadata.name=~"mcp.*")].metadata.name}'],
                           capture_output=True, text=True)
    pod_name = result.stdout.strip().split()[0] if result.stdout.strip() else ""

if pod_name:
    print(f"Found MCP pod: {pod_name}")

    # Copy the current connection.py from the pod to local
    subprocess.run(['kubectl', 'cp', f'default/{pod_name}:/app/app/database/connection.py', 'connection.py.backup'])
    print("Backed up current connection.py")

    # Apply the fix by creating a script that will be executed in the pod
    fix_script = f'''import re

# Read the current file
with open('/app/app/database/connection.py', 'r') as f:
    content = f.read()

# Replace the function with the correct one
pattern = r"def build_clean_asyncpg_url\\(original_url: str\\) -> str:.*?(?=\\n[a-zA-Z_#]|$)"
replacement = ''' + repr(correct_function) + '''

# Use regex to replace the function
import re
updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL | re.MULTILINE)

# Write the updated content back
with open('/app/app/database/connection.py', 'w') as f:
    f.write(updated_content)

print("Successfully updated build_clean_asyncpg_url function")
'''

    # Write the fix script to a temporary file
    script_path = 'apply_fix.py'
    with open(script_path, 'w') as f:
        f.write(fix_script)

    # Copy the script to the pod
    subprocess.run(['kubectl', 'cp', script_path, f'default/{pod_name}:/tmp/apply_fix.py'])

    # Execute the script in the pod
    result = subprocess.run(['kubectl', 'exec', pod_name, '--', 'python', '/tmp/apply_fix.py'],
                           capture_output=True, text=True)

    print("Script execution result:", result.returncode)
    if result.stdout:
        print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    # Clean up
    os.unlink(script_path)
    print("Applied fix to the MCP pod")
else:
    print("Could not find MCP pod")