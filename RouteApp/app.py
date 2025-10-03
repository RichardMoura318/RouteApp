import streamlit as st
from streamlit_folium import st_folium
import folium
from services.tomtom import geocoding
from services.utils import getdata, pointsinray
import pandas as pd
from datetime import time

st.set_page_config(
    page_title='Fretados Belenus',
    layout='wide',
    initial_sidebar_state='collapsed'

)


@st.cache_data
def loaddata():
    return getdata()


lines, points = loaddata()
pointsinselectedray = pd.DataFrame()
zones = points['Bairro'].drop_duplicates().tolist()

map = folium.Map(location=(-23.0712266, -47.0021326),
                 zoom_start=10, zoom_control=False)

st.title('Fretados Belenus')

with st.sidebar:

    st.markdown("### Endereço de Pesquisa")
    searchaddress = st.text_input(
        'Endereço',
        value='R. Comendador João Lucas Vinhedo, 300 - Distrito Industrial, Vinhedo - SP, 13280-000',
        placeholder='Digite um endereço'
    )

    st.markdown("### Filtros de Linha")
    selectedlines = st.multiselect(
        'Linhas',
        options=lines['Linha'].to_list(),
        default=lines['Linha'].to_list(),
        placeholder='Selecione as Linhas'
    )

    st.divider()

    st.markdown("### Filtros de Bairro")
    selectedzone = st.multiselect(
        'Bairro',
        options=zones,
        default=zones,
        placeholder='Selecione o Bairro'
    )

    st.divider()

    st.markdown("### Intervalo de Operação")
    selectedrange = st.slider(
        'Escolha o intervalo de operação:',
        value=(time(00, 00), time(23, 59))
    )

    st.divider()

    st.markdown("### Raio de Busca")
    ray = st.slider(
        'Raio (m)',
        min_value=500,
        max_value=10000,
        step=500,
        value=1000
    )
    st.caption(f'Raio atual: **{ray:,} m**')


starttime, endtime = selectedrange
pointsplot = points.copy()
pointsplot = pointsplot[
    (pointsplot['Linha'].isin(selectedlines)) &
    (pointsplot['Bairro'].isin(selectedzone)) &
    (pointsplot['Horário'] >= starttime) &
    (pointsplot['Horário'] <= endtime)
]


if searchaddress:
    response = geocoding(searchaddress)

    if response['success']:
        lat, lon = response['data']
        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(icon='location-pin', prefix='fa')
        ).add_to(map)
        folium.Circle(
            location=[lat, lon],
            radius=ray,
            color='purple',
            fill=True,
            fill_opacity=0.2).add_to(map)
        pointsinselectedray = pointsinray(
            points=pointsplot, lat=lat, lon=lon, ray=ray)
    else:
        st.warning(f'Endereço não encontrado.{response['error']}')
    searchaddress = None


for idx, i in pointsplot.iterrows():

    location = i['Latitude'], i['Longitude']
    currentline = i['Linha']
    totalstops = len(pointsplot[pointsplot['Linha'] == currentline])
    currentstop = i['Parada']
    stoptime = i['Horário']
    refpoint = i['Ponto de referência']

    if currentstop == 1:
        stoptype ='Ponto de partida'
        pinicon = 'play'
        pincolor = 'green'
    elif currentstop == totalstops:
        stoptype ='Ponto de destino'
        pinicon = 'stop'
        pincolor = 'red'
    else:
        stoptype ='Ponto de passagem'
        pinicon = 'bus'
        pincolor = 'blue'

    pintooltip = f"""
            <b>Linha:</b> {currentline}<br>
            <b>Coordenadas geográficas:</b> {location}<br>
            <b>Horário:</b> {stoptime}<br>
            <b>Referência:</b> {refpoint}<br>
            <b>Tipo de ponto:</b> {stoptype}
            """

    folium.Marker(
        location=location,
        tooltip=folium.Tooltip(pintooltip, max_width=600),
        icon=folium.Icon(icon=pinicon, color=pincolor, prefix='fa')
    ).add_to(map)

st_folium(map, width=1920)
if not pointsinselectedray.empty:
    st.title((f'Pontos dentro do raio de {ray/1000} km do local selecionado'))

    for idx, i in pointsinselectedray.iterrows():
        destinylat = i['Latitude']
        destinylon = i['Longitude']
        distance = i['Distância']
        refpoint = i['Ponto de referência']
        line = i['Linha']
        st.markdown(
            f"""
            <div style="
                border: 1px solid #eee;
                border-radius: 12px;
                padding: 12px 20px;
                margin-bottom: 12px;
                background-color: #fafafa;
                box-shadow: 0 2px 6px rgba(0,0,0,0.05);
                font-family: Arial, sans-serif;
            ">
                <p style="margin:4px 0; font-weight:bold; font-size:16px;">
                    Linha: {line}
                </p>
                <p style="margin:2px 0; font-size:14px;">
                    Latitude: {destinylat}, Longitude: {destinylon}
                </p>
                <p style="margin:2px 0; font-size:14px; color: #555;">
                    Distância do ponto selecionado: {distance} m
                </p>
                <p style="margin:2px 0; font-size:14px; color: #555;">
                    Ponto de referência: {refpoint}
                </p>
                <a href="https://www.google.com/maps/dir/?api=1&origin={lat},{lon}&destination={destinylat},{destinylon}" target="_blank"
                style="
                    text-decoration: none;
                ">
                    <div style="
                        display: inline-block;
                        background-color: #FF4B4B;
                        color: white;
                        padding: 8px 16px;
                        border-radius: 6px;
                        font-weight: bold;
                        font-size: 14px;
                        transition: background 0.3s;
                    " onmouseover="this.style.background='#8a2be2';" onmouseout="this.style.background='#6a0dad';">
                    Verificar trajeto no google
                    </div>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )


else:
    st.warning('Nenhum ponto encontrado no raio selecionado.')
