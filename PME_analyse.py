import pandas as pd
import numpy as np
from datetime import datetime 


df_PME_benef = pd.read_excel('E:/FISEC-DPME/files/Stats SAE_PME.xlsx', sheet_name='PME_Benef')
df_PME_accompagn = pd.read_excel('E:/FISEC-DPME/files/Stats SAE_PME.xlsx', sheet_name='PME_accompag')
df_montant_accordes = pd.read_excel('E:/FISEC-DPME/files/Stats SAE_PME.xlsx', sheet_name='Montant_accord')

montant_idx = df_montant_accordes.set_index(['pays'])
T_montant_idx = montant_idx.transpose()

# --------------------------------------------------------------
# OBTENIR Cumul Crédit (All Instru) du Pays selectionné par mois par année
# --------------------------------------------------------------

def credit_pays_split_par_periode(df_tab, pays = "Bénin", annee = 2019 ):

    rk_data = []

    all_mois   = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    for i in all_mois:
        resultat = df_tab.loc[
                         
                        (df_tab["New_Arrete"].dt.month == i) &
                        (df_tab["New_Arrete"].dt.year == annee) &
                        (df_tab["Libelle Pays"] == pays),
                        "Valeurn"
                    ]

        rk_data.append(resultat.sum())

    return rk_data

# --------------------------------------------------------------
# OBTENIR Cumul Crédit des Pays par Instru
# --------------------------------------------------------------

def credit_UEMOA_split(df_tab, mois = 12, annee = 2019 ):

    rk_data = []

    all_pays   = ['Bénin',"Burkina Faso","Côte d Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo"]

    for i in all_pays:
        resultat = df_tab.loc[
                         
                        (df_tab["New_Arrete"].dt.month == mois) &
                        (df_tab["New_Arrete"].dt.year == annee) &
                        (df_tab["Libelle Pays"] == i),
                        "Valeurn"
                    ]

        rk_data.append((resultat.sum()))

    return rk_data

# --------------------------------------------------------------
# OBTENIR Cumul Crédit des Pays par Instru
# --------------------------------------------------------------

def credit_UEMOA(df_tab, mois = 12, annee = 2019):

    rk_data = []
    all_pays   = ['Bénin',"Burkina Faso","Côte d Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo"]

    for i in all_pays:
        resultat = df_tab.loc[
                        (df_tab["New_Arrete"].dt.month == mois) &
                        (df_tab["New_Arrete"].dt.year == annee) &
                        (df_tab["Libelle Pays"] == i),
                        "Valeurn"
                    ]

        rk_data.append((resultat.sum()))

    return sum(rk_data)#.sort(reverse= True)


# --------------------------------------------------------------
# OBTENIR VALEUR EN FONCTION DES PARAMETRES SELECTIONNES
# --------------------------------------------------------------

def filtreData(df_tab, poste = "Credits a la clientele / Credits aux PME-PMI",
    mois = 11,
    annee = 2019,
    pays = "Bénin",
    banque = "ORABANK-BJ"):
    

    # Appliquer les filtres
    resultat = df_tab.loc[
        (df_tab["POSTE"] == poste) &
        (df_tab["New_Arrete"].dt.month == mois) &
        (df_tab["New_Arrete"].dt.year == annee) &
        (df_tab["Libelle Pays"] == pays) &
        (df_tab["Sigle Assujetti"] == banque),
        "Valeurn"
    ]

    return resultat.sum()

# --------------------------------------------------------------
# BEST PAYS : FINANCEMENT DES PME
# --------------------------------------------------------------

def Rank_pays(df_tab, poste = "Credits a la clientele / Credits aux PME-PMI", mois = 8, annee = 2019):
    rk_data = []
    all_pays   = ['Bénin',"Burkina Faso","Côte d Ivoire", "Guinée Bissau","Mali","Niger","Sénégal","Togo"]

    for i in all_pays:

        resultat = df_tab.loc[
                (df_tab["POSTE"] == poste) &
                (df_tab["New_Arrete"].dt.month == mois) &
                (df_tab["New_Arrete"].dt.year == annee) &
                (df_tab["Libelle Pays"] == i),
                "Valeurn"
            ]

        rk_data.append((resultat.sum(), i))

    rk_data.sort(reverse= True)
    return rk_data[0][1], rk_data[0][0]

