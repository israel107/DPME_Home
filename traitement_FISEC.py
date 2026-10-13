import pandas as pd
import numpy as np
from datetime import datetime 
import os
import streamlit as st


def get_colonne(libele_col):
    valeur = 0
    if "Autres societes financieres Societes d'assurance et Fonds de pension" in libele_col :
        valeur = 1 
    elif "Autres societes financieres Autres intermediaires financiers" in libele_col:
        valeur = 2  
    elif "Autres societes financieres Auxiliaires financiers" in libele_col:
        valeur = 3 
    elif "Societes non financieres Publiques" in libele_col:
        valeur = 4 
    elif "Societes non financieres Autres" in libele_col:
        valeur = 5 
    elif "Menages Entreprises individuelles" in libele_col:
        valeur = 6 
    elif "Menages Particuliers" in libele_col:
        valeur = 7 
    elif libele_col == " ":
        return " "

    return valeur

def get_pays(nom_fichier):

    valeur = ""
    if nom_fichier[-7:-5] == 'BJ': valeur = "Bénin"
    elif nom_fichier[-7:-5] == 'BF': valeur = "Burkina Faso"
    elif nom_fichier[-7:-5] == 'CI': valeur = "Côte d Ivoire"
    elif nom_fichier[-7:-5] == 'GW': valeur = "Guinée Bissau"
    elif nom_fichier[-7:-5] == 'ML': valeur = "Mali"
    elif nom_fichier[-7:-5] == 'NE': valeur = "Niger"
    elif nom_fichier[-7:-5] == 'SN': valeur = "Sénégal"
    elif nom_fichier[-7:-5] == 'TG': valeur = "Togo"

    return valeur

def returnTableau_DF():
    df = pd.DataFrame()

    return df


def returnFISEC_DF(df_ante, l_fichiers, chemin_temporaire ):
    df = pd.DataFrame()

    # Tester
    # dossier = "C:/Users/ckoupoh/Downloads/BU0_ 2025 - 2026/F_30/Excel/"

     
    tab_POSTE  = []
    tab_arrete = []
    tab_lib_pays = []
    tab_code_assuj = [] 
    tab_sigle_assuj = []
    tab_ordre_col = []
    tab_libelle_col = []
    tab_valeur = []
    tab_arrete = []
    for fichier in l_fichiers:
        # print("Nom du fichier "+ fichier)
        # st.info(""" **Nom fichier : ** {}
        # """.format(fichier))
        st.write(fichier.name)
        # st.write(chemin_temporaire)
        # st.text_area(
        #         "Nom fichier ",
        #         value=fichier,
        #         height=200
        #     )
        db_PME = pd.read_excel(fichier)
        
        #boucle sur Colonne POSTE
        #2: quatrième ligne (première ligne des valeurs)
        for i in range(2, len(db_PME['Pays :'].iloc[2:])):

            nombre_col_libelle = len(db_PME.iloc[1][1:])
            for libelle in range(1, nombre_col_libelle):
                tab_POSTE.append(db_PME['Pays :'].iloc[i][11:])
                tab_lib_pays.append(get_pays(fichier.name))

                val_num = db_PME.iloc[i, libelle]
                if val_num == '-' or val_num == ' ':
                    val_num = 0
                tab_valeur.append(val_num)
                tab_arrete.append(db_PME.columns[7])

                m_lign = db_PME.iloc[0: 1]
                val = m_lign.iloc[0, libelle]
                try:
                    code,sep,bank = val.partition("*")
                    tab_code_assuj.append(code)
                    tab_sigle_assuj.append(bank)
                except:
                    code = " "
                    bank = " "
                    tab_code_assuj.append(code)
                    tab_sigle_assuj.append(bank)


                m_chaine = db_PME.iloc[1, libelle] # Résolu
                # print(m_chaine)
                try:
                    lib_colonne = m_chaine[18:-1] 
                    tab_libelle_col.append(lib_colonne)
                    tab_ordre_col.append(get_colonne(lib_colonne))
                except:
                    lib_colonne = " "
                    tab_libelle_col.append(lib_colonne)
                    tab_ordre_col.append(get_colonne(lib_colonne))

                
                    
    df['POSTE'] = tab_POSTE
    df['Arrete'] = tab_arrete
    df['Libellé Pays'] = tab_lib_pays
    df['Code Assujetti'] = tab_code_assuj
    df['Sigle Assujetti'] = tab_sigle_assuj
    df['Ordre Colonne'] = tab_ordre_col
    df['Libelle Colonne'] = tab_libelle_col
    df['Valeur'] = tab_valeur

    df_final = pd.concat([df_ante, df])

    return df_final


# Fonction de style
def color_first_row(row):
    if row.name == 0:
        return ['background-color: yellow'] * len(row)
    else:
        return [''] * len(row)
    
