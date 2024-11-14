import numpy as np
import numpy_financial as npf


def calcular_tir(cash_flows):
    """
    Calcula a Taxa Interna de Retorno (TIR) para uma série de fluxos de caixa.
    """
    try:
        tir = npf.irr(cash_flows)
        return tir
    except Exception:
        return None


def main():
    # Dados da dívida
    valor_divida = 2471.00

    # Opções de parcelamento
    opcoes_parcelamento = [
        {'parcelas': 3, 'total': 2671.65},
        {'parcelas': 4, 'total': 2701.92},
        {'parcelas': 5, 'total': 2732.80},
        {'parcelas': 6, 'total': 2763.66},
    ]

    # Dados da aplicação em renda fixa
    rendimento_diario = 34.00
    dias_uteis_mes = 22
    rendimento_mensal = rendimento_diario * dias_uteis_mes
    taxa_retorno_mensal = (rendimento_mensal / valor_divida) * 100  # em porcentagem

    print("=== Análise de Parcelamento da Dívida ===\n")
    print(f"Valor Original da Dívida: R${valor_divida:.2f}\n")
    print(f"Rendimento da Aplicação:")
    print(f"- R$ {rendimento_diario:.2f} por dia útil")
    print(f"- {dias_uteis_mes} dias úteis por mês")
    print(f"- Rendimento Mensal: R$ {rendimento_mensal:.2f}")
    print(f"- Taxa de Retorno Mensal: {taxa_retorno_mensal:.2f}%\n")

    print("Opções de Parcelamento:\n")
    print("{:<10} {:<15} {:<20} {:<10}".format('Parcelas', 'Total a Pagar', 'Pagamento Mensal', 'TIR (%)'))

    melhores_opcoes = []

    for opcao in opcoes_parcelamento:
        parcelas = opcao['parcelas']
        total_a_pagar = opcao['total']
        pagamento_mensal = total_a_pagar / parcelas

        # Fluxo de caixa: saída inicial (dívida) e entradas das parcelas
        fluxos_caixa = [-valor_divida] + [pagamento_mensal] * parcelas

        tir = calcular_tir(fluxos_caixa)
        tir_percent = tir * 100 if tir is not None else None

        print("{:<10} R$ {:<13.2f} R$ {:<18.2f} {:<10.2f}".format(parcelas, total_a_pagar, pagamento_mensal,
                                                                  tir_percent if tir_percent else 0.00))

        # Armazenar opções com TIR menor que a taxa de retorno da aplicação
        if tir_percent and tir_percent < taxa_retorno_mensal:
            melhores_opcoes.append({'parcelas': parcelas, 'tir': tir_percent, 'total': total_a_pagar})

    print("\n=== Decisão ===\n")
    if melhores_opcoes:
        melhor_opcao = min(melhores_opcoes, key=lambda x: x['tir'])
        print(
            f"A melhor opção de parcelamento é em {melhor_opcao['parcelas']}x com uma TIR de {melhor_opcao['tir']:.2f}% ao mês.")
        print(
            f"Esta opção tem um custo efetivo menor que a taxa de retorno da sua aplicação ({taxa_retorno_mensal:.2f}% ao mês).")
    else:
        print("Nenhuma das opções de parcelamento possui uma TIR menor que a taxa de retorno da sua aplicação.")
        print("Recomenda-se quitar a dívida à vista para maximizar os rendimentos da sua aplicação.")


if __name__ == "__main__":
    main()