# --------------------------------------------------------------
# BEST INSTRUMENT : FINANCEMENT DES PME
# --------------------------------------------------------------
def Rk_instrument(df_tab, mois = 9, annee = 2019, pays = 'Bénin', banque = "ORABANK-BJ"):
    types_credit = df_tab['POSTE'].unique()


    rk_data = []

    for i in types_credit:

        resultat = df_tab.loc[
                (df_tab["POSTE"] == i) &
                (df_tab["New_Arrete"].dt.month == mois) &
                (df_tab["New_Arrete"].dt.year == annee) &
                (df_tab["Libelle Pays"] == pays) &
                (df_tab["Sigle Assujetti"] == banque),
                "Valeurn"
            ]

        rk_data.append((resultat.sum(), i))
        rk_data.sort(reverse= True)

    return rk_data[0][1], rk_data[0][0]


def get_PME_benef(m_pays, m_year ):

    l_periode = ['juin 2021','déc 2021','juin 2022','déc 2022',
                 'juin 2023','déc 2023','juin 2024','déc 2024']
    tx_var = 0
    if m_year == 'juin 2021':
        tx_var = 0
        df_yrs = df_PME_benef[m_year].loc[df_PME_benef['pays']== m_pays ].iloc[0]
    else:
        for i in range(0, len(l_periode)):
            if l_periode[i] == m_year:
                df_yrs = df_PME_benef[m_year].loc[df_PME_benef['pays']== m_pays ].iloc[0]
                df_yrs_ante = df_PME_benef[l_periode[i-1]].loc[df_PME_benef['pays']== m_pays ].iloc[0]
                tx_var = ((df_yrs/df_yrs_ante)-1)*100
                tx_var = round(tx_var, 2)


    return df_yrs, tx_var

def get_Nombre_SAE(df_SAE, m_pays):
     

    df = df_SAE.loc[df_SAE['Pays'] == m_pays] 
    df['Nombre SAE'].iloc[0]

    return df['Nombre SAE'].iloc[0]

def get_PME_accompagn(m_pays, m_year ):
    l_periode = ['juin 2021','déc 2021','juin 2022','déc 2022',
                 'juin 2023','déc 2023','juin 2024','déc 2024']
    tx_var = 0
    if m_year == 'juin 2021':
        tx_var = 0
        df_yrs = df_PME_accompagn[m_year].loc[df_PME_accompagn['pays']== m_pays ].iloc[0]
    else:
        for i in range(0, len(l_periode)):
            if l_periode[i] == m_year:
                df_yrs = df_PME_accompagn[m_year].loc[df_PME_accompagn['pays']== m_pays ].iloc[0]
                df_yrs_ante = df_PME_accompagn[l_periode[i-1]].loc[df_PME_accompagn['pays']== m_pays ].iloc[0]
                tx_var = ((df_yrs/df_yrs_ante)-1)*100
                tx_var = round(tx_var, 2)

    return df_yrs, tx_var
    
def get_Waterfall_data(m_pays):

    list_diff = []

    list_diff.append(T_montant_idx[m_pays].iloc[0])
    for i in range(1, len(T_montant_idx[m_pays])):
        vi = T_montant_idx[m_pays].iloc[i-1]
        vf = T_montant_idx[m_pays].iloc[i]
        diff = vf-vi
        list_diff.append(diff)

    list_diff.append(0)
    list_montant = [round(x/10**6, 2) for x in list_diff]

    return list_montant

def get_montant_accordes(m_pays, m_year ):
    l_periode = ['juin 2021','déc 2021','juin 2022','déc 2022',
                 'juin 2023','déc 2023','juin 2024','déc 2024']
    tx_var = 0
    if m_year == 'juin 2021':
        tx_var = 0
        df_yrs = df_montant_accordes[m_year].loc[df_montant_accordes['pays']== m_pays ].iloc[0]
    else:
        for i in range(0, len(l_periode)):
            if l_periode[i] == m_year:
                df_yrs = df_montant_accordes[m_year].loc[df_montant_accordes['pays']== m_pays ].iloc[0]
                df_yrs_ante = df_montant_accordes[l_periode[i-1]].loc[df_montant_accordes['pays']== m_pays ].iloc[0]
                tx_var = ((df_yrs/df_yrs_ante)-1)*100
                tx_var = round(tx_var, 2)

    return round(df_yrs/10**6, 1), tx_var

def get_montant_PIE(m_period_DPME):

    list_montant = df_montant_accordes[m_period_DPME].values[:8]
    list_montant = [round(x/10**6,2) for x in list_montant]
    list_pays = df_montant_accordes['pays'].values[:8]

    return list_pays, list_montant

