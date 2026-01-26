from mcp.server import Server

server = Server("test-server")

print("Available methods on server object:")
for attr in dir(server):
    if not attr.startswith('_'):
        print(f"- {attr}")

print("\nTrying to access 'tool' attribute:")
try:
    tool_attr = getattr(server, 'tool')
    print(f"Found: {tool_attr}")
except AttributeError as e:
    print(f"AttributeError: {e}")

print("\nTrying to access common method names:")
common_names = ['tool', 'register_tool', 'add_tool', 'define_tool', 'bind_tool']
for name in common_names:
    try:
        attr = getattr(server, name, None)
        if attr:
            print(f"- {name}: {type(attr)} - {attr}")
        else:
            print(f"- {name}: Not found")
    except Exception as e:
        print(f"- {name}: Error - {e}")