#!/usr/bin/env python3
"""
Test script to verify that the MCP server SSL fix is working correctly.
This script tests the MCP server by calling its endpoints directly.
"""

import asyncio
import httpx
import json
from datetime import datetime

async def test_mcp_endpoints():
    """
    Test the MCP server endpoints to verify they're working correctly.
    """
    print("🧪 Testing MCP Server Endpoints...")
    print("=" * 50)

    base_url = "http://localhost:8002"  # Default MCP server URL

    # Test health endpoint first
    print("\n🔍 Testing health endpoint...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{base_url}/health")
            print(f"   Health check status: {response.status_code}")
            if response.status_code == 200:
                health_data = response.json()
                print(f"   Health response: {health_data}")
                print("✅ Health check successful!")
            else:
                print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")

    # Test creating a task
    print("\n📝 Testing add_task endpoint...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            task_data = {
                "user_id": "1",
                "title": f"Test Task {datetime.now().strftime('%H:%M:%S')}",
                "description": "This is a test task created to verify MCP server functionality"
            }

            print(f"   Sending task data: {json.dumps(task_data, indent=2)}")
            response = await client.post(f"{base_url}/add_task", json=task_data)
            print(f"   Add task status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"   Add task response: {result}")

                if "task_id" in result:
                    task_id = result["task_id"]
                    print(f"✅ Task created successfully with ID: {task_id}")

                    # Test listing tasks
                    print(f"\n📋 Testing list_tasks endpoint...")
                    list_data = {
                        "user_id": "1",
                        "status": "all"
                    }
                    response = await client.post(f"{base_url}/list_tasks", json=list_data)
                    print(f"   List tasks status: {response.status_code}")

                    if response.status_code == 200:
                        tasks = response.json()
                        print(f"   Number of tasks found: {len(tasks)}")

                        # Find our test task
                        test_task = next((t for t in tasks if t['id'] == task_id), None)
                        if test_task:
                            print(f"✅ Successfully found our test task: {test_task['title']}")
                        else:
                            print("⚠️  Could not find our test task in the list")
                    else:
                        print(f"❌ List tasks failed: {response.text}")
                        print(f"   Response: {response.text}")
                else:
                    print(f"❌ Add task failed: {result}")
            else:
                print(f"❌ Add task failed: {response.text}")
                print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Add task error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 50)
    print("🧪 MCP Server testing completed!")

if __name__ == "__main__":
    print("🚀 Starting MCP Server Test...")
    asyncio.run(test_mcp_endpoints())