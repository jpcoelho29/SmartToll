import pandas as pd
import numpy as np
import scipy.stats as stats
import warnings

from datetime import datetime

warnings.filterwarnings("ignore", category=UserWarning, module="scipy")


def rotas(data, frequencia, date_range):

    # Converter colunas de data para o tipo apropriado
    data["ENTRADA_DATETIME"] = pd.to_datetime(data["ENTRADA_DATETIME"])

    # Filtrar registros dentro do intervalo de datas especificado
    if date_range[0]:
        data = data[data["ENTRADA_DATETIME"] >= date_range[0]]
    if date_range[1]:
        data = data[data["ENTRADA_DATETIME"] <= date_range[1]]

    # Contar frequência dos percursos agrupados por 'MATRICULA', 'ENTRADA' e 'SAIDA'
    passagens = (
        data.groupby(["MATRICULA", "ENTRADA", "SAIDA"])
        .size()
        .reset_index(name="NUM PASSAGENS")
    )

    # Filtrar percursos conforme a frequência
    if frequencia == True:
        passagens = passagens[passagens["NUM PASSAGENS"] >= 4]
    else:
        passagens = passagens[passagens["NUM PASSAGENS"] < 4]

    # Ordenar os resultados por frequência em ordem decrescente
    passagens = passagens.sort_values(by="NUM PASSAGENS", ascending=False)

    return passagens


# Função para determinar percursos dentro de um intervalo de datas
def percursos_por_intervalo(df, date_range):

    # Converter colunas de data para o tipo apropriado
    df["ENTRADA_DATETIME"] = pd.to_datetime(df["ENTRADA_DATETIME"], errors="coerce")

    # Determinar o ano atual para cobrir todo o ano se necessário
    current_year = datetime.now().year
    if date_range == [False, False]:
        start_of_year = pd.Timestamp(year=current_year, month=1, day=1)
        end_of_year = pd.Timestamp(year=current_year, month=12, day=31)
        df = df[
            (df["ENTRADA_DATETIME"] >= start_of_year)
            & (df["ENTRADA_DATETIME"] <= end_of_year)
        ]
    else:
        if date_range[0]:
            df = df[df["ENTRADA_DATETIME"] >= date_range[0]]
        if date_range[1]:
            df = df[df["ENTRADA_DATETIME"] <= date_range[1]]

    # Filtrar viagens que são especificamente de portagens
    percursos_filtrados = df[df["SERVICO"] == "PORTAGENS"]

    # Renomear coluna 'ENTRADA_DATETIME' para 'DATA'
    percursos_filtrados["DATA"] = percursos_filtrados["ENTRADA_DATETIME"].dt.date

    # Selecionar colunas desejadas
    percursos_filtrados = percursos_filtrados[
        ["DATA", "MATRICULA", "ENTRADA", "SAIDA", "DURACAO_MINUTOS"]
    ]

    # Limpar e converter 'DURACAO_MINUTOS' para inteiros, lidando com valores NA
    percursos_filtrados["DURACAO_MINUTOS"] = (
        percursos_filtrados["DURACAO_MINUTOS"]
        .fillna(0)
        .replace(",", ".", regex=True)
        .astype(float)
        .round()
        .astype(int)
    )

    # Ordenar os resultados por ordem crescente de 'DATA'
    percursos_filtrados = percursos_filtrados.sort_values(by="DATA")

    return percursos_filtrados


