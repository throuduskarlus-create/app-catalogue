import streamlit as st
import pandas as pd
import plotly.express as px

FICHIER = "data/livres_poetry.csv"

st.set_page_config(
    page_title="Tableau de bord",
    page_icon="📊",
    layout="wide"
)


@st.cache_data
def charger_donnees(chemin):
    return pd.read_csv(chemin)


df = charger_donnees(FICHIER)

st.title("📊 Tableau de bord du catalogue")

# -------------------
# FILTRES
# -------------------

st.sidebar.header("Filtres")

recherche = st.sidebar.text_input(
    "Le titre contient"
)

note_min = st.sidebar.slider(
    "Note minimale",
    1,
    5,
    1
)

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
    selection["note"] >= note_min
]

if selection.empty:
    st.warning("Aucun livre trouvé.")
    st.stop()

# -------------------
# CHOIX DU GRAPHIQUE
# -------------------

type_graphique = st.radio(
    "Type de graphique pour les notes",
    ["Barres", "Secteur"]
)

# -------------------
# DEUX GRAPHIQUES
# -------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader(
        "Comment les prix se distribuent-ils ?"
    )

    fig = px.histogram(
        selection,
        x="prix_gbp",
        nbins=10,
        labels={
            "prix_gbp": "Prix (GBP)"
        }
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "La majorité des livres se concentre dans certaines plages de prix."
    )

with col2:

    st.subheader(
        "Combien de livres par note ?"
    )

    par_note = (
        selection["note"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    par_note.columns = [
        "note",
        "nombre"
    ]

    if type_graphique == "Barres":

        fig = px.bar(
            par_note,
            x="note",
            y="nombre",
            labels={
                "note": "Note",
                "nombre": "Nombre de livres"
            }
        )

    else:

        fig = px.pie(
            par_note,
            names="note",
            values="nombre"
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        "Certaines notes sont beaucoup plus fréquentes que d'autres."
    )

# -------------------
# 3E GRAPHIQUE
# -------------------

st.subheader(
    "Le prix et la note vont-ils ensemble ?"
)

fig = px.scatter(
    selection,
    x="prix_gbp",
    y="note",
    size="stock",
    hover_name="titre",
    labels={
        "prix_gbp": "Prix (GBP)",
        "note": "Note sur 5",
        "stock": "Stock"
    }
)

st.plotly_chart(
    fig,
    use_container_width=True
)