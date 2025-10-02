import streamlit as st
import folium
from streamlit_folium import st_folium
from services.routes import getData
from services.tomtom import geocode
import pandas as pd

st.set_page_config(page_title="Fretados", layout="wide")
st.title("Fretados Belenus")

@st.cache_data
def loadData():
    return getData()

lines, points = loadData()

# Inicializa lista de buscas no session_state
if "buscas" not in st.session_state:
    st.session_state.buscas = []

# --- Layout em colunas ---
col1, col2 = st.columns([1, 3])  # 1 parte para controles, 3 partes para mapa

with col1:
    # Seleção de linhas
    selected_lines = st.multiselect(
        "Selecione as linhas para visualizar",
        options=lines["Linha"].tolist(),
        default=lines["Linha"].tolist(),
        placeholder="Selecionar"
    )

    # Busca de endereço
    address = st.text_input("Digite o endereço de busca:")
    search = st.button("Pesquisar endereço:")

    # Slider para o raio do círculo
    raio = st.slider("Defina o raio do círculo (metros):", min_value=50, max_value=20000, value=500, step=50)

# Criar mapa
mapa = folium.Map(location=[-23.55, -46.63], zoom_start=11)

with col2:
    # Adiciona linhas e pontos do fretado
    for linha in selected_lines:
        df_linha = points[points['Linha'] == linha].reset_index(drop=True)
        cor = df_linha['Cor'].iloc[0]

        for idx, row in df_linha.iterrows():
            if idx == 0:
                color = "green"; icon_type = "play"
            elif idx == len(df_linha)-1:
                color = "red"; icon_type = "stop"
            else:
                color = "blue"; icon_type = "bus"

            popup_text = f"""
            <b>Linha:</b> {linha}<br>
            <b>Via:</b> {row['Via']}<br>
            <b>Horário:</b> {row['Horário']}<br>
            <b>Posição na rota:</b> {idx+1} de {len(df_linha)}
            """

            # Plotar marcador
            folium.Marker(
                location=(row['LatOrigem'], row['LongOrigem']),
                popup=folium.Popup(popup_text, max_width=300),
                icon=folium.Icon(color=color, icon=icon_type, prefix="fa")
            ).add_to(mapa)

            # Plotar linha apenas se origem e destino existirem
            if pd.notna(row['LatOrigem']) and pd.notna(row['LongOrigem']) and pd.notna(row['LatDestino']) and pd.notna(row['LongDestino']):
                folium.PolyLine(
                    locations=[(row['LatOrigem'], row['LongOrigem']),
                               (row['LatDestino'], row['LongDestino'])],
                    color=cor,
                    weight=5,
                    opacity=0.7
                ).add_to(mapa)

    # Se clicar em pesquisar, armazena a busca
    if search and address:
        coords = geocode(address)
        if coords:
            st.session_state.buscas.append((coords, address, raio))
        else:
            st.warning("Endereço não encontrado.")

    # Adiciona os círculos e marcadores das buscas anteriores
    for coords, addr, raio_busca in st.session_state.buscas:
        folium.Marker(
            location=coords,
            popup=folium.Popup(f"<b>📍 {addr}</b>", max_width=300),
            icon=folium.Icon(color="purple", icon="search", prefix="fa")
        ).add_to(mapa)

        folium.Circle(
            location=coords,
            radius=raio_busca,
            color="purple",
            fill=True,
            fill_opacity=0.2
        ).add_to(mapa)

    # Renderizar mapa
    st_folium(mapa, width=1200, height=600)
