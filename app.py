import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Rapport Évaluation Session", page_icon="🌺", layout="wide")
st.image("logo_beautiful_soul.png", width=200)

st.markdown("""
    <h1 style='text-align: center; color: #E7383A;'>🌺 Rapport Automatique de Session</h1>
    <h3 style='text-align: center; color: #F29325;'>Évaluations participants Beautiful Soul</h3>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("📁 Importer votre fichier CSV ou Excel", type=['csv', 'xlsx'])

if uploaded_file:
    data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    st.success("✅ Données chargées !")
    st.dataframe(data, use_container_width=True)

    required_cols = {
        'Changements_collectifs', 'Changements_individuels', 
        'Satisfaction', 'Recommandation', 'Appreciation', 'Suggestions'
    }

    if required_cols.issubset(data.columns):
        if st.button("🧠 Générer Rapport IA"):
            with st.spinner("⏳ Génération du rapport en cours..."):

                satisfaction_moyenne = data['Satisfaction'].mean()
                recommandation_moyenne = data['Recommandation'].mean()

                fig1 = px.histogram(data, x='Satisfaction', nbins=10, title='📊 Satisfaction globale (0-10)', color_discrete_sequence=['#E7383A'])
                fig2 = px.histogram(data, x='Recommandation', nbins=10, title='📊 Probabilité de recommandation (0-10)', color_discrete_sequence=['#F29325'])

                st.plotly_chart(fig1, use_container_width=True)
                st.plotly_chart(fig2, use_container_width=True)

                prompt = f"""
                Tu es un expert en rédaction professionnelle en gestion du changement organisationnel et développement du leadership.

                Voici les résultats d'une évaluation suite à une session :

                Satisfaction moyenne : {satisfaction_moyenne:.2f}/10
                Probabilité moyenne de recommandation : {recommandation_moyenne:.2f}/10

                Changements observés au niveau collectif :
                {data['Changements_collectifs'].dropna().tolist()}

                Changements observés au niveau individuel :
                {data['Changements_individuels'].dropna().tolist()}

                Ce que les participants ont le plus apprécié :
                {data['Appreciation'].dropna().tolist()}

                Suggestions d'amélioration :
                {data['Suggestions'].dropna().tolist()}

                Rédige un rapport professionnel structuré ainsi :

                1. Introduction générale
                2. Synthèse quantitative (satisfaction et recommandation)
                3. Analyse qualitative des changements observés (collectifs et individuels)
                4. Principaux points appréciés par les participants
                5. Axes précis d'amélioration proposés par les participants
                6. Conclusion et recommandations concrètes pour les prochaines sessions

                Style clair, professionnel et axé résultats.
                """

                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "system", "content": prompt}]
                )

                rapport = response.choices[0].message.content
                st.markdown("<h2 style='color: #E7383A;'>📝 Rapport de Session</h2>", unsafe_allow_html=True)
                st.markdown(rapport)
                st.download_button("📥 Télécharger Rapport", data=rapport, file_name="rapport_session.txt")

    else:
        st.error(f"⚠️ Votre fichier doit obligatoirement contenir les colonnes : {required_cols}")

st.markdown("""
<style>
    .stButton > button {background-color: #E7383A; color: white;}
    .stButton > button:hover {background-color: #F29325;}
</style>
""", unsafe_allow_html=True)
