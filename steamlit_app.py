import streamlit as st
import requests


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

