import pandas as pd
import random


def getData(path='data/routes.xlsx'):
    df = pd.read_excel(path, sheet_name='Itinerários')

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

    def get_cor(linha):
        if linha in cores_fixas:
            return cores_fixas[linha]
        else:
            return "#%06x" % random.randint(0, 0xFFFFFF)

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

