import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

FICHIER = "data/livres_poetry.csv"

st.set_page_config(
    page_title="Graphiques",
    layout="wide"
)


@st.cache_data
def charger_donnees(chemin):
    return pd.read_csv(chemin)


df = charger_donnees(FICHIER)

st.title("Visualiser le catalogue")

st.write(df.head())

# ------------------
# Graphique Streamlit
# ------------------

st.subheader("Nombre de livres par note")

par_note = df["note"].value_counts().sort_index()

st.bar_chart(par_note)

# ------------------
# Scatter Streamlit
# ------------------

st.subheader("Prix et note, livre par livre")

st.scatter_chart(
    df,
    x="prix_gbp",
    y="note",
    size="stock"
)

# ------------------
# Matplotlib
# ------------------

st.subheader("Répartition des prix")

fig, ax = plt.subplots(figsize=(8, 4))

ax.hist(
    df["prix_gbp"],
    bins=10,
    color="#4C72B0",
    edgecolor="white"
)

ax.set_xlabel("Prix (GBP)")
ax.set_ylabel("Nombre de livres")
ax.set_title("Distribution des prix")

st.pyplot(fig)

# ------------------
# Plotly
# ------------------

st.subheader("Prix et note en interactif")

fig = px.scatter(
    df,
    x="prix_gbp",
    y="note",
    size="stock",
    hover_name="titre",
    labels={
        "prix_gbp": "Prix (GBP)",
        "note": "Note sur 5"
    },
)

st.plotly_chart(
    fig,
    use_container_width=True
)import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

FICHIER = "data/livres_poetry.csv"

st.set_page_config(
    page_title="Graphiques",
    layout="wide"
)


@st.cache_data
def charger_donnees(chemin):
    return pd.read_csv(chemin)


df = charger_donnees(FICHIER)

st.title("Visualiser le catalogue")

st.write(df.head())

# ------------------
# Graphique Streamlit
# ------------------

st.subheader("Nombre de livres par note")

par_note = df["note"].value_counts().sort_index()

st.bar_chart(par_note)

# ------------------
# Scatter Streamlit
# ------------------

st.subheader("Prix et note, livre par livre")

st.scatter_chart(
    df,
    x="prix_gbp",
    y="note",
    size="stock"
)

# ------------------
# Matplotlib
# ------------------

st.subheader("Répartition des prix")

fig, ax = plt.subplots(figsize=(8, 4))

ax.hist(
    df["prix_gbp"],
    bins=10,
    color="#4C72B0",
    edgecolor="white"
)

ax.set_xlabel("Prix (GBP)")
ax.set_ylabel("Nombre de livres")
ax.set_title("Distribution des prix")

st.pyplot(fig)

# ------------------
# Plotly
# ------------------

st.subheader("Prix et note en interactif")

fig = px.scatter(
    df,
    x="prix_gbp",
    y="note",
    size="stock",
    hover_name="titre",
    labels={
        "prix_gbp": "Prix (GBP)",
        "note": "Note sur 5"
    },
)

st.plotly_chart(
    fig,
    use_container_width=True
)