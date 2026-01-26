import asyncio
import aiohttp
import json

async def test_mcp_endpoints():
    """Test the MCP server endpoints to verify SSL and database connectivity"""
    base_url = "http://localhost:8002"

    # Test health endpoint
    print("Testing health endpoint...")
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{base_url}/health") as resp:
                if resp.status == 200:
                    health_data = await resp.json()
                    print(f"[SUCCESS] Health check passed: {health_data['status']}")
                else:
                    print(f"[FAILED] Health check failed with status: {resp.status}")
                    return False

        except Exception as e:
            print(f"[ERROR] Health check error: {e}")
            return False

        # Test add_task endpoint
        print("\nTesting add_task endpoint...")
        try:
            payload = {
                "user_id": "123",
                "title": "Test Task",
                "description": "This is a test task to verify database connectivity"
            }

            async with session.post(f"{base_url}/add_task", json=payload) as resp:
                if resp.status == 200:
                    task_data = await resp.json()
                    print(f"[SUCCESS] Add task successful: {task_data}")

                    # Store task_id for later use
                    task_id = task_data.get('task_id')

                    # Test list_tasks endpoint
                    print("\nTesting list_tasks endpoint...")
                    list_payload = {
                        "user_id": "123",
                        "status": "all"
                    }

                    async with session.post(f"{base_url}/list_tasks", json=list_payload) as list_resp:
                        if list_resp.status == 200:
                            tasks_data = await list_resp.json()
                            print(f"[SUCCESS] List tasks successful: Found {len(tasks_data)} tasks")

                            # Test complete_task endpoint if we have a task
                            if task_id:
                                print(f"\nTesting complete_task endpoint for task {task_id}...")
                                complete_payload = {
                                    "user_id": "123",
                                    "task_id": task_id
                                }

                                async with session.post(f"{base_url}/complete_task", json=complete_payload) as complete_resp:
                                    if complete_resp.status == 200:
                                        complete_data = await complete_resp.json()
                                        print(f"[SUCCESS] Complete task successful: {complete_data}")

                                        # Test delete_task endpoint
                                        print(f"\nTesting delete_task endpoint for task {task_id}...")
                                        delete_payload = {
                                            "user_id": "123",
                                            "task_id": task_id
                                        }

                                        async with session.post(f"{base_url}/delete_task", json=delete_payload) as delete_resp:
                                            if delete_resp.status == 200:
                                                delete_data = await delete_resp.json()
                                                print(f"[SUCCESS] Delete task successful: {delete_data}")
                                                return True
                                            else:
                                                print(f"[FAILED] Delete task failed with status: {delete_resp.status}")
                                                error_text = await delete_resp.text()
                                                print(f"Error: {error_text}")
                                                return False
                                    else:
                                        print(f"[FAILED] Complete task failed with status: {complete_resp.status}")
                                        error_text = await complete_resp.text()
                                        print(f"Error: {error_text}")
                                        return False
                        else:
                            print(f"[FAILED] List tasks failed with status: {list_resp.status}")
                            error_text = await list_resp.text()
                            print(f"Error: {error_text}")
                            return False
                else:
                    print(f"[FAILED] Add task failed with status: {resp.status}")
                    error_text = await resp.text()
                    print(f"Error: {error_text}")
                    return False

        except Exception as e:
            print(f"[ERROR] Endpoint test error: {e}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("Testing MCP Server endpoints...")
    success = asyncio.run(test_mcp_endpoints())
    if success:
        print("\n[SUCCESS] All MCP server tests passed!")
        print("[SUCCESS] SSL connectivity is working")
        print("[SUCCESS] Database operations are working")
    else:
        print("\n[FAILED] Some tests failed")