def get_mois(m_mois):

    rk = 0
    if   m_mois == 'Janvier': rk = 1
    elif m_mois == 'Février': rk = 2
    elif m_mois == 'Mars': rk = 3
    elif m_mois == 'Avril': rk = 4
    elif m_mois == 'Mai': rk = 5
    elif m_mois == 'Juin': rk = 6
    elif m_mois == 'Juillet': rk = 7
    elif m_mois == 'Août': rk = 8
    elif m_mois == 'Septembre': rk = 9
    elif m_mois == 'Octobre': rk = 10
    elif m_mois == 'Novembre': rk = 11
    elif m_mois == 'Décembre': rk = 12

    return rk

def filtreEncours(df, e_annee, e_pays='All', e_mois='Janvier', e_bank='All', e_post='All'):

    df_filtre = df.copy()

    res = 0
    criteres = {
        'Libelle Pays': e_pays,
        'Mois': e_mois,
        'Sigle Assujetti': e_bank,
        'POSTE': e_post
    }

    for colonne, valeur in criteres.items():
        if valeur != "All" :
            df_filtre = df_filtre.loc[(df_filtre[colonne] == valeur) & (df_filtre['Année'] == e_annee)]
            res = df_filtre['Valeurn'].sum()
    
    return res

def Encours_Mois(df, e_annee, e_pays='All', e_bank='All', e_post='All'):

    df_filtre = df.copy()

    res = []
    criteres = {
        'Libelle Pays': e_pays,
        'Sigle Assujetti': e_bank,
        'POSTE': e_post
    }

    for colonne, valeur in criteres.items():
        if valeur != "All" :
            df_filtre = df_filtre.loc[(df_filtre[colonne] == valeur) & (df_filtre['Année'] == e_annee) ]
            for i in range(1, 13):
                df_1 = df_filtre.loc[df_filtre['Mois'] == i]
                val = df_1['Valeurn'].sum()
                res.append(val)
    # print(res)
    return res

def Rk_Encours_Pays(df,  e_annee, e_post='All'):

    df_filtre = df.copy()
    all_pays = ['Bénin',"Burkina Faso","Côte d Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo" ]

    res = []
    criteres = {
        'Année':e_annee,
        'POSTE': e_post
    }

    for colonne, valeur in criteres.items():
        if valeur != "All" :
            df_filtre = df_filtre.loc[(df_filtre[colonne] == valeur) & (df_filtre['Mois'] == 12)]
            for i in all_pays:
                if i == "Côte d Ivoire":
                    df_1 = df_filtre.loc[(df_filtre['Libelle Pays'] == "Côte d Ivoire")]
                    val = df_1['Valeurn'].sum()
                else:
                    df_1 = df_filtre.loc[df_filtre['Libelle Pays'] == i]
                    val = df_1['Valeurn'].sum()
                res.append(val)
    
    d = {"col1": all_pays, "col2":res}
    fin_df = pd.DataFrame(data=d) #
    fin_df.sort_values(by="col2",ascending=False, inplace= True)
    l_pays = fin_df['col1'].values.tolist()
    l_value = fin_df['col2'].values.tolist()

    return l_pays, l_value

def SelectBank_Pays(df, e_pays):

    val = ""
    if e_pays == 'All':
        # df_interm = df.loc['Libelle Pays']
        val = df['Sigle Assujetti'].unique()
    elif e_pays == "Côte d Ivoire":
        df_interm = df.loc[(df['Libelle Pays'] == "Côte d'Ivoire") & (df['Libelle Pays'] == "Côte d Ivoire")]
        val = df_interm['Sigle Assujetti'].unique()
    else:
        df_interm = df.loc[(df['Libelle Pays'] == e_pays) ]
        val = df_interm['Sigle Assujetti'].unique()

    # print(val.tolist())
    return val.tolist()


def RkBank_pays(df_filtre, e_annee, e_pays='All', e_mois='Janvier', e_bank='All', e_post='All'):

    # df_filtre = df.copy()

    res = []
    criteres = {
        'Libelle Pays': e_pays,
         'Mois': e_mois,
        'Sigle Assujetti': e_bank,
        'POSTE': e_post
    }

    for colonne, valeur in criteres.items():
        df_filtre = df_filtre.loc[(df_filtre[colonne] == valeur) & (df_filtre['Année'] == e_annee) ]

        list_bank = df_filtre['Sigle Assujetti'].unique()
        bk_list = []
        val_list = []
        for i in list_bank:
            res = df_filtre.loc[(df_filtre['Sigle Assujetti'] == i)]
            bk_list.append(i)
            val_list.append(res['Valeurn'].sum())
        

        d = {"col1": bk_list, "col2":val_list} #Problème
        fin_df = pd.DataFrame(data=d) #
        fin_df.sort_values(by="col2",ascending=False, inplace= True)

        #print(fin_df["col2"].to_list()[0])


        res1 = fin_df['col1'] 
        # print(res1)

        res2 =  fin_df['col2'] 
    
    
    return res1, res2