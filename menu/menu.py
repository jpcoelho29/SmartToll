def title():

    print(
        r"""
 ____                           _     _____       _  _ 
/ ___|  _ __ ___    __ _  _ __ | |_  |_   _|___  | || |
\___ \ | '_ ` _ \  / _` || '__|| __|   | | / _ \ | || |
___ ) || | | | | || (_| || |   | |_    | || (_) || || |
|____/ |_| |_| |_| \__,_||_|    \__|   |_| \___/ |_||_| v1.0
                                                        
"""
    )


def menu():
    print("\n====================== Menu Principal: ======================\n")
    print("1: 🚗 VIAGENS")
    print("2: 🤑 CUSTOS")
    print("3: 🅿️ ESTACIONAMENTO")
    print("4: 📈 GRÁFICOS")
    print("5: 🔄️ATUALIZAR DADOS")
    print("X: ❌ Sair")


def submenu_viagens():
    print("\n====================== 🚗 VIAGENS 🚗 ======================\n")
    print("1: Percursos portajados realizados num determinado período")
    print("2: Itinerários portajados mais frequentes")
    print("3: Itinerários portajados esporádicos")
    print("4: Distribuição de percursos portajados por dia da semana")
    print("5: Horários de pico de utilização de percursos portajados")
    print("6: Estatísticas inerentes à duração das viagens")
    print("X: Voltar")


def submenu_custos():
    print("\n====================== 🤑 CUSTOS 🤑 ======================\n")
    print("1: Total de custos anuais em portagens")
    print("2: Total de custos mensais em portagens")
    print("3: Total de custos anuais por concessão")
    print("4: Total de custos mensais por concessão")
    print("5: Total de custos anuais por Itinerário")
    print("6: Total de custos mensais por matrícula e periodo")
    print("7: Estatísticas de custos por matrícula e periodo")
    print("X: Voltar")


def submenu_estacionamento():
    print("\n====================== 🅿️ ESTACIONAMENTO 🅿️ ======================\n")
    print("1: Total de estacionamentos por ano")
    print("2: Total de estacionamentos por ano e local")
    print("3: Total de estacionamentos por ano e operador")
    print("X: Voltar")


def submenu_graficos():
    print("====================== 📈 Gráficos 📈 ======================\n")
    print("1: 🚗 GRÁFICOS DE VIAGENS")
    print("2: 🤑 GRÁFICOS DE CUSTOS")
    print("3: 🅿️ GRÁFICOS DE ESTACIONAMENTO")
    print("X: Voltar")


def submenu_graficos_viagens():
    print(
        "\n====================== 📈 🚗 Gráficos de Viagens 🚗 📈 ======================\n"
    )
    print("1: Histograma de duração das viagens")
    print("2: Mapa de calor")
    print("3: Rede de itinerários")
    print("4: Duração de viagens por itinerário")
    print("5: Utilização de percursos portajados")
    print("X: Voltar")


def submenu_graficos_custos():
    print(
        "\n====================== 📈 🤑 Gráficos de Custos 🤑 📈 ======================\n"
    )
    print("1: Histograma de custos por matrícula")
    print("2: Consumo de portagens por matrícula")
    print("3: Mapa de calor de custos totais por matrícula")
    print("4: Mapa de calor de custos médios por matrícula")
    print("5: Boxplot de custos por matrícula")
    print("6: Evolução de custos por itinerário")
    print("X: Voltar")


def submenu_graficos_estacionamento():
    print(
        "\n====================== 📈 🅿️ Gráficos de Estacionamento 🅿️ 📈 ======================\n"
    )
    print("1: Histograma de custos dos estacionamentos")
    print("2: Histograma de duração dos estacionamentos")
    print("3: Dispersão Duracao vs Custos")
    print("X: Voltar")


if __name__ == "__main__":
    pass
