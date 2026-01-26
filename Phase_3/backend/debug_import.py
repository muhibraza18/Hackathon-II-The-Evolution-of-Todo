import sys
from pathlib import Path

print("Python path:")
for p in sys.path:
    print(f"  {p}")

print(f"\nCurrent working directory: {Path.cwd()}")

print("\nTrying to import models...")
try:
    import models
    print("Success: imported models")
except ImportError as e:
    print(f"Failed to import models: {e}")

print("\nTrying to import backend.models...")
try:
    import backend.models
    print("Success: imported backend.models")
except ImportError as e:
    print(f"Failed to import backend.models: {e}")

print("\nTrying to import app.main...")
try:
    import app.main
    print("Success: imported app.main")
except ImportError as e:
    print(f"Failed to import app.main: {e}")