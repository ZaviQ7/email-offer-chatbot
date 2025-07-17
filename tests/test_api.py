from api.api import app

def test_zestimate_endpoint():
    client = app.test_client()
    resp = client.post("/zestimate", json={"address": "123 Main St"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["address"] == "123 Main St"
    assert isinstance(data["zestimate"], (int, float))
