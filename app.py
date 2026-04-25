import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.express as px

# ============================================
# CONFIGURATION
# ============================================
st.set_page_config(
    page_title="DataCollect Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# STYLE CSS PROFESSIONNEL
# ============================================
st.markdown("""
    <style>
        /* Fond général */
        .main { background-color: #f7f9fc; }

        /* Barre latérale */
        section[data-testid="stSidebar"] {
            background-color: #1a2340;
            color: white;
        }
        section[data-testid="stSidebar"] * {
            color: white !important;
        }

        /* Titre principal */
        .titre-principal {
            font-size: 2em;
            font-weight: 700;
            color: #1a2340;
            margin-bottom: 0;
        }
        .sous-titre {
            font-size: 1em;
            color: #6c757d;
            margin-top: 0;
        }

        /* Cartes métriques */
        div[data-testid="metric-container"] {
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }

        /* Bouton principal */
        .stButton > button {
            background-color: #1a2340;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 28px;
            font-weight: 600;
            font-size: 0.95em;
            transition: background 0.3s;
        }
        .stButton > button:hover {
            background-color: #2e3f6f;
        }

        /* Bouton téléchargement */
        .stDownloadButton > button {
            background-color: #f0f4ff;
            color: #1a2340;
            border: 1px solid #1a2340;
            border-radius: 6px;
            font-weight: 600;
        }

        /* Séparateur */
        hr { border: 1px solid #e8ecf0; }

        /* Formulaire */
        .stTextInput > div > input,
        .stSelectbox > div,
        .stNumberInput > div > input,
        .stTextArea > div > textarea {
            border-radius: 6px;
            border: 1px solid #d0d7e2;
        }

        /* Tableau */
        .stDataFrame { border-radius: 8px; }

        /* Alertes */
        .stSuccess { border-radius: 8px; }
        .stWarning { border-radius: 8px; }
        .stError   { border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# ============================================
# FICHIER DE STOCKAGE
# ============================================
FICHIER_CSV   = "data/donnees.csv"
FICHIER_EXCEL = "data/donnees.xlsx"

if not os.path.exists("data"):
    os.makedirs("data")

# ============================================
# FONCTIONS
# ============================================
def charger_donnees():
    if os.path.exists(FICHIER_CSV):
        try:
            df = pd.read_csv(FICHIER_CSV)
            if df.empty or len(df.columns) == 0:
                return pd.DataFrame()
            return df
        except pd.errors.EmptyDataError:
            return pd.DataFrame()
    return pd.DataFrame()

def sauvegarder_donnees(nouvelle_ligne):
    df_existant = charger_donnees()
    df_nouveau  = pd.DataFrame([nouvelle_ligne])
    df_final    = pd.concat([df_existant, df_nouveau], ignore_index=True)
    df_final.to_csv(FICHIER_CSV, index=False, encoding="utf-8-sig")
    df_final.to_excel(FICHIER_EXCEL, index=False, engine="openpyxl")
    return df_final

def exporter_excel(df):
    chemin = "data/export_final.xlsx"
    with pd.ExcelWriter(chemin, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Données")
        workbook  = writer.book
        worksheet = writer.sheets["Données"]
        format_entete = workbook.add_format({
            "bold": True,
            "bg_color": "#1a2340",
            "font_color": "white",
            "border": 1
        })
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, format_entete)
            worksheet.set_column(col_num, col_num, 22)
    return chemin

# ============================================
# BARRE LATERALE
# ============================================
st.sidebar.markdown("""
    <div style='text-align:center; padding: 20px 0 10px 0;'>
        <span style='font-size:2em;'>📊</span>
        <h2 style='margin:5px 0; font-size:1.2em; letter-spacing:1px;'>DataCollect Pro</h2>
        <p style='font-size:0.8em; color:#aab4c8;'>Commerce & Entreprise</p>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
menu = st.sidebar.radio("Navigation", [
    "Accueil",
    "Formulaire",
    "Analyse",
    "Données"
])
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <p style='font-size:0.78em; color:#aab4c8; text-align:center;'>
        Application de collecte et<br>analyse de données commerciales
    </p>
""", unsafe_allow_html=True)

# ============================================
# PAGE ACCUEIL
# ============================================
if menu == "Accueil":
    st.markdown('<p class="titre-principal">DataCollect Pro</p>', unsafe_allow_html=True)
    st.markdown('<p class="sous-titre">Collecte et analyse de données commerciales</p>', unsafe_allow_html=True)
    st.markdown("---")

    df = charger_donnees()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total enregistrements", len(df) if not df.empty else 0)
    with col2:
        st.metric("Secteurs différents",
            df["Secteur"].nunique() if not df.empty and "Secteur" in df.columns else 0)
    with col3:
        st.metric("Satisfaction moyenne",
            round(df["Satisfaction"].mean(), 1) if not df.empty and "Satisfaction" in df.columns else 0)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Collecte**\n\nSaisissez vos données via un formulaire structuré et intuitif.")
    with col2:
        st.success("**Analyse**\n\nVisualisez vos données avec des graphiques interactifs.")
    with col3:
        st.warning("**Export**\n\nTéléchargez vos données en format CSV ou Excel.")

# ============================================
# PAGE FORMULAIRE
# ============================================
elif menu == "Formulaire":
    st.markdown('<p class="titre-principal">Formulaire de collecte</p>', unsafe_allow_html=True)
    st.markdown('<p class="sous-titre">Renseignez les informations de l\'entreprise enquêtée</p>', unsafe_allow_html=True)
    st.markdown("---")

    with st.form("formulaire", clear_on_submit=True):

        st.subheader("Informations générales")
        col1, col2 = st.columns(2)
        with col1:
            nom_entreprise = st.text_input("Nom de l'entreprise *", placeholder="Ex : ABC Commerce")
            secteur = st.selectbox("Secteur d'activité *", [
                "Sélectionnez...",
                "Commerce de détail",
                "Commerce de gros",
                "Services",
                "Industrie",
                "Agriculture",
                "Technologie",
                "Autre"
            ])
        with col2:
            nom_repondant = st.text_input("Nom du répondant *", placeholder="Ex : Jean Dupont")
            taille_entreprise = st.selectbox("Taille de l'entreprise *", [
                "Sélectionnez...",
                "Micro (1-9 employés)",
                "Petite (10-49 employés)",
                "Moyenne (50-249 employés)",
                "Grande (250+ employés)"
            ])

        st.markdown("---")
        st.subheader("Données commerciales")
        col3, col4 = st.columns(2)
        with col3:
            chiffre_affaires = st.number_input("Chiffre d'affaires annuel (FCFA)", min_value=0, step=100000)
            nb_clients = st.number_input("Nombre de clients actifs", min_value=0, step=1)
        with col4:
            nb_employes = st.number_input("Nombre d'employés", min_value=0, step=1)
            annee_creation = st.number_input("Année de création", min_value=1900, max_value=2026, step=1, value=2020)

        st.markdown("---")
        st.subheader("Performance et satisfaction")
        croissance = st.select_slider(
            "Taux de croissance estimé (%)",
            options=[-20, -10, -5, 0, 5, 10, 15, 20, 25, 30, 50],
            value=0
        )
        satisfaction = st.slider("Niveau de satisfaction client (1 à 10)", 1, 10, 5)
        defis = st.multiselect("Principaux défis rencontrés", [
            "Manque de financement",
            "Concurrence accrue",
            "Manque de personnel qualifié",
            "Problèmes logistiques",
            "Digitalisation",
            "Accès aux marchés",
            "Autre"
        ])
        commentaire = st.text_area("Commentaires supplémentaires", placeholder="Vos observations...")

        st.markdown("---")
        soumettre = st.form_submit_button("Soumettre les données")

        if soumettre:
            if not nom_entreprise or not nom_repondant or secteur == "Sélectionnez..." or taille_entreprise == "Sélectionnez...":
                st.error("Veuillez remplir tous les champs obligatoires (*)")
            else:
                nouvelle_ligne = {
                    "Date"            : datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Entreprise"      : nom_entreprise,
                    "Répondant"       : nom_repondant,
                    "Secteur"         : secteur,
                    "Taille"          : taille_entreprise,
                    "Chiffre_Affaires": chiffre_affaires,
                    "Nb_Clients"      : nb_clients,
                    "Nb_Employes"     : nb_employes,
                    "Annee_Creation"  : annee_creation,
                    "Croissance"      : croissance,
                    "Satisfaction"    : satisfaction,
                    "Defis"           : ", ".join(defis),
                    "Commentaire"     : commentaire
                }
                sauvegarder_donnees(nouvelle_ligne)
                st.success("Données enregistrées avec succès.")
                

# ============================================
# PAGE ANALYSE
# ============================================
elif menu == "Analyse":
    st.markdown('<p class="titre-principal">Analyse descriptive</p>', unsafe_allow_html=True)
    st.markdown('<p class="sous-titre">Visualisation et statistiques des données collectées</p>', unsafe_allow_html=True)
    st.markdown("---")

    df = charger_donnees()

    if df.empty:
        st.warning("Aucune donnée disponible. Veuillez remplir le formulaire d'abord.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total entreprises", len(df))
        with col2:
            st.metric("CA moyen (FCFA)",
                f"{int(df['Chiffre_Affaires'].mean()):,}".replace(",", " ")
                if "Chiffre_Affaires" in df.columns else "N/A")
        with col3:
            st.metric("Satisfaction moyenne",
                round(df["Satisfaction"].mean(), 1)
                if "Satisfaction" in df.columns else "N/A")
        with col4:
            st.metric("Employés moyens",
                round(df["Nb_Employes"].mean(), 1)
                if "Nb_Employes" in df.columns else "N/A")

        st.markdown("---")

        # Répartition par secteur
        st.subheader("Répartition par secteur d'activité")
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.pie(df, names="Secteur", hole=0.35,
                color_discrete_sequence=px.colors.qualitative.Set2)
            fig1.update_traces(textposition="inside", textinfo="percent+label")
            fig1.update_layout(showlegend=False, margin=dict(t=30, b=10))
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            secteur_count = df["Secteur"].value_counts().reset_index()
            secteur_count.columns = ["Secteur", "Nombre"]
            fig2 = px.bar(secteur_count, x="Secteur", y="Nombre",
                color="Secteur", color_discrete_sequence=px.colors.qualitative.Set2)
            fig2.update_layout(showlegend=False, margin=dict(t=30, b=10))
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # Répartition par taille
        st.subheader("Répartition par taille d'entreprise")
        col1, col2 = st.columns(2)
        with col1:
            taille_count = df["Taille"].value_counts().reset_index()
            taille_count.columns = ["Taille", "Nombre"]
            fig3 = px.bar(taille_count, x="Taille", y="Nombre",
                color="Taille", color_discrete_sequence=px.colors.qualitative.Pastel)
            fig3.update_layout(showlegend=False, margin=dict(t=30, b=10))
            st.plotly_chart(fig3, use_container_width=True)
        with col2:
            fig4 = px.pie(df, names="Taille", hole=0.35,
                color_discrete_sequence=px.colors.qualitative.Pastel)
            fig4.update_layout(margin=dict(t=30, b=10))
            st.plotly_chart(fig4, use_container_width=True)

        st.markdown("---")

        # Chiffre d'affaires
        st.subheader("Analyse du chiffre d'affaires")
        col1, col2 = st.columns(2)
        with col1:
            fig5 = px.box(df, x="Secteur", y="Chiffre_Affaires",
                color="Secteur", color_discrete_sequence=px.colors.qualitative.Set3)
            fig5.update_layout(showlegend=False, margin=dict(t=30, b=10))
            st.plotly_chart(fig5, use_container_width=True)
        with col2:
            ca_moyen = df.groupby("Secteur")["Chiffre_Affaires"].mean().reset_index()
            ca_moyen.columns = ["Secteur", "CA_Moyen"]
            fig6 = px.bar(ca_moyen, x="Secteur", y="CA_Moyen",
                color="Secteur", color_discrete_sequence=px.colors.qualitative.Set3)
            fig6.update_layout(showlegend=False, margin=dict(t=30, b=10))
            st.plotly_chart(fig6, use_container_width=True)

        st.markdown("---")

        # Satisfaction
        st.subheader("Satisfaction client")
        col1, col2 = st.columns(2)
        with col1:
            fig7 = px.histogram(df, x="Satisfaction", nbins=10,
                color_discrete_sequence=["#1a2340"])
            fig7.update_layout(margin=dict(t=30, b=10))
            st.plotly_chart(fig7, use_container_width=True)
        with col2:
            sat_secteur = df.groupby("Secteur")["Satisfaction"].mean().reset_index()
            sat_secteur.columns = ["Secteur", "Satisfaction_Moyenne"]
            fig8 = px.bar(sat_secteur, x="Secteur", y="Satisfaction_Moyenne",
                color="Secteur", color_discrete_sequence=px.colors.qualitative.Safe)
            fig8.update_layout(showlegend=False, margin=dict(t=30, b=10))
            st.plotly_chart(fig8, use_container_width=True)

        st.markdown("---")

        # Statistiques descriptives
        st.subheader("Statistiques descriptives")
        colonnes_numeriques = ["Chiffre_Affaires", "Nb_Clients", "Nb_Employes", "Satisfaction", "Croissance"]
        colonnes_disponibles = [c for c in colonnes_numeriques if c in df.columns]
        if colonnes_disponibles:
            stats = df[colonnes_disponibles].describe().round(2)
            stats.index = ["Nombre", "Moyenne", "Écart-type", "Min", "Q1", "Médiane", "Q3", "Max"]
            st.dataframe(stats, use_container_width=True)

# ============================================
# PAGE DONNEES
# ============================================
elif menu == "Données":
    st.markdown('<p class="titre-principal">Données collectées</p>', unsafe_allow_html=True)
    st.markdown('<p class="sous-titre">Tableau complet des enregistrements</p>', unsafe_allow_html=True)
    st.markdown("---")

    df = charger_donnees()
    if df.empty:
        st.warning("Aucune donnée disponible.")
    else:
        st.success(f"{len(df)} enregistrement(s) disponible(s)")
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
        st.subheader("Exporter les données")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="Télécharger en CSV",
                data=df.to_csv(index=False).encode("utf-8-sig"),
                file_name="donnees.csv",
                mime="text/csv"
            )
        with col2:
            chemin_excel = exporter_excel(df)
            with open(chemin_excel, "rb") as f:
                st.download_button(
                    label="Télécharger en Excel",
                    data=f,
                    file_name="donnees.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )