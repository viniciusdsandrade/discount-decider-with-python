# retiremente_calculator.py

import math


def calcular_fv_sem_aportes(pv, i, n):
    """
    Calcula o Valor Futuro (FV) com investimento único (sem aportes regulares).

    :param pv: Valor Presente (investimento inicial) em R$
    :param i: Taxa de juros anual (decimal, por exemplo, 11% = 0.11)
    :param n: Número de anos
    :return: Valor Futuro (FV) em R$
    """
    fv = pv * (1 + i) ** n
    return fv


def calcular_fv_com_aportes(pmt, i, n):
    """
    Calcula o Valor Futuro (FV) com aportes regulares (Anuidade).

    :param pmt: Pagamento periódico (aporte regular)
    :param i: Taxa de juros por período (decimal)
    :param n: Número de períodos
    :return: Valor Futuro (FV)
    """
    if i == 0:
        fv = pmt * n
    else:
        fv = pmt * ((1 + i) ** n - 1) / i
    return fv


def calcular_fv_combinada(pv, pmt, taxa_anual, anos, frequencia='mensal'):
    """
    Calcula o Valor Futuro (FV) combinando investimento inicial e aportes regulares
    com diferentes frequências de capitalização de juros.

    :param pv: Valor Presente (investimento inicial)
    :param pmt: Pagamento periódico (aporte regular)
    :param taxa_anual: Taxa de juros anual (em %)
    :param anos: Número de anos
    :param frequencia: Frequência de capitalização ('diaria', 'mensal', 'anual')
    :return: Valor Futuro (FV)
    """
    taxa_anual_decimal = taxa_anual / 100
    n_anos = anos

    if frequencia == 'diaria':
        periodos_por_ano = 365
    elif frequencia == 'mensal':
        periodos_por_ano = 12
    elif frequencia == 'anual':
        periodos_por_ano = 1
    else:
        raise ValueError("Frequência inválida. Escolha entre 'diaria', 'mensal', 'anual'.")

    taxa_periodo = taxa_anual_decimal / periodos_por_ano
    n_periodos = n_anos * periodos_por_ano

    # Valor Futuro do Investimento Inicial
    fv_pv = pv * (1 + taxa_periodo) ** n_periodos

    # Valor Futuro dos Aportes Regulares
    if taxa_periodo == 0:
        fv_pmt = pmt * n_periodos
    else:
        fv_pmt = pmt * ((1 + taxa_periodo) ** n_periodos - 1) / taxa_periodo

    # Valor Futuro Total
    fv_total = fv_pv + fv_pmt

    return fv_total


def calcular_rendimentos(fv, pv, pmt, anos, frequencia='mensal'):
    """
    Calcula os rendimentos acumulados.

    :param fv: Valor Futuro (FV)
    :param pv: Valor Presente (investimento inicial)
    :param pmt: Pagamento periódico (aporte regular)
    :param anos: Número de anos
    :param frequencia: Frequência de capitalização ('diaria', 'mensal', 'anual')
    :return: Rendimentos acumulados
    """
    if frequencia == 'diaria':
        periodos_por_ano = 365
    elif frequencia == 'mensal':
        periodos_por_ano = 12
    elif frequencia == 'anual':
        periodos_por_ano = 1
    else:
        raise ValueError("Frequência inválida. Escolha entre 'diaria', 'mensal', 'anual'.")

    n_periodos = anos * periodos_por_ano

    # Total Investido
    total_investido = pv + pmt * n_periodos

    # Rendimentos
    rendimentos = fv - total_investido

    return rendimentos


def resolver_pmt(fv, pv, i, n):
    """
    Calcula o Aporte Mensal Necessário (PMT) para atingir um determinado Valor Futuro (FV).

    :param fv: Valor Futuro desejado
    :param pv: Valor Presente (investimento inicial)
    :param i: Taxa de juros por período (decimal)
    :param n: Número de períodos
    :return: Aporte Mensal Necessário (PMT)
    """
    if i == 0:
        if n == 0:
            raise ValueError("Número de períodos não pode ser zero.")
        pmt = (fv - pv) / n
    else:
        denominador = ((1 + i) ** n - 1) / i
        if denominador == 0:
            raise ZeroDivisionError("Denominador é zero. Verifique os parâmetros de entrada.")
        pmt = (fv - pv * (1 + i) ** n) / denominador
    return pmt


