import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
from utils import escolha_matricula, filtrar_datas, escolher_itinerario_
from funcionalidades import custos


def histograma_custo_viagens(dataframe):

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
    sns.histplot(df_filtrado["VALOR"], bins=num_bins, kde=True, color="#0897B4")
    plt.title(f"Histograma de Custo das Viagens para a Matrícula {matricula}")
    plt.xlabel("Custo em Euros")
    plt.ylabel("Frequência")
    plt.tight_layout()  # Ajusta o layout para evitar sobreposição de etiquetas
    plt.show()
    return


# Análise de séries temporais de consumo de portagens
def consumo_portagens(df):

    matricula = escolha_matricula(df)

    # Filtrar dados pela matrícula selecionada
    df_filtrado = df[df["MATRICULA"] == matricula]

    # Verificar se existem dados para a matrícula escolhida
    if df_filtrado.empty:
        print("Não há dados de consumo para a matrícula selecionada.")
        return

    # Criar uma coluna 'ANO_MES' para agrupar por ano e mês
    df_filtrado["ANO_MES"] = (
        df_filtrado["ANO"].astype(str)
        + "-"
        + df_filtrado["MES"].astype(str).apply(lambda x: x.zfill(2))
    )

    # Agrupar dados por ano e mês e somar o consumo
    consumo_mensal = df_filtrado.groupby("ANO_MES")["VALOR"].sum().reset_index()

    # Gráfico de linha
    plt.figure(figsize=(12, 6))
    plt.plot(
        consumo_mensal["ANO_MES"], consumo_mensal["VALOR"], marker="o", color="#0897B4"
    )
    plt.title(f"Consumo Mensal de Portagens para a Matrícula {matricula}")
    plt.xlabel("Data")
    plt.ylabel("Consumo Total de Portagens (EUR)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return


def heatmap_custos(dados):

    datas = filtrar_datas()

    dados = custos.distribuicao_custos_dia_semana(dados, datas, "sum")

    pivot_data = dados.pivot_table(
        index="MATRICULA", columns="DIA_SEMANA", values="VALOR"
    )

    pivot_data = pivot_data.fillna(0)

    # Ordem dos dias da semana
    weekday_order = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo",
    ]

    # Reordenar as colunas por dia da semana
    pivot_data = pivot_data.reindex(columns=weekday_order)

    # heatmap de custos por dia da semana
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_data, annot=True, fmt="g", cmap="YlGnBu", linewidths=0.5)
    plt.title("Heatmap de Custo Totais por Dia da Semana")
    plt.xlabel("Dia da Semana")
    plt.ylabel("Matrícula")
    plt.show()
    return


def heatmap_custos_medios(dados):

    datas = filtrar_datas()

    dados = custos.distribuicao_custos_dia_semana(dados, datas, "mean")

    dados["VALOR"] = round(dados["VALOR"], 2)

    pivot_data = dados.pivot_table(
        index="MATRICULA", columns="DIA_SEMANA", values="VALOR"
    )

    pivot_data = pivot_data.fillna(0)

    # Ordem dos dias da semana
    weekday_order = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo",
    ]
    # Reordenar as colunas por dia da semana
    pivot_data = pivot_data.reindex(columns=weekday_order)

    # heatmap de custos por dia da semana
    plt.figure(figsize=(10, 8))
    sns.heatmap(pivot_data, annot=True, fmt="g", cmap="YlGnBu", linewidths=0.5)
    plt.title("Heatmap de Custo Médios por Dia da Semana")
    plt.xlabel("Dia da Semana")
    plt.ylabel("Matrícula")
    plt.show()
    return


def boxplot_custos(dados):

    matricula = escolha_matricula(dados)

    # Filtrar dados pela matrícula selecionada
    df_filtrado = dados[dados["MATRICULA"] == matricula]

    # Verificar se existem dados para a matrícula escolhida
    if df_filtrado.empty:
        print("Não há dados de custos para a matrícula selecionada.")
        return

    # Criar o boxplot
    plt.figure(figsize=(8, 6))
    sns.boxplot(x="VALOR", data=df_filtrado, color="#0897B4")
    plt.title(f"Boxplot de Custos para Matrícula: {matricula}")
    plt.xlabel("Custo (€)")
    plt.show()

    return


def evolucao_custos_itinerario(dados):

    # ecolher intinerario a avaliar
    itinerario = escolher_itinerario_(dados)

    # filtrar por itinerario
    dados = dados[dados["ITINERARIO_"] == itinerario]

    # agrupar média de custos por ano e mes
    df_agrupado = dados.groupby(["ANO", "MES"])["VALOR"].mean().reset_index()

    # nova coluna datetime baseado no ANO e MES
    df_agrupado["DATA"] = (
        df_agrupado["ANO"].astype(str) + "-" + df_agrupado["MES"].astype(str)
    )

    df_agrupado["DATA"] = df_agrupado["DATA"].astype("datetime64[ns]")

    # gráfico de linha com evolução da custo por ano e mes
    plt.figure(figsize=(12, 6))
    plt.plot(df_agrupado["DATA"], df_agrupado["VALOR"], marker="o")
    plt.title(f"Evolução do Custo do Itinerário: {itinerario}")
    plt.xlabel("Ano")
    plt.ylabel("Custo (€)")
    plt.grid(True)
    plt.show()

    return


if __name__ == "__main__":
    pass
