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
    - Três cenários de poupança: guardar 1/6, 1/5 e 1/4 do salário (contribuição anual baseada no salário do período).
    - Os aportes são realizados ao final de cada ano e investidos a uma taxa de 14,25% ao ano (juros compostos).
    - Uma inflação média de 7% ao ano é considerada para calcular o poder de compra real (deflacionando os valores acumulados).

Para cada cenário, o programa calcula:
  1. O patrimônio acumulado nominal em 30 anos.
  2. O rendimento anual e mensal nominal (assumindo que os investimentos rendem 14,25% ao ano).
  3. O patrimônio acumulado real (em termos de valores de hoje), deflacionado pela inflação acumulada em 30 anos.
  4. O rendimento anual e mensal real.

A deflação é feita dividindo os valores nominais pelo fator acumulado de inflação: (1 + 0.07)^30.
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
    Os aportes são realizados no final de cada ano e correspondem a:
       Aporte anual = (salário mensal * 12) * fracao_poupanca
    Os aportes são investidos a uma taxa anual 'taxa_juros' (composta).
    Retorna o patrimônio acumulado nominal ao final do período.
    """
    patrimonio = 0
    for ano in range(1, anos_totais + 1):
        sal_mensal = salario_por_ano(ano)
        salario_anual = sal_mensal * 12
        aporte = salario_anual * fracao_poupanca
        # Tempo de composição: quantos anos o aporte terá para render até o final de 30 anos
        anos_compostos = anos_totais - ano
        patrimonio += aporte * ((1 + taxa_juros) ** anos_compostos)
    return patrimonio


def main():
    anos_totais = 30
    taxa_juros = 0.1425  # 14,25% ao ano
    inflacao = 0.07  # 7% ao ano

    # Cenários de poupança: 1/6, 1/5, 1/4 do salário
    cenarios = {
        "1/6": 1 / 6,
        "1/5": 1 / 5,
        "1/4": 1 / 4
    }

    # Fator de inflação acumulado em 30 anos
    fator_inflacao = (1 + inflacao) ** anos_totais

    print("Simulação de Acúmulo de Capital em 30 anos (Valores Nominais e Reais)")
    print("--------------------------------------------------------------")
    print("Evolução salarial (mensal):")
    print("  Anos 1-2:    R$ 4.400")
    print("  Anos 3-5:    R$ 9.000")
    print("  Anos 6-10:   R$ 15.000")
    print("  Anos 11-15:  R$ 18.000")
    print("  Anos 16-25:  R$ 25.000")
    print("  Anos 26-30:  R$ 28.000")
    print("Taxa de rendimento: 14,25% ao ano")
    print("Taxa de inflação: 7% ao ano")
    print("--------------------------------------------------------------\n")

    for nome, fracao in cenarios.items():
        patrimonio_nominal = simular_poupanca(fracao, anos_totais, taxa_juros)
        rendimento_anual_nominal = patrimonio_nominal * taxa_juros
        rendimento_mensal_nominal = rendimento_anual_nominal / 12

        # Valores reais: deflaciona os valores nominais pelo fator acumulado de inflação em 30 anos
        patrimonio_real = patrimonio_nominal / fator_inflacao
        rendimento_anual_real = rendimento_anual_nominal / fator_inflacao
        rendimento_mensal_real = rendimento_anual_real / 12

        print(f"Cenário: Poupar {nome} do salário")
        print(f"  Patrimônio acumulado nominal em 30 anos: R$ {patrimonio_nominal:,.2f}")
        print(f"  Rendimento anual nominal (14,25%): R$ {rendimento_anual_nominal:,.2f}")
        print(f"  Rendimento mensal nominal: R$ {rendimento_mensal_nominal:,.2f}")
        print(f"  Patrimônio acumulado real (valor de hoje): R$ {patrimonio_real:,.2f}")
        print(f"  Rendimento anual real: R$ {rendimento_anual_real:,.2f}")
        print(f"  Rendimento mensal real: R$ {rendimento_mensal_real:,.2f}\n")


if __name__ == "__main__":
    main()