def resolver_n(fv, pmt, pv, i):
    """
    Calcula o Número de Períodos (n) necessários para atingir um determinado Valor Futuro (FV).

    :param fv: Valor Futuro desejado
    :param pmt: Pagamento periódico (aporte regular)
    :param pv: Valor Presente (investimento inicial)
    :param i: Taxa de juros por período (decimal)
    :return: Número de Períodos (n)
    """
    if i == 0:
        if pmt == 0:
            if pv == 0:
                raise ValueError("PV e PMT não podem ser ambos zero.")
            return fv / pv
        else:
            return (fv - pv) / pmt
    else:
        numerator = fv * i + pmt
        denominator = pv * i + pmt
        if numerator <= 0 or denominator <= 0:
            raise ValueError("Parâmetros resultam em logaritmo de número não positivo.")
        n = math.log(numerator / denominator) / math.log(1 + i)
        return n


def resolver_i(fv, pv, pmt, n, taxa_inicial=0.01, tolerancia=1e-6, max_iter=1000):
    """
    Calcula a Taxa de Juros (i) necessária para atingir um determinado Valor Futuro (FV) usando o Método de Newton-Raphson.

    :param fv: Valor Futuro desejado
    :param pv: Valor Presente (investimento inicial)
    :param pmt: Pagamento periódico (aporte regular)
    :param n: Número de períodos
    :param taxa_inicial: Chute inicial para a taxa de juros
    :param tolerancia: Tolerância para a convergência
    :param max_iter: Número máximo de iterações
    :return: Taxa de juros por período (i) em decimal
    """
    i = taxa_inicial
    for _ in range(max_iter):
        # Função f(i) = PV*(1+i)^n + PMT*((1+i)^n -1)/i - FV
        try:
            fv_calculado = pv * (1 + i) ** n + pmt * ((1 + i) ** n - 1) / i
        except ZeroDivisionError:
            fv_calculado = float('inf')
        f = fv_calculado - fv

        # Derivada de f(i) em relação a i
        try:
            df = pv * n * (1 + i) ** (n - 1) + pmt * (((1 + i) ** n * (n / (1 + i))) - ((1 + i) ** n - 1) / i ** 2)
        except ZeroDivisionError:
            df = float('inf')

        if df == 0:
            raise ZeroDivisionError("Derivada zero durante o cálculo. Método falhou.")

        # Atualiza i usando Newton-Raphson
        i_new = i - f / df

        # Verifica a convergência
        if abs(i_new - i) < tolerancia:
            return i_new

        i = i_new

    raise ValueError("Método de Newton-Raphson não convergiu.")


def calcular_fv_sem_aportes_opcao():
    """
    Opção para calcular o Valor Futuro (FV) sem aportes regulares.
    Considera:
    - Taxa de juros anual
    - Período em anos
    - Aporte inicial único
    """
    print("\n=== Cálculo do Valor Futuro (FV) sem Aportes Regulares ===\n")
    try:
        # Entrada para Valor Presente (Investimento Inicial)
        pv_input = input("Digite o Valor Presente (PV) em R$: ").replace(',', '.')
        pv = float(pv_input)
        if pv < 0:
            print("O Valor Presente (PV) não pode ser negativo.")
            return

        # Entrada para Taxa de Juros Anual
        i_input = input("Digite a taxa de juros anual (em %): ").replace(',', '.')
        i = float(i_input) / 100
        if i < 0:
            print("A taxa de juros anual não pode ser negativa.")
            return

        # Entrada para Período de Investimento em Anos
        n_input = input("Digite o período de investimento (em anos): ").replace(',', '.')
        n = float(n_input)
        if n < 0:
            print("O período de investimento não pode ser negativo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos válidos.")
        return

    # Cálculo do Valor Futuro
    fv = calcular_fv_sem_aportes(pv, i, n)

    # Cálculo dos Rendimentos
    rendimentos = fv - pv

    # Exibição dos Resultados
    print("\n=== Resultados ===")
    print(f"Valor Presente (PV): R$ {pv:,.2f}")
    print(f"Taxa de Juros Anual: {i * 100:.2f}%")
    print(f"Período de Investimento: {n:.2f} anos")
    print(f"Valor Futuro (FV): R$ {fv:,.2f}")
    print(f"Rendimentos Acumulados: R$ {rendimentos:,.2f}")


