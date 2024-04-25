import os
import pandas as pd
import numpy as np
import viagens
import estacionamento
import custos
import graficos_viagens
import graficos_custos
import graficos_estacionamento
import menu
from time import sleep
from utils import (
    filtrar_datas,
    escolher_frequencia,
    escolher_itinerario,
)
from dataframes import check_if_file_exists, files_to_dataframe
import warnings

pd.options.mode.copy_on_write = True
warnings.filterwarnings("ignore")


def dados_portagens():

    file_path = "dados/portagens.csv"
    data_portagens = pd.read_csv(file_path, delimiter=";", decimal=",")

    return data_portagens


def main():

    # criar pastas dados e extratos caso nao existam
    if os.path.exists("dados") is False:
        print("Criando pasta 'extratos'...")
        os.mkdir("dados")
    if os.path.exists("extratos") is False:
        print("Criando pasta 'extratos'...")
        os.mkdir("extratos")

    # check if exists any .csv file in the folder "extratos"
    if len([name for name in os.listdir("extratos") if name.endswith(".csv")]) == 0:
        print(
            '\n❗❗ Adicionar ficheiros de extratos "Via Verde" em formato .csv à pasta "extratos ❗❗"\n'
        )
        print("A aplicação será encerrada!")
        sleep(2)
        return

    # carregar ficheiros
    check_if_file_exists("dados/portagens.csv")
    check_if_file_exists("dados/estacionamento.csv")

    portagens_df = pd.read_csv(
        "dados/portagens.csv",
        sep=";",
        decimal=",",
        parse_dates=["ENTRADA_DATETIME", "SAIDA_DATETIME"],
    )
    estacionamentos_df = pd.read_csv(
        "dados/estacionamento.csv",
        sep=";",
        decimal=",",
        parse_dates=["ENTRADA_DATETIME", "SAIDA_DATETIME"],
    )

    loadMenu = True

    while True:

        if loadMenu:
            menu.title()
        loadMenu = True

        menu.menu()

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":

            menu_viagens(portagens_df)

        elif escolha == "2":

            menu_custos(portagens_df)

        elif escolha == "3":

            menu_estacionamentos(estacionamentos_df)

        elif escolha == "4":

            menu_graficos(portagens_df, estacionamentos_df)

        elif escolha == "5":

            print("\nA ATUALIZAR DADOS", end="")

            files_to_dataframe()
            portagens_df = pd.read_csv(
                "dados/portagens.csv",
                sep=";",
                decimal=",",
                parse_dates=["ENTRADA_DATETIME", "SAIDA_DATETIME"],
            )
            estacionamentos_df = pd.read_csv(
                "dados/estacionamento.csv",
                sep=";",
                decimal=",",
                parse_dates=["ENTRADA_DATETIME", "SAIDA_DATETIME"],
            )
            for i in range(10):
                sleep(0.15)
                print(".", end="", flush=True)
            print("✅")
            sleep(0.5)
            loadMenu = False

        elif escolha.upper() == "X":

            # Caso o utilizador escolha esta opção, a aplicação irá encerrar.
            print("\nA sair da aplicação Smart Toll")
            print("Desejamos uma Boa Viagem!\n")
            break

        else:
            # Opção inválida introduzida pelo utilizador.
            print("\nOpção inválida. Por favor, escolha novamente uma opção!")


