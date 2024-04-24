import os
import pandas as pd
from utils import agrupar_intenerarios


def file_paths():
    paths = []
    for root, dirs, files in os.walk("./extratos/"):
        for file in files:
            if file.endswith(".csv"):
                paths.append(os.path.join(root, file))

    return paths


def files_to_dataframe():

    df = pd.DataFrame()
    # ler ficheiros e juntar num único dataframe
    for path in file_paths():
        if df.empty:
            df = pd.read_csv(
                path, encoding="ISO-8859-1", sep=";", skiprows=7, decimal=","
            )
        else:
            df = pd.concat(
                [
                    df,
                    pd.read_csv(
                        path, encoding="ISO-8859-1", sep=";", skiprows=7, decimal=","
                    ),
                ]
            )

    df = df.drop_duplicates()

    # selecionar apenas as colunas desejadas
    df = df[
        [
            "IDENTIFICADOR",
            "MATRÍCULA",
            "DATA ENTRADA",
            "HORA ENTRADA",
            "ENTRADA",
            "DATA SAÍDA",
            "HORA SAÍDA",
            "SAÍDA",
            "VALOR",
            "VALOR DESCONTO",
            "TAXA IVA",
            "OPERADOR",
            "SERVIÇO",
        ]
    ]

    # renomear colunas
    df.columns = [
        "ID",
        "MATRICULA",
        "DATA_ENTRADA",
        "HORA_ENTRADA",
        "ENTRADA",
        "DATA_SAIDA",
        "HORA_SAIDA",
        "SAIDA",
        "VALOR",
        "VALOR_DES",
        "TAXA_IVA",
        "OPERADOR",
        "SERVICO",
    ]

    # formatar datas e hora para datetime
    df["ENTRADA_DATETIME"] = pd.to_datetime(
        df["DATA_ENTRADA"] + " " + df["HORA_ENTRADA"],
        format="%d-%m-%Y %H:%M",
    )
    df["SAIDA_DATETIME"] = pd.to_datetime(
        df["DATA_SAIDA"] + " " + df["HORA_SAIDA"], format="%d-%m-%Y %H:%M"
    )

    df["ENTRADA_DATETIME"] = df["ENTRADA_DATETIME"].fillna(df["SAIDA_DATETIME"])

    # converter operador e serviços para letra maiúscula
    df["OPERADOR"] = df["OPERADOR"].apply(lambda x: x.upper())
    df["SERVICO"] = df["SERVICO"].apply(lambda x: x.upper())

    # criar coluna de minutos, mes, ano, semana e dia da semana
    df["DURACAO_MINUTOS"] = (
        df["SAIDA_DATETIME"] - df["ENTRADA_DATETIME"]
    ).dt.seconds / 60
    df["DURACAO_MINUTOS"] = df["DURACAO_MINUTOS"].fillna(0)
    df["MES"] = df["SAIDA_DATETIME"].dt.month
    df["ANO"] = df["SAIDA_DATETIME"].dt.year
    df["SEMANA"] = df["SAIDA_DATETIME"].dt.isocalendar().week
    df["DIA_SEMANA"] = df["SAIDA_DATETIME"].dt.dayofweek

    # criar coluna Itinerário
    df[["ENTRADA", "SAIDA"]] = df[["ENTRADA", "SAIDA"]].fillna("N/D")
    df["ITINERARIO"] = df["ENTRADA"] + " - " + df["SAIDA"]
    df["ITINERARIO"] = df["ITINERARIO"].apply(lambda x: x.replace("N/D - ", "", 1))
    df["ITINERARIO"] = df["ITINERARIO"].apply(lambda x: x.upper())
    df["ITINERARIO_"] = df["ITINERARIO"].apply(agrupar_intenerarios)

    # definir tipo de dados
    df["ID"] = df["ID"].astype("int64")
    df["MATRICULA"] = df["MATRICULA"].astype(str)
    df["ENTRADA"] = df["ENTRADA"].astype(str)
    df["SAIDA"] = df["SAIDA"].astype(str)
    df["VALOR"] = df["VALOR"].astype(float)
    df["VALOR_DES"] = df["VALOR_DES"].astype(float)
    df["TAXA_IVA"] = df["TAXA_IVA"].astype(float)
    df["OPERADOR"] = df["OPERADOR"].astype(str)
    df["SERVICO"] = df["SERVICO"].astype(str)

    # filtrar linhas de portagens
    portagens = df[df["SERVICO"] == "PORTAGENS"]
    # filtar linhas de estacionamento
    estacionamento = df[df["SERVICO"].str.contains("ESTACIONAMENTO")]
    estacionamento["ITINERARIO"] = estacionamento["SAIDA"]
    estacionamento = estacionamento[estacionamento["MATRICULA"] != "Desconhecida"]

    # criar ficheiros de portagens e estacionamento
    portagens.to_csv("dados/portagens.csv", sep=";", decimal=",", index=False)
    estacionamento.to_csv("dados/estacionamento.csv", sep=";", decimal=",", index=False)


def check_if_file_exists(filename):
    if not os.path.exists(filename):
        files_to_dataframe()
    return


if __name__ == "__main__":
    import pandas as pd
