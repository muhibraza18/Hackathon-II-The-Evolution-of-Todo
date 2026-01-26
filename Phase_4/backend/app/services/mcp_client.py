import httpx
import json
from typing import Dict, Any, Optional
from ..config import settings


class MCPServerClient:
    """
    Client for communicating with the MCP server to execute tool calls.
    """

    def __init__(self):
        self.base_url = settings.mcp_server_url

    async def call_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generic method to call any MCP tool.

        Args:
            tool_name: Name of the MCP tool to call
            params: Parameters to pass to the tool

        Returns:
            Result from the MCP tool call
        """
        try:
            # Construct the URL for the specific tool
            url = f"{self.base_url}/{tool_name}"

            # Make the HTTP request to the MCP server
            async with httpx.AsyncClient() as client:
                print(f"📡 Calling MCP tool '{tool_name}' at {url}")  # Log tool call
                response = await client.post(url, json=params, timeout=30.0)

                if response.status_code != 200:
                    print(f"❌ MCP tool {tool_name} failed with status {response.status_code}: {response.text}")  # Log error
                    raise Exception(f"MCP tool {tool_name} failed with status {response.status_code}: {response.text}")

                result = response.json()

                print(f"✅ MCP tool {tool_name} succeeded: {result}")  # Log success

                # Handle error responses from the MCP server
                if "error" in result:
                    print(f"❌ MCP tool {tool_name} returned error: {result['error']}")  # Log error
                    raise Exception(f"MCP tool {tool_name} returned error: {result['error']}")

                return result
        except httpx.RequestError as e:
            print(f"❌ HTTP request error for MCP tool {tool_name}: {str(e)}")  # Log error
            raise Exception(f"Failed to connect to MCP server: {str(e)}")
        except Exception as e:
            print(f"❌ Error calling MCP tool {tool_name}: {str(e)}")  # Log error
            raise Exception(f"Error calling MCP tool {tool_name}: {str(e)}")

    # Specific tool methods for convenience
    async def add_task(self, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Call the add_task MCP tool"""
        params = {
            "user_id": user_id,
            "title": title,
            "description": description
        }
        return await self.call_tool("add_task", params)

    async def list_tasks(self, user_id: str, status: Optional[str] = "all") -> Dict[str, Any]:
        """Call the list_tasks MCP tool"""
        params = {
            "user_id": user_id,
            "status": status
        }
        return await self.call_tool("list_tasks", params)

    async def complete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Call the complete_task MCP tool"""
        params = {
            "user_id": user_id,
            "task_id": task_id
        }
        return await self.call_tool("complete_task", params)

    async def delete_task(self, user_id: str, task_id: int) -> Dict[str, Any]:
        """Call the delete_task MCP tool"""
        params = {
            "user_id": user_id,
            "task_id": task_id
        }
        return await self.call_tool("delete_task", params)

    async def update_task(self, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """Call the update_task MCP tool"""
        params = {
            "user_id": user_id,
            "task_id": task_id
        }
        if title is not None:
            params["title"] = title
        if description is not None:
            params["description"] = description
        return await self.call_tool("update_task", params)


# Global instance of the MCP client
mcp_client = MCPServerClient()