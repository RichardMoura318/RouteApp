import pandas as pd
import random
import os
import colorsys

# Caminho seguro para o arquivo Excel
BASE_DIR = os.path.dirname(__file__)
path = os.path.join(BASE_DIR, '..', 'data', 'routes.xlsx')

def getData(path=path):
    # Verifica se o arquivo existe
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    # Lê os dados
    df = pd.read_excel(path, sheet_name='Itinerários')

    # Linhas únicas com horário inicial e final
    lines = df.drop_duplicates(subset=['Linha'])[['Linha']]
    schedule = df.groupby('Linha')['Horário'].agg(['min', 'max']).reset_index()
    schedule.columns = ['Linha', 'Horario Saida', 'Horario Chegada']
    lines = pd.merge(lines, schedule, on='Linha', how='left')

    # Cores fixas
    cores_fixas = {
        "Linha Azul": "blue",
        "Linha Verde": "green",
        "Linha Vermelha": "red",
        "Linha Amarela": "orange"
    }

    # Gera cores aleatórias distintas usando HSV
    def random_color():
        h = random.random()
        s = 0.7 + random.random() * 0.3  # saturação alta
        v = 0.7 + random.random() * 0.3  # brilho alto
        r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v)]
        return f"#{r:02x}{g:02x}{b:02x}"

    # Define a cor de cada linha
    def get_cor(linha):
        return cores_fixas.get(linha, random_color())

    lines["Cor"] = lines["Linha"].apply(get_cor)
    lines = lines.sort_values(by='Linha', ascending=True)

    # Criando DataFrame de pontos
    points = df[['Linha', 'Via', 'Horário', 'Latitude',
                 'Longitude', 'Ponto de referência']].copy()

    # Ordenar por Linha e Horário
    points = points.sort_values(by=['Linha', 'Horário'])

    # Criar colunas de origem e destino
    points['LatOrigem'] = points['Latitude']
    points['LongOrigem'] = points['Longitude']
    points['LatDestino'] = points.groupby('Linha')['Latitude'].shift(-1)
    points['LongDestino'] = points.groupby('Linha')['Longitude'].shift(-1)

    # Adicionar a cor da linha
    points = points.merge(lines[['Linha', 'Cor']], on='Linha', how='left')

    # Selecionar colunas finais
    points = points[['Linha', 'Cor', 'Via', 'Horário',
                     'LatOrigem', 'LongOrigem', 'LatDestino', 'LongDestino']]

    return lines, points
