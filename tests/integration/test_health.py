def test_health(client):
    response = client.get("/health")
    assert response.json == {"status": "Alive"}