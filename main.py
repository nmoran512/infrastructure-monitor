"""This Python script will monitor static network infrastructure"""

from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

class Server(BaseModel):
    id : int
    hostname : str
    status : str

app = FastAPI()

servers = [
    {"id": 101, "hostname": "web-server-01", "status": "online"},
    {"id": 102, "hostname": "db-server-01", "status": "offline"},
    {"id": 103, "hostname": "dns-server-01", "status": "online"},
]

@app.get("/servers")
def get_servers():
    """Get the list of servers"""
    return servers

@app.get("/servers/{server_id}")
def get_server_id(server_id: int):
    for server in servers:
        if server["id"] == server_id:
            return server

    raise HTTPException(
        status_code = 404,
        detail = "Not Found"
    )

@app.post("/servers", status_code=201)
def create_server(server: Server):
    for s in servers:
        if s["id"] == server.id or s["hostname"] == server.hostname:
            raise HTTPException(
                status_code = 409,
                detail = "Already exists"
            )
    servers.append(server.model_dump())
    return server.model_dump()


@app.put("/servers/{server_id}")
def update_server(server_id: int, server: Server):
    if server.id != server_id:
        raise HTTPException(
            status_code = 400,
            detail = "Conflicting IDs"
        )
    for index, s in enumerate(servers):
        if s["id"] == server_id:
            servers[index] = server.model_dump()
            return servers[index]
    raise HTTPException(
        status_code = 404,
        detail = "Not Found"
    )

@app.delete("/servers/{server_id}", status_code=204)
def delete_server(server_id: int):
    for index, server in enumerate(servers):
        if server["id"] == server_id:
            del servers[index]
            return

    raise HTTPException(
        status_code = 404,
        detail = "Not Found"
    )