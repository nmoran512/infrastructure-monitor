"""This is the testing functions for pytest to test code."""
import pytest
from fastapi.testclient import TestClient
from main import app
import main

client = TestClient(app)

@pytest.fixture(autouse=True)
def default_servers():
    main.servers.clear()
    main.servers.extend([
        {"id": 101, "hostname": "web-server-01", "status": "online"},
        {"id": 102, "hostname": "db-server-01", "status": "offline"},
        {"id": 103, "hostname": "dns-server-01", "status": "online"},
    ])

def test_get_servers():
    response = client.get("/servers")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_get_server_by_id():
    response = client.get("/servers/101")
    assert response.status_code == 200
    response_data= response.json()
    assert response_data["id"] == 101 
    assert response_data["hostname"] == "web-server-01"

def test_get_server_not_found():
#tests the get by server id for a not valid server
    response = client.get("/servers/999")
    assert response.status_code == 404

def test_post_success():
#Test successful POST method
    new_server = {
        "id": 104,
        "hostname": "app-server-01",
        "status": "online"
    }
    response = client.post("/servers", json=new_server)
    assert response.status_code == 201
    response_json = response.json()
    assert response_json["id"] == 104
    assert response_json["hostname"] == "app-server-01"

def test_post_duplicate():
#Test posting an already established server
    new_server = {
        "id": 101, 
        "hostname": "web-server-01", 
        "status": "online"
    } 
    response = client.post("/servers", json=new_server)
    assert response.status_code == 409

def test_put_success():
#Testing a successful PUT request
    update_server = {
        "id": 102, 
        "hostname": "db-server-01", 
        "status": "online"
    }
    response = client.put("/servers/102", json=update_server)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == update_server["id"]
    assert response_json["hostname"] == update_server["hostname"]
    assert response_json["status"] == update_server["status"]

def test_put_conflicting_id():
#Testing the PUT method with conflicting IDs
    update_server = {
            "id": 102, 
            "hostname": "db-server-01", 
            "status": "online"
    }
    response = client.put("/servers/101" , json=update_server)
    assert response.status_code == 400

def test_put_with_not_found():
#Testing PUT request for 400 not found error
    update_server = {
                "id": 200, 
                "hostname": "db-server-01", 
                "status": "online"
    }
    response = client.put("/servers/200", json=update_server)
    assert response.status_code == 404

def test_delete_success():
#Test successful DELETE request
    response = client.delete("/servers/101")
    assert response.status_code == 204

def test_delete_unsuccessful():
#Test DELETE request on object not found
    response = client.delete("/servers/999")
    assert response.status_code == 404