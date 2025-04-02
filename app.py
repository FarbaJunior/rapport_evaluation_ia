import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Personnalisation complète (logo et couleurs)
st.set_page_config(
    page_title="Générateur Rapport IA - Beautiful Soul",
    page_icon="🌺",
    layout="wide"
)

# Logo affiché en haut de page
st.image("Logo Beautiful Soul Vectorisé.png", width=200)

# Titres avec couleurs du logo
st.markdown("""
    <h1 style='text-align: center; color: #E7383A;'>🌺 Générateur Automatique de Rapports</h1>
    <h3 style='text-align: center; color: #F29325;'>Gestion du Changement & Leadership</h3>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📁 **Importer votre fichier CSV ou Excel**", type=['csv', 'xlsx'])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    st.success("✅ Données chargées avec succès !")
    st.dataframe(data, use_container_width=True)

    if st.button("🧠 **Générer le Rapport IA**"):
        with st.spinner("⏳ Génération du rapport en cours..."):

            moyenne = data['Note'].mean()
           
            fig = px.histogram(
                data, x='Note', nbins=5,
                title='📊 Distribution des Notes',
                color_discrete_sequence=['#F29325']
            )
            st.plotly_chart(fig, use_container_width=True)

            commentaires = data['Commentaire'].dropna().tolist()

            prompt = f"""
            Tu es un expert en rédaction professionnelle en gestion du changement et leadership.

            Voici les résultats d'une évaluation après une session :
            - Note moyenne : {moyenne:.2f}/5
            - Commentaires des participants : {commentaires}

            Rédige un rapport clair, professionnel structuré ainsi :

            1. **Introduction :** Contexte général rapide de la session.
            2. **Synthèse des évaluations :** Note globale et points forts/faibles mentionnés.
            3. **Analyse détaillée et recommandations concrètes :** Points à garder et améliorations précises à apporter.
            4. **Conclusion :** Résumé clair et proposition de prochaines étapes.

            Utilise un style clair, professionnel et dynamique.
            """

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}]
            )

            rapport = response.choices[0].message.content

            st.markdown("""
                <h2 style='color: #E7383A;'>📝 Rapport Généré</h2>
            """, unsafe_allow_html=True)

            st.markdown(rapport)

            st.download_button(
                "📥 Télécharger le Rapport",
                data=rapport,
                file_name="rapport_session.txt",
                mime="text/plain",
                help="Cliquez pour télécharger le rapport généré"
            )

# Style CSS pour les éléments interactifs
st.markdown("""
<style>
    .stButton > button {
        background-color: #E7383A;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    .stButton > button:hover {
        background-color: #F29325;
        color: white;
    }
    .stFileUploader {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)
