import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Rapport Évaluation Session", page_icon="🌺", layout="wide")
st.image("logo_bs.png", width=200)

st.markdown("""
    <h1 style='text-align: center; color: #E7383A;'>🌺 Rapport Automatique de Session</h1>
    <h3 style='text-align: center; color: #F29325;'>Évaluations participants Beautiful Soul</h3>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📁 Importer votre fichier CSV ou Excel", type=['csv', 'xlsx'])

if uploaded_file:
    data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.success("✅ Données chargées !")
    st.dataframe(data, use_container_width=True)

    # Colonnes attendues (mais optionnelles)
    expected_cols = {
        'Changements_collectifs', 'Changements_individuels', 
        'Satisfaction', 'Recommandation', 'Appreciation', 'Suggestions'
    }

    missing = expected_cols - set(data.columns)
    if missing:
        st.warning(f"⚠️ Certaines colonnes sont absentes du fichier : {missing}. Le rapport sera généré avec les données disponibles.")

    if st.button("🧠 Générer Rapport IA"):
        with st.spinner("⏳ Génération du rapport en cours..."):
            # Valeurs par défaut si colonnes manquantes
            satisfaction_moyenne = data['Satisfaction'].mean() if 'Satisfaction' in data else "Non disponible"
            recommandation_moyenne = data['Recommandation'].mean() if 'Recommandation' in data else "Non disponible"
            changements_collectifs = data['Changements_collectifs'].dropna().tolist() if 'Changements_collectifs' in data else []
            changements_individuels = data['Changements_individuels'].dropna().tolist() if 'Changements_individuels' in data else []
            appreciations = data['Appreciation'].dropna().tolist() if 'Appreciation' in data else []
            suggestions = data['Suggestions'].dropna().tolist() if 'Suggestions' in data else []

            # Graphiques si données présentes
            if 'Satisfaction' in data:
                fig1 = px.histogram(data, x='Satisfaction', nbins=10, title='📊 Satisfaction globale (0-10)', color_discrete_sequence=['#E7383A'])
                st.plotly_chart(fig1, use_container_width=True)
            if 'Recommandation' in data:
                fig2 = px.histogram(data, x='Recommandation', nbins=10, title='📊 Probabilité de recommandation (0-10)', color_discrete_sequence=['#F29325'])
                st.plotly_chart(fig2, use_container_width=True)

            # Prompt GPT-4o
            prompt = f"""
            Tu es un expert en rédaction professionnelle en gestion du changement et leadership.

            Résumé des données d'évaluation collectées lors d'une session :

            Satisfaction moyenne : {satisfaction_moyenne}
            Probabilité moyenne de recommandation : {recommandation_moyenne}

            Changements observés (collectifs) :
            {changements_collectifs}

            Changements observés (individuels) :
            {changements_individuels}

            Appréciations des participants :
            {appreciations}

            Suggestions d'amélioration :
            {suggestions}

            Génère un rapport professionnel structuré en :
            1. Introduction
            2. Analyse quantitative
            3. Analyse qualitative
            4. Ce qui a été apprécié
            5. Axes d'amélioration
            6. Conclusion et recommandations
            """

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": prompt}]
            )

            rapport = response.choices[0].message.content
            st.markdown("<h2 style='color: #E7383A;'>📝 Rapport de Session</h2>", unsafe_allow_html=True)
            st.markdown(rapport)
            st.download_button("📥 Télécharger Rapport", data=rapport, file_name="rapport_session.txt")

st.markdown("""
<style>
    .stButton > button {background-color: #E7383A; color: white;}
    .stButton > button:hover {background-color: #F29325;}
</style>
""", unsafe_allow_html=True)
