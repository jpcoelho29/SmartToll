import os
import pandas as pd
import numpy as np
from utils import dados_matricula, dict_mes

pd.set_option("display.max_rows", 150)


def total_gastos_portagens(portagens, group=["ANO", "MES"]):

    portagens_matricula = dados_matricula(portagens)

    portagens_matricula = (
        portagens_matricula.sort_values(
            by=group,
            ascending=[False if x == group[0] else True for x in group],
        )
        .groupby(group, sort=False)
        .aggregate({"VALOR": "sum", "SERVICO": "count"})
    )
    portagens_matricula["VALOR MÉDIO"] = round(
        portagens_matricula["VALOR"] / portagens_matricula["SERVICO"], 2
    )

    portagens_matricula.rename(
        columns={
            "VALOR": "VALOR (€)",
            "SERVICO": "Nº VIAGENS",
        },
        inplace=True,
    )

    portagens_matricula.reset_index(inplace=True)

    portagens_matricula["MES"] = portagens_matricula["MES"].replace(dict_mes)

    return portagens_matricula


def total_gastos_portagens_concessao(portagens):

    group = ["ANO", "OPERADOR"]

    portagens_matricula = dados_matricula(portagens)

    portagens_matricula = (
        portagens_matricula.sort_values(
            by=group[:-1],
            ascending=[False if x == group[0] else True for x in group[:-1]],
        )
        .groupby(group, sort=False)
        .aggregate({"VALOR": "sum", "SERVICO": "count"})
    )

    portagens_matricula["VALOR MEDIO"] = round(
        portagens_matricula["VALOR"] / portagens_matricula["SERVICO"], 2
    )

    portagens_matricula.rename(
        columns={
            "VALOR": "VALOR (€)",
            "SERVICO": "Nº VIAGENS",
        },
        inplace=True,
    )

    return portagens_matricula.reset_index()


def gastos_por_ITINERARIO(portagens):

    portagens_matricula = dados_matricula(portagens)

    portagens_matricula = portagens_matricula.groupby(
        ["ITINERARIO"], sort=False
    ).aggregate({"VALOR": "sum", "SERVICO": "count"})

    portagens_matricula.rename(
        columns={
            "VALOR": "VALOR (€)",
            "SERVICO": "Nº VIAGENS",
        },
        inplace=True,
    )

    portagens_matricula = (
        portagens_matricula.reset_index()
        .sort_values(by="VALOR (€)", ascending=False)
        .set_index("ITINERARIO")
    )

    return portagens_matricula.reset_index()


if __name__ == "__main__":

    pass
