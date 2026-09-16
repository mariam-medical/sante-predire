import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# ==================== CONFIGURATION ====================
st.set_page_config(
    page_title="Système Médical Intelligent",
    page_icon="✚",
    layout="wide"
)

# ==================== STYLE GLOBAL ====================
st.markdown("""
<style>
/* ===== BOUTONS HTML COLORÉS (Ajouter/Modifier/Supprimer) ===== */
.btn-group {
    display: flex;
    gap: 12px;
    margin-bottom: 25px;
}
.btn-group a {
    flex: 1;
    padding: 14px 20px;
    border-radius: 6px;
    text-align: center;
    font-weight: bold;
    color: white !important;
    text-decoration: none !important;
    font-size: 1.05rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    border: 2px solid #000;
    cursor: pointer;
    display: block;
}
.btn-group a:hover {
    opacity: 0.9;
    color: white !important;
    text-decoration: none !important;
}
.btn-ajouter { background-color: #34a853 !important; }
.btn-modifier { background-color: #1a73e8 !important; }
.btn-supprimer { background-color: #d93025 !important; }

/* ===== Bouton Déconnexion en ROUGE (sidebar) ===== */
section[data-testid="stSidebar"] div.stButton > button {
    background-color: #d93025 !important;
    color: white !important;
    border: none !important;
    font-weight: bold !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] div.stButton > button:hover {
    background-color: #a50e0e !important;
    color: white !important;
}

/* ===== Bouton "Se connecter" / "Accéder" EN BLEU ===== */
div[data-testid="stForm"] button[kind="primaryFormSubmit"],
div[data-testid="stForm"] button[kind="secondaryFormSubmit"] {
    background-color: #1a73e8 !important;
    color: white !important;
    border: none !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
    padding: 12px !important;
    border-radius: 4px !important;
    width: 100% !important;
}
div[data-testid="stForm"] button[kind="primaryFormSubmit"]:hover,
div[data-testid="stForm"] button[kind="secondaryFormSubmit"]:hover {
    background-color: #0d47a1 !important;
    color: white !important;
}

/* ===== Labels EN GRAS (TOUS les champs) ===== */
div[data-testid="stForm"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stSelectbox"] label,
.stTextInput > label,
.stSelectbox > label,
.stNumberInput > label,
.stTextArea > label {
    font-weight: bold !important;
    color: #000 !important;
    font-size: 1.05rem !important;
}

/* ===== Titres ===== */
.main-title { color: #1a73e8; font-size: 2.2rem; font-weight: bold; }
.sub-title { color: #34a853; font-size: 1.4rem; font-weight: 600; }

/* ===== Style des pages auth ===== */
.auth-icon {
    text-align: center;
    margin: 30px 0 10px 0;
    line-height: 1;
}
.auth-title {
    text-align: center;
    color: #1a73e8;
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 5px;
}
.auth-sub {
    text-align: center;
    color: #666;
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)

# ==================== MOT DE PASSE D'ACCÈS GLOBAL ====================
ACCESS_PASSWORD = "SantePredire2026"

# ==================== INITIALISATION ====================
if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
if 'medecin_action' not in st.session_state:
    st.session_state.medecin_action = "ajouter"

# ==================== DONNÉES SIMULÉES ====================
if 'patients' not in st.session_state:
    np.random.seed(42)
    types_maladie = ["Cardiovasculaire", "Diabète", "Respiratoire", "Infection"]
    st.session_state.patients = pd.DataFrame({
        'ID': range(1, 201),
        'Âge': np.random.randint(18, 80, 200),
        'Sexe': np.random.choice(['F', 'M'], 200),
        'IMC': np.round(np.random.uniform(17, 40, 200), 1),
        'Tension': np.random.randint(100, 180, 200),
        'Diabète': np.random.choice([0, 1], 200),
        'Fumeur': np.random.choice([0, 1], 200),
        'Hospitalisations': np.random.randint(0, 6, 200),
        'Durée séjour': np.random.randint(1, 10, 200),
        'Type maladie': np.random.choice(types_maladie, 200),
        'Risque': np.random.choice([0, 1], 200, p=[0.3, 0.7])
    })

if 'medecins' not in st.session_state:
    st.session_state.medecins = pd.DataFrame({
        'ID': [1, 2],
        'Nom': ['Dupont', 'Martin'],
        'Prénom': ['Jean', 'Sophie'],
        'Email': ['jean.dupont@hopital.fr', 'sophie.martin@hopital.fr'],
        'Spécialité': ['Cardiologie', 'Pédiatrie'],
        'Téléphone': ['0102030405', '0607080910']
    })

# ==================== LECTURE DES PARAMÈTRES D'URL ====================
query_action = st.query_params.get("action", None)
if query_action:
    st.session_state.medecin_action = query_action

# ==================== 1ère BARRIÈRE : ACCÈS AU SITE (CLÉ ARGENT) ====================
if not st.session_state.access_granted:
    st.markdown('''
    <div class="auth-icon">
    <svg width="100" height="100" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="silverGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#F0F0F0;stop-opacity:1" />
                <stop offset="50%" style="stop-color:#C0C0C0;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#909090;stop-opacity:1" />
            </linearGradient>
        </defs>
        <path d="M12.65 10C11.83 7.67 9.61 6 7 6C3.69 6 1 8.69 1 12C1 15.31 3.69 18 7 18C9.61 18 11.83 16.33 12.65 14H17V17H20V14H21V12H12.65ZM7 15C5.35 15 4 13.65 4 12C4 10.35 5.35 9 7 9C8.65 9 10 10.35 10 12C10 13.65 8.65 15 7 15Z" 
              fill="url(#silverGrad1)" 
              stroke="#707070" 
              stroke-width="0.7"/>
    </svg>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">Accès Sécurisé</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">Cette application est protégée. Entrez le mot de passe d\'accès.</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("access_form"):
            access_code = st.text_input("Mot de passe d'accès", type="password", key="access_pwd")
            submit_access = st.form_submit_button("Accéder à l'application", use_container_width=True)
        
        if submit_access:
            if access_code == ACCESS_PASSWORD:
                st.session_state.access_granted = True
                st.rerun()
            else:
                st.error("❌ Mot de passe d'accès incorrect")
    st.stop()

# ==================== 2ème BARRIÈRE : CONNEXION (CROIX ROUGE) ====================
if not st.session_state.authenticated:
    st.markdown('''
    <div class="auth-icon">
    <svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <rect x="40" y="10" width="20" height="80" fill="#d93025" rx="3"/>
        <rect x="10" y="40" width="80" height="20" fill="#d93025" rx="3"/>
    </svg>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">Système Médical Intelligent</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-sub">Connectez-vous avec vos identifiants</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Identifiant", key="login_user")
            password = st.text_input("Mot de passe", type="password", key="login_pass")
            role = st.selectbox("Rôle", ["Médecin", "Administrateur"], key="login_role")
            submit_login = st.form_submit_button("Se connecter", use_container_width=True)
        
        if submit_login:
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
st.sidebar.markdown("## ✚ Système Médical")
st.sidebar.markdown(f"👋 Connecté : **{st.session_state.role}**")
st.sidebar.markdown("---")

# ==================== MENU SELON LE RÔLE ====================
if st.session_state.role == "Médecin":
    menu = st.sidebar.radio("Navigation", ["🔍 Prédiction", "🤖 Aide à la décision"])
else:
    menu = st.sidebar.radio("Navigation", [
        "📊 Tableau de bord",
        "🔍 Prédiction",
        "🤖 Aide à la décision",
        "👨‍⚕️ Gestion des médecins",
        "📋 Dossiers médicaux",
        "⚙️ Administration"
    ])

# Déconnexion ROUGE
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Déconnexion", use_container_width=True, key="btn_logout"):
    st.session_state.authenticated = False
    st.session_state.access_granted = False
    st.session_state.role = None
    st.query_params.clear()
    st.rerun()

# ==================== PAGE PRÉDICTION ====================
if menu == "🔍 Prédiction":
    st.title("🔍 Prédiction de risque médical")
    
    st.subheader("📋 Saisie du patient")
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
    
    if st.button("🔍 PRÉDIRE LE RISQUE", use_container_width=True, key="btn_predict", type="primary"):
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
    df = st.session_state.patients
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👤 Patients", len(df))
    with col2:
        st.metric("🩺 Types de maladies", df['Type maladie'].nunique())
    with col3:
        st.metric("⚠️ Risque élevé", int(df['Risque'].sum()))
    with col4:
        st.metric("👨‍⚕️ Médecins", len(st.session_state.medecins))
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(df, names='Type maladie', title='Répartition des types de maladies',
                     color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        risk_by_disease = df.groupby(['Type maladie', 'Risque']).size().reset_index(name='Count')
        fig = px.bar(risk_by_disease, x='Type maladie', y='Count', color='Risque',
                     title='Risque par type de maladie',
                     color_discrete_map={0: '#34a853', 1: '#d93025'},
                     barmode='group')
        st.plotly_chart(fig, use_container_width=True)
    
    st.subheader("📈 Évolution des requêtes par heure")
    heures = ["00h", "02h", "04h", "06h", "08h", "10h", "12h", "14h", "16h", "18h", "20h", "22h"]
    valeurs = [5, 3, 2, 1, 8, 15, 22, 30, 25, 20, 12, 8]
    df_req = pd.DataFrame({"Heure": heures, "Requêtes": valeurs})
    fig = px.bar(df_req, x="Heure", y="Requêtes", title="Requêtes par heure",
                 color="Requêtes", color_continuous_scale="Blues", height=400)
    st.plotly_chart(fig, use_container_width=True)

# ==================== PAGE Q&A RAG ====================
elif menu == "🤖 Aide à la décision":
    st.title("🤖 Aide à la décision (Q&A RAG)")
    question = st.text_area("💬 Posez votre question médicale", height=100,
                            placeholder="Ex: Combien de patients ont le diabète ?")
    
    if st.button("🔍 POSER LA QUESTION", use_container_width=True, key="btn_q", type="primary"):
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
                """)
            else:
                st.info("💡 Essayez : 'Combien de patients ont le diabète ?'")

