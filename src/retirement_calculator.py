# src/retiremente_calculator.py

import math


def calcular_fv_sem_aportes(pv, i, n):
    """
    Calcula o Valor Futuro (FV) com investimento único (sem aportes regulares).

    :param pv: Valor Presente (investimento inicial)
    :param i: Taxa de juros por período (decimal)
    :param n: Número de períodos
    :return: Valor Futuro (FV)
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


def calcular_fv_combinada(pv, pmt, i, n):
    """
    Calcula o Valor Futuro (FV) combinando investimento inicial e aportes regulares.

    :param pv: Valor Presente (investimento inicial)
    :param pmt: Pagamento periódico (aporte regular)
    :param i: Taxa de juros por período (decimal)
    :param n: Número de períodos
    :return: Valor Futuro (FV)
    """
    fv_pv = calcular_fv_sem_aportes(pv, i, n)
    fv_pmt = calcular_fv_com_aportes(pmt, i, n)
    fv_total = fv_pv + fv_pmt
    return fv_total


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
    Calcula a Taxa de Juros (i) necessária para atingir um determinado Valor Futuro (FV) usando o Metodo de Newton-Raphson.

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


def calcular_fv_sem_aportes_opcao():
    """
    Opção para calcular o Valor Futuro (FV) sem aportes regulares.
    """
    print("\n=== Cálculo do Valor Futuro (FV) sem Aportes Regulares ===\n")
    try:
        pv = float(input("Digite o Valor Presente (PV) em R$: ").replace(',', '.'))
        if pv < 0:
            print("O Valor Presente (PV) não pode ser negativo.")
            return
        i = float(input("Digite a taxa de juros por período (em %): ").replace(',', '.')) / 100
        n = int(input("Digite o número de períodos: "))
        if n < 0:
            print("O número de períodos não pode ser negativo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos válidos.")
        return

    fv = calcular_fv_sem_aportes(pv, i, n)
    print("\n=== Resultados ===")
    print(f"Valor Presente (PV): R$ {pv:,.2f}")
    print(f"Taxa de Juros por Período (i): {i * 100:.4f}%")
    print(f"Número de Períodos (n): {n}")
    print(f"Valor Futuro (FV): R$ {fv:,.2f}")


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
    Opção para calcular o Valor Futuro (FV) com investimento inicial + aportes regulares.
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
        i = float(input("Digite a taxa de juros por período (em %): ").replace(',', '.')) / 100
        n = int(input("Digite o número de períodos: "))
        if n < 0:
            print("O número de períodos não pode ser negativo.")
            return
    except ValueError:
        print("Entrada inválida. Por favor, insira valores numéricos válidos.")
        return

    fv = calcular_fv_combinada(pv, pmt, i, n)
    print("\n=== Resultados ===")
    print(f"Valor Presente (PV): R$ {pv:,.2f}")
    print(f"Pagamento Mensal (PMT): R$ {pmt:,.2f}")
    print(f"Taxa de Juros por Período (i): {i * 100:.4f}%")
    print(f"Número de Períodos (n): {n}")
    print(f"Valor Futuro (FV): R$ {fv:,.2f}")


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


if __name__ == "__main__":
    main()
