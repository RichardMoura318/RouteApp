import folium

def create_map(center=(-23.0712266, -47.0021326), zoom_start=10):
    return folium.Map(location=center, zoom_start=zoom_start, zoom_control=False)

def add_marker(map_obj, point):
    location = point['Latitude'], point['Longitude']
    currentline = point['Linha']
    totalstops = point.get('TotalStops', len(point))
    currentstop = point['Parada']
    stoptime = point['Horário']
    refpoint = point['Ponto de referência']

    if currentstop == 1:
        stoptype = 'Ponto de partida'
        markericon = 'play'
        markercolor = 'green'
    elif currentstop == totalstops:
        stoptype = 'Ponto de destino'
        markericon = 'stop'
        markercolor = 'red'
    else:
        stoptype = 'Ponto de passagem'
        markericon = 'bus'
        markercolor = 'blue'

    tooltip = f"""
        <b>Linha:</b> {currentline}<br>
        <b>Coordenadas:</b> {location}<br>
        <b>Horário:</b> {stoptime}<br>
        <b>Referência:</b> {refpoint}<br>
        <b>Tipo de ponto:</b> {stoptype}
    """

    folium.Marker(
        location=location,
        tooltip=folium.Tooltip(tooltip, max_width=600),
        icon=folium.Icon(icon=markericon, color=markercolor, prefix='fa')
    ).add_to(map_obj)

def add_search_location(map_obj, coordinates, radius):
    lat, lon = coordinates
    folium.Marker(
        location=[lat, lon],
        icon=folium.Icon(icon='location-pin', color='purple', prefix='fa')
    ).add_to(map_obj)
    folium.Circle(
        location=[lat, lon],
        radius=radius,
        color='purple',
        fill=True,
        fill_opacity=0.2
    ).add_to(map_obj)
