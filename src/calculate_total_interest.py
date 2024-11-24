# src/calculate_total_interest.py


import math


def calcular_taxa_juros(P, rendimento_total, tipo='mensal'):
    """
    Calcula a taxa de juros composta com base no montante inicial, rendimento total e tipo de rendimento.

    P: Valor inicial da aplicação (R$)
    rendimento_total: Rendimento total acumulado (R$)
    tipo: 'diario' ou 'mensal'

    Retorna:
        taxa: Taxa de juros por período (em decimal)
    """
    try:
        if tipo == 'diario':
            # Para rendimento diário, o período é 1 dia
            periodo = 1
            taxa = rendimento_total / P
        elif tipo == 'mensal':
            # Para rendimento mensal, o período é 23 dias úteis
            periodo = 23
            # Fórmula para juros compostos: M = P * (1 + r)^n
            # Isolando r: r = (M/P)^(1/n) - 1
            montante_final = P + rendimento_total
            taxa = (montante_final / P) ** (1 / periodo) - 1
        else:
            raise ValueError("Tipo deve ser 'diario' ou 'mensal'.")
        return taxa
    except ZeroDivisionError:
        print("Erro: O montante inicial (P) não pode ser zero.")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None


def obter_valor_positivo(prompt):
    """
    Função auxiliar para obter um valor positivo do usuário.
    """
    while True:
        try:
            valor = float(input(prompt))
            if valor < 0:
                print("Por favor, insira um valor positivo.")
            else:
                return valor
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")


def obter_tipo_rendimento():
    """
    Função para obter o tipo de rendimento do usuário.
    """
    while True:
        tipo = input("Digite o tipo de rendimento ('diario' ou 'mensal'): ").strip().lower()
        if tipo in ['diario', 'mensal']:
            return tipo
        else:
            print("Tipo inválido. Por favor, digite 'diario' ou 'mensal'.")


def main():
    print("=== Calculadora de Taxa de Juros de uma Aplicação Financeira ===\n")

    # Entrada de Dados
    P = obter_valor_positivo("Digite o valor inicial da aplicação (R$): ")

    tipo = obter_tipo_rendimento()

    if tipo == 'diario':
        rendimento_total = obter_valor_positivo("Digite o rendimento total diário (R$): ")
    else:
        rendimento_total = obter_valor_positivo("Digite o rendimento total mensal (R$): ")

    print("\n=== Calculando ===\n")

    taxa = calcular_taxa_juros(P, rendimento_total, tipo)

    if taxa is not None:
        taxa_percent = taxa * 100
        print("=== Resultado ===")
        if tipo == 'diario':
            # Cálculo da taxa mensal e anual a partir da taxa diária
            taxa_mensal = (1 + taxa) ** 23 - 1  # 23 dias úteis por mês
            taxa_mensal_percent = taxa_mensal * 100

            taxa_anual = (1 + taxa) ** (23 * 12) - 1  # 23 dias úteis por mês * 12 meses
            taxa_anual_percent = taxa_anual * 100

            print(f"Taxa de Juros Diária: {taxa_percent:.4f}%")
            print(f"Taxa de Juros Mensal (23 dias úteis): {taxa_mensal_percent:.4f}%")
            print(f"Taxa de Juros Anual (276 dias úteis): {taxa_anual_percent:.4f}%")
        else:
            # Cálculo da taxa anual a partir da taxa mensal
            taxa_anual = (1 + (P + rendimento_total) / P - 1) ** 12 - 1  # (1 + r_mensal)^12 -1
            taxa_anual_percent = ((1 + taxa) ** 12 - 1) * 100

            print(f"Taxa de Juros Diária Equivalente: {(math.pow(1 + taxa, 1 / 23) - 1) * 100:.4f}%")
            print(f"Taxa de Juros Mensal: {taxa_percent:.4f}%")
            print(f"Taxa de Juros Anual: {taxa_anual_percent:.4f}%")

        print("\nObrigado por utilizar a calculadora de taxa de juros!")


if __name__ == "__main__":
    main()
