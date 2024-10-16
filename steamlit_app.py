import streamlit as st
import requests
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px 

import io
from azure.storage.blob import BlobServiceClient




st.set_page_config(
    page_title="Tableau de bord Projet 9 : Anlyse de sentiments",
    page_icon="🧊",
    # layout="wide",
    menu_items={
    'Get Help': 'https://www.extremelycoolapp.com/help',
    'Report a bug': "https://www.extremelycoolapp.com/bug",
    'About': "# This is a header. This is an *extremely* cool app!"}
)


@st.cache_data(persist=True)
def load_file():
    source = 'https://iaprojet9.blob.core.windows.net/datap09-2/training.1600000.processed.noemoticon.csv?sp=racwdyt&st=2024-10-16T16:07:39Z&se=2024-11-08T01:07:39Z&spr=https&sv=2022-11-02&sr=b&sig=ytlI1KJUF65RcN4vMnDsF7QE6eLqJBbcuzZQ5rxPmao%3D'
    col = ["sentiment", "ids", "date", "flag", "user", "text"]
    data = pd.read_csv(source,encoding='latin1',names=col)
    data['sentiment'] = data['sentiment'].map({0: 'negative', 4: 'positive'})
    return data


data = load_file()
data_sample = data.sample(50)


st.markdown("<h1 style='color: #7350EA;'>Tableau de bord Projet 9 : Analyse de sentiments</h1>", unsafe_allow_html=True)

st.write('### Aperçu des données')       
st.dataframe(data_sample,use_container_width= True)

col1,col2 = st.columns([.5,.5],gap='medium',
                        vertical_alignment= "bottom")

# WordCloud
with col1:
    col1.subheader('Distribution de la Longueur des Phrases')
    data['txt_length'] = data['text'].apply(len)
    fig1 = px.histogram(data, x='txt_length', nbins=10, 
    labels={'txt_length': 'Longueur des phrases'},
    color_discrete_sequence=['#7350EA'])
    st.write(fig1)

# Histogram
with col2:
    col2.subheader('Distribution des classes ')
    fig = px.histogram(
            data_frame=data, x="sentiment",
            color_discrete_sequence=['#7350EA'])
    st.write(fig)

#WordCloud
st.write('### Nuage de Mots')
text_cloud = " ".join(data_sample['text'])
wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(text_cloud)
fig, ax = plt.subplots(figsize=(8, 4))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# URL API Azure
API_URL = "https://apip09.azurewebsites.net/predict"


#----------------------------------------------------------------------------------------

#     if 'sentiment' not in st.session_state:
#         st.session_state.sentiment = None

#         st.write('### Test du modèle')
    
#         user_input = st.text_input("Entrez une phrase :")

#         # Fonction pour analyser le sentiment
#         def analyze_sentiment():
        
#             response = requests.post(f"{API_URL}/predict_sentiment", params={"text":user_input})
#             st.session_state.sentiment = response.json()['sentiment']
#             
        
        
#         st.session_state.feedback_given = False

#         # Bouton pour analyser
#         if st.button("Analyser"):
#             analyze_sentiment()

# if __name__=="__main__":
#     main()
# Fonction pour analyser le sentiment
st.write('### Test du modèle')

user_input = st.text_input("Entrez une phrase :")

def analyze_sentiment():
    if user_input:
        response = requests.post(f"{API_URL}", json={"text": user_input})
        if response.status_code == 200:
            result = response.json()
            st.session_state.sentiment = result['sentiment']
        else:
            st.error(f"Erreur de l'API: {response.status_code}")

# Afficher le sentiment si déjà calculé
if 'sentiment' in st.session_state:
    st.write(f"**Résultat de l'analyse :** {st.session_state.sentiment}")
    

# Bouton pour analyser
if st.button("Analyser"):
    analyze_sentiment()