def get_commentaire_expander(m_pays, m_period_DPME):

    com_benef = ""
    com_accompagne = ""
    com_montant = ""
    PME_benef, tx_benef = get_PME_benef(m_pays, m_period_DPME)
    var_benef = ""

    PME_accomp, tx_accomp = get_PME_accompagn(m_pays, m_period_DPME)
    var_accomp = ""

    montant_accorde, tx_accord = get_montant_accordes(m_pays, m_period_DPME)
    var_accorde = ""

    if m_period_DPME[:3] == "déc":
        m_period_DPME = "décembre " +m_period_DPME[-4:]

    if tx_benef>0:
        var_benef = ' Soit une hausse de **' +str(tx_benef)+ "**%  comparativement au semestre précédent."
    elif tx_benef == 0:
        var_benef = " Soit une valeur similaire au semestre antérieure." 
    elif tx_benef <0:
        var_benef = ' Soit une baisse de **' +str(tx_benef)+ "**%  par rapport au semestre antérieure."

    if tx_accomp>0:
        var_accomp = ' soit une augmentation de **' +str(tx_accomp)+ "**%"
    elif tx_accomp == 0:
        var_accomp = "semblable au montant dau semestre antérieur"
    elif tx_accomp <0:
        var_accomp = ' soit une diminution de **' +str(tx_accomp)+ "**%"
    
    if tx_accord>0:
        var_accorde = ' soit une augmentation de **' +str(tx_accord)+ "**%"
    elif tx_accord == 0:
        var_accorde = "semblable au montant da la précédente période"
    elif tx_accord <0:
        var_accorde = ' soit une réduction de **' +str(tx_accord)+ "**%"

    if m_period_DPME == "juin 2021":
        com_benef = "Le nombre de PME bénéficiaires d'un prêt bancaire en **"+m_period_DPME+"** a été évalué à **"+ str(int(PME_benef))+"**."
        com_accompagne = "En **"+m_period_DPME+"**, les PME accompagnées par les SAE étaient au nombre de **"+str(PME_accomp)+"**."
        com_montant = "Le montant de crédit accordé au PME via le Dispositif de soutien aux PME s'est établi à **"+str(montant_accorde)+"** millions de FCFA, en "+m_period_DPME+"."
    else:
        com_benef = "Le nombre de PME bénéficiaires d'un prêt bancaire en **"+m_period_DPME+"** a été évalué à "+ str(int(PME_benef))+"."+var_benef
        com_accompagne = "En **"+m_period_DPME+"**, les PME accompagnées par les SAE étaient au nombre de **"+str(PME_accomp)+"** ("+var_accomp+")."
        com_montant = "Le montant de crédit accordé aux Petites et Moyennes Entreprises via le Dispositif de soutien aux PME s'est établi à **"+str(montant_accorde)+"** millions de FCFA, en "+m_period_DPME+" ("+var_accorde+")."

    return com_benef, com_accompagne, com_montant


def get_DPME_montant_financement(m_pays):
    
    vf = df_montant_accordes.loc[df_montant_accordes['pays']== m_pays ].iloc[0].values[1:]
    vf = [round(x/10**6, 2) for x in vf]
    return vf

def get_nbr_PME_accompagn(m_pays):

    vf = df_PME_accompagn.loc[df_PME_accompagn['pays']== m_pays ].iloc[0].values[1:]

    return vf

def get_nbr_PME_benef(m_pays):
    vf = df_PME_benef.loc[df_PME_benef['pays']== m_pays ].iloc[0].values[1:]
    return vf


def get_mois(m_mois):
    if   m_mois == 'Janvier': rk = '01'
    elif m_mois == 'Février': rk = '02'
    elif m_mois == 'Mars': rk = '03'
    elif m_mois == 'Avril': rk = '04'
    elif m_mois == 'Mai': rk = '05'
    elif m_mois == 'Juin': rk = '06'
    elif m_mois == 'Juillet': rk = '07'
    elif m_mois == 'Août': rk = '08'
    elif m_mois == 'Septembre': rk = '09'
    elif m_mois == 'Octobre': rk = '10'
    elif m_mois == 'Novembre': rk = '11'
    elif m_mois == 'Décembre': rk = '12'

    return rk

