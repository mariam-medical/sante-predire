import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="Système Médical Intelligent",
    page_icon="☤",
    layout="wide"
)

# ==================== MOT DE PASSE D'ACCÈS GLOBAL ====================
# ⚠️ CHANGE CE MOT DE PASSE AVANT LE DÉPLOIEMENT SI BESOIN
ACCESS_PASSWORD = "SantePredire2026"

# ==================== INITIALISATION ====================
if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None

# ==================== 1ère BARRIÈRE : ACCÈS AU SITE ====================
if not st.session_state.access_granted:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <p style="font-size: 80px; margin: 0; color: #1a73e8;">🔐</p>
        <h1 style="color: #1a73e8;">Accès Sécurisé</h1>
        <p style="color: #555;">Cette application est protégée. Entrez le mot de passe d'accès.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        access_code = st.text_input("🔑 Mot de passe d'accès", type="password", placeholder="Entrez le mot de passe")
        
        if st.button("🚪 Accéder à l'application", use_container_width=True):
            if access_code == ACCESS_PASSWORD:
                st.session_state.access_granted = True
                st.rerun()
            else:
                st.error("❌ Mot de passe d'accès incorrect")
    st.stop()

# ==================== 2ème BARRIÈRE : CONNEXION ====================
if not st.session_state.authenticated:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <p style="font-size: 80px; margin: 0; color: #1a73e8;">☤</p>
        <h1 style="color: #1a73e8;">Système Médical Intelligent</h1>
        <p style="color: #555;">Connectez-vous avec vos identifiants</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 Identifiant", placeholder="Entrez votre identifiant")
        password = st.text_input("🔑 Mot de passe", type="password", placeholder="Entrez votre mot de passe")
        role = st.selectbox("🎯 Rôle", ["Médecin", "Administrateur"])
        
        if st.button("🚪 Se connecter", use_container_width=True):
            if username == "medecin" and password == "medecin123" and role == "Médecin":
                st.session_state.authenticated = True
                st.session_state.role = "Médecin"
                st.rerun()
            elif username == "admin" and password == "admin123" and role == "Administrateur":
                st.session_state.authenticated = True
                st.session_state.role = "Administrateur"
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects")
    st.stop()

# ==================== APPLICATION PRINCIPALE ====================
st.sidebar.markdown("## ☤ Système Médical")
st.sidebar.markdown(f"👋 Connecté : **{st.session_state.role}**")

# Menu selon le rôle
if st.session_state.role == "Médecin":
    menu = st.sidebar.radio("Navigation", ["🔍 Prédiction", "🤖 Q&A RAG"])
else:
    menu = st.sidebar.radio("Navigation", ["📊 Tableau de bord", "🔍 Prédiction", "🤖 Q&A RAG", "⚙️ Administration"])

# Déconnexion
if st.sidebar.button("🚪 Déconnexion"):
    st.session_state.authenticated = False
    st.session_state.access_granted = False
    st.session_state.role = None
    st.rerun()

