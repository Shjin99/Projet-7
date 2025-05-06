from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
import os
from lightgbm import LGBMClassifier

# Créer l'API
app = FastAPI()

# --- Chemins relatifs vers les fichiers ---
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, "LGBMClassifier1.pkl")
test_path = os.path.join(current_dir, "application_test.csv")

# --- Charger le modèle ---
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# --- Fonction pour charger les données à la demande ---
def load_test_data():
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"Fichier introuvable : {test_path}")
    
    df = pd.read_csv(test_path, index_col=0)
    
    # Vérifier si la colonne 'TARGET' existe et ne pas l'utiliser si elle est absente
    if "TARGET" in df.columns:
        df = df.drop(columns=["TARGET"])
    
    return df

# --- Schémas Pydantic ---
class ClientID(BaseModel):
    client_id: int

class PredictionResult(BaseModel):
    prediction: int
    probability: float

# --- Endpoints ---
@app.get("/")
def welcome():
    return {"message": "API de prédiction de défaut de crédit avec LightGBM"}

@app.get("/clients")
def get_client_ids():
    df = load_test_data()
    return {"client_ids": df.index.tolist()}

@app.post("/predict", response_model=PredictionResult)
def predict(client: ClientID):
    df = load_test_data()

    client_id = client.client_id
    if client_id not in df.index:
        raise HTTPException(status_code=404, detail="Client ID non trouvé dans le jeu de test")

    try:
        model_features = df.columns.tolist()
        client_data = df.loc[client_id, model_features]
        client_input = pd.DataFrame([client_data])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données client : {str(e)}")

    try:
        probability = float(model.predict_proba(client_input)[0][1])
        prediction = int(probability >= 0.2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la prédiction : {str(e)}")

    return PredictionResult(prediction=prediction, probability=probability)

