def calcular_fv_com_aportes_opcao():
    """
    Opção para calcular o Valor Futuro (FV) com aportes regulares (Anuidade).
    """
    print("\n=== Cálculo do Valor Futuro (FV) com Aportes Regulares ===\n")
    try:
        pmt = float(input("Digite o valor da parcela mensal (PMT) em R$: ").replace(',', '.'))
        if pmt < 0:
            print("O valor da parcela (PMT) não pode ser negativo.")
            return
        i = float(input("Digite a taxa de juros por período (em %): ").replace(',', '.')) / 100
        n = int(input("Digite o número de períodos: "))
        if n < 0:
            print("O número de períodos não pode ser negativo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos válidos.")
        return

    fv = calcular_fv_com_aportes(pmt, i, n)
    print("\n=== Resultados ===")
    print(f"Pagamento Mensal (PMT): R$ {pmt:,.2f}")
    print(f"Taxa de Juros por Período (i): {i * 100:.4f}%")
    print(f"Número de Períodos (n): {n}")
    print(f"Valor Futuro (FV): R$ {fv:,.2f}")


def calcular_fv_combinada_opcao():
    """
    Opção para calcular o Valor Futuro (FV) com investimento inicial + aportes regulares,
    utilizando taxa de juros anual e período em anos, e calcular rendimentos para diferentes frequências.
    """
    print("\n=== Cálculo do Valor Futuro (FV) com Investimento Inicial + Aportes Regulares ===\n")
    try:
        pv = float(input("Digite o Valor Presente (PV) em R$: ").replace(',', '.'))
        if pv < 0:
            print("O Valor Presente (PV) não pode ser negativo.")
            return
        pmt = float(input("Digite o valor da parcela mensal (PMT) em R$: ").replace(',', '.'))
        if pmt < 0:
            print("O valor da parcela (PMT) não pode ser negativo.")
            return
        taxa_anual = float(input("Digite a taxa de juros anual (em %): ").replace(',', '.'))
        if taxa_anual < 0:
            print("A taxa de juros anual não pode ser negativa.")
            return
        anos = float(input("Digite o número de anos: "))
        if anos <= 0:
            print("O número de anos deve ser positivo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos válidos.")
        return

    frequencias = ['diaria', 'mensal', 'anual']
    resultados = {}

    for freq in frequencias:
        fv = calcular_fv_combinada(pv, pmt, taxa_anual, anos, frequencia=freq)
        rendimentos = calcular_rendimentos(fv, pv, pmt, anos, frequencia=freq)
        resultados[freq] = {'fv': fv, 'rendimentos': rendimentos}

    print("\n=== Resultados ===")
    print(f"Valor Presente (PV): R$ {pv:,.2f}")
    print(f"Pagamento Mensal (PMT): R$ {pmt:,.2f}")
    print(f"Taxa de Juros Anual: {taxa_anual:.2f}%")
    print(f"Número de Anos: {anos}")
    print("\n--- Frequências de Capitalização ---")
    for freq in frequencias:
        fv = resultados[freq]['fv']
        rendimentos = resultados[freq]['rendimentos']
        print(f"\nFrequência de Capitalização: {freq.capitalize()}")
        print(f"Valor Futuro (FV): R$ {fv:,.2f}")
        print(f"Rendimentos Acumulados: R$ {rendimentos:,.2f}")


