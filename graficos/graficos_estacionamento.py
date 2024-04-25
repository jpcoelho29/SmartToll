import pandas as pd
import numpy as np
import datetime as dt
import networkx as nx
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
from utils import escolha_matricula


def histograma_custo_estacionamento(dataframe):

    matricula = escolha_matricula(dataframe)

    # Filtrar o DataFrame pela matrícula selecionada
    df_filtrado = dataframe[dataframe["MATRICULA"] == matricula]

    # Verificar se existem dados após o filtro
    if df_filtrado.empty:
        print("Não há dados para a matrícula escolhida.")
        return

    # Ordenando o DataFrame df_filtrado por 'VALOR' em ordem decrescente
    df_filtrado = df_filtrado.sort_values(by="VALOR", ascending=False)

    # Calcular o número de bins usando a Regra de Sturges
    num_bins = int(1 + 3.322 * np.log10(len(df_filtrado["VALOR"])))

    # Histograma dos custos das viagens para a matrícula especificada
    plt.figure(figsize=(12, 6))
    sns.histplot(df_filtrado["VALOR"], bins=num_bins, kde=True, color="blue")
    plt.title(f"Histograma de Custo de Estacionamento para a Matrícula {matricula}")
    plt.xlabel("Custo em Euros")
    plt.ylabel("Frequência")
    plt.tight_layout()  # Ajusta o layout para evitar sobreposição de etiquetas
    plt.show()
    return


def histograma_duracao_estacionamento(dataframe):

    matricula = escolha_matricula(dataframe)

    # Filtrar o DataFrame pela matrícula selecionada
    df_filtrado = dataframe[dataframe["MATRICULA"] == matricula]

    # Verificar se existem dados após o filtro
    if df_filtrado.empty:
        print("Não há dados para a matrícula escolhida.")
        return

    # Ordenando o DataFrame df_filtrado por 'DURACAO_MINUTOS' em ordem decrescente
    df_filtrado = df_filtrado.sort_values(by="DURACAO_MINUTOS", ascending=False)

    # Calcular o número de bins usando a Regra de Sturges
    num_bins = int(1 + 3.322 * np.log10(len(df_filtrado["DURACAO_MINUTOS"])))

    # Histograma dos custos das viagens para a matrícula especificada
    plt.figure(figsize=(12, 6))
    sns.histplot(df_filtrado["VALOR"], bins=num_bins, kde=True, color="blue")
    plt.title(f"Histograma de Custo de Estacionamento para a Matrícula {matricula}")
    plt.xlabel("Custo em Euros")
    plt.ylabel("Frequência")
    plt.tight_layout()  # Ajusta o layout para evitar sobreposição de etiquetas
    plt.show()
    return


def dispersao_custo_duracao_estacionamento(dataframe):

    matricula = escolha_matricula(dataframe)

    # Filtrar o DataFrame pela matrícula selecionada
    df_filtrado = dataframe[dataframe["MATRICULA"] == matricula]

    # Verificar se existem dados através do filtro
    if df_filtrado.empty:
        print("Não há dados para a matrícula escolhida.")
        return

    # Plotar o gráfico de dispersão entre custo e duração
    plt.figure(figsize=(12, 6))
    sns.scatterplot(x="VALOR", y="DURACAO_MINUTOS", data=df_filtrado)
    plt.title(f"Dispersão Duração vs Custo para a Matrícula {matricula}")
    plt.xlabel("Custo (€)")
    plt.ylabel("Duração em Minutos")
    plt.tight_layout()  # Ajusta o layout para evitar sobreposição de etiquetas
    plt.show()
    return
