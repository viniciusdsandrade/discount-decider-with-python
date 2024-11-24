# src/financial_calculator.py

import math


def calcular_tae(taxa_mensal):
    """
    Calcula a Taxa Anual Equivalente (TAE) a partir da taxa de juros mensal.

    A TAE é uma medida que permite comparar diferentes ofertas de crédito ou investimentos que possuem taxas compostas em diferentes períodos.

    **Fórmula utilizada:**

        TAE = (1 + r)ⁿ - 1

    Onde:
        - **r** é a taxa de juros mensal.
        - **n** é o número de períodos compostos por ano (neste caso, 12 meses).

    Parameters:
        taxa_mensal (float): Taxa de juros mensal expressa em decimal (por exemplo, 1% = 0.01).

    Returns:
        float: Taxa Anual Equivalente (TAE) em decimal.
    """
    tae = (1 + taxa_mensal) ** 12 - 1
    return tae


def calcular_valor_presente(pmt, taxa_mensal, num_parcelas):
    """
    Calcula o Valor Presente (PV) de uma série de pagamentos mensais.

    O Valor Presente representa o valor atual de uma série de pagamentos futuros descontados a uma taxa de juros específica.

    **Fórmula utilizada:**

        PV = PMT × [ (1 - (1 + r)^(-n)) / r ]

    onde:
        - **PMT** é o valor da parcela mensal.
        - **r** é a taxa de juros mensal.
        - **n** é o número de parcelas.

    **Caso especial:**

    Se a taxa de juros for 0%, o Valor Presente é simplesmente o total das parcelas:

        PV = PMT × n

    Parameters:
        pmt (float): Valor da parcela mensal (Pagamento).
        taxa_mensal (float): Taxa de juros mensal em decimal (por exemplo, 1% = 0.01).
        num_parcelas (int): Número total de parcelas.

    Returns:
        float: Valor Presente (PV).
    """
    if taxa_mensal == 0:
        # Evita divisão por zero se a taxa for 0%
        pv = pmt * num_parcelas
    else:
        pv = pmt * (1 - (1 + taxa_mensal) ** -num_parcelas) / taxa_mensal
    return pv


def calcular_taxa_mensal(pv, pmt, num_parcelas, taxa_inicial=0.01, tolerancia=1e-6, max_iter=1000):
    """
    Calcula a taxa de juros mensal (r) usando o Metodo de Newton-Raphson.

    Determina a taxa de juros mensal que iguala o Valor Presente (PV) a uma série de pagamentos mensais (PMT) ao longo de um número especificado de parcelas.

    **Fórmula a resolver:**

        PV = PMT × [ (1 - (1 + r)^(-n)) / r ]

    Utiliza o Metodo de Newton-Raphson para encontrar r tal que f(r) = 0, onde:

        f(r) = PV - PMT × [ (1 - (1 + r)^(-n)) / r ]

    A derivada f'(r) é:

        f'(r) = PMT × [ ( (1 - (1 + r)^(-n)) / r² ) - ( n × (1 + r)^(-n -1) ) / r ]

    Parameters:
        pv (float): Valor Presente (PV).
        pmt (float): Valor da parcela mensal (Pagamento).
        num_parcelas (int): Número total de parcelas.
        taxa_inicial (float, optional): Chute inicial para a taxa de juros mensal (default: 0.01).
        tolerancia (float, optional): Tolerância para a convergência do metodo (default: 1e-6).
        max_iter (int, optional): Número máximo de iterações permitidas (default: 1000).

    Returns:
        float: Taxa de juros mensal (r) em decimal.

    Raises:
        ZeroDivisionError: Se a derivada é zero durante o cálculo.
        ValueError: Se o metodo não convergir após o número máximo de iterações.
    """
    r = taxa_inicial
    for i in range(max_iter):
        # Função f(r) = PV - PMT * (1 - (1 + r)^-n) / r
        f = pv - calcular_valor_presente(pmt, r, num_parcelas)

        # Derivada de f(r) em relação a r
        if r == 0:
            # Derivada quando r = 0
            df = -pmt * num_parcelas * (num_parcelas + 1) / 2
        else:
            df = pmt * ((1 - (1 + r) ** -num_parcelas) / (r ** 2)) - pmt * (
                    num_parcelas * (1 + r) ** (-num_parcelas - 1)) / r

        # Evita divisão por zero na derivada
        if df == 0:
            raise ZeroDivisionError("A derivada é zero. Método de Newton-Raphson falhou.")

        # Atualiza r usando Newton-Raphson
        r_new = r - f / df

        # Verifica a convergência
        if abs(r_new - r) < tolerancia:
            return r_new

        r = r_new

    raise ValueError("O Método de Newton-Raphson não convergiu após o número máximo de iterações.")


def main():
    """
    Função principal que interage com o usuário para realizar cálculos financeiros.

    Oferece um menu interativo para o usuário escolher entre calcular:

    1. Taxa Anual Equivalente (TAE)
    2. Valor Presente (PV)
    3. Taxa de Juros Mensal (r)
    4. Sair

    A função lida com a entrada do usuário e chama as funções correspondentes para executar os cálculos selecionados.
    """
    print("=== Cálculos Financeiros ===\n")
    print("Escolha uma opção:")
    print("1. Calcular a Taxa Anual Equivalente (TAE)")
    print("2. Calcular o Valor Presente (PV)")
    print("3. Calcular a Taxa de Juros Mensal (r)")
    print("4. Sair")

    while True:
        escolha = input("\nDigite o número da opção desejada (1-4): ").strip()
        if escolha not in ['1', '2', '3', '4']:
            print("Opção inválida. Por favor, escolha entre 1 e 4.")
            continue

        if escolha == '4':
            print("Encerrando o programa. Até logo!")
            break

        if escolha == '1':
            # Calcular TAE
            calcular_tae_opcao()
        elif escolha == '2':
            # Calcular PV
            calcular_pv_opcao()
        elif escolha == '3':
            # Calcular r
            calcular_r_opcao()