def resolver_pmt_opcao():
    """
    Opção para calcular o Aporte Mensal Necessário (PMT).
    """
    print("\n=== Cálculo do Aporte Mensal Necessário (PMT) ===\n")
    try:
        fv = float(input("Digite o Valor Futuro (FV) desejado em R$: ").replace(',', '.'))
        if fv < 0:
            print("O Valor Futuro (FV) não pode ser negativo.")
            return
        pv = float(input("Digite o Valor Presente (PV) em R$: ").replace(',', '.'))
        if pv < 0:
            print("O Valor Presente (PV) não pode ser negativo.")
            return
        i = float(input("Digite a taxa de juros por período (em %): ").replace(',', '.')) / 100
        n = int(input("Digite o número de períodos: "))
        if n <= 0:
            print("O número de períodos deve ser positivo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos válidos.")
        return

    try:
        pmt = resolver_pmt(fv, pv, i, n)
        print("\n=== Resultados ===")
        print(f"Valor Futuro (FV): R$ {fv:,.2f}")
        print(f"Valor Presente (PV): R$ {pv:,.2f}")
        print(f"Taxa de Juros por Período (i): {i * 100:.4f}%")
        print(f"Número de Períodos (n): {n}")
        print(f"Aporte Mensal Necessário (PMT): R$ {pmt:,.2f}")
    except ZeroDivisionError as e:
        print(f"Erro no cálculo: {e}")
    except Exception as e:
        print(f"Erro no cálculo: {e}")


def resolver_n_opcao():
    """
    Opção para calcular o Número de Períodos (n).
    """
    print("\n=== Cálculo do Número de Períodos (n) ===\n")
    try:
        fv = float(input("Digite o Valor Futuro (FV) desejado em R$: ").replace(',', '.'))
        if fv < 0:
            print("O Valor Futuro (FV) não pode ser negativo.")
            return
        pmt = float(input("Digite o valor da parcela mensal (PMT) em R$: ").replace(',', '.'))
        if pmt < 0:
            print("O valor da parcela (PMT) não pode ser negativo.")
            return
        pv = float(input("Digite o Valor Presente (PV) em R$: ").replace(',', '.'))
        if pv < 0:
            print("O Valor Presente (PV) não pode ser negativo.")
            return
        i = float(input("Digite a taxa de juros por período (em %): ").replace(',', '.')) / 100
    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos válidos.")
        return

    try:
        n = resolver_n(fv, pmt, pv, i)
        print("\n=== Resultados ===")
        print(f"Valor Futuro (FV): R$ {fv:,.2f}")
        print(f"Pagamento Mensal (PMT): R$ {pmt:,.2f}")
        print(f"Valor Presente (PV): R$ {pv:,.2f}")
        print(f"Taxa de Juros por Período (i): {i * 100:.4f}%")
        print(f"Número de Períodos (n): {n:.2f} períodos")
    except ValueError as e:
        print(f"Erro no cálculo: {e}")
    except Exception as e:
        print(f"Erro no cálculo: {e}")


def resolver_i_opcao():
    """
    Opção para calcular a Taxa de Juros (i).
    """
    print("\n=== Cálculo da Taxa de Juros (i) ===\n")
    try:
        fv = float(input("Digite o Valor Futuro (FV) desejado em R$: ").replace(',', '.'))
        if fv < 0:
            print("O Valor Futuro (FV) não pode ser negativo.")
            return
        pv = float(input("Digite o Valor Presente (PV) em R$: ").replace(',', '.'))
        if pv < 0:
            print("O Valor Presente (PV) não pode ser negativo.")
            return
        pmt = float(input("Digite o valor da parcela mensal (PMT) em R$: ").replace(',', '.'))
        if pmt < 0:
            print("O valor da parcela (PMT) não pode ser negativo.")
            return
        n = int(input("Digite o número de períodos: "))
        if n <= 0:
            print("O número de períodos deve ser positivo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos válidos.")
        return

    try:
        i = resolver_i(fv, pv, pmt, n)
        tae = (1 + i) ** 12 - 1  # Calculando a Taxa Anual Equivalente (TAE) com base na taxa mensal
        print("\n=== Resultados ===")
        print(f"Valor Futuro (FV): R$ {fv:,.2f}")
        print(f"Valor Presente (PV): R$ {pv:,.2f}")
        print(f"Pagamento Mensal (PMT): R$ {pmt:,.2f}")
        print(f"Número de Períodos (n): {n}")
        print(f"Taxa de Juros por Período (i): {i * 100:.6f}%")
        print(f"Taxa Anual Equivalente (TAE): {tae * 100:.6f}%")
    except ZeroDivisionError as e:
        print(f"Erro no cálculo: {e}")
    except ValueError as e:
        print(f"Erro no cálculo: {e}")
    except Exception as e:
        print(f"Erro no cálculo: {e}")


