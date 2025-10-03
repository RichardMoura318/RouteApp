import pandas as pd
from haversine import haversine, Unit


def getdata(path='data/routes.xlsx'):
    df = pd.read_excel(path)

    # Linhas resumidas
    lines = df.copy()
    lines['Saída'] = lines.groupby('Linha')['Horário'].transform('min')
    lines['Chegada'] = lines.groupby('Linha')['Horário'].transform('max')
    lines = lines.drop_duplicates(subset=['Linha'], keep='first')
    lines = lines[['Linha', 'Latitude', 'Longitude', 'Horário', 'Saída', 'Chegada']]
    lines = lines.sort_values(by=['Linha', 'Horário'], ascending=True)

    # Pontos
    points = df[['Linha','Horário', 'Latitude', 'Longitude', 'Ponto de referência','Bairro']].copy()
    points = points.sort_values(by=['Linha', 'Horário'], ascending=True)
    points['Parada'] = points.groupby('Linha').cumcount() + 1

    return points


def pointsinray(points: pd.DataFrame, lat: float, lon: float, ray: float) -> pd.DataFrame:
    center = (lat, lon)
    points = points.copy()
    points['Distância'] = round(points.apply(
        lambda row: haversine(
            center, (row['Latitude'], row['Longitude']), unit=Unit.METERS),
        axis=1
    ), 2)
    points = points[points['Distância'] <= ray]
    points = points.sort_values(by='Distância', ascending=True)
    return points
