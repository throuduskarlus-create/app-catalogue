import pandas as pd
import streamlit as st
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Tableau de bord du catalogue",
    page_icon="📚",
    layout="wide",
)

FICHIER = "data/livres_poetry.csv"


@st.cache_data
def charger_donnees(chemin):
    return pd.read_csv(chemin)


df = charger_donnees(FICHIER)

# Titre
st.title("📊 Tableau de bord du catalogue")
st.caption("Données collectées sur books.toscrape.com")

# --------------------
# FILTRES
# --------------------

st.sidebar.header("Filtres")

recherche = st.sidebar.text_input(
    "Le titre contient"
)

note_mini = st.sidebar.slider(
    "Note minimale",
    1,
    5,
    1
)

prix_min_val = float(df["prix_gbp"].min())
prix_max_val = float(df["prix_gbp"].max())

prix_min, prix_max = st.sidebar.slider(
    "Fourchette de prix (GBP)",
    prix_min_val,
    prix_max_val,
    (prix_min_val, prix_max_val),
)

# --------------------
# APPLICATION DES FILTRES
# --------------------

selection = df.copy()

if recherche:
    selection = selection[
        selection["titre"].str.contains(
            recherche,
            case=False,
            na=False
        )
    ]

selection = selection[
    (selection["note"] >= note_mini)
    & (selection["prix_gbp"] >= prix_min)
    & (selection["prix_gbp"] <= prix_max)
]

# --------------------
# CAS VIDE
# --------------------

if len(selection) == 0:
    st.warning("Aucun livre ne correspond à ces critères.")
    st.stop()

# --------------------
# INDICATEURS
# --------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Livres retenus",
        len(selection)
    )

with col2:
    st.metric(
        "Prix moyen",
        f"{selection['prix_gbp'].mean():.2f} GBP"
    )

with col3:
    st.metric(
        "Note moyenne",
        f"{selection['note'].mean():.2f} / 5"
    )

with col4:
    st.metric(
        "Stock total",
        int(selection["stock"].sum())
    )

# --------------------
# VISUALISATIONS
# --------------------

st.header("Visualisations")

col_gauche, col_droite = st.columns(2)

# Graphique 1

with col_gauche:

    st.subheader(
        "Comment les prix se distribuent-ils ?"
    )

    fig_prix = px.histogram(
        selection,
        x="prix_gbp",
        nbins=10,
        labels={
            "prix_gbp": "Prix (GBP)"
        }
    )

    st.plotly_chart(
        fig_prix,
        use_container_width=True
    )

    st.caption(
        "Cette répartition montre où se concentrent les prix des livres sélectionnés."
    )

# Graphique 2

with col_droite:

    st.subheader(
        "Combien de livres par note ?"
    )

    par_note = (
        selection["note"]
        .value_counts()
        .sort_index()
    )

    st.bar_chart(par_note)

    st.caption(
        "Les notes les plus représentées apparaissent avec les barres les plus hautes."
    )

# --------------------
# GRAPHIQUE PILOTÉ PAR UN WIDGET
# --------------------

type_graphique = st.selectbox(
    "Type de graphique",
    [
        "Nuage de points",
        "Histogramme"
    ]
)

st.subheader(
    "Le prix et la note vont-ils ensemble ?"
)

if type_graphique == "Nuage de points":

    fig_relation = px.scatter(
        selection,
        x="prix_gbp",
        y="note",
        size="stock",
        hover_name="titre",
        labels={
            "prix_gbp": "Prix (GBP)",
            "note": "Note sur 5"
        },
        title="Relation entre prix et note"
    )

else:

    fig_relation = px.histogram(
        selection,
        x="prix_gbp",
        nbins=10,
        labels={
            "prix_gbp": "Prix (GBP)"
        },
        title="Distribution des prix"
    )

st.plotly_chart(
    fig_relation,
    use_container_width=True
)

correlation = selection["prix_gbp"].corr(
    selection["note"]
)

st.caption(
    f"La corrélation prix/note est de {correlation:.2f}. "
    "Une valeur proche de 0 indique une relation faible."
)

# --------------------
# DONNÉES BRUTES
# --------------------

with st.expander(
    "Voir les données brutes (non filtrées)"
):
    st.dataframe(df)