def calcular_fv_combinada_opcao():
    """
    Opção para calcular o Valor Futuro (FV) com investimento inicial + aportes regulares,
    utilizando taxa de juros anual e período em anos, e calcular rendimentos para diferentes frequências.
    """
    print("\n=== Cálculo do Valor Futuro (FV) com Investimento Inicial + Aportes Regulares ===\n")
    try:
        pv = float(input("Digite o Valor Presente (PV) em R$: ").replace(',', '.'))
        if pv < 0:
            print("O Valor Presente (PV) não pode ser negativo.")
            return
        pmt = float(input("Digite o valor da parcela mensal (PMT) em R$: ").replace(',', '.'))
        if pmt < 0:
            print("O valor da parcela (PMT) não pode ser negativo.")
            return
        taxa_anual = float(input("Digite a taxa de juros anual (em %): ").replace(',', '.'))
        if taxa_anual < 0:
            print("A taxa de juros anual não pode ser negativa.")
            return
        anos = float(input("Digite o número de anos: "))
        if anos <= 0:
            print("O número de anos deve ser positivo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos válidos.")
        return

    frequencias = ['diaria', 'mensal', 'anual']
    resultados = {}

    for freq in frequencias:
        fv = calcular_fv_combinada(pv, pmt, taxa_anual, anos, frequencia=freq)
        rendimentos = calcular_rendimentos(fv, pv, pmt, anos, frequencia=freq)
        resultados[freq] = {'fv': fv, 'rendimentos': rendimentos}

    print("\n=== Resultados ===")
    print(f"Valor Presente (PV): R$ {pv:,.2f}")
    print(f"Pagamento Mensal (PMT): R$ {pmt:,.2f}")
    print(f"Taxa de Juros Anual: {taxa_anual:.2f}%")
    print(f"Número de Anos: {anos}")
    print("\n--- Frequências de Capitalização ---")
    for freq in frequencias:
        fv = resultados[freq]['fv']
        rendimentos = resultados[freq]['rendimentos']
        print(f"\nFrequência de Capitalização: {freq.capitalize()}")
        print(f"Valor Futuro (FV): R$ {fv:,.2f}")
        print(f"Rendimentos Acumulados: R$ {rendimentos:,.2f}")


def main():
    """
    Função principal que interage com o usuário para realizar cálculos financeiros relacionados à aposentadoria.
    """
    print("=== Calculadora de Aposentadoria ===\n")
    print("Escolha uma opção:")
    print("1. Calcular Valor Futuro (FV) sem aportes regulares")
    print("2. Calcular Valor Futuro (FV) com aportes regulares (Anuidade)")
    print("3. Calcular Valor Futuro (FV) com investimento inicial + aportes regulares")
    print("4. Resolver para o Aporte Mensal Necessário (PMT)")
    print("5. Resolver para o Número de Períodos (n)")
    print("6. Resolver para a Taxa de Juros (i)")
    print("7. Sair")

    while True:
        escolha = input("\nDigite o número da opção desejada (1-7): ").strip()
        if escolha not in [str(i) for i in range(1, 8)]:
            print("Opção inválida. Por favor, escolha entre 1 e 7.")
            continue

        if escolha == '7':
            print("Encerrando o programa. Até logo!")
            break

        if escolha == '1':
            calcular_fv_sem_aportes_opcao()
        elif escolha == '2':
            calcular_fv_com_aportes_opcao()
        elif escolha == '3':
            calcular_fv_combinada_opcao()
        elif escolha == '4':
            resolver_pmt_opcao()
        elif escolha == '5':
            resolver_n_opcao()
        elif escolha == '6':
            resolver_i_opcao()


if __name__ == "__main__":
    main()
