from dateutil.parser import *
import re
import time


def verificar_matricula(matricula, matriculas):
    if not matricula in matriculas.values:
        return False
    else:
        return True


def filtrar_datas():
    filtro = [False, False]
    startDate = input(
        "Insira a data inicial (dd/mm/aaaa) ou Enter para ver todos os registos desde o início: "
    )
    endDate = input(
        "Insira a data final (dd/mm/aaaa) ou Enter para ver até ao último registo: "
    )
    try:
        if startDate == "" and endDate == "":
            return filtro
        elif startDate == "" and endDate != "":
            filtro = [False, parse(endDate)]
        elif startDate != "" and endDate == "":
            filtro = [parse(startDate), False]
        else:
            filtro = [parse(startDate), parse(endDate)]
    except:
        print("\nFormato de data inválido. Serão devolvidos todos os dados.\n")
        time.sleep(1.5)
        filtro = [False, False]
    return filtro


# Comentar...
def escolha_matricula(df):

    # Solicitar ao utilizador que insira a matrícula desejada
    matriculas = df["MATRICULA"].unique()
    print("Matrículas disponíveis:\n")
    for idx, matricula in enumerate(matriculas, 1):
        print(f"{idx}. {matricula}")

    escolha = input(
        "\nDigite o número associado à matrícula que deseja visualizar o histograma da duração das viagens: "
    )
    try:
        escolha = int(escolha) - 1
        matricula_escolhida = matriculas[escolha]
    except:
        matricula_escolhida = escolha

    return matricula_escolhida


def escolher_frequencia():

    while True:

        print("\n")
        print("Escolha o tipo de frequência para os itinerários:\n")
        print("1 - Alta Frequência (4 ou mais passagens).")
        print("2 - Baixa Frequência (menos de 3 passagens).")
        print("3 - Frequência Personalizada (especifique o número de passagens).")

        opcao = input("\nDigite o número da opção desejada: ")

        if opcao == "1":
            return 4, ">="  # Retorna 4 para alta frequência.
        elif opcao == "2":
            return 4, "<"  # 3 ou menos para baixa frequência.
        elif opcao == "3":
            try:
                passagens = int(input("Digite o número de passagens: "))

                if passagens > 0 and passagens <= 99:
                    return passagens
                else:
                    print(
                        "Por favor, insira um número de passagens válido (maior que zero e menor que cem)."
                    )
            except ValueError:
                print("Por favor, insira um número inteiro válido.")
        else:
            print("Opção inválida. Tente novamente.")


# Comentar...
def escolher_itinerario(df, frequencia, sign):

    # Contar frequência dos itinerários
    frequencia_itinerarios = df["ITINERARIO"].value_counts()

    if sign == ">=":
        frequencia_itinerarios = frequencia_itinerarios[
            frequencia_itinerarios >= frequencia
        ]
    elif sign == "<":
        frequencia_itinerarios = frequencia_itinerarios[
            frequencia_itinerarios < frequencia
        ]

    if frequencia_itinerarios.empty:
        print(f"Não se registam itinerários que se repitam {frequencia} ou mais vezes.")
        return None

    # Listar itinerários para o usuário escolher
    print("Itinerários disponíveis:")
    for index, (itinerario, count) in enumerate(
        frequencia_itinerarios.items(), start=1
    ):
        print(f"{index}: {itinerario} (Ocorrências: {count})")

    # Solicitar ao usuário para escolher um itinerário
    escolha = input("Selecione o número do itinerário que deseja visualizar: ")
    try:
        escolha = int(escolha) - 1
        itinerario_escolhido = frequencia_itinerarios.index[escolha]
        return itinerario_escolhido

    except (ValueError, IndexError):
        print("Seleção inválida. Tente novamente.")
        return None


def escolher_itinerario_(df):

    itinerary_counts = df["ITINERARIO_"].value_counts()

    print("Itinerários disponíveis:")
    for i, (itinerary, count) in enumerate(itinerary_counts.items(), start=1):
        print(f"{i}: {itinerary} ({count})")

    selected_index = (
        int(input("Selecione o número do itinerário que deseja visualizar: ")) - 1
    )

    while selected_index < 0 or selected_index >= len(itinerary_counts):
        print("Seleção inválida. Tente novamente.")
        selected_index = (
            int(input("Selecione o número do itinerário que deseja visualizar: ")) - 1
        )

    selected_itinerary = itinerary_counts.index[selected_index]

    return selected_itinerary


def dados_matricula(dados):
    matricula = input("Insira a sua matricula: ").upper()
    filtro_datas = filtrar_datas()
    startDate = filtro_datas[0]
    endDate = filtro_datas[1]
    if filtro_datas[0] == False:
        startDate = dados["SAIDA_DATETIME"].min()
    if filtro_datas[1] == False:
        endDate = dados["SAIDA_DATETIME"].max()
    if verificar_matricula(matricula, dados["MATRICULA"]):
        return dados[
            (dados["MATRICULA"] == matricula)
            & (dados["SAIDA_DATETIME"] >= startDate)
            & (dados["SAIDA_DATETIME"] <= endDate)
        ]
    else:
        return False


def agrupar_intenerarios(ITINERARIO):

    list = ITINERARIO.split(" - ")

    sorted_list = sorted(list)

    ITINERARIO = " - ".join(sorted_list)

    ITINERARIO = re.sub(r"\b PV\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b N/S\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b S/N\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b NO\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b II\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b I\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b O S/N\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b NP\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b PN\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b O/E\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b E/O\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b ESTE\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b OESTE\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b POENTE\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b NASCENTE\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b NS\b", "", ITINERARIO)
    ITINERARIO = re.sub(r"\b SN\b", "", ITINERARIO)

    return ITINERARIO.strip()


dict_mes = {
    1: "JANEIRO",
    2: "FEVEREIRO",
    3: "MARCO",
    4: "ABRIL",
    5: "MAIO",
    6: "JUNHO",
    7: "JULHO",
    8: "AGOSTO",
    9: "SETEMBRO",
    10: "OUTUBRO",
    11: "NOVEMBRO",
    12: "DEZEMBRO",
}

dict_dia_semana = {
    0: "DOMINGO",
    1: "SEGUNDA",
    2: "TERCA",
    3: "QUARTA",
    4: "QUINTA",
    5: "SEXTA",
    6: "SABADO",
}
