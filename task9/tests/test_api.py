import pytest


@pytest.mark.anyio
async def test_register_login(client):
    r = await client.post("/register", json={"username": "a", "password": "1"})
    assert r.status_code == 200
    r = await client.post("/login", json={"username": "a", "password": "1"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    hdr = {"Authorization": f"Bearer {token}"}
    r = await client.get("/users/me", headers=hdr)
    assert r.status_code == 200
    assert r.json()["username"] == "a"
    r = await client.get("/users/me")
    assert r.status_code == 401


@pytest.mark.anyio
async def test_notes_isolation(client):
    await client.post("/register", json={"username": "u1", "password": "p"})
    await client.post("/register", json={"username": "u2", "password": "p"})
    t1 = (await client.post("/login", json={"username": "u1", "password": "p"})).json()["access_token"]
    t2 = (await client.post("/login", json={"username": "u2", "password": "p"})).json()["access_token"]
    h1 = {"Authorization": f"Bearer {t1}"}
    h2 = {"Authorization": f"Bearer {t2}"}
    r = await client.post("/notes", json={"text": "n1"}, headers=h1)
    nid = r.json()["id"]
    r = await client.get("/notes", headers=h1)
    assert len(r.json()) == 1
    r = await client.get("/notes", headers=h2)
    assert len(r.json()) == 0
    r = await client.get(f"/notes/{nid}", headers=h2)
    assert r.status_code == 404
    r = await client.delete(f"/notes/{nid}", headers=h2)
    assert r.status_code == 404
    r = await client.delete(f"/notes/{nid}", headers=h1)
    assert r.status_code == 204
    r = await client.get("/notes", headers=h1)
    assert len(r.json()) == 0
