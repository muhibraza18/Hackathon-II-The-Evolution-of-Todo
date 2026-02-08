#!/usr/bin/env python3
"""
Test script to verify that the MCP server is working after the SSL fix.
This script simulates a basic task creation to test the MCP integration.
"""

import asyncio
import httpx
import json
from datetime import datetime

async def test_mcp_integration():
    """
    Test the MCP server integration by calling the list_tasks endpoint.
    """
    print("🧪 Testing MCP Server Integration...")
    print("=" * 50)

    # Test with the MCP server URL that's configured
    mcp_url = "http://localhost:8002"  # Default for local testing

    print(f"\n📡 Testing MCP server at: {mcp_url}")

    # First test health endpoint
    print("\n🔍 Testing health endpoint...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{mcp_url}/health")
            print(f"   Health check status: {response.status_code}")
            if response.status_code == 200:
                health_data = response.json()
                print(f"   Health response: {json.dumps(health_data, indent=2)}")
                print("✅ Health check successful!")
            else:
                print(f"❌ Health check failed: {response.text}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        print("   ⚠️  This may be expected if the MCP server is not running locally")
        return  # Don't continue if health check fails

    # Test the list_tasks endpoint with a sample request
    print(f"\n📋 Testing list_tasks endpoint...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Sample request data matching what the backend sends
            list_data = {
                "user_id": "1",
                "status": "all"
            }

            print(f"   Request data: {json.dumps(list_data, indent=2)}")
            response = await client.post(f"{mcp_url}/list_tasks", json=list_data)
            print(f"   List tasks status: {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                print(f"   List tasks response: {json.dumps(result, indent=2)[:500]}...")  # Truncate long output
                print("✅ List tasks successful!")

                # Test add_task endpoint
                print(f"\n📝 Testing add_task endpoint...")
                task_data = {
                    "user_id": "1",
                    "title": f"Test task created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                    "description": "This is a test task to verify MCP server functionality"
                }

                response = await client.post(f"{mcp_url}/add_task", json=task_data)
                print(f"   Add task status: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    print(f"   Add task response: {json.dumps(result, indent=2)}")

                    if "task_id" in result and result["task_id"]:
                        task_id = result["task_id"]
                        print(f"✅ Task created successfully with ID: {task_id}")

                        # Test the task appears in the list
                        response = await client.post(f"{mcp_url}/list_tasks", json={"user_id": "1", "status": "all"})
                        if response.status_code == 200:
                            tasks = response.json()
                            if any(task.get("id") == task_id for task in tasks):
                                print(f"✅ New task found in task list!")
                            else:
                                print(f"⚠️  New task not found in task list (may be expected)")
                        else:
                            print(f"⚠️  Could not verify task in list: {response.status_code}")
                    else:
                        print(f"❌ Add task response missing task_id: {result}")
                else:
                    print(f"❌ Add task failed: {response.text}")
            else:
                print(f"❌ List tasks failed: {response.text}")
                error_detail = response.text
                if "sslmode" in error_detail.lower() or "ssl" in error_detail.lower():
                    print("🚨 SSL-related error still present - fix not working!")
                else:
                    print("⚠️  Different error - may be configuration related")
    except Exception as e:
        print(f"❌ MCP endpoint test error: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 50)
    print("🧪 MCP Server integration test completed!")

if __name__ == "__main__":
    print("🚀 Starting MCP Server Integration Test...")
    asyncio.run(test_mcp_integration())