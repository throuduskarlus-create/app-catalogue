import streamlit as st
import pandas as pd
import plotly.express as px

FICHIER = "data/livres_poetry.csv"


@st.cache_data
def charger_donnees(chemin):
    return pd.read_csv(chemin)


df = charger_donnees(FICHIER)

# 1) le widget
note_mini = st.sidebar.slider("Note minimale", 1, 5, 1)

# 2) le filtre
selection = df[df["note"] >= note_mini]

# 3) le graphique, construit sur la selection
if len(selection) == 0:
    st.warning("Aucun livre ne correspond.")
    st.stop()

fig = px.histogram(
    selection,
    x="prix_gbp",
    nbins=10,
    labels={"prix_gbp": "Prix (GBP)"},
    title=f"{len(selection)} livres notes {note_mini} ou plus",
)
st.plotly_chart(fig, use_container_width=True)