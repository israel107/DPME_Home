import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os
import pandas as pd
import PME_analyse as pa
import chart as ch
# import traitement_FISEC as tf
import numpy as np
from datetime import datetime
import hashlib
pd.set_option("styler.render.max_elements", 2174640)

st.set_page_config(page_title="DPME", page_icon="📈", layout="wide")
st.markdown("<h2 style='text-align: left; font-size: 40px;  font-weight: bold;'>Tableau de bord du DPME</h2>", unsafe_allow_html=True)
st.image("./pays_uemoa_png.png", caption="", use_container_width=False)
st.markdown("_DABFA-SFE v0.0.1_")

# -------------------------------
# CSS Sheet
# -------------------------------

with open("./style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)

@st.cache_data
def load_data(path):
        #Ajouter Colonne Année
    df_FISEC = pd.read_excel(path)
    return df_FISEC

@st.cache_data
def load_csv(path):
    return pd.read_csv(path)
    
FICHIER_INITIAL = (
    "./Extraction Tableau/excel/UEMOA/"
    "situation financiere_data_2019.xlsx"
)

FICHIER_CUMULATIF = "./data/situation_financiere.xlsx"

# Créer le dossier s'il n'existe pas
# os.makedirs("./unique", exist_ok=True)

# Charger le fichier cumulatif s'il existe,
# sinon charger le fichier initial
if os.path.exists(FICHIER_CUMULATIF):
    df_2019 = load_data(FICHIER_CUMULATIF)
else:
    df_2019 = load_data(FICHIER_INITIAL)
df_2019["New_Arrete"] = pd.to_datetime( df_2019["Arrete"], dayfirst=True, errors="coerce")

# df_2020 = load_data("C:/Users/ckoupoh/Documents/FISEC-DPME/Extraction Tableau/excel/situation financiere_data 2020.xlsx")

# -----------------------------------------------------------------------------------------------------------------------------------
# VARIABLES
# -----------------------------------------------------------------------------------------------------------------------------------

all_years  = ['2018','2019','2020','2021','2022','2023','2024','2025','2026']

all_period = ['Mensuel','Trimestriel','Semestriel','Annuel']

all_pays   = ['Bénin',"Burkina Faso","Côte d Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo"]

# list_bank  = df_2019['Sigle Assujetti'].unique()

all_poste = df_2019['POSTE'].unique()

all_mois = ['Janv','Fev','Mars','Avr','Mai','Juin','Juil','Aout','Sept','Oct','Nov','Dec']

# -----------------------------------------------------------------------------------------------------------------------------------
# SLIDE BAR
# -----------------------------------------------------------------------------------------------------------------------------------

with st.sidebar:
    m_pays = st.selectbox('Pays', all_pays, 0)

    # Selectionner les banques en fonction du pays
    df_pays = df_2019.loc[df_2019['Libelle Pays'] == m_pays]
    list_bank = df_pays['Sigle Assujetti'].unique()

    # m_period_DPME = st.selectbox('Périodes DPME', ['juin 2021','déc 2021','juin 2022','déc 2022','juin 2023','déc 2023','juin 2024','déc 2024'], 0)
    v_annee = st.slider("Années", 2018, 2026, 2022)
    m_mois = st.selectbox('Mois', all_mois, 0)
    # multi_pays = st.multiselect('Select instrument (chart line)', all_pays, ['Bénin',"Burkina Faso"])
    m_bank = st.selectbox('Banques', list_bank, 0)
    m_poste = st.selectbox('Postes', all_poste, 0)


# nbr_SAE_UEMOA = sum([12,18,10,5,8, 16, 33, 26])
# df_SAE = pd.DataFrame({
#     "Pays": all_pays,
#     "Nombre SAE":[12,18,10,5,8, 16, 33, 26, nbr_SAE_UEMOA]
# })

mot = pa.get_preposition(m_pays)

# ------------------------------------------------------------------------------------------------------------------------------------
# EXPANDER
# -------------------------------------------------------------------------------------------------------------------------------------

## PARAMETRES AVEC ----------------> m_period_DPME <------------------------------------------
# PME_benef, tx_benef = pa.get_PME_benef(m_pays, m_period_DPME)
# # print(PME_benef, tx_benef)
# PME_accomp, tx_accomp = pa.get_PME_accompagn(m_pays, m_period_DPME)
# montant_accorde, tx_accord = pa.get_montant_accordes(m_pays, m_period_DPME)
# nbr_SAE = pa.get_Nombre_SAE(df_SAE, m_pays)

# com_benef, com_accompagne, com_montant = pa.get_commentaire_expander(m_pays, m_period_DPME)

st.markdown('#### STATISTIQUES DE TABLEAU')
# ----------------------------------------------------------------------------------
# 3 Fonctions
# ------------------------------------------------------------------------------------
int_mois = all_mois.index(m_mois)+1

valeur_credit = pa.filtreData(df_2019, m_poste, int_mois, int(v_annee), m_pays, m_bank)
tx_valeur_credit = 0

pays, credit_pays = pa.Rank_pays(df_2019, m_poste, int_mois, int(v_annee))
tx_credit_pays = 0

# instru, instru_pays = pa.Rk_instrument(df_2019, int_mois, int(v_annee), m_pays, m_bank)

valeur_credit_UEMOA = pa.credit_UEMOA(df_2019, int_mois, int(v_annee))
tx_credit_UEMOA = 0

# ----------------------------------------------------------------------------------
# Données DPME
# ------------------------------------------------------------------------------------
# Transformer les séparators , en .
montant_accorde_fr = f"{valeur_credit:,.0f}".replace(",", ".")
tx_accord_fr = f"{tx_valeur_credit:,.2f}%".replace(",", ".")

credit_UMOA = f"{valeur_credit_UEMOA:,.0f}".replace(",", ".")
tx_benef_fr = f"{tx_credit_UEMOA:,.2f}%".replace(",", ".")

PME_niv_pays = f"{credit_pays:,.0f}".replace(",", ".")
tx_accomp_fr = f"{tx_credit_pays:,.2f}%".replace(",", ".")

with st.expander("CREDIT AUX PME (en Millions FCFA)"): 

    valeur1, valeur2, valeur3 = st.columns(3, gap='small')

    with valeur1:
        st.metric(label="Crédit par Pays par Période / Instrument", value=montant_accorde_fr, delta=tx_accord_fr)

    with valeur2:
        st.metric(label="Crédit Meilleur Pays / Instru : "+ pays, value=PME_niv_pays , delta=tx_accomp_fr )

    with valeur3:
        st.metric(label="Crédit PME UEMOA (Mns) / Période", value= credit_UMOA, delta=f"{0:.2f}%")

    # m_interpr = 20
    # st.info("""
    #     **Commentaires** (_{}_)
            
    #     - {}
    #     - {}
    #     - {}
    #     - Le nombre de Structures d'Accompagnement et d'Encadrement (**SAE**) de juin 2021 à décembre 2024 a demeuré à **{}**.
    #     """.format(m_pays,com_benef, com_accompagne, com_montant, nbr_SAE))


# -----------------------------------------------------------------------------------------------------------------------------------
# 2 CHARTS : Financement / Pays - 
# -----------------------------------------------------------------------------------------------------------------------------------
st.write("Taille des données: " +str(len(df_2019))+ " lignes")
st.markdown('#### GRAPHIQUES')

BC_colors =['rgb(133, 32, 12)', 'rgb(194, 72, 48)', 'rgb(228, 185, 176)']
split_credit = pa.credit_UEMOA_split(df_2019, int_mois, int(v_annee))

credit_plit_par_period = pa.credit_pays_split_par_periode(df_2019, m_pays, int(v_annee))
prep = pa.get_preposition(m_pays)

valeur1, valeur2  = st.columns(2, gap='small')

with valeur1:
    fig_line = ch.credit_par_mois(all_mois, credit_plit_par_period, "Evolution des crédits octroyés aux PME par mois par les banques "+prep+ " "+m_pays, "En millions")
    st.plotly_chart(fig_line, width='stretch')

with valeur2:
    fig_cercle = ch.chart_pie(all_pays, split_credit, BC_colors , m_hole=.3, m_size_font=16, m_titre='Crédit aux PME (en Mns FCFA) par pays en '+ m_mois +" 2019")
    st.plotly_chart(fig_cercle, width='stretch')

# -----------------------------------------------------------------------------------------------------------------------------------
# MISE A JOUR DES DONNEES : MERGE PRECÉDENTES ET NOUVELLES DONNÉES
# -----------------------------------------------------------------------------------------------------------------------------------

st.markdown('#### MISE A JOUR DES DONNEES')

tab_1_data, tab_2_data = st.columns(2, gap='small')


# ============================================================
# INITIALISATION DU DATAFRAME CUMULATIF
# ============================================================

if "df_updated" not in st.session_state:

    # On part du fichier principal
    st.session_state.df_updated = df_2019.copy()


# ============================================================
# INITIALISATION DE LA LISTE DES FICHIERS DEJA TRAITES
# ============================================================

if "fichiers_traites" not in st.session_state:

    st.session_state.fichiers_traites = set()


# ============================================================
# UPLOAD
# ============================================================

with tab_1_data:

    uploaded_files = st.file_uploader(
        "Charger fichier TABLEAU",
        accept_multiple_files=True,
        type=["csv", "xlsx", "xls"]
    )


    if uploaded_files:

        for fichier in uploaded_files:

            # ------------------------------------------------
            # Créer une empreinte unique du fichier
            # ------------------------------------------------

            file_bytes = fichier.getvalue()

            file_hash = hashlib.md5(
                file_bytes
            ).hexdigest()


            # ------------------------------------------------
            # Vérifier si le fichier a déjà été ajouté
            # ------------------------------------------------

            if file_hash not in st.session_state.fichiers_traites:

                # ============================================
                # LECTURE DU FICHIER
                # ============================================

                if fichier.name.lower().endswith(".csv"):

                    df_new = load_csv(fichier)

                else:

                    df_new = load_data(fichier)


                # ============================================
                # AJOUT AU DATAFRAME PRINCIPAL
                # ============================================

                st.session_state.df_updated = pd.concat(
                    [
                        st.session_state.df_updated,
                        df_new
                    ],
                    ignore_index=True
                )


                # ============================================
                # MEMORISER LE FICHIER
                # ============================================

                st.session_state.fichiers_traites.add(
                    file_hash
                )


                st.success(
                    f"✅ {fichier.name} ajouté : "
                    f"{len(df_new):,} lignes"
                    .replace(",", " ")
                )


                # ============================================
                # SAUVEGARDE LOCALE
                # ============================================

                os.makedirs(
                    "tempDir",
                    exist_ok=True
                )

                chemin_temporaire = os.path.join(
                    "tempDir",
                    fichier.name
                )

                with open(
                    chemin_temporaire,
                    "wb"
                ) as f:

                    f.write(file_bytes)


            else:

                st.info(
                    f"ℹ️ {fichier.name} a déjà été ajouté."
                )


# ============================================================
# DATAFRAME FINAL
# ============================================================

df_updated = st.session_state.df_updated


# ============================================================
# AFFICHAGE
# ============================================================

if st.session_state.fichiers_traites:

    df_updated = st.session_state.df_updated

    st.markdown('##### Présentation des données cumulées')

    st.dataframe(
        df_updated,
        height= 200,
        use_container_width= True
    )

    st.success(
        f"Nombre total de lignes : "
        f"**{len(df_updated):,}**".replace(",", " ")
    )

    # #
    if st.button("Enregistrer"):

        # Enregistrer toujours sous le même nom
        st.session_state.df_updated.to_excel(
            FICHIER_CUMULATIF,
            index=False
        )
    
        st.success(
            "Données enregistrées dans : "
            + FICHIER_CUMULATIF
        )

        

   
