# -*- coding: utf-8 -*-
"""
InflationShield_Simulation_Real.py

Simulação para calcular o patrimônio acumulado em 30 anos, considerando:
    - Evolução salarial (valores mensais):
        * Anos 1 a 2:     R$ 4.400
        * Anos 3 a 5:     R$ 9.000
        * Anos 6 a 10:    R$ 15.000
        * Anos 11 a 15:   R$ 18.000
        * Anos 16 a 25:   R$ 25.000
        * Anos 26 a 30:   R$ 28.000
    - Três cenários de poupança: guardar 1/6, 1/5 e 1/4 do salário,
      onde o aporte anual é calculado com base no salário do período.
    - Os aportes são realizados no final de cada ano e investidos a uma taxa de 14,25% ao ano (juros compostos).
    - É considerada uma inflação média de 7% ao ano para deflacionar os valores e obter o poder de compra atual.

Para cada cenário, o programa calcula e exibe:
  1. Patrimônio Nominal acumulado em 30 anos.
  2. Patrimônio Real (em termos de valores de hoje).
  3. Rendimento Anual Nominal (14,25% do patrimônio nominal).
  4. Rendimento Anual Real (14,25% do patrimônio real).
  5. Rendimento Mensal Nominal (dividido por 12).
  6. Rendimento Mensal Real (dividido por 12).
  7. Média Mensal Acumulada Nominal (patrimônio nominal ÷ 360).
  8. Média Mensal Acumulada Real (patrimônio real ÷ 360).

Essa "média mensal acumulada" mostra quanto, em média, foi poupado por mês ao longo dos 30 anos.
"""


def salario_por_ano(ano):
    """Retorna o salário mensal (em R$) para o ano corrente, conforme os intervalos informados."""
    if 1 <= ano <= 2:
        return 4400
    elif 3 <= ano <= 5:
        return 9000
    elif 6 <= ano <= 10:
        return 15000
    elif 11 <= ano <= 15:
        return 18000
    elif 16 <= ano <= 25:
        return 25000
    elif 26 <= ano <= 30:
        return 28000
    else:
        return 0


def simular_poupanca(fracao_poupanca, anos_totais=30, taxa_juros=0.1425):
    """
    Simula o acúmulo de capital durante 'anos_totais' anos.
    Cada aporte anual é calculado como:
         Aporte = (salário mensal * 12) * fracao_poupanca
    O aporte é realizado no final do ano e composto à taxa 'taxa_juros' durante os anos restantes até 30.
    Retorna o patrimônio acumulado nominal ao final do período.
    """
    patrimonio = 0
    for ano in range(1, anos_totais + 1):
        sal_mensal = salario_por_ano(ano)
        salario_anual = sal_mensal * 12
        aporte = salario_anual * fracao_poupanca
        # Tempo de composição para o aporte realizado no final do ano "ano":
        anos_compostos = anos_totais - ano
        patrimonio += aporte * ((1 + taxa_juros) ** anos_compostos)
    return patrimonio


def main():
    anos_totais = 30
    taxa_juros = 0.1425  # 14,25% ao ano
    inflacao = 0.07  # 7% ao ano

    # Cenários de poupança: 1/6, 1/5 e 1/4 do salário
    cenarios = {
        "1/6": 1 / 6,
        "1/5": 1 / 5,
        "1/4": 1 / 4
    }

    # Fator de inflação acumulado em 30 anos
    fator_inflacao = (1 + inflacao) ** anos_totais
    total_meses = anos_totais * 12  # 360 meses

    print("Simulação de Acúmulo de Capital em 30 anos (Valores Nominais e Reais)")
    print("--------------------------------------------------------------")
    print("Evolução salarial (mensal):")
    print("  Anos 1-2:    R$ 4.400")
    print("  Anos 3-5:    R$ 9.000")
    print("  Anos 6-10:   R$ 15.000")
    print("  Anos 11-15:  R$ 18.000")
    print("  Anos 16-25:  R$ 25.000")
    print("  Anos 26-30:  R$ 28.000")
    print("Taxa de rendimento dos investimentos: 14,25% ao ano")
    print("Taxa de inflação: 7% ao ano")
    print("--------------------------------------------------------------\n")

    # Cabeçalho da tabela
    print("{:<10}{:<28}{:<28}{:<28}{:<28}{:<28}{:<28}{:<28}".format(
        "Cenário",
        "Patrimônio Nominal (R$)",
        "Patrimônio Real (R$)",
        "Rend. Anual Nominal (R$)",
        "Rend. Anual Real (R$)",
        "Rend. Mensal Real (R$)",
        "Média Mensal Nominal (R$)",
        "Média Mensal Real (R$)"
    ))

    for nome, fracao in cenarios.items():
        patrimonio_nominal = simular_poupanca(fracao, anos_totais, taxa_juros)
        rendimento_anual_nominal = patrimonio_nominal * taxa_juros
        rendimento_mensal_nominal = rendimento_anual_nominal / 12

        # Valores reais: deflaciona os valores nominais pelo fator acumulado de inflação
        patrimonio_real = patrimonio_nominal / fator_inflacao
        rendimento_anual_real = rendimento_anual_nominal / fator_inflacao
        rendimento_mensal_real = rendimento_anual_real / 12

        # Média mensal acumulada (nominal e real)
        media_mensal_nominal = patrimonio_nominal / total_meses
        media_mensal_real = patrimonio_real / total_meses

        print("{:<10}{:<28,.2f}{:<28,.2f}{:<28,.2f}{:<28,.2f}{:<28,.2f}{:<28,.2f}{:<28,.2f}".format(
            nome, patrimonio_nominal, patrimonio_real, rendimento_anual_nominal,
            rendimento_anual_real, rendimento_mensal_real, media_mensal_nominal,
            media_mensal_real
        ))


if __name__ == "__main__":
    main()
