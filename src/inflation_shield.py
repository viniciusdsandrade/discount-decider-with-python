# -*- coding: utf-8 -*-
"""
InflationShield.py

Cálculo do percentual do salário que deve ser poupado mensalmente
para, em T anos, acumular o capital necessário a gerar uma renda anual
equivalente ao salário atual ajustado pela inflação, preservando assim
o poder de compra.

O usuário deve informar:
    - Salário atual (mensal, em R$)
    - Taxa média de inflação anual (em %)
    - Taxa de rendimento anual dos investimentos (em %)

A partir disso, para cada horizonte de tempo T (em anos), o programa
calcula:

1. Salário Futuro Necessário (anual):
   S_target = salário_atual_anual * (1 + inflacao)^T

2. Capital Necessário para gerar essa renda, assumindo uma retirada perpétua:
   C_target = S_target / juros

3. Percentual do salário (anual) que deve ser poupado, usando a fórmula:
   p = (1 + inflacao)^T / [ (1 + juros)^T - 1 ]
   Esse p (em fração) representa a parcela do salário anual que precisa ser
   poupada anualmente para atingir C_target.
   Como a contribuição é distribuída de forma proporcional ao salário mensal,
   esse mesmo percentual se aplica mensalmente.

4. Capital Acumulado com contribuições anuais de A = p * (salário_atual_anual),
   após T anos, investido a uma taxa de juros anual, composto pela fórmula:
   VF = A * [ ((1 + juros)^T - 1) / juros ]

Os horizontes de tempo analisados são: 5, 10, 15, 20, 25, 30, 35 e 40 anos.
"""


def calcular_percentual_e_acumulado(salario_mensal, inflacao_percent, juros_percent, horizontes):
    # Converter taxas percentuais para decimais
    inflacao = inflacao_percent / 100.0
    juros = juros_percent / 100.0

    # Calcular o salário anual atual
    salario_anual = salario_mensal * 12

    resultados = []

    for T in horizontes:
        # Fórmula para a fração de contribuição necessária (p):
        # p = (1 + inflacao)^T / [ (1 + juros)^T - 1 ]
        p = (1 + inflacao) ** T / ((1 + juros) ** T - 1)
        percentual = p * 100  # converter em porcentagem

        # Contribuição anual necessária:
        A = p * salario_anual

        # Capital acumulado após T anos (valor futuro dos aportes):
        capital_acumulado = A * (((1 + juros) ** T - 1) / juros)

        resultados.append((T, percentual, capital_acumulado))
    return resultados


def main():
    print("InflationShield - Cálculo do percentual de poupança para preservar o poder de compra")
    try:
        salario_mensal = float(input("Digite seu salário atual (mensal, em R$): "))
        inflacao_percent = float(input("Digite a taxa média de inflação anual (em %): "))
        juros_percent = float(input("Digite a taxa de rendimento anual dos investimentos (em %): "))
    except ValueError:
        print("Valor inválido. Certifique-se de digitar números.")
        return

    # Definindo os horizontes em anos
    horizontes = [5, 10, 15, 20, 25, 30, 35, 40]

    resultados = calcular_percentual_e_acumulado(salario_mensal, inflacao_percent, juros_percent, horizontes)

    print("\nResultados:")
    print("{:<8}{:<30}{:<30}".format("Anos", "Percentual a Poupar (do salário mensal) (%)", "Capital Acumulado (R$)"))
    for T, perc, capital in resultados:
        print("{:<8}{:<30.2f}{:<30.2f}".format(T, perc, capital))


if __name__ == "__main__":
    main()
