import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from utils import escolha_matricula


# Comentar...
def rede_itinerarios(df, date_range):

    # Converter colunas de data para o tipo apropriado
    df["ENTRADA_DATETIME"] = pd.to_datetime(df["ENTRADA_DATETIME"])

    # Aplicar o filtro de datas ao DataFrame
    if date_range[0]:
        df = df[df["ENTRADA_DATETIME"] >= date_range[0]]
    if date_range[1]:
        df = df[df["ENTRADA_DATETIME"] <= date_range[1]]

    matricula = escolha_matricula(df)

    # Filtrar dados pela matrícula selecionada
    df_filtrado = df[df["MATRICULA"] == matricula]

    # Verificar se existem dados para a matrícula escolhida
    if df_filtrado.empty:
        print("Não há dados de consumo para a matrícula selecionada.")
        return

    # Continua a processar apenas os dados filtrados
    df_filtrado = df_filtrado[df_filtrado["SERVICO"] == "PORTAGENS"].drop_duplicates(
        subset=["ENTRADA", "SAIDA"]
    )

    # Criar o grafo
    G = nx.DiGraph()
    for _, row in df_filtrado.iterrows():
        G.add_edge(row["ENTRADA"], row["SAIDA"])

    # Desenhar o grafo
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(
        G, seed=42
    )  # Posicionamento dos nós com seed fixo para consistência
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="skyblue",
        node_size=7000,
        edge_color="k",
        linewidths=1,
        font_size=15,
        arrows=True,
        arrowsize=20,
    )
    plt.title("Rede de Itinerários de Portagens")
    plt.show()
    return


# Comentar...
def heatmap_distribuicao(df):
    # Preparar os dados para o heatmap
    # Assumindo que 'df' já tem índices corretos e colunas dos dias da semana corretas
    heatmap_data = df.set_index("MATRICULA")

    # Excluir a coluna de 'Total de Passagens' se presente para visualização apenas dos dias
    if "Total de Passagens" in heatmap_data.columns:
        heatmap_data = heatmap_data.drop("Total de Passagens", axis=1)

    print(heatmap_data)

    # Criar o heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlGnBu", linewidths=0.5)
    plt.title("Heatmap de Distribuição de Viagens por Dia da Semana")
    plt.xlabel("Dia da Semana")
    plt.ylabel("Matrícula")
    plt.show()
    return


# Comentar...
def histograma_duracao_viagens(df, date_range):

    # Converter colunas de data para o tipo apropriado
    df["ENTRADA_DATETIME"] = pd.to_datetime(df["ENTRADA_DATETIME"])

    # Aplicar o filtro de datas ao DataFrame
    if date_range[0]:
        df = df[df["ENTRADA_DATETIME"] >= date_range[0]]
    if date_range[1]:
        df = df[df["ENTRADA_DATETIME"] <= date_range[1]]

    matricula = escolha_matricula(df)

    # Filtrar o DataFrame pela matrícula selecionada
    df_filtrado = df[df["MATRICULA"] == matricula]

    # Verificar se existem dados após o filtro
    if df_filtrado.empty:
        print("Não há dados para a matrícula escolhida.")
        return

    # Ordenando o DataFrame df_filtrado por 'DURACAO_MINUTOS' em ordem crescente
    df_filtrado = df_filtrado.sort_values(by="DURACAO_MINUTOS", ascending=True)

    # Calcular o número de bins usando a Regra de Sturges
    num_bins = int(1 + 3.322 * np.log10(len(df_filtrado["DURACAO_MINUTOS"])))

    # Plotar o histograma das durações das viagens para a matrícula especificada
    plt.figure(figsize=(12, 6))
    sns.histplot(
        df_filtrado["DURACAO_MINUTOS"], bins=num_bins, kde=True, color="#0897B4"
    )
    plt.title(f"Histograma de Duração das Viagens para a Matrícula {matricula}")
    plt.xlabel("Duração em Minutos")
    plt.ylabel("Frequência")
    plt.grid(True)
    plt.tight_layout()  # Ajusta o layout para evitar sobreposição de etiquetas
    plt.show()
    return