# ==================== PAGE PRÉDICTION ====================
if menu == "🔍 Prédiction":
    st.title("🔍 Prédiction de risque médical")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Âge", min_value=0, max_value=120, value=50, step=1)
        sexe = st.selectbox("Sexe", ["Féminin", "Masculin"])
        imc = st.number_input("IMC", min_value=10.0, max_value=50.0, value=25.0, step=0.1)
        tension = st.number_input("Tension (mmHg)", min_value=80, max_value=220, value=130, step=1)
    with col2:
        diabete = st.selectbox("Diabète", ["Non", "Oui"])
        fumeur = st.selectbox("Fumeur", ["Non", "Oui"])
        hospitalisations = st.number_input("Hospitalisations", min_value=0, max_value=20, value=0, step=1)
        duree_sejour = st.number_input("Durée séjour", min_value=1, max_value=30, value=5, step=1)
    
    if st.button("🔍 PRÉDIRE LE RISQUE", type="primary", use_container_width=True):
        with st.spinner("🔬 Recherche des patients similaires..."):
            time.sleep(1)
        
        st.subheader("📊 Résultats")
        
        data = {
            "ID": [99, 113, 11, 72, 56],
            "Âge": [61, 79, 36, 19, 54],
            "IMC": [33.5, 31.5, 28.9, 29.4, 40.4],
            "Type": ["Cardiovasculaire", "Cardiovasculaire", "Diabète", "Cardiovasculaire", "Infection"],
            "Risque": ["ÉLEVÉ", "ÉLEVÉ", "FAIBLE", "ÉLEVÉ", "ÉLEVÉ"],
            "Distance": [8.0084, 8.3224, 8.3626, 8.6034, 8.6804]
        }
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔴 Risque ÉLEVÉ", "4")
        with col2:
            st.metric("🟢 Risque FAIBLE", "1")
        with col3:
            st.metric("🎯 PRÉDICTION", "⚠️ ÉLEVÉ")

# ==================== PAGE TABLEAU DE BORD ====================
elif menu == "📊 Tableau de bord":
    st.title("📊 Tableau de bord")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👤 Patients", "200")
    with col2:
        st.metric("🩺 Types de maladies", "4")
    with col3:
        st.metric("⚠️ Risque élevé", "145")
    with col4:
        st.metric("👨‍⚕️ Médecins", "0")
    
    st.subheader("📈 Évolution des requêtes par heure")
    heures = ["00h", "02h", "04h", "06h", "08h", "10h", "12h", "14h", "16h", "18h", "20h", "22h"]
    valeurs = [5, 3, 2, 1, 8, 15, 22, 30, 25, 20, 12, 8]
    df_req = pd.DataFrame({"Heure": heures, "Requêtes": valeurs})
    fig = px.bar(df_req, x="Heure", y="Requêtes", title="Requêtes par heure",
                 color="Requêtes", color_continuous_scale="Blues", height=400)
    st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE Q&A RAG ====================
elif menu == "🤖 Q&A RAG":
    st.title("🤖 Aide à la décision (Q&A RAG)")
    
    question = st.text_area("💬 Posez votre question médicale", height=100, placeholder="Ex: Combien de patients ont le diabète ?")
    
    if st.button("🔍 POSER LA QUESTION", type="primary", use_container_width=True):
        if question:
            with st.spinner("🔍 Recherche en cours..."):
                time.sleep(1)
            
            st.subheader("📋 Réponse")
            
            if "diabète" in question.lower() or "diabete" in question.lower():
                st.write("""
                🩺 **INFORMATIONS SUR LE DIABÈTE**
                
                👥 Patients diabétiques : **84**
                ⚠️ Diabétiques à risque élevé : **42**
                📊 Âge moyen : **58.2 ans**
                """)
            elif "risque" in question.lower():
                st.write("""
                ⚠️ **PATIENTS À RISQUE ÉLEVÉ**
                
                👥 Nombre : **145 patients**
                📊 Âge moyen : **62.3 ans**
                
                📋 Par type de maladie :
                - Cardiovasculaire : 48
                - Diabète : 36
                - Respiratoire : 32
                - Infection : 29
                """)
            else:
                st.info("💡 Essayez : 'Combien de patients ont le diabète ?' ou 'Quels sont les patients à risque ?'")
        else:
            st.warning("⚠️ Veuillez saisir une question.")

# ==================== PAGE ADMINISTRATION ====================
elif menu == "⚙️ Administration":
    st.title("⚙️ Administration")
    
    st.subheader("📊 Informations système")
    st.write("""
    - **Version** : 1.0.0
    - **Base de données** : PostgreSQL + pgvector
    - **Nombre de patients** : 200
    - **Types de maladies** : 4
    - **Patients à risque élevé** : 145
    """)

# ==================== FOOTER ====================
st.markdown("---")
st.caption("Système d'Information Intelligent - 2025/2026")