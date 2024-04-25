import numpy as np
import pandas as pd
import datetime
from funcionalidades import viagens
from utils import dict_mes, escolha_matricula, filtrar_datas


def total_custos_anual(dados):

    ano = None
    erro = False

    try:
        ano = int(input("Insira o ano (YYYY): "))
        if ano > datetime.datetime.today().year:
            raise Exception("Ano inválido. Tente novamente.")
        dados = dados[dados["ANO"] == ano]
        dados = (
            dados.groupby("MATRICULA")
            .aggregate({"VALOR": "sum", "SERVICO": "count"})
            .reset_index()
            .sort_values(by="VALOR", ascending=False)
        )
        dados["VALOR MEDIO (€)"] = round(dados["VALOR"] / dados["SERVICO"], 2)

        dados.rename(
            columns={
                "VALOR": "VALOR (€)",
                "SERVICO": "Nº VIAGENS",
            },
            inplace=True,
        )
    except Exception as e:
        print(f"\n{e}")
        erro = True

    return dados, ano, erro


def total_custos_mensal(dados):

    ano = None
    erro = False

    try:
        ano = int(input("Insira o ano (YYYY): "))
        if ano > datetime.datetime.today().year:
            raise Exception("Ano inválido. Tente novamente.")
        dados = dados[dados["ANO"] == ano]
        dados = (
            dados.groupby(["MATRICULA", "MES"])
            .aggregate({"VALOR": "sum", "SERVICO": "count"})
            .reset_index()
            .sort_values(by=["MATRICULA", "MES"], ascending=True)
        )
        dados["VALOR MEDIO (€)"] = round(dados["VALOR"] / dados["SERVICO"], 2)

        dados.rename(
            columns={
                "VALOR": "VALOR (€)",
                "SERVICO": "Nº VIAGENS",
            },
            inplace=True,
        )
        dados["MES"] = dados["MES"].replace(dict_mes)

    except Exception as e:
        print(f"\n{e}")
        erro = True

    return dados, ano, erro


def total_custos_concessao_anual(dados):

    ano = None
    erro = False

    try:
        ano = int(input("Insira o ano (YYYY): "))
        if ano > datetime.datetime.today().year:
            raise Exception("Ano inválido. Tente novamente.")
        dados = dados[dados["ANO"] == ano]
        dados = (
            dados.groupby(["OPERADOR", "MATRICULA"])
            .aggregate({"VALOR": "sum", "SERVICO": "count"})
            .reset_index()
            .sort_values(by="VALOR", ascending=False)
        )
        dados["VALOR MEDIO (€)"] = round(dados["VALOR"] / dados["SERVICO"], 2)

        dados.rename(
            columns={
                "VALOR": "VALOR (€)",
                "SERVICO": "Nº VIAGENS",
            },
            inplace=True,
        )
    except:
        print("Ano inválido. Tente novamente.")

    return dados, ano, erro


def total_custos_concessao_mensal(dados):
    ano = None
    erro = False
    try:
        ano = int(input("Insira o ano (YYYY): "))
        if ano > datetime.datetime.today().year:
            raise Exception("Ano inválido. Tente novamente.")
        dados = dados[dados["ANO"] == ano]

        dados = (
            dados.groupby(["OPERADOR", "MES"])
            .aggregate({"VALOR": "sum", "SERVICO": "count"})
            .reset_index()
            .sort_values(by=["VALOR", "OPERADOR", "MES"], ascending=[False, True, True])
        )

        dados["VALOR MEDIO (€)"] = round(dados["VALOR"] / dados["SERVICO"], 2)

        dados.rename(
            columns={
                "VALOR": "VALOR (€)",
                "SERVICO": "Nº VIAGENS",
            },
            inplace=True,
        )

        dados["MES"] = dados["MES"].replace(dict_mes)
    except:

        print("Ano inválido. Tente novamente.")

    return dados, ano, erro


def total_custos_itinerario_anual(dados):
    ano = None
    erro = False
    try:
        ano = int(input("Insira o ano (YYYY): "))
        if ano > datetime.datetime.today().year:
            raise Exception("Ano inválido. Tente novamente.")

        dados = dados[dados["ANO"] == ano]

        dados = (
            dados.groupby(["ITINERARIO_", "MATRICULA"])
            .aggregate({"VALOR": "sum", "SERVICO": "count"})
            .reset_index()
            .sort_values(by=["VALOR"], ascending=[False])
        )

        dados["VALOR MEDIO (€)"] = round(dados["VALOR"] / dados["SERVICO"], 2)

        dados.rename(
            columns={
                "VALOR": "VALOR (€)",
                "SERVICO": "Nº VIAGENS",
            },
            inplace=True,
        )

    except:

        print("Ano inválido. Tente novamente.")

    return dados, ano, erro


