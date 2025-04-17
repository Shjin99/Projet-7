import streamlit as st
import requests
import pandas as pd

# URL de ton API FastAPI
API_URL = "https://credit-api-j1n5.onrender.com/predict"  # Si ton API tourne en local sur ce port, sinon mets l'URL correcte

# Titre de l'application Streamlit
st.title("Prédiction de défaut de crédit")

# Description de l'application
st.markdown("""
Cette application permet de prédire si un client fera défaut sur un prêt à partir de son ID client.
Entrez l'ID du client pour obtenir la prédiction.
""")

# Demander l'ID du client via l'interface Streamlit
client_id = st.number_input("Entrez l'ID du client", min_value=0, step=1)

# Lorsque l'utilisateur clique sur le bouton "Prédire"
if st.button("Prédire"):
    if client_id >= 0:
        # Envoyer une requête POST à ton API FastAPI avec l'ID du client
        response = requests.post(API_URL, json={"client_id": client_id})
        
        if response.status_code == 200:
            # Si la requête est réussie, on récupère la prédiction
            prediction_data = response.json()
            
            # Afficher la prédiction et la probabilité
            st.write(f"**Prédiction** : {'Défaut' if prediction_data['prediction'] == 1 else 'Non défaut'}")
            st.write(f"**Probabilité de défaut** : {prediction_data['probability']:.2f}")
            
            # Ajouter la décision de crédit accepté ou refusé
            if prediction_data['prediction'] == 1:
                st.write("**Crédit Refusé** : Le client a été jugé à risque de défaut.")
            else:
                st.write("**Crédit Accepté** : Le client a été jugé fiable.")
        else:
            st.error("Erreur lors de la récupération de la prédiction. Vérifiez l'ID du client.")
    else:
        st.warning("L'ID du client doit être supérieur ou égal à 0.")

