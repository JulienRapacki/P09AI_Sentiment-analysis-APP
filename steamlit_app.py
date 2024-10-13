import streamlit as st
import requests
import pandas as pd
import plotly.express as px 


col = ["sentiment","text"]

data = pd.read_csv('https://drive.google.com/file/d/1Ci6qfxGyf7OTosW38CUYsfsvcLv8GMJa/view?usp=sharing',encoding = 'latin1', names= col)

data['sentiment'].plot(kind ='hist')


st.set_page_config(
    page_title="Real-Time Data Science Dashboard",
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