# Comentar...
def linha_tempo_itinerario(df, itinerario):

    # Filtrar o DataFrame pelo itinerário selecionado
    df_filtrado_itinerario = df[df["ITINERARIO"] == itinerario]

    # Verificar se existem dados para o itinerário escolhido
    if df_filtrado_itinerario.empty:
        print("Não há dados para o itinerário escolhido.")
        return

    matricula = escolha_matricula(df_filtrado_itinerario)

    # Filtrar dados pela matrícula selecionada
    df_filtrado = df_filtrado_itinerario[
        df_filtrado_itinerario["MATRICULA"] == matricula
    ]

    # Verificar se existem dados para a matrícula escolhida
    if df_filtrado.empty:
        print("\nNão há dados para a matrícula selecionada.")
        return

    # Converter 'DATA_ENTRADA' para datetime se ainda não for
    if not pd.api.types.is_datetime64_any_dtype(df_filtrado["ENTRADA_DATETIME"]):
        df_filtrado["ENTRADA_DATETIME"] = pd.to_datetime(
            df_filtrado["ENTRADA_DATETIME"]
        )

    # Agrupar por data e calcular média da duração
    duracao_media_por_data = (
        df_filtrado.groupby("ENTRADA_DATETIME")["DURACAO_MINUTOS"].mean().reset_index()
    )

    # Verificar se existem dados
    if duracao_media_por_data.empty:
        print("\nNão existem dados suficientes para gerar um gráfico.")
        return

    # Plotar o gráfico de linha
    plt.figure(figsize=(14, 7))
    sns.lineplot(
        data=duracao_media_por_data,
        x="ENTRADA_DATETIME",
        y="DURACAO_MINUTOS",
        marker="o",
    )
    plt.title(
        f"Variação da duração das viagens ao longo do tempo para o Itinerário {itinerario} ({matricula})"
    )
    plt.xlabel("Datas")
    plt.ylabel("Duração média das viagens (minutos)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()  # Ajusta o layout para evitar sobreposição de etiquetas
    plt.show()
    return


# Comentar...
def viagens_por_mes_vv(df):

    matricula = escolha_matricula(df)

    # Filtrar dados pela matrícula selecionada
    df_filtrado = df[df["MATRICULA"] == matricula]

    # Verificar se existem dados para a matrícula escolhida
    if df_filtrado.empty:
        print("Não há dados para a matrícula selecionada.")
        return

    # Garantir que 'ENTRADA_DATETIME' está no formato datetime.
    if not pd.api.types.is_datetime64_any_dtype(df_filtrado["ENTRADA_DATETIME"]):
        df_filtrado["ENTRADA_DATETIME"] = pd.to_datetime(
            df_filtrado["ENTRADA_DATETIME"]
        )

    # Extrair o mês e o ano da data de entrada para facilitar agrupamento e visualização
    df_filtrado["MES"] = df_filtrado["ENTRADA_DATETIME"].dt.month
    df_filtrado["ANO"] = df_filtrado["ENTRADA_DATETIME"].dt.year

    # Agrupar por ano e mês
    viagens_por_mes = (
        df_filtrado.groupby(["ANO", "MES"]).size().reset_index(name="NUMERO_DE_VIAGENS")
    )

    # Converter 'ANO' e 'MES' para uma coluna de string que representará o período
    viagens_por_mes["PERIODO"] = (
        viagens_por_mes["ANO"].astype(int).astype(str)
        + " - "
        + viagens_por_mes["MES"].astype(int).apply(lambda x: f"{x:02}")
    )

    # Plotar o gráfico de barras
    plt.figure(figsize=(14, 7))
    sns.barplot(
        data=viagens_por_mes, x="PERIODO", y="NUMERO_DE_VIAGENS", color="#4CABA6"
    )
    plt.title(f"Percursos portajados por Mês (Matrícula: {matricula})")
    plt.xlabel("Ano - Mês")
    plt.ylabel("Número de Viagens")
    plt.xticks(rotation=45)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    pass
