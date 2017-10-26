import support

non_zeros_balances = support.get_nonzero_balances()
print non_zeros_balances
for el in non_zeros_balances:
    print support.get_data("/exchange/ticker", [("currencyPair", el)])