import datetime as dt


def estacionamento_anual(dados):

    ano = None
    erro = False

    try:
        ano = int(input("Insira o ano (YYYY): "))
        if ano > dt.datetime.today().year:
            raise Exception("Ano inválido. Tente novamente.")
        dados = dados[dados["ANO"] == ano]
        dados = (
            dados.groupby("MATRICULA")
            .aggregate({"VALOR": "sum", "DURACAO_MINUTOS": "sum", "SERVICO": "count"})
            .reset_index()
            .sort_values(by="VALOR", ascending=False)
        )
        dados["VALOR MEDIO (€)"] = round(dados["VALOR"] / dados["SERVICO"], 2)
        dados["VALOR MEDIO (hora)"] = round(
            dados["VALOR"] / (dados["DURACAO_MINUTOS"] / 60), 2
        )

        dados.rename(
            columns={
                "VALOR": "VALOR (€)",
                "SERVICO": "Nº ESTACIONAMENTOS",
            },
            inplace=True,
        )
    except Exception as e:
        print(f"\n{e}")
        erro = True

    return dados, ano, erro


def estacionamento_anual_local(dados):

    ano = None
    erro = False

    try:
        ano = int(input("Insira o ano (YYYY): "))
        if ano > dt.datetime.today().year:
            raise Exception("Ano inválido. Tente novamente.")
        dados = dados[dados["ANO"] == ano]
        dados = (
            dados.groupby(["MATRICULA", "ITINERARIO"])
            .aggregate({"VALOR": "sum", "DURACAO_MINUTOS": "sum", "SERVICO": "count"})
            .reset_index()
            .sort_values(by="VALOR", ascending=False)
        )
        dados["VALOR MEDIO (€)"] = round(dados["VALOR"] / dados["SERVICO"], 2)
        dados["VALOR MEDIO (hora)"] = round(
            dados["VALOR"] / (dados["DURACAO_MINUTOS"] / 60), 2
        )

        dados.rename(
            columns={
                "VALOR": "VALOR (€)",
                "SERVICO": "Nº ESTACIONAMENTOS",
            },
            inplace=True,
        )
    except Exception as e:
        print(f"\n{e}")
        erro = True

    return dados, ano, erro


def estacionamento_anual_operador(dados):

    ano = None
    erro = False

    try:
        ano = int(input("Insira o ano (YYYY): "))
        if ano > dt.datetime.today().year:
            raise Exception("Ano inválido. Tente novamente.")
        dados = dados[dados["ANO"] == ano]
        dados = (
            dados.groupby(["OPERADOR"])
            .aggregate({"VALOR": "sum", "DURACAO_MINUTOS": "sum", "SERVICO": "count"})
            .reset_index()
            .sort_values(by="VALOR", ascending=False)
        )
        dados["VALOR MEDIO (€)"] = round(dados["VALOR"] / dados["SERVICO"], 2)
        dados["VALOR MEDIO (hora)"] = round(
            dados["VALOR"] / (dados["DURACAO_MINUTOS"] / 60), 2
        )

        dados.rename(
            columns={
                "VALOR": "VALOR (€)",
                "SERVICO": "Nº ESTACIONAMENTOS",
            },
            inplace=True,
        )
    except Exception as e:
        print(f"\n{e}")
        erro = True

    return dados, ano, erro


if __name__ == "__main__":
    pass