# ==================== PAGE GESTION DES MÉDECINS ====================
elif menu == "👨‍⚕️ Gestion des médecins":
    st.markdown('<p class="main-title">👨‍⚕️ Gestion des médecins</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">📋 Liste des médecins</p>', unsafe_allow_html=True)
    st.dataframe(st.session_state.medecins, use_container_width=True)
    
    st.markdown("---")
    
    # ===== BOUTONS HTML COLORÉS =====
    st.markdown("""
    <div class="btn-group">
        <a href="?action=ajouter" target="_self" class="btn-ajouter">➕ Ajouter</a>
        <a href="?action=modifier" target="_self" class="btn-modifier">✏️ Modifier</a>
        <a href="?action=supprimer" target="_self" class="btn-supprimer">🗑️ Supprimer</a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    action = st.session_state.medecin_action
    
    # ---------- FORMULAIRE AJOUTER ----------
    if action == "ajouter":
        st.subheader("➕ Ajouter un médecin")
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom", key="add_nom")
            prenom = st.text_input("Prénom", key="add_prenom")
            email = st.text_input("Email", key="add_email")
        with col2:
            specialite = st.text_input("Spécialité", key="add_specialite")
            telephone = st.text_input("Téléphone", key="add_telephone")
        
        if st.button("✅ Ajouter le médecin", use_container_width=True, key="btn_add", type="primary"):
            if nom and prenom and email:
                new_id = int(st.session_state.medecins['ID'].max()) + 1 if len(st.session_state.medecins) > 0 else 1
                new_medecin = pd.DataFrame({
                    'ID': [new_id], 'Nom': [nom], 'Prénom': [prenom],
                    'Email': [email], 'Spécialité': [specialite], 'Téléphone': [telephone]
                })
                st.session_state.medecins = pd.concat([st.session_state.medecins, new_medecin], ignore_index=True)
                st.success(f"✅ Médecin {nom} {prenom} ajouté !")
                st.rerun()
            else:
                st.error("❌ Nom, Prénom et Email sont obligatoires")
    
    # ---------- FORMULAIRE MODIFIER ----------
    elif action == "modifier":
        st.subheader("✏️ Modifier un médecin")
        if len(st.session_state.medecins) > 0:
            medecin_options = st.session_state.medecins.apply(
                lambda x: f"{x['Nom']} {x['Prénom']} (ID: {x['ID']})", axis=1
            ).tolist()
            selected = st.selectbox("Choisir un médecin à modifier", medecin_options, key="edit_select")
            idx = medecin_options.index(selected)
            med = st.session_state.medecins.iloc[idx]
            
            col1, col2 = st.columns(2)
            with col1:
                new_nom = st.text_input("Nom", value=med['Nom'], key="edit_nom")
                new_prenom = st.text_input("Prénom", value=med['Prénom'], key="edit_prenom")
                new_email = st.text_input("Email", value=med['Email'], key="edit_email")
            with col2:
                new_specialite = st.text_input("Spécialité", value=med['Spécialité'], key="edit_specialite")
                new_telephone = st.text_input("Téléphone", value=med['Téléphone'], key="edit_telephone")
            
            if st.button("💾 Enregistrer les modifications", use_container_width=True, key="btn_edit"):
                st.session_state.medecins.at[idx, 'Nom'] = new_nom
                st.session_state.medecins.at[idx, 'Prénom'] = new_prenom
                st.session_state.medecins.at[idx, 'Email'] = new_email
                st.session_state.medecins.at[idx, 'Spécialité'] = new_specialite
                st.session_state.medecins.at[idx, 'Téléphone'] = new_telephone
                st.success(f"✅ Médecin {new_nom} {new_prenom} modifié !")
                st.rerun()
        else:
            st.info("Aucun médecin à modifier.")
    
    # ---------- FORMULAIRE SUPPRIMER ----------
    elif action == "supprimer":
        st.subheader("🗑️ Supprimer un médecin")
        if len(st.session_state.medecins) > 0:
            medecin_options = st.session_state.medecins.apply(
                lambda x: f"{x['Nom']} {x['Prénom']} (ID: {x['ID']})", axis=1
            ).tolist()
            selected = st.selectbox("Choisir un médecin à supprimer", medecin_options, key="del_select")
            
            if st.button("🗑️ SUPPRIMER", use_container_width=True, key="btn_del"):
                idx = medecin_options.index(selected)
                medecin_id = st.session_state.medecins.iloc[idx]['ID']
                st.session_state.medecins = st.session_state.medecins[
                    st.session_state.medecins['ID'] != medecin_id
                ].reset_index(drop=True)
                st.success("✅ Médecin supprimé !")
                st.rerun()
        else:
            st.info("Aucun médecin à supprimer.")

# ==================== PAGE DOSSIERS MÉDICAUX ====================
elif menu == "📋 Dossiers médicaux":
    st.title("📋 Dossiers médicaux")
    df = st.session_state.patients
    
    col1, col2, col3 = st.columns(3)
    with col1:
        type_filter = st.selectbox("Type de maladie", ["Tous"] + df['Type maladie'].unique().tolist())
    with col2:
        risque_filter = st.selectbox("Risque", ["Tous", "Élevé", "Faible"])
    with col3:
        search = st.text_input("🔍 Rechercher par ID")
    
    filtered_df = df.copy()
    if type_filter != "Tous":
        filtered_df = filtered_df[filtered_df['Type maladie'] == type_filter]
    if risque_filter != "Tous":
        risque_val = 1 if risque_filter == "Élevé" else 0
        filtered_df = filtered_df[filtered_df['Risque'] == risque_val]
    if search and search.isdigit():
        filtered_df = filtered_df[filtered_df['ID'] == int(search)]
    
    st.dataframe(filtered_df, use_container_width=True, height=500)
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Télécharger (CSV)",
        data=csv,
        file_name="dossiers_medicaux.csv",
        mime="text/csv"
    )

# ==================== PAGE ADMINISTRATION ====================
elif menu == "⚙️ Administration":
    st.title("⚙️ Administration")
    st.subheader("📊 Informations système")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👤 Patients", len(st.session_state.patients))
    with col2:
        st.metric("🩺 Maladies", st.session_state.patients['Type maladie'].nunique())
    with col3:
        st.metric("👨‍⚕️ Médecins", len(st.session_state.medecins))
    with col4:
        st.metric("📦 Version", "1.0.0")
    
    st.markdown("---")
    
    with st.expander("📤 Ingestion de documents"):
        uploaded_file = st.file_uploader("Choisir un fichier", type=["csv", "txt", "pdf"])
        if uploaded_file and st.button("Lancer l'ingestion"):
            with st.spinner("Ingestion..."):
                time.sleep(2)
            st.success("✅ Document ingéré !")
    
    with st.expander("🔄 Réindexation"):
        modele = st.selectbox("Modèle", ["BioBERT", "ClinicalBERT", "DrBERT"])
        if st.button("Lancer la réindexation"):
            with st.spinner("Réindexation..."):
                time.sleep(2)
            st.success("✅ Réindexation terminée !")
    
    with st.expander("📋 Journaux d'audit"):
        st.write("Aucun log pour le moment.")

# ==================== FOOTER ====================
st.markdown("---")
st.caption("Système d'Information Intelligent - 2025/2026")
