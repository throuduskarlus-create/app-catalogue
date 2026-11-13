import pandas as pd
import streamlit as st

# 1. Configuration de la page (première instruction Streamlit)
st.set_page_config(
    page_title="Explorateur de catalogue", page_icon="📚", layout="wide"
)

FICHIER = "data/livres_poetry.csv"


@st.cache_data
def charger_donnees(chemin):
  return pd.read_csv(chemin)


df = charger_donnees(FICHIER)

# Titre et légende
st.title("Explorateur de catalogue — Poésie")
st.caption("Données collectées sur books.toscrape.com")

# --- BARRE LATÉRALE : LES FILTRES ---
st.sidebar.header("Filtres")
recherche = st.sidebar.text_input("Le titre contient")
note_mini = st.sidebar.slider("Note minimale", 1, 5, 1)

prix_min_val = float(df["prix_gbp"].min())
prix_max_val = float(df["prix_gbp"].max())
prix_min, prix_max = st.sidebar.slider(
    "Fourchette de prix (GBP)",
    prix_min_val,
    prix_max_val,
    (prix_min_val, prix_max_val),
)

# --- APPLICATION DES FILTRES ---
selection = df.copy()
if recherche:
  selection = selection[
      selection["titre"].str.contains(recherche, case=False, na=False)
  ]
selection = selection[
    (selection["note"] >= note_mini)
    & (selection["prix_gbp"] >= prix_min)
    & (selection["prix_gbp"] <= prix_max)
]

# --- CAS VIDE ---
if len(selection) == 0:
  st.warning("Aucun livre ne correspond à ces critères.")
else:
  # --- 4 INDICATEURS CÔTE À CÔTE ---
  col1, col2, col3, col4 = st.columns(4)
  with col1:
    st.metric("Livres retenus", len(selection))
  with col2:
    st.metric("Prix moyen", f"{selection['prix_gbp'].mean():.2f} GBP")
  with col3:
    st.metric("Note moyenne", f"{selection['note'].mean():.2f} / 5")
  with col4:
    st.metric("Stock total", int(selection["stock"].sum()))

  # --- TABLEAU ET PALMARÈS ---
  st.subheader("Catalogue filtré")
  st.dataframe(selection)

  gauche, droite = st.columns(2)
  with gauche:
    st.subheader("Les 5 mieux notés")
    st.dataframe(selection.nlargest(5, "note")[["titre", "note", "prix_gbp"]])
  with droite:
    st.subheader("Les 5 moins chers")
    st.dataframe(
        selection.nsmallest(5, "prix_gbp")[["titre", "note", "prix_gbp"]]
    )

# --- DONNÉES BRUTES ---
with st.expander("Voir les données brutes (non filtrées)"):
  st.dataframe(df)