def consumo_portagens_por_matricula(df, data_range):

    df["ENTRADA_DATETIME"] = pd.to_datetime(df["ENTRADA_DATETIME"], errors="coerce")

    # Aplicar o filtro de datas
    # Determinar o ano atual para cobrir todo o ano se necessário
    current_year = datetime.now().year
    if data_range == [False, False]:
        start_of_year = pd.Timestamp(year=current_year, month=1, day=1)
        end_of_year = pd.Timestamp(year=current_year, month=12, day=31)
        df = df[
            (df["ENTRADA_DATETIME"] >= start_of_year)
            & (df["ENTRADA_DATETIME"] <= end_of_year)
        ]
    else:
        if data_range[0]:
            df = df[df["ENTRADA_DATETIME"] >= data_range[0]]
        if data_range[1]:
            df = df[df["ENTRADA_DATETIME"] <= data_range[1]]

    # Converter valores de portagens para float, limpando possíveis erros de formatação
    df["VALOR"] = df["VALOR"].replace(",", ".", regex=True).astype(float)

    # Extrair ano e mês para agrupamento
    df["ANO"] = df["ENTRADA_DATETIME"].dt.year
    df["MES"] = df["ENTRADA_DATETIME"].dt.month

    # Agrupar dados por matrícula, ano e mês e calcular o total de portagens
    consumo_mensal = (
        df.groupby(["MATRICULA", "ANO", "MES"])["VALOR"].sum().reset_index()
    )
    consumo_mensal.columns = [
        "MATRICULA",
        "ANO",
        "MES",
        "CONSUMO MENSAL DE PORTAGENS (EUR)",
    ]

    # Calcular o consumo total anual por matrícula
    consumo_anual = df.groupby(["MATRICULA", "ANO"])["VALOR"].sum().reset_index()
    consumo_anual.columns = ["MATRICULA", "ANO", "CONSUMO ANUAL DE PORTAGENS (EUR)"]

    return consumo_mensal, consumo_anual


def distribuicao_viagens_dia_semana(df, date_filter):

    df["ENTRADA_DATETIME"] = pd.to_datetime(df["ENTRADA_DATETIME"], errors="coerce")

    # Aplicar filtro de datas ao DataFrame
    current_year = datetime.now().year
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

    # Extração e formatação da semana para nome de coluna
    df["SEMANA"] = df["ENTRADA_DATETIME"].dt.strftime("%U")
    nome_coluna_semana = f"Semana {df['SEMANA'].iloc[0]}"

    # Extrair o dia da semana e adicionar como nova coluna com o nome dinâmico
    df[nome_coluna_semana] = df["ENTRADA_DATETIME"].dt.day_name()

    # Traduzir para português
    days_translation = {
        "Monday": "Segunda-feira",
        "Tuesday": "Terça-feira",
        "Wednesday": "Quarta-feira",
        "Thursday": "Quinta-feira",
        "Friday": "Sexta-feira",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }
    df[nome_coluna_semana] = df[nome_coluna_semana].replace(days_translation)

    # Contar quantas viagens ocorrem em cada dia da semana para cada matrícula
    distribuicao_por_matricula = (
        df.groupby(["MATRICULA", nome_coluna_semana]).size().unstack(fill_value=0)
    )

    # Ordenar os resultados por dia da semana
    order = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo",
    ]
    distribuicao_por_matricula = distribuicao_por_matricula.reindex(
        columns=order, fill_value=0
    )

    # Adicionar uma coluna com o total de passagens por matrícula ao longo da semana
    distribuicao_por_matricula["Total de Passagens"] = distribuicao_por_matricula.sum(
        axis=1
    )

    # Fazer reset ao índice para tornar 'MATRICULA' uma coluna
    distribuicao_por_matricula.reset_index(inplace=True)

    return distribuicao_por_matricula


