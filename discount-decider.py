import math


def calcular_parcela(P, r, n):
    """
    Calcula o valor da parcela mensal de um empréstimo amortizado.
    P: Valor do empréstimo
    r: Taxa de juros mensal (em decimal)
    n: Número de parcelas
    """
    if r == 0:
        return P / n
    parcela = P * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return parcela


def calcular_total_pagamento(parcela, n):
    """
    Calcula o pagamento total do empréstimo.
    parcela: Valor da parcela mensal
    n: Número de parcelas
    """
    return parcela * n


def calcular_montante_final(P, r, n):
    """
    Calcula o montante final após n meses com juros compostos.
    P: Montante inicial
    r: Taxa de rendimento mensal (em decimal)
    n: Número de meses
    """
    return P * ((1 + r) ** n)


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


def main():
    print("=== Comparador de Pagamento de Empréstimo vs. Investimento ===\n")

    # Entrada de Dados
    saved_amount = obter_valor_positivo("Digite o montante inicial guardado (R$): ")
    saved_interest_rate_percent = obter_valor_positivo("Digite a taxa de rendimento mensal do montante guardado (%): ")
    saved_interest_rate = saved_interest_rate_percent / 100

    loan_amount = obter_valor_positivo("Digite o valor da dívida (R$): ")
    loan_months = int(obter_valor_positivo("Digite o número de parcelas: "))
    loan_interest_rate_percent = obter_valor_positivo("Digite a taxa de juros mensal da dívida (%): ")
    loan_interest_rate = loan_interest_rate_percent / 100

    monthly_discount = obter_valor_positivo("Digite o desconto por mês para pagamento antecipado (R$): ")

    print("\n=== Calculando ===\n")

    # Opção 1: Pagamento Normal
    parcela_normal = calcular_parcela(loan_amount, loan_interest_rate, loan_months)
    total_pago_normal = calcular_total_pagamento(parcela_normal, loan_months)
    montante_final_normal = calcular_montante_final(saved_amount, saved_interest_rate, loan_months)

    print("=== Opção 1: Pagamento Normal ===")
    print(f"Valor da Parcela Mensal: R$ {parcela_normal:.2f}")
    print(f"Total Pago ao Final: R$ {total_pago_normal:.2f}")
    print(f"Montante Final Guardado: R$ {montante_final_normal:.2f}\n")

    # Opção 2: Pagamento Antecipado com Desconto
    parcela_antecipada = parcela_normal - monthly_discount
    # As parcelas não podem ser menores que zero
    parcela_antecipada = max(parcela_antecipada, 0)
    total_pago_antecipado = calcular_total_pagamento(parcela_antecipada, loan_months)

    # Calculando o impacto no montante guardado
    # Suposição: O desconto por mês reduz o montante guardado disponível para rendimento
    # Portanto, o montante guardado rende sobre (saved_amount - desconto)
    montante_final_antecipado = calcular_montante_final(saved_amount - (monthly_discount * loan_months),
                                                        saved_interest_rate, loan_months)

    print("=== Opção 2: Pagamento Antecipado com Desconto ===")
    print(f"Valor da Parcela Mensal com Desconto: R$ {parcela_antecipada:.2f}")
    print(f"Total Pago ao Final com Desconto: R$ {total_pago_antecipado:.2f}")
    print(f"Montante Final Guardado: R$ {montante_final_antecipado:.2f}\n")

    # Comparação
    economia = total_pago_normal - total_pago_antecipado
    rendimento_adicional = montante_final_antecipado - montante_final_normal

    print("=== Comparação ===")
    print(f"Economia no Pagamento do Empréstimo: R$ {economia:.2f}")
    print(f"Rendimento Extra do Montante Guardado: R$ {rendimento_adicional:.2f}")

    if economia > rendimento_adicional:
        print("\nÉ mais vantajoso pagar antecipadamente o empréstimo.")
    else:
        print("\nÉ mais vantajoso manter o pagamento normal e deixar o montante guardado rendendo.")


if __name__ == "__main__":
    main()