def calcular_tae_opcao():
    """
    Gerencia a interação com o usuário para calcular a Taxa Anual Equivalente (TAE).

    Solicita ao usuário a taxa de juros mensal, valida a entrada e exibe a TAE calculada.
    """
    print("\n=== Cálculo da Taxa Anual Equivalente (TAE) ===\n")
    while True:
        try:
            taxa_input = input("Digite a taxa de juros mensal (em %): ").replace(',', '.')
            taxa_mensal = float(taxa_input) / 100
            if taxa_mensal < 0:
                print("A taxa de juros mensal não pode ser negativa. Tente novamente.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido para a taxa de juros mensal.")

    tae = calcular_tae(taxa_mensal)
    print("\n=== Resultados ===")
    print(f"Taxa de Juros Mensal: {taxa_mensal * 100:.4f}%")
    print(f"Taxa Anual Equivalente (TAE): {tae:.6f} ou {tae * 100:.4f}%")


def calcular_pv_opcao():
    """
    Gerencia a interação com o usuário para calcular o Valor Presente (PV).

    Solicita ao usuário o valor da parcela mensal, a taxa de juros mensal e o número de parcelas,
    valida as entradas e exibe o Valor Presente calculado.
    """
    print("\n=== Cálculo do Valor Presente (PV) ===\n")
    while True:
        try:
            pmt_input = input("Digite o valor da parcela mensal (PMT) em R$: ").replace(',', '.')
            pmt = float(pmt_input)
            if pmt < 0:
                print("O valor da parcela não pode ser negativo. Tente novamente.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido para o valor da parcela.")

    while True:
        try:
            taxa_input = input("Digite a taxa de juros mensal (em %): ").replace(',', '.')
            taxa_mensal = float(taxa_input) / 100
            if taxa_mensal < 0:
                print("A taxa de juros mensal não pode ser negativa. Tente novamente.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido para a taxa de juros mensal.")

    while True:
        try:
            n_input = input("Digite o número de parcelas: ")
            num_parcelas = int(n_input)
            if num_parcelas <= 0:
                print("O número de parcelas deve ser positivo. Tente novamente.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro válido para o número de parcelas.")

    pv = calcular_valor_presente(pmt, taxa_mensal, num_parcelas)
    print("\n=== Resultados ===")
    print(f"Valor da Parcela Mensal (PMT): R$ {pmt:.2f}")
    print(f"Taxa de Juros Mensal: {taxa_mensal * 100:.4f}%")
    print(f"Número de Parcelas: {num_parcelas}")
    print(f"Valor Presente (PV): R$ {pv:.2f}")


def calcular_r_opcao():
    """
    Gerencia a interação com o usuário para calcular a Taxa de Juros Mensal (r).

    Solicita ao usuário o Valor Presente, o valor da parcela mensal e o número de parcelas,
    valida as entradas, realiza o cálculo utilizando 'calcular_taxa_mensal', e exibe os resultados.
    """
    print("\n=== Cálculo da Taxa de Juros Mensal (r) ===\n")
    while True:
        try:
            pv_input = input("Digite o Valor Presente (PV) em R$: ").replace(',', '.')
            pv = float(pv_input)
            if pv < 0:
                print("O Valor Presente (PV) não pode ser negativo. Tente novamente.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido para o Valor Presente (PV).")

    while True:
        try:
            pmt_input = input("Digite o valor da parcela mensal (PMT) em R$: ").replace(',', '.')
            pmt = float(pmt_input)
            if pmt <= 0:
                print("O valor da parcela deve ser positivo. Tente novamente.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido para o valor da parcela.")

    while True:
        try:
            n_input = input("Digite o número de parcelas: ")
            num_parcelas = int(n_input)
            if num_parcelas <= 0:
                print("O número de parcelas deve ser positivo. Tente novamente.")
                continue
            break
        except ValueError:
            print("Entrada inválida. Por favor, insira um número inteiro válido para o número de parcelas.")

    # Chute inicial para a taxa de juros
    taxa_inicial = 0.01  # 1%
    try:
        r = calcular_taxa_mensal(pv, pmt, num_parcelas, taxa_inicial=taxa_inicial)
        print("\n=== Resultados ===")
        print(f"Valor Presente (PV): R$ {pv:.2f}")
        print(f"Valor da Parcela Mensal (PMT): R$ {pmt:.2f}")
        print(f"Número de Parcelas: {num_parcelas}")
        print(f"Taxa de Juros Mensal (r): {r * 100:.6f}%")
        tae = calcular_tae(r)
        print(f"Taxa Anual Equivalente (TAE): {tae * 100:.6f}%")
    except ZeroDivisionError as zde:
        print(f"Erro no cálculo: {zde}")
    except ValueError as ve:
        print(f"Erro no cálculo: {ve}")


if __name__ == "__main__":
    main()
