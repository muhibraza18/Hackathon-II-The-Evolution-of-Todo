from mcp.server import Server
from mcp.types import Tool
import inspect

server = Server("test-server")

print("Checking experimental attribute:")
if hasattr(server, 'experimental'):
    exp = getattr(server, 'experimental')
    print(f"Experimental: {exp}")
    print(f"Experimental methods: {dir(exp)}")

    # Look for tool registration in experimental
    for attr_name in dir(exp):
        if 'tool' in attr_name.lower() or 'register' in attr_name.lower():
            attr = getattr(exp, attr_name)
            print(f"- experimental.{attr_name}: {type(attr)}")

# Check if there's a decorator approach
print("\nLooking for function decorators...")
import mcp
for attr_name in dir(mcp):
    if 'tool' in attr_name.lower():
        attr = getattr(mcp, attr_name)
        print(f"- mcp.{attr_name}: {type(attr)} - {attr}")

# Check mcp.types
import mcp.types
print(f"\nmcp.types attributes with 'tool': {[attr for attr in dir(mcp.types) if 'tool' in attr.lower()]}")

# Check if there's a decorator in mcp.server
import mcp.server
print(f"\nmcp.server attributes with 'tool': {[attr for attr in dir(mcp.server) if 'tool' in attr.lower()]}")