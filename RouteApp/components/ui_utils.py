import streamlit as st

def display_point_card(point, origin):
    destinylat = point['Latitude']
    destinylon = point['Longitude']
    distance = point['Distância']
    refpoint = point['Ponto de referência']
    line = point['Linha']
    origin_lat, origin_lon = origin

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
            <p style="margin:4px 0; font-weight:bold; font-size:16px;">Linha: {line}</p>
            <p style="margin:2px 0; font-size:14px;">Latitude: {destinylat}, Longitude: {destinylon}</p>
            <p style="margin:2px 0; font-size:14px; color: #555;">Distância do ponto selecionado: {distance} m</p>
            <p style="margin:2px 0; font-size:14px; color: #555;">Ponto de referência: {refpoint}</p>
            <a href="https://www.google.com/maps/dir/?api=1&origin={origin_lat},{origin_lon}&destination={destinylat},{destinylon}" target="_blank" style="text-decoration: none;">
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
