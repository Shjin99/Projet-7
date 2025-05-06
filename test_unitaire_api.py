from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_welcome():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API de prédiction de défaut de crédit avec LightGBM"}

def test_get_clients():
    response = client.get("/clients")
    assert response.status_code == 200
    data = response.json()
    assert "client_ids" in data
    assert isinstance(data["client_ids"], list)
    assert len(data["client_ids"]) > 0  # S'assure que la liste n'est pas vide

def test_predict_valid_id():
    client_ids = client.get("/clients").json()["client_ids"]
    if client_ids:
        valid_id = client_ids[0]
        response = client.post("/predict", json={"client_id": valid_id})
        assert response.status_code == 200
        result = response.json()
        assert "prediction" in result
        assert "probability" in result
        assert isinstance(result["prediction"], int)
        assert 0 <= result["probability"] <= 1
    else:
        assert False, "La liste des client_ids est vide"

def test_predict_invalid_id():
    response = client.post("/predict", json={"client_id": -999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Client ID non trouvé dans le jeu de test"
