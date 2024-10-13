import streamlit as st
import requests
import pandas as pd
import plotly.express as px 

import io
from azure.storage.blob import BlobServiceClient


connection_string = "DefaultEndpointsProtocol=https;AccountName=iaprojet9;AccountKey=FRefYH7L7rj9B7hWclYNiRoOPOcK0z46/6NvT50aEvHM+cn4P/1+WEkFNyweLJk4E0qqYa6HMWAX+AStGbeb1Q==;EndpointSuffix=core.windows.net"
container_name = "datap09"
blob_name = "training.1600000.processed.noemoticon.csv"

# Créer un client BlobService
blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Créer un client pour le conteneur
container_client = blob_service_client.get_container_client(container_name)

# Lire le fichier CSV directement depuis le Blob Storage
blob_client = container_client.get_blob_client(blob_name)

# Télécharger le contenu du blob dans un DataFrame Pandas
blob_data = blob_client.download_blob()
col = ["sentiment", "ids", "date", "flag", "user", "text"]
data = pd.read_csv(io.BytesIO(blob_data.readall()),encoding = 'latin1', names= col)

data['sentiment'].plot(kind ='hist')


st.set_page_config(
    page_title="Tableau de bord Projet 9",
    page_icon="✅",
    layout="wide",
)
fig = px.histogram(
        data_frame=data, y="sentiment")
st.write(fig)

# URL de votre API Azure
API_URL = "https://p07.azurewebsites.net"


#----------------------------------------------------------------------------------------

if 'sentiment' not in st.session_state:
    st.session_state.sentiment = None
if 'feedback_given' not in st.session_state:
    st.session_state.feedback_given = False

st.title("Analyse de sentiment")

user_input = st.text_input("Entrez une phrase :")

# Fonction pour analyser le sentiment
def analyze_sentiment():
    
    response = requests.post(f"{API_URL}/predict_sentiment", params={"text":user_input})
    st.session_state.sentiment = response.json()['sentiment']
    st.session_state.probability = response.json()['probability']
    
    
st.session_state.feedback_given = False

# Bouton pour analyser
if st.button("Analyser"):
    analyze_sentiment()