def menu_custos(dados):
    while True:

        menu.submenu_custos()

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":

            resultado, ano, erro = custos.total_custos_anual(dados)
            if erro:
                continue
            if resultado.empty:
                print("\nSem dados para mostrar!")
                continue
            print("\n")
            print(f"========== CUSTO ANUAL DE PORTAGENS EM {ano} ==========\n")
            print(resultado.to_string(index=False))

        elif escolha == "2":

            resultado, ano, erro = custos.total_custos_mensal(dados)
            if erro:
                continue
            if resultado.empty:
                print("\nSem dados para mostrar!")
                continue
            print("\n")
            print(f"========== CUSTO MENSAL DE PORTAGENS EM {ano} ==========\n")
            print(resultado.to_string(index=False))

        elif escolha == "3":

            resultado, ano, erro = custos.total_custos_concessao_anual(dados)
            if erro:
                continue
            if resultado.empty:
                print("\nSem dados para mostrar!")
                continue
            print("\n")
            print(f"========== CUSTO ANUAL POR CONCESSÃO EM {ano} ==========\n")
            print(resultado.to_string(index=False))

        elif escolha == "4":

            resultado, ano, erro = custos.total_custos_concessao_mensal(dados)
            if erro:
                continue
            if resultado.empty:
                print("\nSem dados para mostrar!")
                continue
            print("\n")
            print(f"========== CUSTO MENSAL POR CONCESSÃO EM {ano} ==========\n")
            print(resultado.to_string(index=False))

        elif escolha == "5":

            resultado, ano, erro = custos.total_custos_itinerario_anual(dados)
            if erro:
                continue
            if resultado.empty:
                print("\nSem dados para mostrar!")
                continue
            print("\n")
            print(f"========== CUSTO ANUAL POR Itinerário EM {ano} ==========\n")
            print(resultado.to_string(index=False))

        elif escolha == "6":

            resultado, matricula, data_inicial, data_final = (
                custos.custos_mensais_por_matricula_e_periodo(dados)
            )

            if resultado.empty:
                print("\nSem dados para mostrar!")
                continue

            print("\n")
            print(f"========== CUSTO MENSAL MATRICULA: {matricula} ==========")
            print(f"\nDe {data_inicial.date()} a {data_final.date()}\n")
            print(resultado.to_string(index=False))

        elif escolha == "7":

            resultado, data_inicial, data_final = (
                custos.estatisticas_de_custos_por_periodo(dados)
            )

            if resultado.empty:
                print("\nSem dados para mostrar!")
                continue

            print("\n")
            print(f"========== ESTATÍSTICAS DE CUSTOS ==========")
            print(f"\nDe {data_inicial.date()} a {data_final.date()}\n")
            print(resultado.to_string(index=False))

        elif escolha.upper() == "X":

            break

        else:
            # Opção inválida introduzida pelo utilizador.
            print("\nOpção inválida. Por favor, escolha novamente uma opção!")
            continue


def menu_viagens(dados):

    while True:

        menu.submenu_viagens()

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":

            # Percursos realizados pelos veículos da frota automóvel num determinado intervalo de tempo.
            # FEITO
            date_range = filtrar_datas()
            resultado = viagens.percursos_por_intervalo(dados, date_range)
            print("\n")
            print(resultado.to_string(index=False))

        elif escolha == "2":
            # Identificação dos percursos frequentes, com uma frequência de passagens Via Verde superior ou igual a quatro.
            # FEITO
            rota_frequente = True
            date_range = filtrar_datas()
            resultado = viagens.rotas(dados, rota_frequente, date_range=date_range)
            print("\n")
            print(resultado.to_string(index=False))

        elif escolha == "3":

            # Identificação dos percursos esporádicos, com uma frequência de passagens Via Verde igual a um.
            # FEITO
            rota_frequente = False
            date_range = filtrar_datas()
            resultado = viagens.rotas(dados, rota_frequente, date_range=date_range)
            print("\n")
            print(resultado.to_string(index=False))

        elif escolha == "4":

            # Distribuição das viagens por dia da semana, consoante o período temporal definido pelo utilizador.
            # FEITO
            date_range = filtrar_datas()
            resultado = viagens.distribuicao_viagens_dia_semana(dados, date_range)
            print("\n")
            print(resultado.to_string(index=False))

        elif escolha == "5":

            # Identificação das horas de pico associadas à utilização de percursos portajados.
            # FEITO
            date_range = filtrar_datas()
            resultado = viagens.horas_de_pico(dados, date_range)
            print("\n")
            print(resultado.to_string(index=False))

        elif escolha == "6":

            # ...
            # FEITO
            date_range = filtrar_datas()
            resultado = viagens.estatisticas_duracao_viagens(dados, date_range)
            print("\n")
            print(resultado.to_string(index=False))

        elif escolha.upper() == "X":
            break

        else:
            # Opção inválida introduzida pelo utilizador.
            print("\nOpção inválida. Por favor, escolha novamente uma opção!")
            continue