def get_value_par_pays(df):

    df_bn = df.loc[df['Libelle Pays']  == 'Bénin']
    val_bn = round(df_bn['Valeurn'].sum()/1000,2)

    df_bf = df.loc[df['Libelle Pays']  == 'Burkina Faso']
    val_bf = round(df_bf['Valeurn'].sum()/1000,2)


    df_ci = df.loc[df['Libelle Pays']  == 'Côte d Ivoire']
    val_ci = round(df_ci['Valeurn'].sum()/1000,2)

    df_gb = df.loc[df['Libelle Pays']  == 'Guinée Bissau']
    val_gb = round(df_gb['Valeurn'].sum()/1000,2)

    df_ml = df.loc[df['Libelle Pays']  == 'Mali']
    val_ml = round(df_ml['Valeurn'].sum()/1000,2)

    df_ng = df.loc[df['Libelle Pays']  == 'Niger']
    val_ng = round(df_ng['Valeurn'].sum()/1000,2)


    df_sn = df.loc[df['Libelle Pays']  == 'Sénégal']
    val_sn = round(df_sn['Valeurn'].sum()/1000,2)


    df_tg = df.loc[df['Libelle Pays']  == 'Togo']
    val_tg = round(df_tg['Valeurn'].sum()/1000,2)


    return [val_bn, val_bf, val_ci, val_gb, val_ml, val_ng, val_sn, val_tg]

def get_contrib_par_pays(df):

    df_uemoa = df.loc[df['Libelle Pays']  != '']
    val_uemoa = df_uemoa['Valeurn'].sum()

    df_bn = df.loc[df['Libelle Pays']  == 'Bénin']
    val_bn = round((df_bn['Valeurn'].sum()/val_uemoa)*100,2)

    df_bf = df.loc[df['Libelle Pays']  == 'Burkina Faso']
    val_bf = round((df_bf['Valeurn'].sum()/val_uemoa)*100,2)


    df_ci = df.loc[df['Libelle Pays']  == 'Côte d Ivoire']
    val_ci = round((df_ci['Valeurn'].sum()/val_uemoa)*100,2)

    df_gb = df.loc[df['Libelle Pays']  == 'Guinée Bissau']
    val_gb = round((df_gb['Valeurn'].sum()/val_uemoa)*100,2)

    df_ml = df.loc[df['Libelle Pays']  == 'Mali']
    val_ml = round((df_ml['Valeurn'].sum()/val_uemoa)*100,2)

    df_ng = df.loc[df['Libelle Pays']  == 'Niger']
    val_ng = round((df_ng['Valeurn'].sum()/val_uemoa)*100,2)


    df_sn = df.loc[df['Libelle Pays']  == 'Sénégal']
    val_sn = round((df_sn['Valeurn'].sum()/val_uemoa)*100,2)


    df_tg = df.loc[df['Libelle Pays']  == 'Togo']
    val_tg = round((df_tg['Valeurn'].sum()/val_uemoa)*100,2)


    return [val_bn, val_bf, val_ci, val_gb, val_ml, val_ng, val_sn, val_tg]
    
def get_preposition(pays):
    if pays == 'Bénin': return "au"
    elif pays == 'Burkina Faso': return "au"
    elif pays == 'Côte d Ivoire': return "en"
    elif pays == 'Guinée Bissau': return "en"
    elif pays == 'Mali': return "au"
    elif pays == 'Niger': return "au"
    elif pays == 'Sénégal': return "au"
    elif pays == 'Togo': return "au"
    elif pays == 'UEMOA': return "dans l'"
     

def get_value_par_annee(df, pays):

    df_bn = df.loc[df['Libelle Pays']  == pays]
    val_bn = round(df_bn['Valeurn'].sum()/1000,2)

    return val_bn

def get_value_par_banks(df, pays):

    return 0

def get_value_par_instru(df, pays):

    return 0

# def get_classement_Instrument(v, m_pays, v_annee):

#     df = ""
#     if m_pays == 'UEMOA':
#         df = v.loc[v['Libelle Pays']  != ""]
#     else:
#         df = v.loc[v['Libelle Pays']  == m_pays]
    
#     df = df.loc[str(v_annee)]
#     df = round(df.groupby("Libelle Poste")['Valeurn'].sum()/1000,2)
#     df = df.sort_values(ascending=False)

#     vf = df[["Portefeuille d'effets commerciaux  ", 'Credits a la clientele  ',
#        'Credits a long terme  ', 'Affacturage  ',
#        'Autres a court terme  ', 'Credit de location-financement  ',
#        'Credits a moyen terme  ', 'Creances en souffrance  '
#         ]].sort_values(ascending=False) #'Titres de placement et titres de l activité de portefeuille'
    
#     return vf