import streamlit as st
import pandas as pd

# Importation du module
from streamlit_option_menu import option_menu
from streamlit_authenticator import Authenticate

# --- Charger les données utilisateur depuis le CSV ---
chemin_fichier_csv = "users.csv"
try:
    df_utilisateurs = pd.read_csv(chemin_fichier_csv)
    # Assurez-vous que les colonnes correspondent exactement à :
    # 'name', 'password', 'email', 'failed_login_attemps', 'logged_in', 'role'
    donnees_utilisateurs = {
        "usernames": {
            row["name"]: {
                "name": row["name"],
                "password": row[
                    "password"
                ],  # IMPORTANT : Les mots de passe doivent être HACHÉS dans le CSV
                "email": row["email"],
                "failed_login_attemps": row["failed_login_attemps"],
                "logged_in": row["logged_in"],
                "role": row["role"],
            }
            for _, row in df_utilisateurs.iterrows()
        }
    }
except FileNotFoundError:
    st.error(
        f"Erreur : Fichier CSV non trouvé à l'emplacement : {chemin_fichier_csv}.  Assurez-vous que le fichier existe et que le chemin est correct."
    )
    st.stop()  # Arrête l'exécution si le fichier n'est pas trouvé

# --- Configuration de Streamlit Authenticator ---
authenticator = Authenticate(
    donnees_utilisateurs,  # Les données des comptes
    "cookie name",  # Le nom du cookie, un str quelconque
    "cookie key",  # La clé du cookie, un str quelconque
    30,  # Le nombre de jours avant que le cookie expire
)

authenticator.login()


def accueil():
    st.title("Bienvenue sur la page de Maëlle")


if st.session_state["authentication_status"]:

    # Le bouton de déconnexion dans la sidebar avec le bienvenue utilisateur
    with st.sidebar:
        st.write(f"Bonjour **{st.session_state['name']}** ! Vous êtes connecté(e).")
        authenticator.logout("Déconnexion", "sidebar")

    # Création du menu qui va afficher les choix qui se trouvent dans la variable options
    with st.sidebar:
        selection = option_menu(menu_title=None, options=["Accueil", "Photos de chats"])

    # Affichage du contenu principal en fonction de la sélection
    if selection == "Accueil":
        accueil()
        st.write("Et parce que les chats sont trop mignons!")
        st.markdown("---")  # Une ligne de séparation
        st.image(
            "https://creapills.com/wp-content/uploads/2019/10/lingvistov-dessin-chat-quotidien-312.jpg"
        )
    elif selection == "Photos de chats":
        st.header("Photos de chats")
        st.write("Voici une sélection de photos de chats pour votre plaisir :")
        # Exemple de grille avec st.columns
        cols = st.columns(3)  # Crée 3 colonnes
        cols[0].image(
            "https://cdn.pixabay.com/photo/2020/05/03/06/51/kitten-5124104_1280.jpg",
            width=200,
        )
        cols[1].image(
            "https://chatfaitdubien.fr/wp-content/uploads/2016/12/800_600____2__pension-chat-63_36.jpg",
            width=200,
        )
        cols[2].image(
            "https://cdn.shopify.com/s/files/1/0402/6505/6418/files/ragdol-mignon_480x480.jpg?v=1698920651",
            width=200,
        )


elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning("Les champs username et mot de passe doivent être remplie")
