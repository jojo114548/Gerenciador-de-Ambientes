def test_home_login(client):
    resp = client.get("/")
    assert resp.status_code == 200