def menu_estacionamentos(dados):

    while True:

        menu.submenu_estacionamento()

        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":

            resultado, ano, erro = estacionamento.estacionamento_anual(dados)
            if erro:
                continue
            if resultado.empty:
                print("\nSem dados para mostrar!")
                continue
            print("\n")
            print(f"========== ESTACIONAMENTOS EM {ano} ==========\n")
            print(resultado.to_string(index=False))

        elif escolha == "2":

            resultado, ano, erro = estacionamento.estacionamento_anual_local(dados)
            if erro:
                continue
            if resultado.empty:
                print("\nSem dados para mostrar!")
                continue
            print("\n")
            print(f"========== ESTACIONAMENTOS EM {ano} POR LOCAL==========\n")
            print(resultado.to_string(index=False))

        elif escolha == "3":

            resultado, ano, erro = estacionamento.estacionamento_anual_operador(dados)
            if erro:
                continue
            if resultado.empty:
                print("\nSem dados para mostrar!")
                continue
            print("\n")
            print(f"========== ESTACIONAMENTOS EM {ano} POR OPERADOR==========\n")
            print(resultado.to_string(index=False))

        elif escolha.upper() == "X":
            break

        else:
            # Opção inválida introduzida pelo utilizador.
            print("\nOpção inválida. Por favor, escolha novamente uma opção!")
            continue


def menu_graficos(portagens_df, estacionamentos_df):
    while True:
        menu.submenu_graficos()
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":
            menu_graficos_viagens(portagens_df)
        elif escolha == "2":
            menu_graficos_custos(portagens_df)
        elif escolha == "3":
            menu_graficos_estacionamentos(estacionamentos_df)

        elif escolha.upper() == "X":
            break

        else:
            # Opção inválida introduzida pelo utilizador.
            print("\nOpção inválida. Por favor, escolha novamente uma opção!")
            continue


def menu_graficos_viagens(dados):
    while True:
        menu.submenu_graficos_viagens()
        escolha = input("Escolha uma opção: ").strip()

        if escolha == "1":

            date_range = filtrar_datas()
            graficos_viagens.histograma_duracao_viagens(dados, date_range)

        elif escolha == "2":

            date_range = filtrar_datas()
            resultado = viagens.distribuicao_viagens_dia_semana(dados, date_range)
            graficos_viagens.heatmap_distribuicao(resultado)

        elif escolha == "3":

            date_range = filtrar_datas()
            graficos_viagens.rede_itinerarios(dados, date_range)

        elif escolha == "4":

            frequencia, sign = escolher_frequencia()
            itinerario = escolher_itinerario(dados, frequencia, sign)
            graficos_viagens.linha_tempo_itinerario(dados, itinerario)

        elif escolha == "5":

            graficos_viagens.viagens_por_mes_vv(dados)

        elif escolha.upper() == "X":
            break

        else:
            # Opção inválida introduzida pelo utilizador.
            print("\nOpção inválida. Por favor, escolha novamente uma opção!")
            continue


def menu_graficos_custos(dados):
    while True:
        menu.submenu_graficos_custos()
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":

            graficos_custos.histograma_custo_viagens(dados)

        elif escolha == "2":

            graficos_custos.consumo_portagens(dados)

        elif escolha == "3":

            graficos_custos.heatmap_custos(dados)

        elif escolha == "4":

            graficos_custos.heatmap_custos_medios(dados)

        elif escolha == "5":

            graficos_custos.boxplot_custos(dados)

        elif escolha == "6":

            graficos_custos.evolucao_custos_itinerario(dados)

        elif escolha.upper() == "X":
            break

        else:
            # Opção inválida introduzida pelo utilizador.
            print("\nOpção inválida. Por favor, escolha novamente uma opção!")
            continue


def menu_graficos_estacionamentos(dados):
    while True:
        menu.submenu_graficos_estacionamento()
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            graficos_estacionamento.histograma_custo_estacionamento(dados)
        elif escolha == "2":
            graficos_estacionamento.histograma_duracao_estacionamento(dados)
        elif escolha == "3":
            graficos_estacionamento.dispersao_custo_duracao_estacionamento(dados)
        elif escolha.upper() == "X":
            break
        else:
            # Opção inválida introduzida pelo utilizador.
            print("\nOpção inválida. Por favor, escolha novamente uma opção!")
            continue


if __name__ == "__main__":
    main()
