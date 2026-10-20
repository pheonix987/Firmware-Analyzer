def test_clear_route(client):
    response = client.delete("clear")
    assert response.json == {"message": "Cleared Successfully"}
    assert response.status_code == 200