def custos_mensais_por_matricula_e_periodo(data):

    matricula = escolha_matricula(data)
    date_range = filtrar_datas()

    # Filtrar registros dentro do intervalo de datas especificado
    if date_range[0]:
        data = data[data["ENTRADA_DATETIME"] >= date_range[0]]
    else:
        date_range[0] = data["ENTRADA_DATETIME"].min()
        data = data[data["ENTRADA_DATETIME"] >= date_range[0]]
    if date_range[1]:
        data = data[data["ENTRADA_DATETIME"] <= date_range[1]]
    else:
        date_range[1] = data["ENTRADA_DATETIME"].max()
        data = data[data["ENTRADA_DATETIME"] <= date_range[1]]

    data = data[data["MATRICULA"] == matricula]
    data = (
        data.groupby(["ANO", "MES"])
        .aggregate({"VALOR": "sum", "SERVICO": "count"})
        .reset_index()
    )

    data["VALOR MEDIO (€)"] = round(data["VALOR"] / data["SERVICO"], 2)

    data.rename(
        columns={
            "VALOR": "VALOR (€)",
            "SERVICO": "Nº VIAGENS",
        },
        inplace=True,
    )

    data["MES"] = data["MES"].replace(dict_mes)

    return data, matricula, date_range[0], date_range[1]


def estatisticas_de_custos_por_periodo(data):

    date_range = filtrar_datas()

    # Filtrar registros dentro do intervalo de datas especificado
    if date_range[0]:
        data = data[data["ENTRADA_DATETIME"] >= date_range[0]]
    else:
        date_range[0] = data["ENTRADA_DATETIME"].min()
        data = data[data["ENTRADA_DATETIME"] >= date_range[0]]
    if date_range[1]:
        data = data[data["ENTRADA_DATETIME"] <= date_range[1]]
    else:
        date_range[1] = data["ENTRADA_DATETIME"].max()
        data = data[data["ENTRADA_DATETIME"] <= date_range[1]]

    # Agrupar por matrícula
    data = data.groupby("MATRICULA")["VALOR"]

    # Calcular as estatísticas
    resultado = pd.DataFrame(
        {
            "Matrícula": [matricula for matricula, _ in data],
            "Mínimo": [float(np.min(g.to_numpy())) for _, g in data],
            "Máximo": [float(np.max(g.to_numpy())) for _, g in data],
            "Média": [float(round(np.mean(g.to_numpy()))) for _, g in data],
            "Mediana": [float(round(np.median(g.to_numpy()))) for _, g in data],
            "Moda": [
                float(g.mode()[0]) if not g.mode().empty else np.nan for _, g in data
            ],
            "Desvio_Padrão": [float(round(np.std(g.to_numpy()))) for _, g in data],
            "IQR": [
                float(
                    round(
                        np.percentile(g.to_numpy(), 75)
                        - np.percentile(g.to_numpy(), 25)
                    )
                )
                for _, g in data
            ],
            "Tipo de Distribuição": [
                viagens.identificar_distribuicao(g.to_numpy()) for _, g in data
            ],
        }
    )

    return resultado, date_range[0], date_range[1]


def distribuicao_custos_dia_semana(df, date_filter, method):

    df["ENTRADA_DATETIME"] = pd.to_datetime(df["ENTRADA_DATETIME"], errors="coerce")

    # Aplicar filtro de datas ao DataFrame
    current_year = datetime.datetime.today().year
    if date_filter == [False, False]:
        start_of_year = pd.Timestamp(year=current_year, month=1, day=1)
        end_of_year = pd.Timestamp(year=current_year, month=12, day=31)
        df = df[
            (df["ENTRADA_DATETIME"] >= start_of_year)
            & (df["ENTRADA_DATETIME"] <= end_of_year)
        ]
    else:
        if date_filter[0]:
            df = df[df["ENTRADA_DATETIME"] >= date_filter[0]]
        if date_filter[1]:
            df = df[df["ENTRADA_DATETIME"] <= date_filter[1]]

    # Extrair o dia da semana e adicionar como nova coluna com o nome dinâmico
    df["DIA_SEMANA"] = df["ENTRADA_DATETIME"].dt.weekday

    # Traduzir para português
    days_translation = {
        0: "Segunda-feira",
        1: "Terça-feira",
        2: "Quarta-feira",
        3: "Quinta-feira",
        4: "Sexta-feira",
        5: "Sábado",
        6: "Domingo",
    }

    # Contar quantas viagens ocorrem em cada dia da semana para cada matrícula
    custos_por_matricula = df.groupby(["MATRICULA", "DIA_SEMANA"])["VALOR"].agg(method)

    custos_por_matricula = custos_por_matricula.reset_index()

    custos_por_matricula = custos_por_matricula.sort_values(
        by=["MATRICULA", "DIA_SEMANA"]
    )

    custos_por_matricula = custos_por_matricula.replace(
        {"DIA_SEMANA": days_translation}
    )

    return custos_por_matricula


if __name__ == "__main__":

    pass
