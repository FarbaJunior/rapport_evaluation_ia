import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
import os

# Utiliser secrets Streamlit Cloud directement
openai_api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=openai_api_key)

# Interface Streamlit reste identique (rien d'autre à changer)

st.set_page_config(page_title="Générateur Rapport IA - Beautiful Soul", page_icon="🌺", layout="wide")
st.image("Logo Beautiful Soul Vectorisé.png", width=200)

st.markdown("""
    <h1 style='text-align: center; color: #E7383A;'>🌺 Générateur Automatique de Rapports</h1>
    <h3 style='text-align: center; color: #F29325;'>Gestion du Changement & Leadership</h3>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📁 Importer votre fichier CSV ou Excel", type=['csv', 'xlsx'])

if uploaded_file:
    data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.success("✅ Données chargées !")
    st.dataframe(data, use_container_width=True)

    if st.button("🧠 Générer le Rapport IA"):
        with st.spinner("⏳ Génération du rapport..."):
            moyenne = data['Note'].mean()
            fig = px.histogram(data, x='Note', nbins=5, title='📊 Distribution des Notes', color_discrete_sequence=['#F29325'])
            st.plotly_chart(fig, use_container_width=True)

            commentaires = data['Commentaire'].dropna().tolist()
            prompt = f"""
            Tu es un expert en rédaction professionnelle en gestion du changement et leadership.
            Voici les résultats d'une évaluation après une session :
            - Note moyenne : {moyenne:.2f}/5
            - Commentaires : {commentaires}
            Génère un rapport professionnel structuré (Intro, Synthèse, Analyse, Conclusion).
            """

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}]
            )

            rapport = response.choices[0].message.content
            st.markdown("<h2 style='color: #E7383A;'>📝 Rapport Généré</h2>", unsafe_allow_html=True)
            st.markdown(rapport)
            st.download_button("📥 Télécharger le Rapport", data=rapport, file_name="rapport_session.txt")

st.markdown("""
<style>
    .stButton > button {background-color: #E7383A; color: white;}
    .stButton > button:hover {background-color: #F29325;}
</style>
""", unsafe_allow_html=True)
