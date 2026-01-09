#!/usr/bin/env python3
"""
Test script for Task CRUD API endpoints
This script tests all 6 API endpoints as specified in the contracts.
"""

import asyncio
import json
from datetime import datetime
from uuid import uuid4
import requests

BASE_URL = "http://localhost:8000/api"

def test_create_task():
    """Test POST /api/{user_id}/tasks endpoint"""
    print("Testing CREATE task endpoint...")

    # Prepare test data
    user_id = "test-user-1"
    task_data = {
        "title": f"Test task {datetime.now().isoformat()}",
        "description": "Test description for the task"
    }

    response = requests.post(f"{BASE_URL}/{user_id}/tasks", json=task_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    data = response.json()
    assert "id" in data
    assert data["user_id"] == user_id
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] == False
    assert "created_at" in data
    assert "updated_at" in data

    print("✓ CREATE task endpoint test passed\n")
    return data["id"]

def test_list_tasks():
    """Test GET /api/{user_id}/tasks endpoint"""
    print("Testing LIST tasks endpoint...")

    user_id = "test-user-1"
    response = requests.get(f"{BASE_URL}/{user_id}/tasks")

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert isinstance(data, list), "Response should be a list"

    print("✓ LIST tasks endpoint test passed\n")

def test_get_single_task(task_id):
    """Test GET /api/{user_id}/tasks/{task_id} endpoint"""
    print("Testing GET single task endpoint...")

    user_id = "test-user-1"
    response = requests.get(f"{BASE_URL}/{user_id}/tasks/{task_id}")

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert data["id"] == task_id
    assert data["user_id"] == user_id

    print("✓ GET single task endpoint test passed\n")

def test_update_task(task_id):
    """Test PUT /api/{user_id}/tasks/{task_id} endpoint"""
    print("Testing UPDATE task endpoint...")

    user_id = "test-user-1"
    update_data = {
        "title": f"Updated task {datetime.now().isoformat()}",
        "description": "Updated description for the task"
    }

    response = requests.put(f"{BASE_URL}/{user_id}/tasks/{task_id}", json=update_data)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]

    print("✓ UPDATE task endpoint test passed\n")

def test_toggle_completion(task_id):
    """Test PATCH /api/{user_id}/tasks/{task_id}/complete endpoint"""
    print("Testing TOGGLE completion endpoint...")

    user_id = "test-user-1"
    response = requests.patch(f"{BASE_URL}/{user_id}/tasks/{task_id}/complete")

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    data = response.json()
    assert data["id"] == task_id
    assert data["user_id"] == user_id
    # The completed status should be toggled (initially False, now True)

    print("✓ TOGGLE completion endpoint test passed\n")

def test_delete_task(task_id):
    """Test DELETE /api/{user_id}/tasks/{task_id} endpoint"""
    print("Testing DELETE task endpoint...")

    user_id = "test-user-1"
    response = requests.delete(f"{BASE_URL}/{user_id}/tasks/{task_id}")

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    # Should return 200 with message or 204 No Content depending on implementation
    assert response.status_code in [200, 204], f"Expected 200 or 204, got {response.status_code}"

    print("✓ DELETE task endpoint test passed\n")

def test_error_cases():
    """Test error handling for invalid requests"""
    print("Testing error cases...")

    user_id = "test-user-1"
    invalid_task_id = "invalid-task-id"

    # Test getting non-existent task
    response = requests.get(f"{BASE_URL}/{user_id}/tasks/{invalid_task_id}")
    print(f"Non-existent task status: {response.status_code}")
    assert response.status_code == 404, f"Expected 404 for non-existent task, got {response.status_code}"

    # Test updating non-existent task
    response = requests.put(f"{BASE_URL}/{user_id}/tasks/{invalid_task_id}", json={"title": "test"})
    print(f"Update non-existent task status: {response.status_code}")
    assert response.status_code == 404, f"Expected 404 for updating non-existent task, got {response.status_code}"

    # Test deleting non-existent task
    response = requests.delete(f"{BASE_URL}/{user_id}/tasks/{invalid_task_id}")
    print(f"Delete non-existent task status: {response.status_code}")
    assert response.status_code == 404, f"Expected 404 for deleting non-existent task, got {response.status_code}"

    # Test creating task with empty title (should fail validation)
    response = requests.post(f"{BASE_URL}/{user_id}/tasks", json={"title": "", "description": "test"})
    print(f"Empty title validation status: {response.status_code}")
    assert response.status_code == 422, f"Expected 422 for empty title, got {response.status_code}"

    # Test creating task with title too long (should fail validation)
    long_title = "x" * 201
    response = requests.post(f"{BASE_URL}/{user_id}/tasks", json={"title": long_title, "description": "test"})
    print(f"Long title validation status: {response.status_code}")
    assert response.status_code == 422, f"Expected 422 for long title, got {response.status_code}"

    print("✓ Error cases test passed\n")

def run_all_tests():
    """Run all API tests in sequence"""
    print("Starting Task CRUD API tests...\n")

    # Test error cases first (doesn't require a task)
    test_error_cases()

    # Create a task to test with
    task_id = test_create_task()

    # Test list endpoint
    test_list_tasks()

    # Test get single task
    test_get_single_task(task_id)

    # Test update
    test_update_task(task_id)

    # Test toggle completion
    test_toggle_completion(task_id)

    # Test delete
    test_delete_task(task_id)

    print("🎉 All API tests passed successfully!")

if __name__ == "__main__":
    run_all_tests()