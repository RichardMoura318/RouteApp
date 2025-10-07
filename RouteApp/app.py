import streamlit as st
from datetime import time
import pandas as pd
from services.utils import getdata, pointsinray, log
from services.tomtom import geocoding
from components.map_utils import create_map, add_marker, add_search_location
from components.ui_utils import display_point_card

st.set_page_config(page_title="Fretados", layout="wide")

if "log_loaded" not in st.session_state:
    log("Iniciando carregamento de dados")
    st.session_state["log_loaded"] = True

lines, points = getdata()
customers = lines['Cliente'].drop_duplicates()

st.title("Fretados")

with st.sidebar:    
    searchaddress = st.text_input("Endereço", placeholder="Digite um endereço")
    selectedlines = st.multiselect("Linhas", options=lines['Linha'].to_list(), default=lines['Linha'].to_list())
    selectedcustomer = st.multiselect("Clientes", options=customers.to_list(), default=customers.to_list())
    selectedrange = st.slider("Intervalo de operação", value=(time(0,0), time(23,59)))
    ray = st.slider("Raio (m)", 500, 10000, 1000, step=500)
    st.caption(f"Raio atual: **{ray:,} m**")

starttime, endtime = selectedrange
points_filtered = points[
    (points['Linha'].isin(selectedlines)) &
    (points['Cliente'].isin(selectedcustomer)) &
    (points['Horário'] >= starttime) &
    (points['Horário'] <= endtime)
]

coordinates = None
if searchaddress:
    response = geocoding(searchaddress)
    if response["success"]:
        coordinates = response["data"]
    else:
        st.warning(f"Endereço não encontrado: {response['error']}")

map_obj = create_map()
if coordinates:
    add_search_location(map_obj, coordinates, ray)
for idx, point in points_filtered.iterrows():
    add_marker(map_obj, point)

st.components.v1.html(map_obj._repr_html_(), height=600)

if coordinates:
    points_in_radius = pointsinray(points_filtered, lat=coordinates[0], lon=coordinates[1], ray=ray)
    if not points_in_radius.empty:
        st.title(f"Pontos dentro do raio de {ray/1000} km do local selecionado")
        for idx, point in points_in_radius.iterrows():
            display_point_card(point, origin=coordinates)
    else:
        st.warning("Nenhum ponto encontrado no raio selecionado.")
