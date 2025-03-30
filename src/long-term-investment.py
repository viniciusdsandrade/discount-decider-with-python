import math


def monthly_rate(annual_rate: float) -> float:
    """
    Retorna a taxa mensal efetiva dada a taxa anual efetiva.
    """
    return (1 + annual_rate) ** (1 / 12) - 1


def final_balance_50_months(annual_rate: float, extra_monthly_deposit: float,
                            rent_deposit: float = 1000.0,
                            initial_capital: float = 100000.0,
                            months: int = 50) -> float:
    """
    Calcula o saldo final após 'months' meses, considerando:
    - annual_rate: taxa anual efetiva;
    - extra_monthly_deposit: aporte extra mensal (além do depósito fixo do aluguel);
    - rent_deposit: depósito fixo mensal proveniente do aluguel;
    - initial_capital: capital inicial.

    Em cada mês, o saldo rende juros e são somados os depósitos (rent_deposit + extra_monthly_deposit).
    """
    i = monthly_rate(annual_rate)
    balance = initial_capital
    for _ in range(months):
        balance *= (1 + i)
        balance += (rent_deposit + extra_monthly_deposit)
    return balance


def solve_required_deposit(annual_rate: float,
                           desired_monthly_interest: float = 3600.0,
                           rent_deposit: float = 1000.0,
                           initial_capital: float = 100000.0,
                           months: int = 50) -> float:
    """
    Determina, por meio de busca binária, qual o valor do depósito extra mensal necessário para que,
    ao final de 'months' meses, o saldo acumulado gere 'desired_monthly_interest'
    de rendimentos mensais.

    O fluxo mensal já inclui o depósito fixo do aluguel.
    """
    i_mensal = monthly_rate(annual_rate)
    needed_capital = desired_monthly_interest / i_mensal
    left, right = 0.0, 20000.0
    for _ in range(100):
        mid = (left + right) / 2
        final_bal = final_balance_50_months(annual_rate, mid, rent_deposit, initial_capital, months)
        if final_bal >= needed_capital:
            right = mid
        else:
            left = mid
    return (left + right) / 2


def generate_monthly_table(annual_rate: float, extra_monthly_deposit: float,
                           rent_deposit: float = 1000.0,
                           initial_capital: float = 100000.0,
                           months: int = 50):
    """
    Gera os dados mês a mês da evolução do saldo.
    Retorna uma lista de tuplas com os seguintes dados para cada mês:
      (Mês, Saldo Inicial, Juros do mês, Depósito Total do mês, Saldo Final)
    """
    i = monthly_rate(annual_rate)
    balance = initial_capital
    table = []
    for m in range(1, months + 1):
        start_balance = balance
        interest = start_balance * i
        deposit = rent_deposit + extra_monthly_deposit
        balance = start_balance * (1 + i) + deposit
        table.append((m, start_balance, interest, deposit, balance))
    return table


# Definindo os cenários de taxa anual
rates = [0.06, 0.09, 0.12, 0.1425]

output_text = ""

for r in rates:
    i = monthly_rate(r)
    extra_deposit = solve_required_deposit(r)
    total_deposit = extra_deposit + 1000.0  # Soma do depósito extra com o fixo do aluguel
    final_capital = final_balance_50_months(r, extra_deposit)
    needed_capital = 3600 / i  # Capital que gera R$ 3.600 mensais

    output_text += f"Cenário: Taxa Anual = {r * 100:.2f}%, Taxa Mensal = {i * 100:.3f}%\n"
    output_text += f"Depósito Extra Necessário: R$ {extra_deposit:,.2f}\n"
    output_text += f"Total Depósito Mensal (Aluguel + Extra): R$ {total_deposit:,.2f}\n"
    output_text += f"Capital Final (aprox.): R$ {final_capital:,.2f}\n"
    output_text += f"Capital Necessário para gerar R$ 3.600/mês: R$ {needed_capital:,.2f}\n"
    output_text += "-" * 70 + "\n"
    output_text += f"{'Mês':>3} | {'Saldo Inicial':>15} | {'Juros':>10} | {'Depósito':>10} | {'Saldo Final':>15}\n"

    monthly_data = generate_monthly_table(r, extra_deposit)
    for row in monthly_data:
        month, start_balance, interest, deposit, end_balance = row
        output_text += (f"{month:3d} | R$ {start_balance:14,.2f} | R$ {interest:9,.2f} | "
                        f"R$ {deposit:9,.2f} | R$ {end_balance:14,.2f}\n")
    output_text += "=" * 70 + "\n\n"

# Salva o resultado em um arquivo .txt
with open("tabela_resultados.txt", "w", encoding="utf-8") as f:
    f.write(output_text)

print("Arquivo 'tabela_resultados.txt' gerado com sucesso!")
