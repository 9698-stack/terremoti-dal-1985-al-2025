import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Titolo della pagina
st.title("Analisi dei terremoti in Italia - Grafici interattivi")

# Caricamento del dataset
df = df = pd.read_csv(r"C:\Users\UTENTE\Downloads\terremoti_italia_ingv.csv", encoding="latin1")

# Convertiamo la colonna 'time' in datetime
df['time'] = pd.to_datetime(df['time'], errors='coerce')

# Creiamo una colonna con l'anno
df['year'] = df['time'].dt.year

# ---------------------------
# Selettore interattivo di anni
# ---------------------------
st.sidebar.subheader("Filtra per intervallo di anni")
min_year = int(df['year'].min())
max_year = int(df['year'].max())
year_range = st.sidebar.slider("Seleziona intervallo di anni:", min_year, max_year, (min_year, max_year))

# Filtriamo il dataframe
df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Raggruppiamo i dati filtrati
events_per_year = df_filtered.groupby('year').size()
avg_mag_per_year = df_filtered.groupby('year')['mag'].mean()

# ---------------------------
# GRAFICO INTERATTIVO — Numero di terremoti per anno
# ---------------------------
st.subheader(f"Numero di terremoti per anno ({year_range[0]} - {year_range[1]})")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(
    x=events_per_year.index,
    y=events_per_year.values,
    mode='lines+markers',
    name='Numero di eventi',
    line=dict(color='blue'),
    marker=dict(size=8)
))
fig1.update_layout(
    xaxis_title='Anno',
    yaxis_title='Numero di eventi',
    template='plotly_white'
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------
# GRAFICO INTERATTIVO — Numero eventi + magnitudo media
# ---------------------------
st.subheader(f"Numero di eventi e magnitudo media per anno ({year_range[0]} - {year_range[1]})")

fig2 = go.Figure()

# Linea numero eventi
fig2.add_trace(go.Scatter(
    x=events_per_year.index,
    y=events_per_year.values,
    mode='lines+markers',
    name='Numero di eventi',
    line=dict(color='blue')
))

# Linea magnitudo media (secondo asse)
fig2.add_trace(go.Scatter(
    x=avg_mag_per_year.index,
    y=avg_mag_per_year.values,
    mode='lines+markers',
    name='Magnitudo media',
    line=dict(color='red', dash='dash'),
    yaxis='y2'
))

fig2.update_layout(
    xaxis=dict(title='Anno'),
    yaxis=dict(title='Numero di eventi', side='left', showgrid=True),
    yaxis2=dict(title='Magnitudo media', overlaying='y', side='right'),
    template='plotly_white'
)

st.plotly_chart(fig2, use_container_width=True)

# Mostra anche il dataframe filtrato
st.subheader("Dataset filtrato")
st.dataframe(df_filtered)
