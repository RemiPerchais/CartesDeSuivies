
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore

# Titre de l'application
st.title("Analyse des donées de suivis 📊")


# Cacher le menu Streamlit (qui inclut le lien GitHub) et le footer
hide_menu = """
<style>
#MainMenu {visibility: hidden;}  /* Cache le menu principal */
footer {visibility: hidden;}      /* Cache le footer Streamlit */
header {visibility: hidden;}      /* Cache le header */
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

# Chargement du fichier Excel
uploaded_file = st.file_uploader("Déposez votre fichier Excel ici", type=["xlsx", "xls"])

if uploaded_file:
    # Lire le fichier Excel dans un DataFrame pandas
    df = pd.read_excel(uploaded_file)

    # Afficher un aperçu des données
    st.subheader("Aperçu des données :")
    st.write(df.head())


    # Sélectionner une colonne numérique pour le graphe
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

    dates = df.iloc[2:, 1]
    dates = pd.to_datetime(dates)
    st.write("Valeur de dates :", dates)

    ep = df.iloc[2:, 2]
    st.write("Valeur de ep :", ep)

    r_car = df.iloc[2:, 3]
    st.write("Valeur de r² :", r_car)


    val_cible = 520
    nb_mesure_dek = 1
    ep = pd.to_numeric(ep)
    zs = zscore(ep) #calcul des zscores
    ep_SA = ep[np.abs(zs) < 1] #filtrage des données avec zscore < 1
    moy_ep_SA = ep_SA.mean()
    std_ep_SA = ep_SA.std()




    Moins3sig = val_cible - 3*std_ep_SA/np.sqrt(nb_mesure_dek)
    Plus3sig = val_cible + 3*std_ep_SA/np.sqrt(nb_mesure_dek)
    Moins6sig = val_cible - 6*std_ep_SA/np.sqrt(nb_mesure_dek)
    Plus6sig = val_cible + 6*std_ep_SA/np.sqrt(nb_mesure_dek)

    
    if numeric_columns:
        column = st.selectbox("Choisissez une colonne pour le graphe", numeric_columns)

        # Générer le graphe
        fig, ax = plt.subplots()
        plt.figure()
        plt.plot(dates, ep, marker="o", linestyle="-", color="r", label="ep")

        plt.axhline(y=Moins3sig, color="red", linestyle="--", label="Moyenne")
        plt.axhline(y=Plus3sig, color="green", linestyle="-.", label="Seuil 50")  # Seuil à 50

        # Afficher le graphe dans Streamlit
        st.pyplot(fig)
    else:
        st.warning("Aucune colonne numérique détectée dans le fichier Excel.")

