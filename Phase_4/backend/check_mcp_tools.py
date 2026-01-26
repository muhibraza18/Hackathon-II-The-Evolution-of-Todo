from mcp.server import Server
import inspect

server = Server("test-server")

print("Server type:", type(server))
print("Server module:", server.__class__.__module__)

# Let's see if there are decorators or other ways to register tools
print("\nServer methods that might be related to tools:")
for attr_name in dir(server):
    if 'tool' in attr_name.lower() or 'register' in attr_name.lower() or 'add' in attr_name.lower():
        attr = getattr(server, attr_name)
        if callable(attr):
            print(f"- {attr_name}: {inspect.signature(attr) if hasattr(attr, '__call__') else 'callable'}")

# Check if there are decorator-style methods
print("\nTrying to see if there are decorator methods on the class itself:")
server_class = server.__class__
for attr_name in dir(server_class):
    if 'tool' in attr_name.lower() or 'register' in attr_name.lower() or 'add' in attr_name.lower():
        attr = getattr(server_class, attr_name)
        print(f"- Class.{attr_name}: {type(attr)}")

# Check if there's a decorator for functions
print("\nTrying to see if there are function decorators available in the module:")
import mcp.server
for name in dir(mcp.server):
    if 'tool' in name.lower():
        obj = getattr(mcp.server, name)
        print(f"- mcp.server.{name}: {type(obj)} - {obj}")