def horas_de_pico(df, date_filter):

    # Assegurar que 'ENTRADA_DATETIME' e 'SAIDA_DATETIME' estão no formato datetime
    df["ENTRADA_DATETIME"] = pd.to_datetime(df["ENTRADA_DATETIME"], errors="coerce")
    df["SAIDA_DATETIME"] = pd.to_datetime(df["SAIDA_DATETIME"], errors="coerce")

    # Aplicar filtro de datas ao DataFrame
    current_year = datetime.now().year
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

    # Criar colunas para hora de entrada e saída formatadas
    # df['HORA_ENTRADA'] = pd.to_datetime(df['ENTRADA_DATETIME'], format='%H:%M')
    df["HORA_ENTRADA"] = df["ENTRADA_DATETIME"].dt.strftime("%H:%M")
    df["HORA_SAIDA"] = df["SAIDA_DATETIME"].dt.strftime("%H:%M")

    # Criar colunas para hora de entrada formatada como hora inteira
    df["HORA_ENTRADA"] = df["ENTRADA_DATETIME"].dt.hour  # Aqui é apenas a hora
    df["HORA_SAIDA"] = df["SAIDA_DATETIME"].dt.hour  # Aqui é apenas a hora

    # Criar coluna para itinerário
    df["ITINERARIO"] = df["ENTRADA"] + " - " + df["SAIDA"]

    periodo_pico = (
        df.groupby(["MATRICULA", "ITINERARIO", "HORA_ENTRADA", "HORA_SAIDA"])
        .size()
        .reset_index(name="FREQUENCIA")
    )

    # Filtrar apenas itinerários com uma frequência superior a 2
    periodo_pico = periodo_pico[periodo_pico["FREQUENCIA"] > 2]

    # Reorganizar colunas para colocar 'FREQUENCIA' como última coluna
    periodo_pico = periodo_pico[
        ["MATRICULA", "ITINERARIO", "HORA_ENTRADA", "HORA_SAIDA", "FREQUENCIA"]
    ]

    return periodo_pico


# Comentar...
def identificar_distribuicao(dados):

    # Testar várias distribuições e retornar a que tiver o maior p-valor
    resultados = {}
    resultados["Normal"] = stats.normaltest(dados).pvalue if len(dados) > 8 else 0
    resultados["Logarítmica"] = (
        stats.normaltest(np.log(dados[dados > 0])).pvalue
        if np.all(dados > 0) and len(dados) > 8
        else 0
    )
    resultados["Exponencial"] = stats.kstest(
        dados, "expon", args=(np.min(dados), np.mean(dados))
    ).pvalue
    resultados["Uniforme"] = stats.kstest(
        dados, "uniform", args=(np.min(dados), np.max(dados) - np.min(dados))
    ).pvalue

    melhor_ajuste = max(resultados, key=resultados.get)

    return melhor_ajuste


def estatisticas_duracao_viagens(df, date_filter):

    # Assegurar que 'ENTRADA_DATETIME' está no formato datetime
    df["ENTRADA_DATETIME"] = pd.to_datetime(df["ENTRADA_DATETIME"], errors="coerce")

    # Aplicar filtro de datas ao DataFrame
    current_year = datetime.now().year
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

    # Corrigir valores numéricos que podem estar como strings com vírgulas
    df["DURACAO_MINUTOS"] = (
        df["DURACAO_MINUTOS"].replace(",", ".", regex=True).astype(float)
    )

    # Agrupar por matrícula
    grupo = df.groupby("MATRICULA")["DURACAO_MINUTOS"]

    # Calcular as estatísticas
    resultado = pd.DataFrame(
        {
            "Matrícula": [matricula for matricula, _ in grupo],
            "Mínimo": [int(np.min(g.to_numpy())) for _, g in grupo],
            "Máximo": [int(np.max(g.to_numpy())) for _, g in grupo],
            "Média": [int(round(np.mean(g.to_numpy()))) for _, g in grupo],
            "Mediana": [int(round(np.median(g.to_numpy()))) for _, g in grupo],
            "Moda": [
                int(g.mode()[0]) if not g.mode().empty else np.nan for _, g in grupo
            ],
            "Desvio_Padrão": [int(round(np.std(g.to_numpy()))) for _, g in grupo],
            "IQR": [
                int(
                    round(
                        np.percentile(g.to_numpy(), 75)
                        - np.percentile(g.to_numpy(), 25)
                    )
                )
                for _, g in grupo
            ],
            "Tipo de Distribuição": [
                identificar_distribuicao(g.to_numpy()) for _, g in grupo
            ],
        }
    )

    return resultado


if __name__ == "__main__":
    pass
