import streamlit as st
import requests
import pandas as pd
import plotly.express as px 

import io
from azure.storage.blob import BlobServiceClient


source = 'https://iaprojet9.blob.core.windows.net/datap09/training.1600000.processed.noemoticon.csv?sp=r&st=2024-10-13T15:49:55Z&se=2024-10-13T23:49:55Z&sv=2022-11-02&sr=b&sig=AdZWjPFpKQ7SKNdUtKK%2FaChZSxgXJCIBMCKoNzfCqPM%3D'


col = ["sentiment", "ids", "date", "flag", "user", "text"]
data = pd.read_csv(source,encoding = 'latin1', names= col)

data['sentiment'].plot(kind ='hist')


st.set_page_config(
    page_title="Tableau de bord Projet 9 ",
    page_icon="✅",
    layout="wide",
)
fig = px.histogram(title='Distribution des classes',
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

