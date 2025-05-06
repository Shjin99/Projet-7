from fastapi import FastAPI, HTTPException
import pandas as pd
import pickle
from pydantic import BaseModel
from lightgbm import LGBMClassifier
import uvicorn
import os

# --- Obtenir le répertoire du fichier actuel (api.py) ---
current_dir = os.path.dirname(__file__)

# --- Chemins relatifs vers les fichiers ---
model_path = os.path.join(current_dir, "LGBMClassifier1.pkl")
test_path = os.path.join(current_dir, "application_test.csv")

# --- Charger le modèle pré-entraîné ---
with open(model_path, 'rb') as f:
    model = pickle.load(f)

application_test = pd.read_csv(test_path, index_col=0)

# --- Définir les features utilisées par le modèle
model_features = application_test.drop(columns=["TARGET"]).columns.tolist()

# --- Créer l'API ---
app = FastAPI()

class ClientID(BaseModel):
    client_id: int

class PredictionResult(BaseModel):
    prediction: int
    probability: float

@app.get("/")
def welcome():
    return {"message": "API de prédiction de défaut de crédit avec LightGBM"}

@app.get("/clients")
def get_client_ids():
    return {"client_ids": application_test.index.tolist()}

@app.post("/predict", response_model=PredictionResult)
def predict(client: ClientID):
    client_id = client.client_id

    # Vérifier que le client_id existe dans le DataFrame (index)
    if client_id not in application_test.index:
        raise HTTPException(status_code=404, detail="Client ID non trouvé dans le jeu de test")

    try:
        # Extraire les données pour le client à partir de l'index
        client_data = application_test.loc[client_id, model_features]
        client_input = pd.DataFrame([client_data])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données client : {str(e)}")

    try:
        # Effectuer la prédiction avec le modèle
        probability = float(model.predict_proba(client_input)[0][1])
        prediction = int(probability >= 0.2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")

    return PredictionResult(prediction=prediction, probability=probability)















